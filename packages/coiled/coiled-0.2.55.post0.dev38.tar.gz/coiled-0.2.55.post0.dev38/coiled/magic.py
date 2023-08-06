import asyncio
import logging
import platform
import typing
from logging import getLogger
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Lock
from typing import Dict, List, Optional, Set

from packaging.utils import parse_wheel_filename

from coiled._beta.core import CloudBeta
from coiled.scan import PackageInfo, scan_prefix
from coiled.types import ResolvedPackageInfo
from coiled.utils import validate_wheel

logger = getLogger("coiled.package_sync")
subdir_datas = {}
PYTHON_VERSION = platform.python_version_tuple()


async def default_python() -> PackageInfo:
    python_version = platform.python_version()
    python_pkg: PackageInfo = {
        "name": "python",
        "path": None,
        "source": "conda",
        "channel_url": "https://conda.anaconda.org/conda-forge",
        "channel": "conda-forge",
        "subdir": "linux-64",
        "conda_name": "python",
        "version": python_version,
        "wheel_target": None,
    }
    return python_pkg


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


async def approximate_packages(
    cloud: CloudBeta,
    packages: List[PackageInfo],
    priorities: Dict[str, int],
    strict: bool = False,
) -> typing.List[ResolvedPackageInfo]:
    results = await cloud._approximate_packages(
        packages=[
            {
                "name": pkg["name"],
                "priority_override": 100 if strict else priorities.get(pkg["name"]),
                "python_major_version": PYTHON_VERSION[0],
                "python_minor_version": PYTHON_VERSION[1],
                "python_patch_version": PYTHON_VERSION[2],
                "source": pkg["source"],
                "channel_url": pkg["channel_url"],
                "channel": pkg["channel"],
                "subdir": pkg["subdir"],
                "conda_name": pkg["conda_name"],
                "version": pkg["version"],
                "wheel_target": pkg["wheel_target"],
            }
            for pkg in packages
        ]
    )
    result_map = {r["name"]: r for r in results}
    finalized_packages: typing.List[ResolvedPackageInfo] = []
    for pkg in packages:
        if pkg["wheel_target"] and result_map[pkg["name"]]["include"]:
            if pkg["wheel_target"].endswith(".egg"):
                finalized_packages.append(
                    await create_wheel_from_egg(
                        pkg_name=pkg["name"],
                        version=pkg["version"],
                        src=pkg["wheel_target"],
                    )
                )
            else:
                finalized_packages.append(
                    await create_wheel(
                        pkg_name=pkg["name"],
                        version=pkg["version"],
                        src=pkg["wheel_target"],
                    )
                )
        else:
            finalized_packages.append(
                {
                    "name": pkg["name"],
                    "source": pkg["source"],
                    "channel": pkg["channel"],
                    "conda_name": pkg["conda_name"],
                    "client_version": pkg["version"],
                    "specifier": result_map[pkg["name"]]["specifier"] or "",
                    "include": result_map[pkg["name"]]["include"],
                    "note": result_map[pkg["name"]]["note"],
                    "error": result_map[pkg["name"]]["error"],
                    "sdist": None,
                    "md5": None,
                }
            )
    return finalized_packages


async def create_environment_approximation(
    cloud: CloudBeta,
    priorities: Dict[str, int],
    only: Optional[Set[str]] = None,
    strict: bool = False,
) -> typing.List[ResolvedPackageInfo]:
    packages = await scan_prefix()
    python = next((p for p in packages if p["name"] == "python"), None)
    if not python:
        packages.append(await default_python())
    if only:
        packages = filter(lambda pkg: pkg["name"] in only, packages)
    # TODO: private conda channels
    result = await approximate_packages(
        cloud=cloud,
        packages=[pkg for pkg in packages],
        priorities=priorities,
        strict=strict,
    )
    return result


if __name__ == "__main__":
    from logging import basicConfig

    basicConfig(level=logging.INFO)

    from rich.console import Console
    from rich.table import Table

    async def run():
        async with CloudBeta(asynchronous=True) as cloud:
            return await create_environment_approximation(
                cloud=cloud,
                priorities={"dask": 100, "twisted": -2, "graphviz": -1, "icu": -1},
            )

    result = asyncio.run(run())

    table = Table(title="Packages")
    keys = ("name", "source", "include", "client_version", "specifier", "error", "note")

    for key in keys:
        table.add_column(key)

    for pkg in result:
        row_values = [str(pkg.get(key, "")) for key in keys]
        table.add_row(*row_values)
    console = Console()
    console.print(table)
