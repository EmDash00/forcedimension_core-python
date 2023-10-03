import ctypes as ct
import glob
import os
import platform
import sys
import unittest.mock as __mock
from functools import lru_cache
from typing import Final, Iterable, List, Literal, Optional, Set, Tuple, Union

from forcedimension_core.containers import VersionTuple

VERSION_TARGET = VersionTuple(3, 16, 0, 0)

SUPPORTED_PLATFORMS: Final[Set[str]] = {'linux', 'win32', 'darwin'}


def _get_search_info(
    lib_name: Union[Literal['libdrd'], Literal['libdhd']],
    search_dirs: Iterable[str] = (),
    silent=False
) -> Optional[List[str]]:
    if sys.platform not in SUPPORTED_PLATFORMS:
        if not silent:
            sys.stderr.write(
                "Unsupported platform."
            )

        return None

    search_dirs = list(search_dirs)

    if sys.platform == "win32":
        if platform.architecture()[0] == "64bit":
            lib_name = lib_name[3:] + "64"

        lib_versions = glob.glob(
            "{}\\sdk-*".format(
                os.path.join(
                    "c:",
                    os.sep,
                    "Program Files",
                    "Force Dimension"
                )
            )
        )[0]

        lib_versions.sort()

        search_dirs.append(
            os.path.join(lib_versions[-1], "bin", f"{lib_name}.dll")
        )

        return search_dirs

    if sys.platform.startswith("linux"):
        lib_ext = '.so'
        platform_name = 'lin'
        compiler = 'gcc'
    elif sys.platform == 'darwin':
        lib_ext = '.dylib'
        platform_name = 'mac'
        compiler = 'clang'

    lib_dir = "lib"
    machine = platform.machine()

    if (libpath := os.environ.get('FORCEDIM_SDK')) is not None:
        lib_folder = os.path.realpath(
            os.path.join(
                libpath,
                "lib",
                "release",
                f"{platform_name}-{machine}-{compiler}",  # type: ignore
            )
        )

        search_dirs.append(
            glob.glob(f"{lib_folder}/{lib_name + lib_ext}*")[0]  # type: ignore
        )

    search_dirs.extend([
        f"/usr/local/lib/{lib_name + lib_ext}",  # type: ignore
        f"/usr/lib/{lib_name + lib_ext}",  # type: ignore
    ])

    return search_dirs  # type: ignore


def _get_version(lib):
    major = ct.c_int()
    minor = ct.c_int()
    release = ct.c_int()
    revision = ct.c_int()

    lib.dhdGetSDKVersion(
        ct.byref(major),
        ct.byref(minor),
        ct.byref(release),
        ct.byref(revision)
    )

    return VersionTuple(
        major.value,
        minor.value,
        release.value,
        revision.value
    )


@lru_cache
def load(
    lib_name: Union[Literal['libdrd'], Literal['libdhd']],
    search_dirs=(),
    silent=False
):
    should_mock = (
        os.environ.get('__sphinx_build__', 'False') == 'True' or
        os.environ.get('__forcedim_unittest__', 'False') == 'True'
    )

    if should_mock:
        return __mock.Mock()

    if (search_info := _get_search_info(lib_name, search_dirs, silent)) is None:
        return None

    search_dirs = search_info
    load_failed = False

    for lib_path in search_dirs:
        if not os.path.isfile(lib_path):
            continue

        if sys.platform == "win32":
            path = os.getenv("PATH")
            if (path is not None and directory not in path):
                os.environ["PATH"] = f"{path};{directory}"

        try:
            lib = ct.CDLL(lib_path)
        except OSError:
            if silent:
                break
            else:
                sys.stderr.write(
                    "Library could not be loaded. Do you"
                    "have missing dependencies?\n"
                    "Ensure you have libusb-1."
                )

        if (version := _get_version(lib)) < VERSION_TARGET:
            if not silent:
                sys.stderr.write(
                    f"Invalid version. v{version} found "
                    f"but {VERSION_TARGET} is required.\n"
                )

            return None

        return lib
    if not silent:
        sys.stderr.write(
            f"Could not find {lib_name}. Is it installed?\n"
        )

    return None


if (_libdrd_load := load('libdrd')) is None:
    raise ImportError("There were problems loading libdrd.")

_libdrd = _libdrd_load
_libdhd = _libdrd_load
