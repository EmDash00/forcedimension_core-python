import ctypes
import getpass
import glob
import os
import pathlib
import platform
import sys
import unittest.mock as __mock
from typing import Final, Iterable, List, Set

from forcedimension_core.containers import VersionTuple

VERSION_TARGET = VersionTuple(3, 16, 0, 0)

SUPPORTED_PLATFORMS: Final[Set[str]] = {'linux', 'win32', 'cygwin', 'darwin'}

_ctypes_impl = ctypes
_getpass_impl = getpass
_glob_impl = glob
_os_impl = os
_pathlib_impl = pathlib
_platform_impl = platform
_sys_impl = sys

_test_load = False

def _get_search_paths_win32(search_dirs: Iterable[str] = ()):
    search_dirs = list(search_dirs)

    if _platform_impl.architecture()[0] == '64bit':
        lib_name = "drd64"
    else:
        lib_name = "drd"

    if _os_impl.environ.get('FDSDK'):
        search_dirs.append(
            _os_impl.path.join(
                _os_impl.environ.get(
                    'FDSDK'), 'bin', f'{lib_name}.dll'  # type: ignore
            )
        )

    if _sys_impl.platform == 'cygwin':
        root = _os_impl.path.join(
            _os_impl.path.sep + 'cygdrive',
            _pathlib_impl.Path.home().drive[0].lower()
        )
    else:
        root = _pathlib_impl.Path.home().drive + _os_impl.path.sep

    app_local = _os_impl.path.join(
        root, 'Users', _getpass_impl.getuser(), 'AppData', 'Local'
    )

    lib_versions = _glob_impl.glob(
        f'{_os_impl.path.join(root, "Program Files", "Force Dimension")}'
        f'{_os_impl.path.sep}sdk-*'
    )

    lib_versions_local = _glob_impl.glob(
        f'{_os_impl.path.join(app_local, "Force Dimension")}'
        f'{_os_impl.path.sep}sdk-*'
    )

    lib_versions.sort()
    lib_versions_local.sort()

    if lib_versions:
        search_dirs.append(
            _os_impl.path.join(
                lib_versions_local[-1], "bin", f"{lib_name}.dll"
            )
        )

    if lib_versions_local:
        search_dirs.append(
            _os_impl.path.join(lib_versions[-1], "bin", f"{lib_name}.dll")
        )

    return search_dirs

def _get_search_paths_unix(search_dirs: Iterable[str] = ()):
    search_dirs = list(search_dirs)
    machine = _platform_impl.machine()

    if _sys_impl.platform == 'linux':
        lib_file = "libdrd.so"
        platform_name = 'lin'
        compiler = 'gcc'
    else:
        lib_file = "libdrd.dylib"
        platform_name = 'mac'
        compiler = 'clang'

    if (libpath := _os_impl.environ.get('FDSDK')):
        lib_folder = _os_impl.path.realpath(
            _os_impl.path.join(
                libpath,
                "lib",
                "release",
                f"{platform_name}-{machine}-{compiler}",  # type: ignore
            )
        )
        # type: ignore
        if (glob_res := _glob_impl.glob(f"{lib_folder}/{lib_file}*")):  # type: ignore
            search_dirs.append(glob_res[0])

    # Legacy support for the old environment variable

    if (libpath := _os_impl.environ.get('FORCEDIM_SDK')):
        lib_folder = _os_impl.path.realpath(
            _os_impl.path.join(
                libpath,
                "lib",
                "release",
                f"{platform_name}-{machine}-{compiler}",  # type: ignore
            )
        )

        if (glob_res := _glob_impl.glob(f"{lib_folder}/{lib_file}*")):  # type: ignore
            search_dirs.append(glob_res[0])

    lib_loc_local = os.path.join(
        _os_impl.path.expanduser('~'),
        '.local', 'lib', lib_file  # type: ignore
    )

    lib_loc = os.path.join(
        _os_impl.path.sep, 'usr', 'local', 'lib', lib_file  # type: ignore
    )

    glob_res_local = _glob_impl.glob(lib_loc_local + '.*')
    glob_res = _glob_impl.glob(lib_loc + '.*')

    glob_res_local.sort()
    glob_res.sort()

    search_dirs.append(lib_loc_local)
    if glob_res_local:
        search_dirs.append(glob_res_local[-1])

    search_dirs.append(lib_loc)
    if glob_res:
        search_dirs.append(glob_res[-1])

    return search_dirs  # type: ignore


def _get_search_paths(
    search_dirs: Iterable[str] = (), silent: bool = False
):
    if _sys_impl.platform == 'win32' or _sys_impl.platform == 'cygwin':
        return _get_search_paths_win32(search_dirs)
    elif _sys_impl.platform == 'linux' or _sys_impl.platform == 'darwin':
        return _get_search_paths_unix(search_dirs)
    else:
        if not silent:
            _sys_impl.stderr.write("Unsupported platform.\n")

        return []


def _get_version(lib: _ctypes_impl.CDLL):
    major = _ctypes_impl.c_int()
    minor = _ctypes_impl.c_int()
    release = _ctypes_impl.c_int()
    revision = _ctypes_impl.c_int()

    lib.dhdGetSDKVersion(
        _ctypes_impl.byref(major),
        _ctypes_impl.byref(minor),
        _ctypes_impl.byref(release),
        _ctypes_impl.byref(revision)
    )

    return VersionTuple(
        major.value,
        minor.value,
        release.value,
        revision.value
    )


def _should_mock():
    return (
        _os_impl.environ.get('__fdsdkpy_sphinx_build__', 'False') == 'True' or
        _os_impl.environ.get('__fdsdkpy_unittest__', 'False') == 'True'
    )


def load(
    search_dirs=(),
    silent=False,
):

    if _os_impl.environ.get('__fdsdkpy_unittest_runtime__', 'False') == 'True':
        return None

    if _should_mock() and not _test_load:
        return __mock.Mock()

    if not (search_dirs := _get_search_paths(search_dirs, silent)):
        return None

    for lib_path in search_dirs:
        if not _os_impl.path.isfile(lib_path):
            continue

        # Make sure to add the directory to PATH for Windows DLL loading
        if _sys_impl.platform == "win32":

            path = _os_impl.environ.get('PATH')
            directory, _ = _os_impl.path.split(lib_path)

            if not path:
                _os_impl.environ['PATH'] = directory
            else:
                if directory not in path:
                    _os_impl.environ['PATH'] = f"{directory};{path}"

        try:
            lib = _ctypes_impl.CDLL(lib_path)
        except OSError:
            if not silent:
                _sys_impl.stderr.write(
                    "Library was found but could not be loaded. Do you "
                    "have missing dependencies?\n"
                    "Ensure you have libusb-1."
                )

            return None
        if (version := _get_version(lib)) < VERSION_TARGET:  # type: ignore
            if not silent:
                _sys_impl.stderr.write(
                    f"Invalid version. v{version} found "
                    f"but v{VERSION_TARGET} is required.\n"
                )

            return None

        return lib  # type: ignore
    if not silent:
        _sys_impl.stderr.write(
            "Could not find libdrd. Is it installed?\n"  # type: ignore
        )

    return None

if (_libdrd_load := load()) is None:
    raise ImportError(
        "There were problems loading libdrd. Check if you have it installed "
        "properly. For more information on installation consult: "
        ""
    )

_libdrd = _libdrd_load
_libdhd = _libdrd_load
