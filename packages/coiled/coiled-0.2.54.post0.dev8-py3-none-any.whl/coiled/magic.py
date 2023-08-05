import asyncio
import json
import logging
import platform
import typing
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from hashlib import md5
from logging import getLogger
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Lock
from typing import Dict, Iterable, List, Optional, Set, Union

import aiohttp
import backoff
import pkg_resources
from coiled.scan import PackageInfo, scan_prefix
from coiled.types import ResolvedPackageInfo
from coiled.utils import validate_wheel
from dask import config
from packaging import specifiers, version
from packaging.tags import Tag
from packaging.utils import parse_wheel_filename
from typing_extensions import TypedDict

logger = getLogger("coiled.package_sync")
subdir_datas = {}
PYTHON_VERSION = platform.python_version_tuple()


class PackageLevel(TypedDict):
    name: str
    level: int


class SpecifierStrict:
    # hacky workaround for conda versions not
    # sticking to PEP440
    # eg packaging turns 2022c into 2022rc0 otherwise
    def __init__(self, specifier: str):
        self.specifier = specifier

    def __contains__(self, item: str):
        return self.specifier == item

    def __str__(self):
        return f"=={self.specifier}"


class SpecifierLoose:
    def __contains__(self, item: str):
        return True

    def __str__(self):
        return ""


SpecifierType = Union[specifiers.SpecifierSet, SpecifierStrict, SpecifierLoose]


def create_specifier(v: str, priority: int) -> SpecifierType:
    # Note specifiers are created using the parsed version due to
    # https://github.com/pypa/packaging/issues/583
    if not len(v.split(".")) > 2:
        if priority == -1:
            return SpecifierLoose()
        return SpecifierStrict(v)
    try:
        parsed_version = version.parse(v)
        if not isinstance(parsed_version, version.Version):
            return specifiers.SpecifierSet("")
        else:
            if priority >= 100:
                return specifiers.SpecifierSet(
                    f"=={parsed_version}",
                    prereleases=parsed_version.is_prerelease,
                )
            elif priority == -1:
                return specifiers.SpecifierSet("", parsed_version.is_prerelease)
            else:
                return specifiers.SpecifierSet(
                    f"~={parsed_version}",
                    prereleases=parsed_version.is_prerelease,
                )
    except (version.InvalidVersion, specifiers.InvalidSpecifier):
        return specifiers.SpecifierSet("")


def any_matches(versions: Iterable[str], specifier: SpecifierType):
    if not versions:
        return False
    if specifier == specifiers.SpecifierSet("") and versions:
        # An empty specifier can also mean an invalid version
        # comparisons will throw an invalidversion exception
        # so just skip the check
        return True
    valid_versions = []
    for v in versions:
        # removing all the invalid versions so we dont even try
        # to compare against them
        try:
            version.parse(v)
            valid_versions.append(v)
        except version.InvalidVersion:
            pass
    return any(v in specifier for v in valid_versions)


# private threadpool required to prevent deadlocks
# while waiting for a lock
_lockPool = ThreadPoolExecutor(max_workers=1)


@asynccontextmanager
async def async_thread_lock(lock: Lock):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(_lockPool, lock.acquire)
    try:
        yield
    finally:
        lock.release()


class CondaCache:
    CACHE_DIR = Path(config.PATH) / "coiled-cache"

    channel_memory_cache: typing.DefaultDict[
        str, typing.DefaultDict[str, typing.Dict]
    ] = defaultdict(lambda: defaultdict(dict))

    lock = Lock()

    @backoff.on_exception(backoff.expo, aiohttp.ClientConnectionError, max_time=60)
    async def load_channel_repo_data(self, channel: str):
        logger.info(f"Loading conda metadata.json for {channel}")
        if not self.CACHE_DIR.exists():
            self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        channel_filename = Path(md5(channel.encode("utf-8")).hexdigest()).with_suffix(
            ".json"
        )
        channel_fp = self.CACHE_DIR / channel_filename
        headers = {}
        channel_cache_meta_fp = channel_fp.with_suffix(".meta_cache")
        if channel_cache_meta_fp.exists():
            with channel_cache_meta_fp.open("r") as cache_meta_f:
                channel_cache_meta = json.load(cache_meta_f)
            if channel_cache_meta.get("etag"):
                headers["If-None-Match"] = channel_cache_meta["etag"]
            headers["If-Modified-Since"] = channel_cache_meta["mod"]
        async with aiohttp.ClientSession() as client:
            resp = await client.get(channel + "/" + "repodata.json", headers=headers)
            if resp.status == 304:
                logger.info(f"Cached version is valid for {channel}, loading")
                data = json.loads(channel_fp.read_text())
            else:
                logger.info(f"Downloading fresh conda repodata for {channel}")
                data = await resp.json()
                assert resp.status, await resp.content.read()
                channel_fp.write_text(json.dumps(data))
                cache_meta = {"mod": resp.headers["Last-Modified"]}
                if resp.headers.get("Etag"):
                    cache_meta["etag"] = resp.headers["ETag"]
                channel_cache_meta_fp.write_text(json.dumps(cache_meta))

            for pkg in [
                *data["packages"].values(),
                *data.get("packages.conda", {}).values(),
            ]:
                self.channel_memory_cache[channel][pkg["name"]][pkg["version"]] = pkg

    async def fetch_repo_data(self, channel: str) -> typing.Dict[str, typing.Dict]:
        async with async_thread_lock(self.lock):
            # check again once we have the lock in case
            # someone beat us to it
            if not self.channel_memory_cache.get(channel):
                await self.load_channel_repo_data(channel)
                return self.channel_memory_cache[channel]
            else:
                return self.channel_memory_cache[channel]

    async def is_available(
        self,
        name: str,
        channel_url: str,
        specifier: SpecifierType,
    ) -> bool:
        repo_data = await self.fetch_repo_data(channel=channel_url + "/linux-64")
        if repo_data.get(name):
            return any_matches(versions=repo_data[name].keys(), specifier=specifier)
        else:
            return False


class CondaEnv:
    global_repo_cache = CondaCache()

    @staticmethod
    async def create_approximation(
        packages: List[PackageInfo], priorities: Dict[str, int], strict: bool = False
    ) -> List[ResolvedPackageInfo]:
        conda_approximation = list(
            await asyncio.gather(
                *(
                    CondaEnv.handle_conda_package(
                        pkg, priorities=priorities, strict=strict
                    )
                    for pkg in packages
                )
            )
        )

        # we install python from conda-forge on cluster, so always include python as conda package
        # even if the user isn't using conda locally
        if not conda_approximation:
            conda_approximation = [await CondaEnv.default_python()]

        return conda_approximation

    @staticmethod
    async def default_python() -> ResolvedPackageInfo:
        python_version = platform.python_version()
        specifier = specifiers.SpecifierSet(f"=={python_version}")
        python_pkg: ResolvedPackageInfo = {
            "name": "python",
            "source": "conda",
            "sdist": None,
            "conda_name": "python",
            "client_version": python_version,
            "specifier": str(specifier),
            "include": True,
            "channel": "conda-forge",
            "error": None,
            "note": None,
            "md5": None,
        }
        if not await CondaEnv.global_repo_cache.is_available(
            name="python",
            channel_url="https://conda.anaconda.org/conda-forge",
            specifier=specifier,
        ):
            python_pkg["include"] = False
            python_pkg[
                "error"
            ] = "Only python versions available on conda-forge are supported"

        return python_pkg

    @staticmethod
    async def handle_conda_package(
        pkg: PackageInfo,
        priorities: Dict[str, int],
        strict: bool = False,
    ) -> ResolvedPackageInfo:
        # strict mode overrides all priorities
        priority = 100 if strict else priorities.get(pkg["name"].lower(), 50)
        if priority == -2:
            return {
                "channel": pkg["channel"],
                "sdist": None,
                "source": pkg["source"],
                "conda_name": pkg["conda_name"],
                "name": pkg["name"],
                "client_version": pkg["version"],
                "specifier": "",
                "include": False,
                "error": None,
                "note": "Package ignored, no risk",
                "md5": None,
            }
        specifier = create_specifier(pkg["version"], priority=priority)
        package_info: ResolvedPackageInfo = {
            "channel": pkg["channel"],
            "sdist": None,
            "source": "conda",
            "conda_name": pkg["conda_name"],
            "name": pkg["name"],
            "client_version": pkg["version"],
            "specifier": str(specifier),
            "include": True,
            "note": None,
            "error": None,
            "md5": None,
        }
        assert pkg["channel_url"], pkg
        assert pkg["subdir"], pkg
        if pkg[
            "subdir"
        ] != "noarch" and not await CondaEnv.global_repo_cache.is_available(
            name=pkg["conda_name"], channel_url=pkg["channel_url"], specifier=specifier  # type: ignore
        ):
            package_info["include"] = False
            package_info[
                "error"
            ] = f"{pkg['version']} has no install candidate for linux-64"
        return package_info


class PipCache:
    def __init__(self, client: aiohttp.ClientSession, arch: str = "x86_64"):
        self.client = client

        linuxes = (
            "manylinux",
            "manylinux1",
            "manylinux2010",
            "manylinux2014",
            # https://peps.python.org/pep-0600/
            # TODO check gclibc and add appropriate manylinux_2_x
            "manylinux_2_5",
            "manylinux_2_12",
            "manylinux_2_17",
        )

        self.looking_for = [
            Tag(f"py{PYTHON_VERSION[0]}", "none", "any"),
            Tag(f"cp{PYTHON_VERSION[0]}{PYTHON_VERSION[1]}", "none", "any"),
        ]

        # TODO arm support
        for linux in linuxes:
            self.looking_for.extend(
                [
                    Tag(f"py{PYTHON_VERSION[0]}", "none", linux),
                    Tag(f"py{PYTHON_VERSION[0]}", "none", f"{linux}_{arch}"),
                ]
            )

    @backoff.on_exception(backoff.expo, aiohttp.ClientConnectionError, max_time=60)
    async def fetch(self, package_name):
        resp = await self.client.get(f"/pypi/{package_name}/json")
        data = await resp.json()
        pkgs = {}

        if not data.get("releases"):
            logger.debug(f"Didn't find any releases for '{package_name}' on PyPI.")
            return pkgs

        for build_version, builds in data["releases"].items():
            for build in [
                b
                for b in builds
                if not b.get("yanked")
                and b["packagetype"] not in ["bdist_dumb", "bdist_wininst", "bdist_rpm"]
            ]:
                if build["packagetype"] == "bdist_wheel":
                    _, _, _, tags = parse_wheel_filename(build["filename"])
                elif build["packagetype"] == "sdist":
                    tags = [
                        Tag(f"py{PYTHON_VERSION[0]}", "none", "any"),
                    ]
                else:
                    dist = pkg_resources.Distribution.from_filename(build["filename"])
                    tags = [Tag(f"py{dist.py_version}", "none", "any")]

                # filter by tags (i.e., python version)
                if any(valid in tags for valid in self.looking_for):
                    pkgs[build_version] = build
        return pkgs


class PackageBuildError(Exception):
    pass


WHEEL_BUILD_LOCKS: Dict[str, Lock] = {}


async def create_wheel(pkg_name: str, version: str, src: str) -> ResolvedPackageInfo:
    lock = WHEEL_BUILD_LOCKS.setdefault(pkg_name, Lock())
    with lock:
        tmpdir = TemporaryDirectory()
        outdir = Path(tmpdir.name) / Path(pkg_name)
        logger.info(f"Attempting to create a wheel for {pkg_name} @ {src}")
        p = await asyncio.create_subprocess_shell(
            cmd=f"pip wheel --wheel-dir {outdir} --no-deps --use-pep517 --no-cache-dir {src}",
        )
        await p.wait()
        if p.returncode:
            return {
                "name": pkg_name,
                "source": "pip",
                "channel": None,
                "conda_name": None,
                "client_version": version,
                "specifier": "",
                "include": False,
                "error": (
                    "Failed to build a wheel for the"
                    " package, will not be included in environment, check stdout for details"
                ),
                "note": None,
                "sdist": None,
                "md5": None,
            }
        wheel_fn = next(file for file in outdir.iterdir() if file.suffix == ".whl")
        _, build_version, _, _ = parse_wheel_filename(str(wheel_fn.name))
        has_python, md5 = await validate_wheel(wheel_fn)
    return {
        "name": pkg_name,
        "source": "pip",
        "channel": None,
        "conda_name": None,
        "client_version": str(build_version),
        "specifier": "",
        "include": True,
        "error": None if has_python else "Built wheel contains no python files!",
        "note": f"Wheel built from {src}",
        "sdist": wheel_fn.open("rb"),
        "md5": md5,
    }


async def create_wheel_from_egg(
    pkg_name: str, version: str, src: str
) -> ResolvedPackageInfo:
    tmpdir = TemporaryDirectory()
    outdir = Path(tmpdir.name) / Path(pkg_name)
    outdir.mkdir(parents=True)
    logger.info(f"Attempting to create a wheel for {pkg_name} in directory {src}")
    p = await asyncio.create_subprocess_shell(
        cmd=f"wheel convert --dest-dir {outdir} {src}"
    )
    await p.wait()
    if p.returncode:
        return {
            "name": pkg_name,
            "source": "pip",
            "channel": None,
            "conda_name": None,
            "client_version": version,
            "specifier": "",
            "include": False,
            "error": (
                "Failed to build a wheel for the"
                " package, will not be included in environment, check stdout for details"
            ),
            "note": None,
            "sdist": None,
            "md5": None,
        }
    wheel_fn = next(file for file in outdir.iterdir() if file.suffix == ".whl")
    has_python, md5 = await validate_wheel(Path(wheel_fn))
    return {
        "name": pkg_name,
        "source": "pip",
        "channel": None,
        "conda_name": None,
        "client_version": version,
        "specifier": "",
        "include": True,
        "error": None if has_python else "Built wheel has no python files!",
        "note": "Wheel built from local egg",
        "sdist": wheel_fn.open("rb"),
        "md5": md5,
    }


async def handle_pip_package(
    package: PackageInfo,
    repo: PipCache,
    priorities: Dict[str, int],
    strict: bool = False,
) -> ResolvedPackageInfo:
    priority = 100 if strict else priorities.get(package["name"].lower(), 50)
    if priority == -2:
        return {
            "name": package["name"],
            "source": package["source"],
            "channel": package["channel"],
            "client_version": package["version"],
            "conda_name": package["conda_name"],
            "specifier": "",
            "include": False,
            "note": "Package ignored, no risk",
            "error": None,
            "sdist": None,
            "md5": None,
        }
    if package["wheel_target"]:
        assert package["wheel_target"]
        if package["wheel_target"].endswith(".egg"):  # type: ignore
            return await create_wheel_from_egg(
                pkg_name=package["name"],
                version=package["version"],
                src=package["wheel_target"],  # type: ignore
            )
        else:
            assert package["wheel_target"]
            return await create_wheel(
                pkg_name=package["name"],
                version=package["version"],
                src=package["wheel_target"],  # type: ignore
            )
    else:
        specifier = create_specifier(package["version"], priority=priority)
        data = await repo.fetch(package["name"])
        if not any_matches(versions=data.keys(), specifier=specifier):
            return {
                "name": package["name"],
                "source": package["source"],
                "conda_name": package["conda_name"],
                "channel": package["channel"],
                "client_version": package["version"],
                "specifier": str(specifier),
                "include": False,
                "note": None,
                "error": f"Cannot find {package['version']}{specifier} on pypi.org, "
                "currently only packages from pypi.org are supported. "
                "Custom conda channels are supported if your package is available there instead.",
                "sdist": None,
                "md5": None,
            }
        return {
            "name": package["name"],
            "source": package["source"],
            "channel": package["channel"],
            "conda_name": package["conda_name"],
            "client_version": package["version"],
            "specifier": str(specifier),
            "include": True,
            "note": None,
            "error": None,
            "sdist": None,
            "md5": None,
        }


async def create_pip_env_approximation(
    packages: List[PackageInfo],
    priorities: Dict[str, int],
    strict: bool = False,
) -> typing.List[ResolvedPackageInfo]:
    async with aiohttp.ClientSession("https://pypi.org") as client:
        pip_cache = PipCache(client=client)
        return [
            pkg
            for pkg in await asyncio.gather(
                *(
                    handle_pip_package(
                        pkg, repo=pip_cache, priorities=priorities, strict=strict
                    )
                    for pkg in packages
                )
            )
            if pkg
        ]


async def create_environment_approximation(
    priorities: Dict[str, int], only: Optional[Set[str]] = None, strict: bool = False
) -> typing.List[ResolvedPackageInfo]:
    packages = await scan_prefix()
    if only:
        packages = filter(lambda pkg: pkg["name"] in only, packages)  # type: ignore
    # TODO: private conda channels
    # TODO: detect pre-releases and only set --pre flag for those packages (for conda)
    conda_env_future = asyncio.create_task(
        CondaEnv.create_approximation(
            packages=[pkg for pkg in packages if pkg["source"] == "conda"],
            priorities=priorities,
            strict=strict,
        )
    )
    pip_env_future = asyncio.create_task(
        create_pip_env_approximation(
            packages=[pkg for pkg in packages if pkg["source"] == "pip"],
            priorities=priorities,
            strict=strict,
        )
    )
    return list(await conda_env_future) + list(await pip_env_future)


if __name__ == "__main__":
    from logging import basicConfig

    basicConfig(level=logging.INFO)

    from rich.console import Console
    from rich.table import Table

    result = asyncio.run(
        create_environment_approximation(
            priorities={"dask": 100, "twisted": -2, "graphviz": -1, "icu": -1}
        )
    )

    table = Table(title="Packages")
    keys = ("name", "source", "include", "client_version", "specifier", "issue")

    for key in keys:
        table.add_column(key)

    for pkg in result:
        row_values = [str(pkg.get(key, "")) for key in keys]
        table.add_row(*row_values)
    console = Console()
    console.print(table)
