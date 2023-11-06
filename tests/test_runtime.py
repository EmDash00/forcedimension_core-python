import ctypes
import getpass
import glob
import importlib
import os
import pathlib
import platform
import sys
import unittest
from ctypes import CFUNCTYPE, POINTER, c_int
from random import randint
from typing import Optional, Set, Type

import forcedimension_core.runtime as runtime


class MockDHD:
    argtypes = [
        POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)
    ]
    restype = None

    major: int = 3
    minor: int = 16
    release: int = 0
    revision: int = 0

    ret = 0

    path: str = ""

    @staticmethod
    @CFUNCTYPE(restype, *argtypes)
    def dhdGetSDKVersion(major, minor, release, revision):
        major.contents.value = MockDHD.major
        minor.contents.value = MockDHD.minor
        release.contents.value = MockDHD.release
        revision.contents.value = MockDHD.revision

        return MockDHD.ret


class MockCtypes:
    c_int = ctypes.c_int
    byref = ctypes.byref

    should_load_successfully: bool = True

    @staticmethod
    def CDLL(lib_path: str) -> Type[MockDHD]:
        if MockCtypes.should_load_successfully:
            MockDHD.path = lib_path
            return MockDHD

        raise OSError


class MockGetPass:
    user: str = "GeneEric"

    @staticmethod
    def getuser():
        return MockGetPass.user


class MockGlob:
    should_fail: bool = False

    @staticmethod
    def glob(pathname: str):
        if MockGlob.should_fail:
            return []

        if not (
            pathname.endswith('sdk-*') or
            pathname.endswith('.*') or
            pathname.endswith('*dylib')
        ):
            return [pathname.replace('*', '')]


        if pathname.endswith('*dylib'):
            return [
                pathname.replace('*', '3.14.0.'),
                pathname.replace('*', '3.15.0.'),
                pathname.replace('*', '3.16.0.'),
            ]

        return [
            pathname.replace('*', '3.14.0'),
            pathname.replace('*', '3.15.0'),
            pathname.replace('*', '3.16.0'),
        ]


class MockSys:
    class stderr:
        data: str

        @staticmethod
        def write(err: str):
            MockSys.stderr.data = err

    platform: str = 'linux'


class MockEnviron:
    FORCEDIM_SDK: str = '/home/GeneEric/forcedimension_sdk'
    FDSDK: str = '/home/GeneEric/forcedimension_sdk'
    PATH: Optional[str] = None

    _environ = {}

    def __getitem__(self, key: str):
        return self.get(key)

    def __setitem__(self, key: str, value):
        if key == 'PATH':
            MockEnviron.PATH = value
            return

        MockEnviron._environ[key] = value

    def get(self, key: str, /, default=None):

        if key == 'FDSDK':
            return MockEnviron.FDSDK

        if key == 'FORCEDIM_SDK':
            return MockEnviron.FORCEDIM_SDK

        if key == 'PATH':
            return MockEnviron.PATH

        return os.environ.get(key, default)


class MockOS:
    sep: str = '/'
    environ: MockEnviron = MockEnviron()

    class path:
        VALID_PATHS: Set[str] = set()
        HOME: str = "/home/GeneEric"
        sep: str = '/'

        @staticmethod
        def join(*paths: str) -> str:
            if MockSys.platform != 'win32':
                return MockOS.path.sep.join(paths)

            if not (len(paths[0]) <= 3 and paths[0][1] == ':'):
                return MockOS.path.sep.join(paths)

            return paths[0] + MockOS.path.sep.join(paths[1:])

        @staticmethod
        def split(path: str):
            parts = path.split(MockOS.path.sep)
            return MockOS.path.sep.join(parts[:-1]), parts[-1]

        @staticmethod
        def realpath(*args, **kwargs):
            return os.path.realpath(*args, **kwargs)

        @staticmethod
        def expanduser(path: str):
            return path.replace('~', MockOS.path.HOME)

        @staticmethod
        def isfile(path: str) -> bool:
            if path in MockOS.path.VALID_PATHS:
                return True

            return False


class MockPathlib:
    class Path:
        drive: str = "C:"

        @classmethod
        def home(cls):
            return cls()


class MockPlatform:
    bits: str = '64bit'
    linkage: str = 'ELF'

    machine_type: str = 'x86_64'

    @staticmethod
    def architecture():
        return (MockPlatform.bits, MockPlatform.linkage)

    @staticmethod
    def machine():
        return MockPlatform.machine_type


class TestRuntime(unittest.TestCase):
    def test_get_version(self):
        for _ in range(100):
            MockDHD.major = randint(0, 100)
            MockDHD.minor = randint(0, 100)
            MockDHD.release = randint(0, 100)
            MockDHD.revision = randint(0, 100)

            ret = runtime._get_version(MockDHD)  # type: ignore

            self.assertEqual(ret.major, MockDHD.major)
            self.assertEqual(ret.minor, MockDHD.minor)
            self.assertEqual(ret.release, MockDHD.release)
            self.assertEqual(ret.revision, MockDHD.revision)

    def test_should_mock(self):
        os.environ['__fdsdkpy_unittest__'] = 'False'
        os.environ['__fdsdkpy_sphinx_build__'] = 'False'
        self.assertFalse(runtime._should_mock())

        os.environ['__fdsdkpy_unittest__'] = 'True'
        os.environ['__fdsdkpy_sphinx_build__'] = 'False'
        self.assertTrue(runtime._should_mock())

        os.environ['__fdsdkpy_unittest__'] = 'False'
        os.environ['__fdsdkpy_sphinx_build__'] = 'True'
        self.assertTrue(runtime._should_mock())

        os.environ['__fdsdkpy_unittest__'] = 'True'
        os.environ['__fdsdkpy_sphinx_build__'] = 'True'
        self.assertTrue(runtime._should_mock())

    def test_get_search_info(self):
        runtime._getpass_impl = MockGetPass
        runtime._glob_impl = MockGlob
        runtime._sys_impl = MockSys
        runtime._os_impl = MockOS
        runtime._pathlib_impl = MockPathlib
        runtime._platform_impl = MockPlatform

        UNSUPPORTED_PLATFORMS = ('aix', 'emscripten', 'wasi')

        for unsupported_platform in UNSUPPORTED_PLATFORMS:
            MockSys.platform = unsupported_platform
            self.assertFalse(runtime._get_search_paths())
            self.assertEqual(MockSys.stderr.data, "Unsupported platform.\n")

            MockSys.stderr.data = ""
            self.assertFalse(runtime._get_search_paths(silent=True))
            self.assertEqual(MockSys.stderr.data, "")



        MockPlatform.machine_type = 'x86_64'
        MockSys.platform = 'linux'
        MockEnviron.FDSDK = '/home/GeneEric/forcedimension_sdk'
        MockEnviron.FORCEDIM_SDK = '/home/GeneEric2/forcedimension_sdk'
        MockOS.sep = '/'
        MockOS.path.sep = MockOS.sep

        self.assertListEqual(
            runtime._get_search_paths(),
            [
                '/home/GeneEric/forcedimension_sdk/lib/release/lin-x86_64-gcc/'
                'libdrd.so.3.16.0',
                '/home/GeneEric2/forcedimension_sdk/lib/release/lin-x86_64-gcc'
                '/libdrd.so.3.16.0',
                MockOS.path.expanduser('~/.local/lib/libdrd.so'),
                MockOS.path.expanduser('~/.local/lib/libdrd.so.3.16.0'),
                '/usr/local/lib/libdrd.so',
                '/usr/local/lib/libdrd.so.3.16.0'
            ]
        )

        MockGlob.should_fail = True
        self.assertListEqual(
            runtime._get_search_paths(),
            [
                MockOS.path.expanduser('~/.local/lib/libdrd.so'),
                '/usr/local/lib/libdrd.so',
            ]
        )
        MockGlob.should_fail = False


        MockPlatform.machine_type = 'x86_64'
        MockSys.platform = 'linux'
        MockEnviron.FDSDK = ''
        MockEnviron.FORCEDIM_SDK = '/home/GeneEric2/forcedimension_sdk'
        MockOS.sep = '/'
        MockOS.path.sep = MockOS.sep

        self.assertListEqual(
            runtime._get_search_paths(),
            [
                '/home/GeneEric2/forcedimension_sdk/lib/release/lin-x86_64-gcc'
                '/libdrd.so.3.16.0',
                MockOS.path.expanduser('~/.local/lib/libdrd.so'),
                MockOS.path.expanduser('~/.local/lib/libdrd.so.3.16.0'),
                '/usr/local/lib/libdrd.so',
                '/usr/local/lib/libdrd.so.3.16.0'
            ]
        )

        MockPlatform.machine_type = 'x86_64'
        MockSys.platform = 'linux'
        MockEnviron.FDSDK = '/home/GeneEric/forcedimension_sdk'
        MockEnviron.FORCEDIM_SDK = ''
        MockOS.sep = '/'
        MockOS.path.sep = MockOS.sep

        self.assertListEqual(
            runtime._get_search_paths(),
            [
                '/home/GeneEric/forcedimension_sdk/lib/release/lin-x86_64-gcc/'
                'libdrd.so.3.16.0',
                MockOS.path.expanduser('~/.local/lib/libdrd.so'),
                MockOS.path.expanduser('~/.local/lib/libdrd.so.3.16.0'),
                '/usr/local/lib/libdrd.so',
                '/usr/local/lib/libdrd.so.3.16.0'
            ]
        )

        MockPlatform.machine_type = 'x86_64'
        MockSys.platform = 'linux'
        MockEnviron.FDSDK = ''
        MockEnviron.FORCEDIM_SDK = ''
        MockOS.sep = '/'
        MockOS.path.sep = MockOS.sep

        self.assertListEqual(
            runtime._get_search_paths(),
            [
                MockOS.path.expanduser('~/.local/lib/libdrd.so'),
                MockOS.path.expanduser('~/.local/lib/libdrd.so.3.16.0'),
                '/usr/local/lib/libdrd.so',
                '/usr/local/lib/libdrd.so.3.16.0'
            ]
        )

        MockPlatform.machine_type = 'aarch64'
        MockSys.platform = 'linux'
        MockEnviron.FDSDK = '/home/GeneEric/forcedimension_sdk'
        MockEnviron.FORCEDIM_SDK = '/home/GeneEric2/forcedimension_sdk'
        MockOS.sep = '/'
        MockOS.path.sep = MockOS.sep

        self.assertListEqual(
            runtime._get_search_paths(),
            [
                '/home/GeneEric/forcedimension_sdk/lib/release/lin-aarch64-gcc'
                '/libdrd.so.3.16.0',
                '/home/GeneEric2/forcedimension_sdk/lib/release/lin-aarch64-gcc'
                '/libdrd.so.3.16.0',
                MockOS.path.expanduser('~/.local/lib/libdrd.so'),
                MockOS.path.expanduser('~/.local/lib/libdrd.so.3.16.0'),
                '/usr/local/lib/libdrd.so',
                '/usr/local/lib/libdrd.so.3.16.0'
            ]
        )

        MockPlatform.machine_type = 'armv7l'
        MockSys.platform = 'linux'
        MockEnviron.FDSDK = '/home/GeneEric/forcedimension_sdk'
        MockEnviron.FORCEDIM_SDK = '/home/GeneEric2/forcedimension_sdk'
        MockOS.sep = '/'
        MockOS.path.sep = MockOS.sep

        self.assertListEqual(
            runtime._get_search_paths(),
            [
                '/home/GeneEric/forcedimension_sdk/lib/release/lin-armv7l-gcc/'
                'libdrd.so.3.16.0',
                '/home/GeneEric2/forcedimension_sdk/lib/release/lin-armv7l-gcc/'
                'libdrd.so.3.16.0',
                MockOS.path.expanduser('~/.local/lib/libdrd.so'),
                MockOS.path.expanduser('~/.local/lib/libdrd.so.3.16.0'),
                '/usr/local/lib/libdrd.so',
                '/usr/local/lib/libdrd.so.3.16.0'
            ]
        )

        MockPlatform.machine_type = 'x86_64'
        MockSys.platform = 'darwin'
        MockEnviron.FDSDK = '/home/GeneEric/forcedimension_sdk'
        MockEnviron.FORCEDIM_SDK = '/home/GeneEric2/forcedimension_sdk'
        MockOS.sep = '/'
        MockOS.path.sep = MockOS.sep

        self.assertListEqual(
            runtime._get_search_paths(),
            [
                '/home/GeneEric/forcedimension_sdk/lib/release/'
                'mac-x86_64-clang/libdrd.3.16.0.dylib',

                '/home/GeneEric2/forcedimension_sdk/lib/release/'
                'mac-x86_64-clang/libdrd.3.16.0.dylib',

                MockOS.path.expanduser('~/.local/lib/libdrd.dylib'),

                MockOS.path.expanduser('~/.local/lib/libdrd.3.16.0.dylib'),

                '/usr/local/lib/libdrd.dylib',
                '/usr/local/lib/libdrd.3.16.0.dylib'
            ]
        )

        MockPlatform.machine_type = 'arm64'
        MockSys.platform = 'darwin'
        MockEnviron.FDSDK = '/home/GeneEric/forcedimension_sdk'
        MockEnviron.FORCEDIM_SDK = '/home/GeneEric2/forcedimension_sdk'
        MockOS.sep = '/'
        MockOS.path.sep = MockOS.sep

        self.assertListEqual(
            runtime._get_search_paths(),
            [
                '/home/GeneEric/forcedimension_sdk/lib/release/'
                'mac-arm64-clang/libdrd.3.16.0.dylib',

                '/home/GeneEric2/forcedimension_sdk/lib/release/'
                'mac-arm64-clang/libdrd.3.16.0.dylib',

                MockOS.path.expanduser('~/.local/lib/libdrd.dylib'),
                MockOS.path.expanduser('~/.local/lib/libdrd.3.16.0.dylib'),
                '/usr/local/lib/libdrd.dylib',
                '/usr/local/lib/libdrd.3.16.0.dylib'

            ]
        )

        MockGetPass.user = "GeneEric"
        MockSys.platform = 'win32'
        MockPathlib.Path.drive = "C:"
        MockPlatform.bits = '64bit'

        MockOS.sep = '\\'
        MockEnviron.FDSDK = 'C:\\Program Files\\Force Dimension\\sdk-3.16.0'
        MockOS.path.sep = MockOS.sep
        MockOS.path.HOME = 'C:\\Users\\GeneEric'

        self.assertListEqual(
            runtime._get_search_paths(),
            [
                'C:\\Program Files\\Force Dimension\\sdk-3.16.0\\bin\\drd64.dll',

                'C:\\Users\\GeneEric\\AppData\\Local\\'
                'Force Dimension\\sdk-3.16.0\\bin\\drd64.dll',

                'C:\\Program Files\\Force Dimension\\sdk-3.16.0\\bin\\drd64.dll'
            ]
        )

        MockGlob.should_fail = True
        self.assertListEqual(
            runtime._get_search_paths(),
            [
                'C:\\Program Files\\Force Dimension\\sdk-3.16.0\\bin\\drd64.dll'
            ]
        )
        MockGlob.should_fail = False

        MockGetPass.user = "GeneEric"
        MockSys.platform = 'win32'
        MockPathlib.Path.drive = "C:"
        MockPlatform.bits = '64bit'

        MockOS.sep = '\\'
        MockEnviron.FDSDK = ''
        MockOS.path.sep = MockOS.sep
        MockOS.path.HOME = 'C:\\Users\\GeneEric'

        self.assertListEqual(
            runtime._get_search_paths(),
            [
                'C:\\Users\\GeneEric\\AppData\\Local\\'
                'Force Dimension\\sdk-3.16.0\\bin\\drd64.dll',

                'C:\\Program Files\\Force Dimension\\sdk-3.16.0\\bin\\drd64.dll'
            ]
        )

        MockGetPass.user = "GeneEric"
        MockSys.platform = 'win32'
        MockPathlib.Path.drive = "C:"
        MockPlatform.bits = '32bit'

        MockOS.sep = '\\'
        MockEnviron.FDSDK = 'C:\\Program Files\\Force Dimension\\sdk-3.16.0'
        MockOS.path.sep = MockOS.sep
        MockOS.path.HOME = 'C:\\Users\\GeneEric'

        self.assertListEqual(
            runtime._get_search_paths(),
            [
                'C:\\Program Files\\Force Dimension\\sdk-3.16.0\\bin\\drd.dll',

                'C:\\Users\\GeneEric\\AppData\\Local\\'
                'Force Dimension\\sdk-3.16.0\\bin\\drd.dll',

                'C:\\Program Files\\Force Dimension\\sdk-3.16.0\\bin\\drd.dll'
            ]
        )

        MockGetPass.user = "GeneEric"
        MockSys.platform = 'cygwin'
        MockPathlib.Path.drive = "C:"
        MockPlatform.bits = '64bit'

        MockOS.sep = '/'
        MockEnviron.FDSDK = '/cygdrive/c/Program Files/Force Dimension/sdk-3.16.0'
        MockOS.path.sep = MockOS.sep
        # MockOS.path.HOME = 'C:\\Users\\GeneEric'

        self.assertListEqual(
            runtime._get_search_paths(),
            [
                '/cygdrive/c/Program Files/'
                'Force Dimension/sdk-3.16.0/bin/drd64.dll',

                '/cygdrive/c/Users/GeneEric/AppData/Local/'
                'Force Dimension/sdk-3.16.0/bin/drd64.dll',

                '/cygdrive/c/Program Files/'
                'Force Dimension/sdk-3.16.0/bin/drd64.dll',
            ]
        )

        MockGetPass.user = "GeneEric"
        MockSys.platform = 'cygwin'
        MockPathlib.Path.drive = "C:"
        MockPlatform.bits = '64bit'

        MockOS.sep = '/'
        MockEnviron.FDSDK = ''
        MockOS.path.sep = MockOS.sep

        self.assertListEqual(
            runtime._get_search_paths(),
            [
                '/cygdrive/c/Users/GeneEric/AppData/Local/'
                'Force Dimension/sdk-3.16.0/bin/drd64.dll',

                '/cygdrive/c/Program Files/'
                'Force Dimension/sdk-3.16.0/bin/drd64.dll'
            ]
        )

        MockGetPass.user = "GeneEric"
        MockSys.platform = 'cygwin'
        MockPathlib.Path.drive = "C:"
        MockPlatform.bits = '32bit'

        MockOS.sep = '/'
        MockEnviron.FDSDK = '/cygdrive/c/Program Files/Force Dimension/sdk-3.16.0'
        MockOS.path.sep = MockOS.sep

        self.assertListEqual(
            runtime._get_search_paths(),
            [
                '/cygdrive/c/Program Files/'
                'Force Dimension/sdk-3.16.0/bin/drd.dll',

                '/cygdrive/c/Users/GeneEric/AppData/Local/'
                'Force Dimension/sdk-3.16.0/bin/drd.dll',

                '/cygdrive/c/Program Files/'
                'Force Dimension/sdk-3.16.0/bin/drd.dll',
            ]
        )

    def test_load(self):
        runtime._test_load = True

        runtime._ctypes_impl = MockCtypes

        UNSUPPORTED_PLATFORMS = ('aix', 'emscripten', 'wasi')

        for unsupported_platform in UNSUPPORTED_PLATFORMS:
            MockSys.platform = unsupported_platform
            self.assertIsNone(runtime.load())

        MockGetPass.user = "GeneEric"
        MockSys.platform = 'win32'
        MockPathlib.Path.drive = "C:"
        MockPlatform.bits = '64bit'

        MockOS.sep = '\\'
        MockEnviron.FDSDK = 'C:\\Program Files\\Force Dimension\\sdk-3.16.0'
        MockOS.path.sep = MockOS.sep
        MockOS.path.HOME = 'C:\\Users\\GeneEric'

        MockDHD.major = 3
        MockDHD.minor = 16
        MockDHD.release = 0
        MockDHD.revision = 0

        paths = [
            'C:\\Program Files\\Force Dimension\\sdk-3.16.0\\bin\\drd64.dll',

            'C:\\Users\\GeneEric\\AppData\\Local\\'
            'Force Dimension\\sdk-3.16.0\\bin\\drd64.dll',

            'C:\\Program Files\\Force Dimension\\sdk-3.16.0\\bin\\drd64.dll'
        ]

        MockOS.path.VALID_PATHS = set(paths)

        lib = runtime.load()
        self.assertEqual(
            MockEnviron.PATH,
            'C:\\Program Files\\Force Dimension\\sdk-3.16.0\\bin'
        )

        MockEnviron.PATH = 'C:\\Program Files\\Force Dimension\\sdk-3.1.0\\bin'
        lib = runtime.load()
        self.assertEqual(
            MockEnviron.PATH,
            'C:\\Program Files\\Force Dimension\\sdk-3.16.0\\bin;'
            'C:\\Program Files\\Force Dimension\\sdk-3.1.0\\bin'
        )

        MockEnviron.PATH = 'C:\\Program Files\\Force Dimension\\sdk-3.16.0\\bin'
        lib = runtime.load()
        self.assertEqual(
            MockEnviron.PATH,
            'C:\\Program Files\\Force Dimension\\sdk-3.16.0\\bin'
        )

        MockCtypes.should_load_successfully = False

        self.assertIsNone(runtime.load())
        self.assertEqual(
            MockSys.stderr.data,
            "Library was found but could not be loaded. Do you have missing "
            "dependencies?\nEnsure you have libusb-1."
        )

        MockSys.stderr.data = ""
        self.assertIsNone(runtime.load(silent=True))
        self.assertEqual(MockSys.stderr.data, "")

        MockDHD.major = 3
        MockDHD.minor = 15
        MockDHD.release = 0
        MockDHD.revision = 0

        MockCtypes.should_load_successfully = True

        self.assertIsNone(runtime.load())
        self.assertEqual(
            MockSys.stderr.data,
            "Invalid version. v3.15.0-0 found but v3.16.0-0 is required.\n"
        )

        MockSys.stderr.data = ""
        self.assertIsNone(runtime.load(silent=True))
        self.assertEqual(MockSys.stderr.data, "")

        MockDHD.major = 3
        MockDHD.minor = 16
        MockDHD.release = 0
        MockDHD.revision = 0

        for i in range(len(paths) - 1):
            lib = runtime.load()
            self.assertEqual(lib.path, paths[i])  # type: ignore
            MockOS.path.VALID_PATHS.remove(paths[i])

        self.assertIsNone(runtime.load())
        self.assertEqual(
            MockSys.stderr.data,
            "Could not find libdrd. Is it installed?\n"
        )

        MockSys.stderr.data = ""
        self.assertIsNone(runtime.load(silent=True))
        self.assertEqual(MockSys.stderr.data, "")



        MockPlatform.machine_type = 'x86_64'
        MockSys.platform = 'linux'
        MockEnviron.FDSDK = '/home/GeneEric/forcedimension_sdk'
        MockEnviron.FORCEDIM_SDK = '/home/GeneEric2/forcedimension_sdk'
        MockOS.sep = '/'
        MockOS.path.sep = MockOS.sep
        MockOS.path.HOME = '/home/GeneEric'
        MockOS.path.VALID_PATHS = set([
            '/home/GeneEric/forcedimension_sdk/lib/release/lin-x86_64-gcc/'
            'libdrd.so.3.16.0',
            '/home/GeneEric2/forcedimension_sdk/lib/release/lin-x86_64-gcc/'
            'libdrd.so.3.16.0',
            MockOS.path.expanduser('~/.local/lib/libdrd.so'),
            MockOS.path.expanduser('~/.local/lib/libdrd.so.3.16.0'),
            '/usr/local/lib/libdrd.so',
            '/usr/local/lib/libdrd.so.3.16.0'
        ])

        self.assertEqual(
            runtime.load().path,   # type: ignore
            '/home/GeneEric/forcedimension_sdk/lib/release/lin-x86_64-gcc/'
            'libdrd.so.3.16.0'
        )

        os.environ['__fdsdkpy_unittest_runtime__'] = 'True'
        self.assertRaises(ImportError, lambda: importlib.reload(runtime))

        os.environ['__fdsdkpy_unittest_runtime__'] = 'False'
        runtime._ctypes_impl = ctypes
        runtime._getpass_impl = getpass
        runtime._glob_impl = glob
        runtime._os_impl = os
        runtime._pathlib_impl = pathlib
        runtime._platform_impl = platform
        runtime._sys_impl = sys

        runtime._test_load = False
