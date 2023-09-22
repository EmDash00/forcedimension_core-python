from ctypes import CFUNCTYPE, c_bool, c_byte, c_double
from typing import Any
from random import random
import unittest

import forcedimension_core.dhd as dhd
import forcedimension_core.runtime as runtime

libdhd = runtime._libdhd


class MockDHD:
    class dhdKbHit:
        argtypes = []
        restype = c_bool
        ret = True

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock():
            return MockDHD.dhdKbHit.ret

    class dhdKbGet:
        argtypes = []
        restype = c_byte
        ret = 0x4B

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock():
            return MockDHD.dhdKbGet.ret


    class dhdGetTime:
        argtypes = []
        restype = c_double
        ret = 0.0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock():
            return MockDHD.dhdGetTime.ret


    class dhdSleep:
        argtypes = [c_double]
        restype = None


class TestOSIndependentSDK(unittest.TestCase):
    def assertSignaturesEqual(self, first: Any, second: Any):
        for argtype1, argtype2 in zip(first.argtypes, second.argtypes):
            self.assertIs(argtype1, argtype2)

        self.assertIs(first.restype, second.restype)

    def test_kbHit(self):
        self.assertSignaturesEqual(libdhd.dhdKbHit, MockDHD.dhdKbHit)

        libdhd.dhdKbHit = MockDHD.dhdKbHit.mock  # type: ignore

        MockDHD.dhdKbHit.ret = True
        self.assertEqual(dhd.os_independent.kbHit(), MockDHD.dhdKbHit.ret)

        MockDHD.dhdKbHit.ret = False
        self.assertEqual(dhd.os_independent.kbHit(), MockDHD.dhdKbHit.ret)

    def test_kbGet(self):
        self.assertSignaturesEqual(libdhd.dhdKbGet, MockDHD.dhdKbGet)

        libdhd.dhdKbGet = MockDHD.dhdKbGet.mock  # type: ignore

        for i in range(128):
            MockDHD.dhdKbGet.ret = i
            self.assertEqual(
                dhd.os_independent.kbGet(), chr(MockDHD.dhdKbGet.ret)
            )

    def test_getTime(self):
        self.assertSignaturesEqual(libdhd.dhdGetTime, MockDHD.dhdGetTime)

        libdhd.dhdGetTime = MockDHD.dhdGetTime.mock  # type: ignore

        for _ in range(100_000):
            MockDHD.dhdGetTime.ret = random()
            self.assertEqual(
                dhd.os_independent.getTime(), MockDHD.dhdGetTime.ret
            )

    def test_sleep(self):
        self.assertSignaturesEqual(libdhd.dhdSleep, MockDHD.dhdSleep)
