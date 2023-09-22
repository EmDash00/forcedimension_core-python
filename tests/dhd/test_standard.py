import unittest
import warnings
from ctypes import (CFUNCTYPE, POINTER, c_bool, c_byte, c_char, c_char_p,
                    c_double, c_int, c_size_t, c_ubyte, c_uint, c_uint32,
                    c_ushort)
from random import randint, random
from typing import Any, Optional
from forcedimension_core.containers import Status

import forcedimension_core.dhd as dhd
import forcedimension_core.runtime as runtime
from forcedimension_core import ErrorNum
from forcedimension_core.dhd.constants import MAX_STATUS, ComMode, DeviceType, VelocityEstimatorMode

libdhd = runtime._libdhd


class MockDHD:
    class dhdErrorGetLast:
        argtypes = []
        restype = c_int

        ret: int = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock():
            return MockDHD.dhdErrorGetLast.ret

    class dhdErrorGetLastStr:
        argtypes = []
        restype = c_char_p
        errno: int = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock():
            return MockDHD.dhdErrorGetStr.mock(
                MockDHD.dhdErrorGetLastStr.errno
            )

    class dhdErrorGetStr:
        argtypes = [c_int]
        restype = c_char_p

        err_strs = [
            'no error',
            'undocumented error',
            'communication error',
            'device controller busy',
            'no driver found',
            'no device found',
            'operation not available',
            'operation timed out',
            'geometric error',
            'expert mode disabled',
            'feature not implemented',
            'out of memory',
            'device not ready',
            'file not found',
            'device configuration failed',
            'index outside valid range',
            'feature or device no longer supported',
            'argument is null or invalid',
            'redundant encoder integrity test failed',
            'feature is not enabled',
            'device is in use',
            'invalid parameter',
            'robotic regulation is not running'
        ]

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(errno: int):
            return MockDHD.dhdErrorGetStr.err_strs[errno].encode('ascii')

    class dhdEnableSimulator:
        argtypes = [c_bool]
        restype = None

        enable = False

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enable: bool):
            MockDHD.dhdEnableSimulator.enable = enable

    class dhdGetDeviceCount:
        argtypes = []
        restype = c_int
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock():
            return MockDHD.dhdGetDeviceCount.ret

    class dhdGetAvailableCount:
        argtypes = []
        restype = c_int
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock():
            return MockDHD.dhdGetAvailableCount.ret

    class dhdSetDevice:
        argtypes = [c_byte]
        restype = c_int

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdSetDevice.ID = ID

            return MockDHD.dhdSetDevice.ret


    class dhdGetDeviceID:
        argtypes = []
        restype = c_int
        ID: int = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock():
            return MockDHD.dhdGetDeviceID.ID

    class dhdGetSerialNumber:
        argtypes = [POINTER(c_ushort), c_byte]
        restype = c_int

        serial_number = 1

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(serial_number, ID):
            MockDHD.dhdGetSerialNumber.ID = ID
            serial_number.contents.value = MockDHD.dhdGetSerialNumber.serial_number

            return MockDHD.dhdGetSerialNumber.ret

    class dhdOpen:
        argtypes = []
        restype = c_int
        is_open = True
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock():
            MockDHD.dhdOpen.is_open = True
            MockDHD.dhdOpenType.is_open = True
            MockDHD.dhdOpenSerial.is_open = True
            MockDHD.dhdOpenID.is_open = True

            return MockDHD.dhdOpen.ret

    class dhdOpenType:
        argtypes = [c_int]
        restype = c_int

        devtype = DeviceType.NONE
        is_open = True
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(devtype):
            MockDHD.dhdOpenType.devtype = devtype

            MockDHD.dhdOpen.is_open = True
            MockDHD.dhdOpenType.is_open = True
            MockDHD.dhdOpenSerial.is_open = True
            MockDHD.dhdOpenID.is_open = True

            return MockDHD.dhdOpenType.ret

    class dhdOpenSerial:
        argtypes = [c_int]
        restype = c_int

        serial = 0
        is_open = True
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(serial):
            MockDHD.dhdOpenSerial.serial = serial
            MockDHD.dhdOpen.is_open = True
            MockDHD.dhdOpenType.is_open = True
            MockDHD.dhdOpenSerial.is_open = True
            MockDHD.dhdOpenID.is_open = True

            return MockDHD.dhdOpenSerial.ret

    class dhdOpenID:
        argtypes = [c_byte]
        restype = c_int

        ID = 0
        is_open = True
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdOpen.is_open = True
            MockDHD.dhdOpenType.is_open = True
            MockDHD.dhdOpenSerial.is_open = True
            MockDHD.dhdOpenID.is_open = True

            MockDHD.dhdOpenID.ID = ID

            return MockDHD.dhdOpenID.ret

    class dhdClose:
        argtypes = [c_byte]
        restype = c_int

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdClose.ID = ID

            MockDHD.dhdOpen.is_open = False
            MockDHD.dhdOpenType.is_open = False
            MockDHD.dhdOpenSerial.is_open = False
            MockDHD.dhdOpenID.is_open = False

            return MockDHD.dhdClose.ret

    class dhdCheckControllerMemory:
        argtypes = [c_byte]
        restype = c_int

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdCheckControllerMemory.ID = ID
            return MockDHD.dhdCheckControllerMemory.ret

    class dhdStop:
        argtypes = [c_byte]
        restype = c_int

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdStop.ID = ID
            return MockDHD.dhdStop.ret

    class dhdGetComMode:
        argtypes = [c_byte]
        restype = c_int

        ID = 0
        ret = ComMode.SYNC

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdGetComMode.ID = ID
            return MockDHD.dhdGetComMode.ret

    class dhdEnableForce:
        argtypes = [c_bool, c_byte]
        restype = c_int

        ID = 0
        ret = 0
        is_enabled = False

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enable, ID):
            MockDHD.dhdEnableForce.ID = ID
            MockDHD.dhdEnableForce.is_enabled = enable

            return MockDHD.dhdEnableForce.ret

    class dhdEnableGripperForce:
        argtypes = [c_bool, c_byte]
        restype = c_int

        ID = 0
        ret = 0
        is_enabled = False

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enable, ID):
            MockDHD.dhdEnableGripperForce.ID = ID
            MockDHD.dhdEnableForce.is_enabled = enable

            return MockDHD.dhdEnableGripperForce.ret

    class dhdGetSystemType:
        argtypes = [c_byte]
        restype = c_int

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdGetSystemType.ID = ID
            return MockDHD.dhdGetSystemType.ret

    class dhdGetSystemRev:
        argtypes = [c_byte]
        restype = c_int

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdGetSystemRev.ID = ID
            return MockDHD.dhdGetSystemRev.ret

    class dhdGetSystemName:
        argtypes = [c_byte]
        restype = c_char_p

        ID = 0
        ret: Optional[bytes] = b"lorem ipsem"

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdGetSystemName.ID = ID
            return MockDHD.dhdGetSystemName.ret

    class dhdGetVersion:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        ID = 0
        ver = 3.14
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ver, ID):
            MockDHD.dhdGetVersion.ID = ID
            ver.contents.value = MockDHD.dhdGetVersion.ver

            return MockDHD.dhdGetVersion.ret

    class dhdGetSDKVersion:
        argtypes = [
            POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int)
        ]
        restype = None

        major = 3
        minor = 16
        release = 0
        revision = 0

        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(major, minor, release, revision):
            major.contents.value = MockDHD.dhdGetSDKVersion.major
            minor.contents.value = MockDHD.dhdGetSDKVersion.minor
            release.contents.value = MockDHD.dhdGetSDKVersion.release
            revision.contents.value = MockDHD.dhdGetSDKVersion.revision

            return MockDHD.dhdGetSDKVersion.ret

    class dhdGetComponentVersionStr:
        argtypes = [c_uint32, c_char_p, c_size_t, c_byte]
        restype = c_int

        ID = 0
        ret = 0

        component = 0

        description = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
            "do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco "
            "laboris nisi ut aliquip ex ea commodo consequat. Duis aute "
            "irure dolor in reprehenderit in voluptate velit esse cillum "
            "dolore eu fugiat nulla pariatur. Excepteur sint occaecat "
            "cupidatat non proident, sunt in culpa qui officia deserunt "
            "mollit anim id est laborum. "
        )

        @staticmethod
        @CFUNCTYPE(restype, c_uint32, POINTER(c_char), c_size_t, c_byte)
        def mock(component, buffer, size, ID):
            for i in range(size):
                buffer[i] = ord(
                    MockDHD.dhdGetComponentVersionStr.description[i]
                )

            MockDHD.dhdGetComponentVersionStr.component = component
            MockDHD.dhdGetComponentVersionStr.ID = ID

            return MockDHD.dhdGetComponentVersionStr.ret

    class dhdGetStatus:
        argtypes = [POINTER(c_int), c_byte]
        restype = c_int

        ID = 0
        status = Status()
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(status, ID):
            MockDHD.dhdGetStatus.ID = ID

            for i in range(MAX_STATUS):
                status[i] = MockDHD.dhdGetStatus.status[i]

            return MockDHD.dhdGetStatus.ret


    class dhdGetDeviceAngleRad:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        angle: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(angle, ID):
            MockDHD.dhdGetDeviceAngleRad.ID = ID
            angle.contents.value = MockDHD.dhdGetDeviceAngleRad.angle
            return MockDHD.dhdGetDeviceAngleRad.ret

    class dhdGetDeviceAngleDeg:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        angle: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(angle, ID):
            MockDHD.dhdGetDeviceAngleDeg.ID = ID
            angle.contents.value = MockDHD.dhdGetDeviceAngleDeg.angle
            return MockDHD.dhdGetDeviceAngleDeg.ret

    class dhdGetEffectorMass:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        ID = 0
        mass: float = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(mass, ID):
            MockDHD.dhdGetEffectorMass.ID = ID
            mass.contents.value = MockDHD.dhdGetEffectorMass.mass
            return MockDHD.dhdGetEffectorMass.ret

    class dhdGetButton:
        argtypes = [c_int, c_byte]
        restype = c_int

        ID = 0
        ret: int = 0

        index = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(index, ID):
            MockDHD.dhdGetButton.ID = ID
            MockDHD.dhdGetButton.index = index
            return MockDHD.dhdGetButton.ret

    class dhdGetButtonMask:
        argtypes = [c_byte]
        restype = c_uint

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdGetButtonMask.ID = ID
            return MockDHD.dhdGetButtonMask.ret

    class dhdSetOutput:
        argtypes = [c_uint, c_byte]
        restype = c_int

        mask = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(mask, ID):
            MockDHD.dhdSetOutput.ID = ID
            MockDHD.dhdSetOutput.mask = mask
            return MockDHD.dhdSetOutput.ret

    class dhdIsLeftHanded:
        argtypes = [c_byte]
        restype = c_bool

        ID = 0
        ret = False

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdIsLeftHanded.ID = ID
            return MockDHD.dhdIsLeftHanded.ret


    class dhdHasBase:
        argtypes = [c_byte]
        restype = c_bool

        ID = 0
        ret = False

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdHasBase.ID = ID
            return MockDHD.dhdHasBase.ret

    class dhdHasWrist:
        argtypes = [c_byte]
        restype = c_bool

        ID = 0
        ret = False

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdHasWrist.ID = ID
            return MockDHD.dhdHasWrist.ret

    class dhdHasActiveWrist:
        argtypes = [c_byte]
        restype = c_bool

        ID = 0
        ret = False

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdHasActiveWrist.ID = ID
            return MockDHD.dhdHasActiveWrist.ret

    class dhdHasGripper:
        argtypes = [c_byte]
        restype = c_bool

        ID = 0
        ret = False

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdHasGripper.ID = ID
            return MockDHD.dhdHasGripper.ret

    class dhdHasActiveGripper:
        argtypes = [c_byte]
        restype = c_bool

        ID = 0
        ret = False

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdHasActiveGripper.ID = ID
            return MockDHD.dhdHasActiveGripper.ret

    class dhdReset:
        argtypes = [c_byte]
        restype = c_int

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdReset.ID = ID
            return MockDHD.dhdReset.ret

    class dhdWaitForReset:
        argtypes = [c_int, c_byte]
        restype = c_int

        timeout: int = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(timeout, ID):
            MockDHD.dhdWaitForReset.ID = ID
            MockDHD.dhdWaitForReset.timeout = timeout

            return MockDHD.dhdWaitForReset.ret

    class dhdSetStandardGravity:
        argtypes = [c_double, c_byte]
        restype = c_int

        gravity: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(gravity, ID):
            MockDHD.dhdSetStandardGravity.ID = ID
            MockDHD.dhdSetStandardGravity.gravity = gravity
            return MockDHD.dhdSetStandardGravity.ret

    class dhdSetGravityCompensation:
        argtypes = [c_bool, c_byte]
        restype = c_int

        enabled: bool = False

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enabled, ID):
            MockDHD.dhdSetGravityCompensation.ID = ID
            MockDHD.dhdSetGravityCompensation.enabled = enabled
            return MockDHD.dhdSetGravityCompensation.ret


    class dhdSetBrakes:
        argtypes = [c_bool, c_byte]
        restype = c_int

        enabled = False

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enabled, ID):
            MockDHD.dhdSetBrakes.ID = ID
            MockDHD.dhdSetBrakes.enabled = enabled
            return MockDHD.dhdSetBrakes.ret

    class dhdSetDeviceAngleRad:
        argtypes = [c_double, c_byte]
        restype = c_int

        angle = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(angle, ID):
            MockDHD.dhdSetDeviceAngleRad.ID = ID
            MockDHD.dhdSetDeviceAngleRad.angle = angle
            return MockDHD.dhdSetDeviceAngleRad.ret

    class dhdSetDeviceAngleDeg:
        argtypes = [c_double, c_byte]
        restype = c_int

        angle = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(angle, ID):
            MockDHD.dhdSetDeviceAngleDeg.ID = ID
            MockDHD.dhdSetDeviceAngleDeg.angle = angle
            return MockDHD.dhdSetDeviceAngleDeg.ret

    class dhdSetEffectorMass:
        argtypes = [c_double, c_byte]
        restype = c_int

        mass = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(mass, ID):
            MockDHD.dhdSetEffectorMass.ID = ID
            MockDHD.dhdSetEffectorMass.mass = mass

            return MockDHD.dhdSetEffectorMass.ret

    class dhdGetPosition:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        px: float = 0
        py: float = 0
        pz: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(px, py, pz, ID):
            MockDHD.dhdGetPosition.ID = ID

            px.contents.value = MockDHD.dhdGetPosition.px
            py.contents.value = MockDHD.dhdGetPosition.py
            pz.contents.value = MockDHD.dhdGetPosition.pz

            return MockDHD.dhdGetPosition.ret

    class dhdGetForce:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        fx: float = 0
        fy: float = 0
        fz: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(fx, fy, fz, ID):
            MockDHD.dhdGetForce.ID = ID

            fx.contents.value = MockDHD.dhdGetForce.fx
            fy.contents.value = MockDHD.dhdGetForce.fy
            fz.contents.value = MockDHD.dhdGetForce.fz

            return MockDHD.dhdGetForce.ret

    class dhdSetForce:
        argtypes = [c_double, c_double, c_double, c_byte]
        restype = c_int

        fx = 0
        fy = 0
        fz = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(fx, fy, fz, ID):
            MockDHD.dhdSetForce.ID = ID

            MockDHD.dhdSetForce.fx = fx
            MockDHD.dhdSetForce.fy = fy
            MockDHD.dhdSetForce.fz = fz

            return MockDHD.dhdSetForce.ret

    class dhdGetOrientationRad:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        oa: float = 0
        ob: float = 0
        og: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(oa, ob, og, ID):
            MockDHD.dhdGetOrientationRad.ID = ID

            oa.contents.value = MockDHD.dhdGetOrientationRad.oa
            ob.contents.value = MockDHD.dhdGetOrientationRad.ob
            og.contents.value = MockDHD.dhdGetOrientationRad.og

            return MockDHD.dhdGetOrientationRad.ret

    class dhdGetOrientationDeg:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        oa: float = 0
        ob: float = 0
        og: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(oa, ob, og, ID):
            MockDHD.dhdGetOrientationDeg.ID = ID

            oa.contents.value = MockDHD.dhdGetOrientationDeg.oa
            ob.contents.value = MockDHD.dhdGetOrientationDeg.ob
            og.contents.value = MockDHD.dhdGetOrientationDeg.og

            return MockDHD.dhdGetOrientationDeg.ret

    class dhdGetPositionAndOrientationRad:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double),
            POINTER(c_double), POINTER(c_double), POINTER(c_double),
            c_byte
        ]
        restype = c_int

        px: float = 0
        py: float = 0
        pz: float = 0

        oa: float = 0
        ob: float = 0
        og: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(px, py, pz, oa, ob, og, ID):
            MockDHD.dhdGetPositionAndOrientationRad.ID = ID

            px.contents.value = MockDHD.dhdGetPositionAndOrientationRad.px
            py.contents.value = MockDHD.dhdGetPositionAndOrientationRad.py
            pz.contents.value = MockDHD.dhdGetPositionAndOrientationRad.pz

            oa.contents.value = MockDHD.dhdGetPositionAndOrientationRad.oa
            ob.contents.value = MockDHD.dhdGetPositionAndOrientationRad.ob
            og.contents.value = MockDHD.dhdGetPositionAndOrientationRad.og

            return MockDHD.dhdGetPositionAndOrientationRad.ret

    class dhdGetPositionAndOrientationDeg:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double),
            POINTER(c_double), POINTER(c_double), POINTER(c_double),
            c_byte
        ]
        restype = c_int

        px: float = 0
        py: float = 0
        pz: float = 0

        oa: float = 0
        ob: float = 0
        og: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(px, py, pz, oa, ob, og, ID):
            MockDHD.dhdGetPositionAndOrientationDeg.ID = ID

            px.contents.value = MockDHD.dhdGetPositionAndOrientationDeg.px
            py.contents.value = MockDHD.dhdGetPositionAndOrientationDeg.py
            pz.contents.value = MockDHD.dhdGetPositionAndOrientationDeg.pz

            oa.contents.value = MockDHD.dhdGetPositionAndOrientationDeg.oa
            ob.contents.value = MockDHD.dhdGetPositionAndOrientationDeg.ob
            og.contents.value = MockDHD.dhdGetPositionAndOrientationDeg.og

            return MockDHD.dhdGetPositionAndOrientationDeg.ret

    class dhdGetPositionAndOrientationFrame:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double),
            POINTER(c_double), c_byte
        ]
        restype = c_int

        px: float = 0
        py: float = 0
        pz: float = 0

        frame = [[0.0] * 3] * 3

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(px, py, pz, frame, ID):
            MockDHD.dhdGetPositionAndOrientationFrame.ID = ID

            px.contents.value = MockDHD.dhdGetPositionAndOrientationFrame.px
            py.contents.value = MockDHD.dhdGetPositionAndOrientationFrame.py
            pz.contents.value = MockDHD.dhdGetPositionAndOrientationFrame.pz

            for i in range(3):
                for j in range(3):
                    frame[3 * i + j] = (
                        MockDHD.dhdGetPositionAndOrientationFrame.frame[i][j]
                    )

            return MockDHD.dhdGetPositionAndOrientationFrame.ret

    class dhdGetForceAndTorque:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double),
            POINTER(c_double), POINTER(c_double), POINTER(c_double),
            c_byte
        ]
        restype = c_int

        fx: float = 0
        fy: float = 0
        fz: float = 0

        tx: float = 0
        ty: float = 0
        tz: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(fx, fy, fz, tx, ty, tz, ID):
            MockDHD.dhdGetForceAndTorque.ID = ID

            fx.contents.value = MockDHD.dhdGetForceAndTorque.fx
            fy.contents.value = MockDHD.dhdGetForceAndTorque.fy
            fz.contents.value = MockDHD.dhdGetForceAndTorque.fz

            tx.contents.value = MockDHD.dhdGetForceAndTorque.tx
            ty.contents.value = MockDHD.dhdGetForceAndTorque.ty
            tz.contents.value = MockDHD.dhdGetForceAndTorque.tz

            return MockDHD.dhdGetForceAndTorque.ret

    class dhdSetForceAndTorque:
        argtypes = [
            c_double, c_double, c_double, c_double, c_double, c_double, c_byte
        ]
        restype = c_int

        fx = 0
        fy = 0
        fz = 0

        tx = 0
        ty = 0
        tz = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(fx, fy, fz, tx, ty, tz, ID):
            MockDHD.dhdSetForceAndTorque.ID = ID

            MockDHD.dhdSetForceAndTorque.fx = fx
            MockDHD.dhdSetForceAndTorque.fy = fy
            MockDHD.dhdSetForceAndTorque.fz = fz

            MockDHD.dhdSetForceAndTorque.tx = tx
            MockDHD.dhdSetForceAndTorque.ty = ty
            MockDHD.dhdSetForceAndTorque.tz = tz

            return MockDHD.dhdSetForceAndTorque.ret

    class dhdGetOrientationFrame:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        frame = [[0.0] * 3] * 3

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(frame, ID):
            MockDHD.dhdGetOrientationFrame.ID = ID

            for i in range(3):
                for j in range(3):
                    frame[3 * i + j] = (
                        MockDHD.dhdGetOrientationFrame.frame[i][j]
                    )

            return MockDHD.dhdGetOrientationFrame.ret


    class dhdGetGripperAngleDeg:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        angle: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(angle, ID):
            MockDHD.dhdGetGripperAngleDeg.ID = ID
            angle.contents.value = MockDHD.dhdGetGripperAngleDeg.angle
            return MockDHD.dhdGetGripperAngleDeg.ret

    class dhdGetGripperAngleRad:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        angle: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(angle, ID):
            MockDHD.dhdGetGripperAngleRad.ID = ID
            angle.contents.value = MockDHD.dhdGetGripperAngleRad.angle
            return MockDHD.dhdGetGripperAngleRad.ret

    class dhdGetGripperGap:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        gap: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(gap, ID):
            MockDHD.dhdGetGripperGap.ID = ID
            gap.contents.value = MockDHD.dhdGetGripperGap.gap
            return MockDHD.dhdGetGripperGap.ret

    class dhdGetGripperThumbPos:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        px: float = 0
        py: float = 0
        pz: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(px, py, pz, ID):
            MockDHD.dhdGetGripperThumbPos.ID = ID

            px.contents.value = MockDHD.dhdGetGripperThumbPos.px
            py.contents.value = MockDHD.dhdGetGripperThumbPos.py
            pz.contents.value = MockDHD.dhdGetGripperThumbPos.pz

            return MockDHD.dhdGetGripperThumbPos.ret

    class dhdGetGripperFingerPos:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        px: float = 0
        py: float = 0
        pz: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(px, py, pz, ID):
            MockDHD.dhdGetGripperFingerPos.ID = ID

            px.contents.value = MockDHD.dhdGetGripperFingerPos.px
            py.contents.value = MockDHD.dhdGetGripperFingerPos.py
            pz.contents.value = MockDHD.dhdGetGripperFingerPos.pz

            return MockDHD.dhdGetGripperFingerPos.ret

    class dhdGetComFreq:
        argtypes = [c_byte]
        restype = c_double

        ID = 0
        ret: float = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdGetComFreq.ID = ID
            return MockDHD.dhdGetComFreq.ret


    class dhdSetForceAndGripperForce:
        argtypes = [c_double, c_double, c_double, c_double, c_byte]
        restype = c_int

        fx = 0
        fy = 0
        fz = 0
        fg = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(fx, fy, fz, fg, ID):
            MockDHD.dhdSetForceAndGripperForce.ID = ID

            MockDHD.dhdSetForceAndGripperForce.fx = fx
            MockDHD.dhdSetForceAndGripperForce.fy = fy
            MockDHD.dhdSetForceAndGripperForce.fz = fz
            MockDHD.dhdSetForceAndGripperForce.fg = fg

            return MockDHD.dhdSetForceAndGripperForce.ret


    class dhdSetForceAndTorqueAndGripperForce:
        argtypes = [
            c_double, c_double, c_double, c_double,
            c_double, c_double, c_double, c_byte
        ]
        restype = c_int

        fx = 0
        fy = 0
        fz = 0
        tx = 0
        ty = 0
        tz = 0
        fg = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(fx, fy, fz, tx, ty, tz, fg, ID):
            MockDHD.dhdSetForceAndTorqueAndGripperForce.ID = ID

            MockDHD.dhdSetForceAndTorqueAndGripperForce.fx = fx
            MockDHD.dhdSetForceAndTorqueAndGripperForce.fy = fy
            MockDHD.dhdSetForceAndTorqueAndGripperForce.fz = fz
            MockDHD.dhdSetForceAndTorqueAndGripperForce.tx = tx
            MockDHD.dhdSetForceAndTorqueAndGripperForce.ty = ty
            MockDHD.dhdSetForceAndTorqueAndGripperForce.tz = tz
            MockDHD.dhdSetForceAndTorqueAndGripperForce.fg = fg

            return MockDHD.dhdSetForceAndTorqueAndGripperForce.ret

    class dhdGetForceAndTorqueAndGripperForce:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double),
            POINTER(c_double), POINTER(c_double), POINTER(c_double),
            POINTER(c_double), c_byte
        ]
        restype = c_int

        fx: float = 0
        fy: float = 0
        fz: float = 0

        tx: float = 0
        ty: float = 0
        tz: float = 0

        fg: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(fx, fy, fz, tx, ty, tz, fg, ID):
            MockDHD.dhdGetForceAndTorqueAndGripperForce.ID = ID

            fx.contents.value = MockDHD.dhdGetForceAndTorqueAndGripperForce.fx
            fy.contents.value = MockDHD.dhdGetForceAndTorqueAndGripperForce.fy
            fz.contents.value = MockDHD.dhdGetForceAndTorqueAndGripperForce.fz

            tx.contents.value = MockDHD.dhdGetForceAndTorqueAndGripperForce.tx
            ty.contents.value = MockDHD.dhdGetForceAndTorqueAndGripperForce.ty
            tz.contents.value = MockDHD.dhdGetForceAndTorqueAndGripperForce.tz

            fg.contents.value = MockDHD.dhdGetForceAndTorqueAndGripperForce.fg

            return MockDHD.dhdGetForceAndTorqueAndGripperForce.ret


    class dhdConfigLinearVelocity:
        argtypes = [c_int, c_int, c_byte]
        restype = c_int

        ms = 0
        mode = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ms, mode, ID):
            MockDHD.dhdConfigLinearVelocity.ID = ID

            MockDHD.dhdConfigLinearVelocity.ms = ms
            MockDHD.dhdConfigLinearVelocity.mode = mode

            return MockDHD.dhdConfigLinearVelocity.ret

    class dhdGetLinearVelocity:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        vx: float = 0
        vy: float = 0
        vz: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(vx, vy, vz, ID):
            MockDHD.dhdGetLinearVelocity.ID = ID

            vx.contents.value = MockDHD.dhdGetLinearVelocity.vx
            vy.contents.value = MockDHD.dhdGetLinearVelocity.vy
            vz.contents.value = MockDHD.dhdGetLinearVelocity.vz

            return MockDHD.dhdGetLinearVelocity.ret

    class dhdConfigAngularVelocity:
        argtypes = [c_int, c_int, c_byte]
        restype = c_int

        ms = 0
        mode = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ms, mode, ID):
            MockDHD.dhdConfigAngularVelocity.ID = ID

            MockDHD.dhdConfigAngularVelocity.ms = ms
            MockDHD.dhdConfigAngularVelocity.mode = mode

            return MockDHD.dhdConfigAngularVelocity.ret

    class dhdGetAngularVelocityRad:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        wx: float = 0
        wy: float = 0
        wz: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(wx, wy, wz, ID):
            MockDHD.dhdGetAngularVelocityRad.ID = ID

            wx.contents.value = MockDHD.dhdGetAngularVelocityRad.wx
            wy.contents.value = MockDHD.dhdGetAngularVelocityRad.wy
            wz.contents.value = MockDHD.dhdGetAngularVelocityRad.wz

            return MockDHD.dhdGetAngularVelocityRad.ret


    class dhdGetAngularVelocityDeg:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        wx: float = 0
        wy: float = 0
        wz: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(wx, wy, wz, ID):
            MockDHD.dhdGetAngularVelocityDeg.ID = ID

            wx.contents.value = MockDHD.dhdGetAngularVelocityDeg.wx
            wy.contents.value = MockDHD.dhdGetAngularVelocityDeg.wy
            wz.contents.value = MockDHD.dhdGetAngularVelocityDeg.wz

            return MockDHD.dhdGetAngularVelocityDeg.ret

    class dhdConfigGripperVelocity:
        argtypes = [c_int, c_int, c_byte]
        restype = c_int

        ms = 0
        mode = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ms, mode, ID):
            MockDHD.dhdConfigGripperVelocity.ID = ID

            MockDHD.dhdConfigGripperVelocity.ms = ms
            MockDHD.dhdConfigGripperVelocity.mode = mode

            return MockDHD.dhdConfigGripperVelocity.ret

    class dhdGetGripperLinearVelocity:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        vg: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(vg, ID):
            MockDHD.dhdGetGripperLinearVelocity.ID = ID
            vg.contents.value = MockDHD.dhdGetGripperLinearVelocity.vg
            return MockDHD.dhdGetGripperLinearVelocity.ret

    class dhdGetGripperAngularVelocityRad:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        wg: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(wg, ID):
            MockDHD.dhdGetGripperAngularVelocityRad.ID = ID
            wg.contents.value = MockDHD.dhdGetGripperAngularVelocityRad.wg
            return MockDHD.dhdGetGripperAngularVelocityRad.ret

    class dhdGetGripperAngularVelocityDeg:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        wg: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(wg, ID):
            MockDHD.dhdGetGripperAngularVelocityDeg.ID = ID
            wg.contents.value = MockDHD.dhdGetGripperAngularVelocityDeg.wg
            return MockDHD.dhdGetGripperAngularVelocityDeg.ret


    class dhdEmulateButton:
        argtypes = [c_bool, c_byte]
        restype = c_int

        enable = False

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enable, ID):
            MockDHD.dhdEmulateButton.ID = ID
            MockDHD.dhdEmulateButton.enable = enable
            return MockDHD.dhdEmulateButton.ret

    class dhdGetBaseAngleXRad:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        base_angle_x: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(base_angle_x, ID):
            MockDHD.dhdGetBaseAngleXRad.ID = ID
            base_angle_x.contents.value = (
                MockDHD.dhdGetBaseAngleXRad.base_angle_x
            )
            return MockDHD.dhdGetBaseAngleXRad.ret

    class dhdGetBaseAngleXDeg:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        base_angle_x: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(base_angle_x, ID):
            MockDHD.dhdGetBaseAngleXDeg.ID = ID
            base_angle_x.contents.value = (
                MockDHD.dhdGetBaseAngleXDeg.base_angle_x
            )
            return MockDHD.dhdGetBaseAngleXDeg.ret

    class dhdSetBaseAngleXRad:
        argtypes = [c_double, c_byte]
        restype = c_int

        base_angle_x = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(base_angle_x, ID):
            MockDHD.dhdSetBaseAngleXRad.ID = ID
            MockDHD.dhdSetBaseAngleXRad.base_angle_x = base_angle_x
            return MockDHD.dhdSetBaseAngleXRad.ret

    class dhdSetBaseAngleXDeg:
        argtypes = [c_double, c_byte]
        restype = c_int

        base_angle_x = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(base_angle_x, ID):
            MockDHD.dhdSetBaseAngleXDeg.ID = ID
            MockDHD.dhdSetBaseAngleXDeg.base_angle_x = base_angle_x
            return MockDHD.dhdSetBaseAngleXDeg.ret

    class dhdGetBaseAngleZRad:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        base_angle_z: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(base_angle_z, ID):
            MockDHD.dhdGetBaseAngleZRad.ID = ID
            base_angle_z.contents.value = (
                MockDHD.dhdGetBaseAngleZRad.base_angle_z
            )
            return MockDHD.dhdGetBaseAngleZRad.ret

    class dhdGetBaseAngleZDeg:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        base_angle_z: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(base_angle_z, ID):
            MockDHD.dhdGetBaseAngleZDeg.ID = ID
            base_angle_z.contents.value = (
                MockDHD.dhdGetBaseAngleZDeg.base_angle_z
            )
            return MockDHD.dhdGetBaseAngleZDeg.ret

    class dhdSetBaseAngleZRad:
        argtypes = [c_double, c_byte]
        restype = c_int

        base_angle_z = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(base_angle_z, ID):
            MockDHD.dhdSetBaseAngleZRad.ID = ID
            MockDHD.dhdSetBaseAngleZRad.base_angle_z = base_angle_z
            return MockDHD.dhdSetBaseAngleZRad.ret

    class dhdSetBaseAngleZDeg:
        argtypes = [c_double, c_byte]
        restype = c_int

        base_angle_z = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(base_angle_z, ID):
            MockDHD.dhdSetBaseAngleZDeg.ID = ID
            MockDHD.dhdSetBaseAngleZDeg.base_angle_z = base_angle_z
            return MockDHD.dhdSetBaseAngleZDeg.ret

    class dhdSetVibration:
        argtypes = [c_double, c_double, c_int, c_byte]
        restype = c_int

        freq = 0
        amplitude = 0
        profile = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(freq, amplitude, profile, ID):
            MockDHD.dhdSetVibration.ID = ID
            MockDHD.dhdSetVibration.freq = freq
            MockDHD.dhdSetVibration.amplitude = amplitude
            MockDHD.dhdSetVibration.profile = profile

            return MockDHD.dhdSetVibration.ret

    class dhdSetMaxForce:
        argtypes = [c_double, c_byte]
        restype = c_int

        limit: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(max_force, ID):
            MockDHD.dhdSetMaxForce.ID = ID
            MockDHD.dhdSetMaxForce.limit = max_force
            return MockDHD.dhdSetMaxForce.ret


    class dhdSetMaxTorque:
        argtypes = [c_double, c_byte]
        restype = c_int

        limit: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(max_torque, ID):
            MockDHD.dhdSetMaxTorque.ID = ID
            MockDHD.dhdSetMaxTorque.limit = max_torque
            return MockDHD.dhdSetMaxTorque.ret

    class dhdSetMaxGripperForce:
        argtypes = [c_double, c_byte]
        restype = c_int

        limit: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(max_gripper_force, ID):
            MockDHD.dhdSetMaxGripperForce.ID = ID
            MockDHD.dhdSetMaxGripperForce.limit = max_gripper_force
            return MockDHD.dhdSetMaxGripperForce.ret

    class dhdGetMaxForce:
        argtypes = [c_byte]
        restype = c_double

        ID = 0
        ret: float = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdGetMaxForce.ID = ID
            return MockDHD.dhdGetMaxForce.ret

    class dhdGetMaxTorque:
        argtypes = [c_byte]
        restype = c_double

        ID = 0
        ret: float = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdGetMaxTorque.ID = ID
            return MockDHD.dhdGetMaxTorque.ret

    class dhdGetMaxGripperForce:
        argtypes = [c_byte]
        restype = c_double

        ID = 0
        ret: float = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdGetMaxGripperForce.ID = ID
            return MockDHD.dhdGetMaxGripperForce.ret


class TestStandardSDK(unittest.TestCase):
    def assertSignaturesEqual(self, first: Any, second: Any):
        for argtype1, argtype2 in zip(first.argtypes, second.argtypes):
            self.assertIs(argtype1, argtype2)

        self.assertIs(first.restype, second.restype)

    def assertIDImpl(self, func, impl):
        func()
        self.assertEqual(-1, impl.ID)

        for ID in range(100):
            func(ID=ID)
            self.assertEqual(ID, impl.ID)

    def assertRetImpl(self, func, impl):
        for errno in ErrorNum:
            impl.ret = errno
            ret = func()
            self.assertEqual(ret, impl.ret)

    def test_errorGetLast(self):
        self.assertSignaturesEqual(
            libdhd.dhdErrorGetLast, MockDHD.dhdErrorGetLast
        )

        libdhd.dhdErrorGetLast = MockDHD.dhdErrorGetLast.mock  # type: ignore
        for error_num in ErrorNum:
            MockDHD.dhdErrorGetLast.ret = int(error_num)

            ret = dhd.errorGetLast()
            self.assertIsInstance(ret, ErrorNum)
            self.assertEqual(ret, error_num)

    def test_errorGetLastStr(self):
        self.assertSignaturesEqual(
            libdhd.dhdErrorGetLastStr, MockDHD.dhdErrorGetLastStr
        )

        libdhd.dhdErrorGetLastStr = MockDHD.dhdErrorGetLastStr.mock  # type: ignore
        for errno in ErrorNum:
            MockDHD.dhdErrorGetLastStr.errno = errno

            # supress the "memory leaks" warning
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')

                self.assertEqual(
                    dhd.errorGetLastStr(
                    ), MockDHD.dhdErrorGetStr.err_strs[errno]
                )

    def test_errorGetStr(self):
        self.assertSignaturesEqual(
            libdhd.dhdErrorGetStr, MockDHD.dhdErrorGetStr
        )

        libdhd.dhdErrorGetStr = MockDHD.dhdErrorGetStr.mock  # type: ignore
        for errno in ErrorNum:

            # supress the "memory leaks" warning
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')

                self.assertEqual(
                    dhd.errorGetStr(
                        errno), MockDHD.dhdErrorGetStr.err_strs[errno]
                )

    def test_enableSimulator(self):
        self.assertSignaturesEqual(
            libdhd.dhdEnableSimulator, MockDHD.dhdEnableSimulator
        )

        libdhd.dhdEnableSimulator = MockDHD.dhdEnableSimulator.mock  # type: ignore

        dhd.enableSimulator(True)
        self.assertTrue(MockDHD.dhdEnableSimulator.enable)

        dhd.enableSimulator(False)
        self.assertFalse(MockDHD.dhdEnableSimulator.enable)

    def test_getDeviceCount(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetDeviceCount, MockDHD.dhdGetDeviceCount
        )

        libdhd.dhdGetDeviceCount = MockDHD.dhdGetDeviceCount.mock  # type: ignore

        for count in range(100):
            MockDHD.dhdGetDeviceCount.ret = count
            self.assertEqual(dhd.getDeviceCount(), MockDHD.dhdGetDeviceCount.ret)


    def test_setDevice(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetDevice, MockDHD.dhdSetDevice
        )

        libdhd.dhdSetDevice = MockDHD.dhdSetDevice.mock  # type: ignore

        for ID in range(100):
            dhd.setDevice(ID)
            self.assertEqual(ID, MockDHD.dhdSetDevice.ID)

        self.assertRetImpl(lambda: dhd.setDevice(0), MockDHD.dhdSetDevice)

    def test_getDeviceID(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetDeviceID, MockDHD.dhdGetDeviceID
        )

        libdhd.dhdGetDeviceID = MockDHD.dhdGetDeviceID.mock  # type: ignore

        for ID in range(100):
            MockDHD.dhdGetDeviceID.ID = ID
            self.assertEqual(dhd.getDeviceID(), ID)

    def test_getSerialNumber(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetSerialNumber, MockDHD.dhdGetSerialNumber
        )

        libdhd.dhdGetSerialNumber = MockDHD.dhdGetSerialNumber.mock  # type: ignore

        for serial_number in range(100):
            MockDHD.dhdGetSerialNumber.serial_number = serial_number

            self.assertEqual(dhd.getSerialNumber(), serial_number)

        self.assertIDImpl(dhd.getSerialNumber, MockDHD.dhdGetSerialNumber)

        MockDHD.dhdGetSerialNumber.ret = 1
        self.assertEqual(dhd.getSerialNumber(), -1)

    def test_open(self):
        self.assertSignaturesEqual(libdhd.dhdOpen, MockDHD.dhdOpen)
        libdhd.dhdOpen = MockDHD.dhdOpen.mock  # type: ignore

        dhd.open()
        self.assertTrue(MockDHD.dhdOpen.is_open)

        self.assertRetImpl(dhd.open, MockDHD.dhdOpen)

    def test_openID(self):
        self.assertSignaturesEqual(libdhd.dhdOpenID, MockDHD.dhdOpenID)
        libdhd.dhdOpenID = MockDHD.dhdOpenID.mock  # type: ignore

        self.assertIDImpl(lambda ID=-1: dhd.openID(ID), MockDHD.dhdOpenID)
        self.assertTrue(MockDHD.dhdOpenID.is_open)
        self.assertRetImpl(lambda: dhd.openID(0), MockDHD.dhdOpenID)

    def test_openType(self):
        self.assertSignaturesEqual(libdhd.dhdOpenType, MockDHD.dhdOpenType)
        libdhd.dhdOpenType = MockDHD.dhdOpenType.mock  # type: ignore

        for devtype in DeviceType:
            dhd.openType(devtype)
            self.assertEqual(devtype, MockDHD.dhdOpenType.devtype)

        self.assertTrue(MockDHD.dhdOpenType.is_open)
        self.assertRetImpl(
            lambda: dhd.openType(DeviceType.NONE), MockDHD.dhdOpenType
        )

    def test_openSerial(self):
        self.assertSignaturesEqual(libdhd.dhdOpenSerial, MockDHD.dhdOpenSerial)
        libdhd.dhdOpenSerial = MockDHD.dhdOpenSerial.mock  # type: ignore

        for serial in range(100):
            dhd.openSerial(serial)
            self.assertEqual(serial, MockDHD.dhdOpenSerial.serial)

        self.assertRetImpl(lambda: dhd.openSerial(0), MockDHD.dhdOpenSerial)

    def test_close(self):
        self.assertSignaturesEqual(libdhd.dhdClose, MockDHD.dhdClose)
        libdhd.dhdClose = MockDHD.dhdClose.mock  # type: ignore
        MockDHD.dhdOpen.is_open = True
        MockDHD.dhdOpenType.is_open = True
        MockDHD.dhdOpenSerial.is_open = True
        MockDHD.dhdOpenID.is_open = True
        dhd.close()

        self.assertFalse(MockDHD.dhdOpen.is_open)
        self.assertFalse(MockDHD.dhdOpenType.is_open)
        self.assertFalse(MockDHD.dhdOpenSerial.is_open)
        self.assertFalse(MockDHD.dhdOpenID.is_open)

        self.assertIDImpl(dhd.close, MockDHD.dhdClose)
        self.assertRetImpl(lambda: dhd.close(0), MockDHD.dhdClose)

    def test_checkControllerMemory(self):
        self.assertSignaturesEqual(
            libdhd.dhdCheckControllerMemory, MockDHD.dhdCheckControllerMemory
        )

        libdhd.dhdCheckControllerMemory = (  # type: ignore
            MockDHD.dhdCheckControllerMemory.mock
        )

        self.assertIDImpl(
            dhd.checkControllerMemory, MockDHD.dhdCheckControllerMemory
        )

    def test_stop(self):
        self.assertSignaturesEqual(libdhd.dhdStop, MockDHD.dhdStop)
        libdhd.dhdStop = MockDHD.dhdStop.mock  # type: ignore

        self.assertIDImpl(dhd.stop, MockDHD.dhdStop)


    def test_getComMode(self):
        self.assertSignaturesEqual(libdhd.dhdGetComMode, MockDHD.dhdGetComMode)
        libdhd.dhdGetComMode = MockDHD.dhdGetComMode.mock  # type: ignore

        for com_mode in ComMode:
            MockDHD.dhdGetComMode.ret = com_mode
            self.assertEqual(dhd.getComMode(), com_mode)

    def test_enableForce(self):
        self.assertSignaturesEqual(
            libdhd.dhdEnableForce, MockDHD.dhdEnableForce
        )

        libdhd.dhdEnableForce = MockDHD.dhdEnableForce.mock  # type: ignore

        dhd.enableForce(True)
        self.assertTrue(MockDHD.dhdEnableForce.is_enabled)

        dhd.enableForce(False)
        self.assertFalse(MockDHD.dhdEnableForce.is_enabled)

        self.assertRetImpl(
            lambda: dhd.enableForce(True), MockDHD.dhdEnableForce
        )

    def test_getSystemType(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetSystemType, MockDHD.dhdGetSystemType
        )

        libdhd.dhdGetSystemType = MockDHD.dhdGetSystemType.mock  # type: ignore

        for devtype in DeviceType:
            MockDHD.dhdGetSystemType.ret = devtype
            self.assertEqual(dhd.getSystemType(), devtype)

        self.assertIDImpl(dhd.getSystemType, MockDHD.dhdGetSystemType)

    def test_getSystemRev(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetSystemRev, MockDHD.dhdGetSystemRev
        )

        libdhd.dhdGetSystemRev = MockDHD.dhdGetSystemRev.mock  # type: ignore

        for devtype in DeviceType:
            MockDHD.dhdGetSystemRev.ret = devtype
            self.assertEqual(dhd.getSystemRev(), devtype)

        self.assertIDImpl(dhd.getSystemRev, MockDHD.dhdGetSystemRev)

    def test_getSystemName(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetSystemName, MockDHD.dhdGetSystemName
        )

        libdhd.dhdGetSystemName = MockDHD.dhdGetSystemName.mock  # type: ignore


        with warnings.catch_warnings():
            warnings.simplefilter('ignore')

            MockDHD.dhdGetSystemName.ret = b"lorem ipsem"

            self.assertEqual(
                dhd.getSystemName(),
                MockDHD.dhdGetSystemName.ret.decode('utf-8')
            )

            MockDHD.dhdGetSystemName.ret = None

            self.assertIs(dhd.getSystemName(), None)

            self.assertIDImpl(dhd.getSystemName, MockDHD.dhdGetSystemName)


    def test_getVersion(self):
        self.assertSignaturesEqual(libdhd.dhdGetVersion, MockDHD.dhdGetVersion)

        libdhd.dhdGetVersion = MockDHD.dhdGetVersion.mock  # type: ignore

        for _ in range(100):
            MockDHD.dhdGetVersion.ver = random()
            self.assertAlmostEqual(dhd.getVersion(), MockDHD.dhdGetVersion.ver)

        self.assertIDImpl(dhd.getVersion, MockDHD.dhdGetVersion)

        for ret in range(1, len(ErrorNum)):
            MockDHD.dhdGetVersion.ret = ret
            self.assertEqual(dhd.getVersion(), -1.0)

    # TODO: remove
    def test_getVersionStr(self):
        ...

    def test_getSDKVersion(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetSDKVersion, MockDHD.dhdGetSDKVersion
        )

        libdhd.dhdGetSDKVersion = MockDHD.dhdGetSDKVersion.mock  # type: ignore
        version = dhd.getSDKVersion()

        self.assertEqual(version.major, MockDHD.dhdGetSDKVersion.major)
        self.assertEqual(version.minor, MockDHD.dhdGetSDKVersion.minor)
        self.assertEqual(version.release, MockDHD.dhdGetSDKVersion.release)
        self.assertEqual(version.revision, MockDHD.dhdGetSDKVersion.revision)

    def test_getComponentVersionStr(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetComponentVersionStr, MockDHD.dhdGetComponentVersionStr
        )

        libdhd.dhdGetComponentVersionStr = (  # type: ignore
            MockDHD.dhdGetComponentVersionStr.mock
        )

        for N in range(1, len(MockDHD.dhdGetComponentVersionStr.description)):
            component = randint(0, 100)
            ID = randint(0, 100)

            self.assertEqual(
                dhd.getComponentVersionStr(component, N, ID),
                MockDHD.dhdGetComponentVersionStr.description[:N]
            )
            self.assertEqual(
                component, MockDHD.dhdGetComponentVersionStr.component
            )
            self.assertEqual(ID, MockDHD.dhdGetComponentVersionStr.ID)

        MockDHD.dhdGetComponentVersionStr.ret = 1
        self.assertEqual(dhd.getComponentVersionStr(0), "")

        for N in range(100):
            self.assertRaises(
                ValueError, lambda: dhd.getComponentVersionStr(0, -N)
            )

    def test_getStatus(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetStatus, MockDHD.dhdGetStatus
        )

        libdhd.dhdGetStatus = MockDHD.dhdGetStatus.mock  # type: ignore

        for i in range(len(MockDHD.dhdGetStatus.status)):
            MockDHD.dhdGetStatus.status[i] = randint(0, 10)


        status = Status()
        dhd.getStatus(status)

        for i in range(len(MockDHD.dhdGetStatus.status)):
            self.assertEqual(status[i], MockDHD.dhdGetStatus.status[i])

        self.assertIDImpl(
            lambda ID=-1: dhd.getStatus(status, ID),
            MockDHD.dhdGetStatus
        )
        self.assertRetImpl(lambda: dhd.getStatus(status), MockDHD.dhdGetStatus)

    def test_getDeviceAngleRad(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetDeviceAngleRad, MockDHD.dhdGetDeviceAngleRad
        )

        libdhd.dhdGetDeviceAngleRad = MockDHD.dhdGetDeviceAngleRad.mock  # type: ignore

        for _ in range(100):
            MockDHD.dhdGetDeviceAngleRad.angle = random()

            out = c_double()
            dhd.getDeviceAngleRad(out)
            self.assertAlmostEqual(
                out.value, MockDHD.dhdGetDeviceAngleRad.angle
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.getDeviceAngleRad(out, ID),
            MockDHD.dhdGetDeviceAngleRad
        )

        self.assertRetImpl(
            lambda: dhd.getDeviceAngleRad(out), MockDHD.dhdGetDeviceAngleRad
        )


    def test_getDeviceAngleDeg(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetDeviceAngleDeg, MockDHD.dhdGetDeviceAngleDeg
        )

        libdhd.dhdGetDeviceAngleDeg = MockDHD.dhdGetDeviceAngleDeg.mock  # type: ignore

        for _ in range(100):
            MockDHD.dhdGetDeviceAngleDeg.angle = random()

            out = c_double()
            dhd.getDeviceAngleDeg(out)
            self.assertAlmostEqual(
                out.value, MockDHD.dhdGetDeviceAngleDeg.angle
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.getDeviceAngleDeg(out, ID),
            MockDHD.dhdGetDeviceAngleDeg
        )

        self.assertRetImpl(
            lambda: dhd.getDeviceAngleDeg(out), MockDHD.dhdGetDeviceAngleDeg
        )

    def test_getEffectorMass(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetEffectorMass, MockDHD.dhdGetEffectorMass
        )

        libdhd.dhdGetEffectorMass = (  # type: ignore
            MockDHD.dhdGetEffectorMass.mock
        )

        for _ in range(100):
            MockDHD.dhdGetEffectorMass.mass = random()

            self.assertAlmostEqual(
                dhd.getEffectorMass(), MockDHD.dhdGetEffectorMass.mass
            )

        for ret in range(1, 100):
            MockDHD.dhdGetEffectorMass.ret = -ret
            self.assertAlmostEqual(dhd.getEffectorMass(), -1.0)

        self.assertIDImpl(dhd.getEffectorMass, MockDHD.dhdGetEffectorMass)

    def test_getButton(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetButton, MockDHD.dhdGetButton
        )

        libdhd.dhdGetButton = (  # type: ignore
            MockDHD.dhdGetButton.mock
        )

        for index in range(100):
            MockDHD.dhdGetButton.ret = randint(0, 1)

            self.assertEqual(
                dhd.getButton(index), MockDHD.dhdGetButton.ret
            )

            self.assertEqual(index, MockDHD.dhdGetButton.index)

        MockDHD.dhdGetButton.ret = -1
        self.assertEqual(dhd.getButton(0), -1)

        self.assertIDImpl(
            lambda ID = -1: dhd.getButton(0, ID), MockDHD.dhdGetButton
        )

    def test_getButtonMask(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetButtonMask, MockDHD.dhdGetButtonMask
        )

        libdhd.dhdGetButtonMask = (  # type: ignore
            MockDHD.dhdGetButtonMask.mock
        )

        for i in range(32):
            MockDHD.dhdGetButtonMask.ret = 0x1 < i

            self.assertEqual(
                dhd.getButtonMask(), MockDHD.dhdGetButtonMask.ret
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.getButtonMask(ID), MockDHD.dhdGetButtonMask
        )

    def test_setOutput(self):
        self.assertSignaturesEqual(libdhd.dhdSetOutput, MockDHD.dhdSetOutput)
        libdhd.dhdSetOutput = MockDHD.dhdSetOutput.mock  # type: ignore

        for _ in range(100):
            mask = randint(0, 0x1 << 32 - 1)

            dhd.setOutput(mask)
            self.assertEqual(mask, MockDHD.dhdSetOutput.mask)

        self.assertIDImpl(
            lambda ID = -1: dhd.setOutput(0, ID), MockDHD.dhdSetOutput
        )

    def test_isLeftHanded(self):
        self.assertSignaturesEqual(
            libdhd.dhdIsLeftHanded, MockDHD.dhdIsLeftHanded
        )

        libdhd.dhdIsLeftHanded = MockDHD.dhdIsLeftHanded.mock  # type: ignore

        MockDHD.dhdIsLeftHanded.ret = False
        self.assertFalse(dhd.isLeftHanded())

        MockDHD.dhdIsLeftHanded.ret = True
        self.assertTrue(dhd.isLeftHanded())

        self.assertIDImpl(dhd.isLeftHanded, MockDHD.dhdIsLeftHanded)


    def test_hasBase(self):
        self.assertSignaturesEqual(
            libdhd.dhdHasBase, MockDHD.dhdHasBase
        )

        libdhd.dhdHasBase = MockDHD.dhdHasBase.mock  # type: ignore

        MockDHD.dhdHasBase.ret = False
        self.assertFalse(dhd.hasBase())

        MockDHD.dhdHasBase.ret = True
        self.assertTrue(dhd.hasBase())

        self.assertIDImpl(dhd.hasBase, MockDHD.dhdHasBase)

    def test_hasWrist(self):
        self.assertSignaturesEqual(
            libdhd.dhdHasWrist, MockDHD.dhdHasWrist
        )

        libdhd.dhdHasWrist = MockDHD.dhdHasWrist.mock  # type: ignore

        MockDHD.dhdHasWrist.ret = False
        self.assertFalse(dhd.hasWrist())

        MockDHD.dhdHasWrist.ret = True
        self.assertTrue(dhd.hasWrist())

        self.assertIDImpl(dhd.hasWrist, MockDHD.dhdHasWrist)

    def test_hasActiveWrist(self):
        self.assertSignaturesEqual(
            libdhd.dhdHasActiveWrist, MockDHD.dhdHasActiveWrist
        )

        libdhd.dhdHasActiveWrist = MockDHD.dhdHasActiveWrist.mock  # type: ignore

        MockDHD.dhdHasActiveWrist.ret = False
        self.assertFalse(dhd.hasActiveWrist())

        MockDHD.dhdHasActiveWrist.ret = True
        self.assertTrue(dhd.hasActiveWrist())

        self.assertIDImpl(dhd.hasActiveWrist, MockDHD.dhdHasActiveWrist)

    def test_hasGripper(self):
        self.assertSignaturesEqual(
            libdhd.dhdHasGripper, MockDHD.dhdHasGripper
        )

        libdhd.dhdHasGripper = MockDHD.dhdHasGripper.mock  # type: ignore

        MockDHD.dhdHasGripper.ret = False
        self.assertFalse(dhd.hasGripper())

        MockDHD.dhdHasGripper.ret = True
        self.assertTrue(dhd.hasGripper())

        self.assertIDImpl(dhd.hasGripper, MockDHD.dhdHasGripper)

    def test_hasActiveGripper(self):
        self.assertSignaturesEqual(
            libdhd.dhdHasActiveGripper, MockDHD.dhdHasActiveGripper
        )

        libdhd.dhdHasActiveGripper = MockDHD.dhdHasActiveGripper.mock  # type: ignore

        MockDHD.dhdHasActiveGripper.ret = False
        self.assertFalse(dhd.hasActiveGripper())

        MockDHD.dhdHasActiveGripper.ret = True
        self.assertTrue(dhd.hasActiveGripper())

        self.assertIDImpl(dhd.hasActiveGripper, MockDHD.dhdHasActiveGripper)

    def test_reset(self):
        self.assertSignaturesEqual(libdhd.dhdReset, MockDHD.dhdReset)

        libdhd.dhdReset = MockDHD.dhdReset.mock  # type: ignore

        self.assertIDImpl(dhd.reset, MockDHD.dhdReset)
        self.assertRetImpl(dhd.reset, MockDHD.dhdReset)

    def test_waitForReset(self):
        self.assertSignaturesEqual(
            libdhd.dhdWaitForReset, MockDHD.dhdWaitForReset
        )

        libdhd.dhdWaitForReset = MockDHD.dhdWaitForReset.mock  # type: ignore

        for timeout in range(1, 100):
            dhd.waitForReset(timeout)
            self.assertEqual(timeout, MockDHD.dhdWaitForReset.timeout)

        for timeout in range(100):
            self.assertRaises(
                ValueError, lambda: dhd.waitForReset(-timeout)
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.waitForReset(ID=ID),
            MockDHD.dhdWaitForReset
        )
        self.assertRetImpl(dhd.waitForReset, MockDHD.dhdWaitForReset)

    def test_setStandardGravity(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetStandardGravity, MockDHD.dhdSetStandardGravity
        )

        libdhd.dhdSetStandardGravity = (  # type: ignore
            MockDHD.dhdSetStandardGravity.mock
        )

        for _ in range(100):
            dhd.setStandardGravity(g := random())
            self.assertAlmostEqual(g, MockDHD.dhdSetStandardGravity.gravity)

        self.assertIDImpl(
            lambda ID = -1: dhd.setStandardGravity(0, ID),
            MockDHD.dhdSetStandardGravity
        )

        self.assertRetImpl(
            lambda: dhd.setStandardGravity(0),
            MockDHD.dhdSetStandardGravity
        )

    def test_setGravityCompensation(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetGravityCompensation, MockDHD.dhdSetGravityCompensation
        )

        libdhd.dhdSetGravityCompensation = (  # type: ignore
            MockDHD.dhdSetGravityCompensation.mock
        )

        dhd.setGravityCompensation(True)
        self.assertTrue(MockDHD.dhdSetGravityCompensation.enabled)

        dhd.setGravityCompensation(False)
        self.assertFalse(MockDHD.dhdSetGravityCompensation.enabled)

        self.assertIDImpl(
            lambda ID = -1: dhd.setGravityCompensation(True, ID),
            MockDHD.dhdSetGravityCompensation
        )
        self.assertRetImpl(
            lambda: dhd.setGravityCompensation(True),
            MockDHD.dhdSetGravityCompensation
        )

    def test_setBrakes(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetBrakes, MockDHD.dhdSetBrakes
        )

        libdhd.dhdSetBrakes = (  # type: ignore
            MockDHD.dhdSetBrakes.mock
        )

        dhd.setBrakes(True)
        self.assertTrue(MockDHD.dhdSetBrakes.enabled)

        dhd.setBrakes(False)
        self.assertFalse(MockDHD.dhdSetBrakes.enabled)

        self.assertIDImpl(
            lambda ID = -1: dhd.setBrakes(True, ID),
            MockDHD.dhdSetBrakes
        )
        self.assertRetImpl(
            lambda: dhd.setBrakes(True),
            MockDHD.dhdSetBrakes
        )

    def test_setDeviceAngleRad(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetDeviceAngleRad, MockDHD.dhdSetDeviceAngleRad
        )

        libdhd.dhdSetDeviceAngleRad = (  # type: ignore
            MockDHD.dhdSetDeviceAngleRad.mock
        )

        for _ in range(100):
            dhd.setDeviceAngleRad(angle := random())
            self.assertAlmostEqual(angle, MockDHD.dhdSetDeviceAngleRad.angle)

        self.assertIDImpl(
            lambda ID = -1: dhd.setDeviceAngleRad(0, ID),
            MockDHD.dhdSetDeviceAngleRad
        )

        self.assertRetImpl(
            lambda: dhd.setDeviceAngleRad(0),
            MockDHD.dhdSetDeviceAngleRad
        )

    def test_setDeviceAngleDeg(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetDeviceAngleDeg, MockDHD.dhdSetDeviceAngleDeg
        )

        libdhd.dhdSetDeviceAngleDeg = (  # type: ignore
            MockDHD.dhdSetDeviceAngleDeg.mock
        )

        for _ in range(100):
            dhd.setDeviceAngleDeg(angle := random())
            self.assertAlmostEqual(angle, MockDHD.dhdSetDeviceAngleDeg.angle)

        self.assertIDImpl(
            lambda ID = -1: dhd.setDeviceAngleDeg(0, ID),
            MockDHD.dhdSetDeviceAngleDeg
        )

        self.assertRetImpl(
            lambda: dhd.setDeviceAngleDeg(0),
            MockDHD.dhdSetDeviceAngleDeg
        )

    def test_setEffectorMass(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetEffectorMass, MockDHD.dhdSetEffectorMass
        )

        libdhd.dhdSetEffectorMass = (  # type: ignore
            MockDHD.dhdSetEffectorMass.mock
        )

        for _ in range(100):
            dhd.setEffectorMass(mass := random())
            self.assertAlmostEqual(mass, MockDHD.dhdSetEffectorMass.mass)

        self.assertIDImpl(
            lambda ID = -1: dhd.setEffectorMass(0, ID),
            MockDHD.dhdSetEffectorMass
        )

        self.assertRetImpl(
            lambda: dhd.setEffectorMass(0),
            MockDHD.dhdSetEffectorMass
        )

    def test_getPosition(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetPosition, MockDHD.dhdGetPosition
        )

        libdhd.dhdGetPosition = MockDHD.dhdGetPosition.mock  # type: ignore
        out = [0.0, 0.0, 0.0]

        for _ in range(100):
            MockDHD.dhdGetPosition.px = random()
            MockDHD.dhdGetPosition.py = random()
            MockDHD.dhdGetPosition.pz = random()

            dhd.getPosition(out)

            self.assertAlmostEqual(out[0], MockDHD.dhdGetPosition.px)
            self.assertAlmostEqual(out[1], MockDHD.dhdGetPosition.py)
            self.assertAlmostEqual(out[2], MockDHD.dhdGetPosition.pz)

        self.assertIDImpl(
            lambda ID = -1: dhd.getPosition(out, ID), MockDHD.dhdGetPosition
        )
        self.assertRetImpl(
            lambda: dhd.getPosition(out), MockDHD.dhdGetPosition
        )

    def test_getForce(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetForce, MockDHD.dhdGetForce
        )

        libdhd.dhdGetForce = MockDHD.dhdGetForce.mock  # type: ignore
        out = [0.0, 0.0, 0.0]

        for _ in range(100):
            MockDHD.dhdGetForce.fx = random()
            MockDHD.dhdGetForce.fy = random()
            MockDHD.dhdGetForce.fz = random()

            dhd.getForce(out)

            self.assertAlmostEqual(out[0], MockDHD.dhdGetForce.fx)
            self.assertAlmostEqual(out[1], MockDHD.dhdGetForce.fy)
            self.assertAlmostEqual(out[2], MockDHD.dhdGetForce.fz)

        self.assertIDImpl(
            lambda ID = -1: dhd.getForce(out, ID), MockDHD.dhdGetForce
        )
        self.assertRetImpl(
            lambda: dhd.getForce(out), MockDHD.dhdGetForce
        )


    def test_setForce(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetForce, MockDHD.dhdSetForce
        )

        libdhd.dhdSetForce = MockDHD.dhdSetForce.mock  # type: ignore
        out = [0.0, 0.0, 0.0]

        for _ in range(100):
            out[0] = random()
            out[1] = random()
            out[2] = random()

            dhd.setForce(out)

            self.assertAlmostEqual(out[0], MockDHD.dhdSetForce.fx)
            self.assertAlmostEqual(out[1], MockDHD.dhdSetForce.fy)
            self.assertAlmostEqual(out[2], MockDHD.dhdSetForce.fz)

        self.assertIDImpl(
            lambda ID = -1: dhd.setForce(out, ID), MockDHD.dhdSetForce
        )
        self.assertRetImpl(
            lambda: dhd.setForce(out), MockDHD.dhdSetForce
        )

    def test_getOrientationRad(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetOrientationRad, MockDHD.dhdGetOrientationRad
        )

        libdhd.dhdGetOrientationRad = (  # type: ignore
            MockDHD.dhdGetOrientationRad.mock
        )
        out = [0.0, 0.0, 0.0]

        for _ in range(100):
            MockDHD.dhdGetOrientationRad.oa = random()
            MockDHD.dhdGetOrientationRad.ob = random()
            MockDHD.dhdGetOrientationRad.og = random()

            dhd.getOrientationRad(out)

            self.assertAlmostEqual(out[0], MockDHD.dhdGetOrientationRad.oa)
            self.assertAlmostEqual(out[1], MockDHD.dhdGetOrientationRad.ob)
            self.assertAlmostEqual(out[2], MockDHD.dhdGetOrientationRad.og)

        self.assertIDImpl(
            lambda ID = -1: dhd.getOrientationRad(out, ID),
            MockDHD.dhdGetOrientationRad
        )
        self.assertRetImpl(
            lambda: dhd.getOrientationRad(out), MockDHD.dhdGetOrientationRad
        )


    def test_getOrientationDeg(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetOrientationDeg, MockDHD.dhdGetOrientationDeg
        )

        libdhd.dhdGetOrientationDeg = (  # type: ignore
            MockDHD.dhdGetOrientationDeg.mock
        )
        out = [0.0, 0.0, 0.0]

        for _ in range(100):
            MockDHD.dhdGetOrientationDeg.oa = random()
            MockDHD.dhdGetOrientationDeg.ob = random()
            MockDHD.dhdGetOrientationDeg.og = random()

            dhd.getOrientationDeg(out)

            self.assertAlmostEqual(out[0], MockDHD.dhdGetOrientationDeg.oa)
            self.assertAlmostEqual(out[1], MockDHD.dhdGetOrientationDeg.ob)
            self.assertAlmostEqual(out[2], MockDHD.dhdGetOrientationDeg.og)

        self.assertIDImpl(
            lambda ID = -1: dhd.getOrientationDeg(out, ID),
            MockDHD.dhdGetOrientationDeg
        )
        self.assertRetImpl(
            lambda: dhd.getOrientationDeg(out), MockDHD.dhdGetOrientationDeg
        )

    def test_getPositionAndOrientationRad(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetPositionAndOrientationRad,
            MockDHD.dhdGetPositionAndOrientationRad
        )

        libdhd.dhdGetPositionAndOrientationRad = (  # type: ignore
            MockDHD.dhdGetPositionAndOrientationRad.mock
        )

        p_out = [0.0, 0.0, 0.0]
        o_out = [0.0, 0.0, 0.0]

        for _ in range(100):
            MockDHD.dhdGetPositionAndOrientationRad.oa = random()
            MockDHD.dhdGetPositionAndOrientationRad.ob = random()
            MockDHD.dhdGetPositionAndOrientationRad.og = random()

            MockDHD.dhdGetPositionAndOrientationRad.px = random()
            MockDHD.dhdGetPositionAndOrientationRad.py = random()
            MockDHD.dhdGetPositionAndOrientationRad.pz = random()

            dhd.getPositionAndOrientationRad(p_out, o_out)

            self.assertAlmostEqual(
                p_out[0], MockDHD.dhdGetPositionAndOrientationRad.px
            )
            self.assertAlmostEqual(
                p_out[1], MockDHD.dhdGetPositionAndOrientationRad.py
            )
            self.assertAlmostEqual(
                p_out[2], MockDHD.dhdGetPositionAndOrientationRad.pz
            )

            self.assertAlmostEqual(
                o_out[0], MockDHD.dhdGetPositionAndOrientationRad.oa
            )
            self.assertAlmostEqual(
                o_out[1], MockDHD.dhdGetPositionAndOrientationRad.ob
            )
            self.assertAlmostEqual(
                o_out[2], MockDHD.dhdGetPositionAndOrientationRad.og
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.getPositionAndOrientationRad(p_out, o_out, ID),
            MockDHD.dhdGetPositionAndOrientationRad
        )
        self.assertRetImpl(
            lambda: dhd.getPositionAndOrientationRad(p_out, o_out),
            MockDHD.dhdGetPositionAndOrientationRad
        )

    def test_getPositionAndOrientationDeg(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetPositionAndOrientationDeg,
            MockDHD.dhdGetPositionAndOrientationDeg
        )

        libdhd.dhdGetPositionAndOrientationDeg = (  # type: ignore
            MockDHD.dhdGetPositionAndOrientationDeg.mock
        )

        p_out = [0.0, 0.0, 0.0]
        o_out = [0.0, 0.0, 0.0]

        for _ in range(100):
            MockDHD.dhdGetPositionAndOrientationDeg.oa = random()
            MockDHD.dhdGetPositionAndOrientationDeg.ob = random()
            MockDHD.dhdGetPositionAndOrientationDeg.og = random()

            MockDHD.dhdGetPositionAndOrientationDeg.px = random()
            MockDHD.dhdGetPositionAndOrientationDeg.py = random()
            MockDHD.dhdGetPositionAndOrientationDeg.pz = random()

            dhd.getPositionAndOrientationDeg(p_out, o_out)

            self.assertAlmostEqual(
                p_out[0], MockDHD.dhdGetPositionAndOrientationDeg.px
            )
            self.assertAlmostEqual(
                p_out[1], MockDHD.dhdGetPositionAndOrientationDeg.py
            )
            self.assertAlmostEqual(
                p_out[2], MockDHD.dhdGetPositionAndOrientationDeg.pz
            )

            self.assertAlmostEqual(
                o_out[0], MockDHD.dhdGetPositionAndOrientationDeg.oa
            )
            self.assertAlmostEqual(
                o_out[1], MockDHD.dhdGetPositionAndOrientationDeg.ob
            )
            self.assertAlmostEqual(
                o_out[2], MockDHD.dhdGetPositionAndOrientationDeg.og
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.getPositionAndOrientationDeg(p_out, o_out, ID),
            MockDHD.dhdGetPositionAndOrientationDeg
        )
        self.assertRetImpl(
            lambda: dhd.getPositionAndOrientationDeg(p_out, o_out),
            MockDHD.dhdGetPositionAndOrientationDeg
        )


    def test_getPositionAndOrientationFrame(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetPositionAndOrientationFrame,
            MockDHD.dhdGetPositionAndOrientationFrame
        )

        libdhd.dhdGetPositionAndOrientationFrame = (  # type: ignore
            MockDHD.dhdGetPositionAndOrientationFrame.mock
        )

        p_out = [0.0, 0.0, 0.0]
        frame = [[0.0] * 3 for _ in range(3)]

        for _ in range(100):
            MockDHD.dhdGetPositionAndOrientationFrame.px = random()
            MockDHD.dhdGetPositionAndOrientationFrame.py = random()
            MockDHD.dhdGetPositionAndOrientationFrame.pz = random()

            for i in range(3):
                for j in range(3):
                    MockDHD.dhdGetPositionAndOrientationFrame.frame[i][j] = (
                        random()
                    )

            dhd.getPositionAndOrientationFrame(p_out, frame)

            self.assertAlmostEqual(
                p_out[0], MockDHD.dhdGetPositionAndOrientationFrame.px
            )
            self.assertAlmostEqual(
                p_out[1], MockDHD.dhdGetPositionAndOrientationFrame.py
            )
            self.assertAlmostEqual(
                p_out[2], MockDHD.dhdGetPositionAndOrientationFrame.pz
            )

            self.assertListEqual(
                frame,
                MockDHD.dhdGetPositionAndOrientationFrame.frame
            )


        self.assertIDImpl(
            lambda ID = -1: dhd.getPositionAndOrientationFrame(
                p_out, frame, ID
            ),
            MockDHD.dhdGetPositionAndOrientationFrame
        )
        self.assertRetImpl(
            lambda: dhd.getPositionAndOrientationFrame(p_out, frame),
            MockDHD.dhdGetPositionAndOrientationFrame
        )

    def test_getForceAndTorque(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetForceAndTorque, MockDHD.dhdGetForceAndTorque
        )

        libdhd.dhdGetForceAndTorque = MockDHD.dhdGetForceAndTorque.mock  # type: ignore

        f_out = [0.0, 0.0, 0.0]
        t_out = [0.0, 0.0, 0.0]

        for _ in range(100):
            MockDHD.dhdGetForceAndTorque.fx = random()
            MockDHD.dhdGetForceAndTorque.fy = random()
            MockDHD.dhdGetForceAndTorque.fz = random()

            MockDHD.dhdGetForceAndTorque.tx = random()
            MockDHD.dhdGetForceAndTorque.ty = random()
            MockDHD.dhdGetForceAndTorque.tz = random()


            dhd.getForceAndTorque(f_out, t_out)

            self.assertAlmostEqual(f_out[0], MockDHD.dhdGetForceAndTorque.fx)
            self.assertAlmostEqual(f_out[1], MockDHD.dhdGetForceAndTorque.fy)
            self.assertAlmostEqual(f_out[2], MockDHD.dhdGetForceAndTorque.fz)

            self.assertAlmostEqual(t_out[0], MockDHD.dhdGetForceAndTorque.tx)
            self.assertAlmostEqual(t_out[1], MockDHD.dhdGetForceAndTorque.ty)
            self.assertAlmostEqual(t_out[2], MockDHD.dhdGetForceAndTorque.tz)

        self.assertIDImpl(
            lambda ID = -1: dhd.getForceAndTorque(f_out, t_out, ID),
            MockDHD.dhdGetForceAndTorque
        )
        self.assertRetImpl(
            lambda: dhd.getForceAndTorque(f_out, t_out),
            MockDHD.dhdGetForceAndTorque
        )


    def test_setForceAndTorque(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetForceAndTorque, MockDHD.dhdSetForceAndTorque
        )

        libdhd.dhdSetForceAndTorque = MockDHD.dhdSetForceAndTorque.mock  # type: ignore

        f = [0.0, 0.0, 0.0]
        t = [0.0, 0.0, 0.0]

        for _ in range(100):
            f[0] = random()
            f[1] = random()
            f[2] = random()

            t[0] = random()
            t[1] = random()
            t[2] = random()

            dhd.setForceAndTorque(f, t)

            self.assertAlmostEqual(f[0], MockDHD.dhdSetForceAndTorque.fx)
            self.assertAlmostEqual(f[1], MockDHD.dhdSetForceAndTorque.fy)
            self.assertAlmostEqual(f[2], MockDHD.dhdSetForceAndTorque.fz)

            self.assertAlmostEqual(t[0], MockDHD.dhdSetForceAndTorque.tx)
            self.assertAlmostEqual(t[1], MockDHD.dhdSetForceAndTorque.ty)
            self.assertAlmostEqual(t[2], MockDHD.dhdSetForceAndTorque.tz)

        self.assertIDImpl(
            lambda ID = -1: dhd.setForceAndTorque(f, t, ID),
            MockDHD.dhdSetForceAndTorque
        )
        self.assertRetImpl(
            lambda: dhd.setForceAndTorque(f, t), MockDHD.dhdSetForceAndTorque
        )


    def test_getOrientationFrame(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetOrientationFrame,
            MockDHD.dhdGetOrientationFrame
        )

        libdhd.dhdGetOrientationFrame = (  # type: ignore
            MockDHD.dhdGetOrientationFrame.mock
        )

        frame = [[0.0] * 3] * 3

        for _ in range(100):
            for i in range(3):
                for j in range(3):
                    MockDHD.dhdGetOrientationFrame.frame[i][j] = (
                        random()
                    )

            dhd.getOrientationFrame(frame)
            self.assertListEqual(
                frame,
                MockDHD.dhdGetOrientationFrame.frame
            )


        self.assertIDImpl(
            lambda ID = -1: dhd.getOrientationFrame(frame, ID),
            MockDHD.dhdGetOrientationFrame
        )
        self.assertRetImpl(
            lambda: dhd.getOrientationFrame(frame),
            MockDHD.dhdGetOrientationFrame
        )

    def test_getGripperAngleRad(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetGripperAngleRad, MockDHD.dhdGetGripperAngleRad
        )

        libdhd.dhdGetGripperAngleRad = (  # type: ignore
            MockDHD.dhdGetGripperAngleRad.mock
        )

        out = c_double()
        for _ in range(100):
            MockDHD.dhdGetGripperAngleRad.angle = random()
            dhd.getGripperAngleRad(out)

            self.assertAlmostEqual(
                out.value, MockDHD.dhdGetGripperAngleRad.angle
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.getGripperAngleRad(out, ID),
            MockDHD.dhdGetGripperAngleRad
        )

        self.assertRetImpl(
            lambda: dhd.getGripperAngleRad(out),
            MockDHD.dhdGetGripperAngleRad
        )

    def test_getGripperAngleDeg(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetGripperAngleDeg, MockDHD.dhdGetGripperAngleDeg
        )

        libdhd.dhdGetGripperAngleDeg = (  # type: ignore
            MockDHD.dhdGetGripperAngleDeg.mock
        )

        out = c_double()
        for _ in range(100):
            MockDHD.dhdGetGripperAngleDeg.angle = random()
            dhd.getGripperAngleDeg(out)

            self.assertAlmostEqual(
                out.value, MockDHD.dhdGetGripperAngleDeg.angle
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.getGripperAngleDeg(out, ID),
            MockDHD.dhdGetGripperAngleDeg
        )

        self.assertRetImpl(
            lambda: dhd.getGripperAngleDeg(out),
            MockDHD.dhdGetGripperAngleDeg
        )

    def test_getGripperGap(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetGripperGap, MockDHD.dhdGetGripperGap
        )

        libdhd.dhdGetGripperGap = (  # type: ignore
            MockDHD.dhdGetGripperGap.mock
        )

        out = c_double()
        for _ in range(100):
            MockDHD.dhdGetGripperGap.gap = random()
            dhd.getGripperGap(out)

            self.assertAlmostEqual(
                out.value, MockDHD.dhdGetGripperGap.gap
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.getGripperGap(out, ID),
            MockDHD.dhdGetGripperGap
        )

        self.assertRetImpl(
            lambda: dhd.getGripperGap(out),
            MockDHD.dhdGetGripperGap
        )

    def test_getGripperThumbPos(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetGripperThumbPos, MockDHD.dhdGetGripperThumbPos
        )

        libdhd.dhdGetGripperThumbPos = MockDHD.dhdGetGripperThumbPos.mock  # type: ignore
        out = [0.0, 0.0, 0.0]

        for _ in range(100):
            MockDHD.dhdGetGripperThumbPos.px = random()
            MockDHD.dhdGetGripperThumbPos.py = random()
            MockDHD.dhdGetGripperThumbPos.pz = random()

            dhd.getGripperThumbPos(out)

            self.assertAlmostEqual(out[0], MockDHD.dhdGetGripperThumbPos.px)
            self.assertAlmostEqual(out[1], MockDHD.dhdGetGripperThumbPos.py)
            self.assertAlmostEqual(out[2], MockDHD.dhdGetGripperThumbPos.pz)

        self.assertIDImpl(
            lambda ID = -1: dhd.getGripperThumbPos(out, ID),
            MockDHD.dhdGetGripperThumbPos
        )
        self.assertRetImpl(
            lambda: dhd.getGripperThumbPos(out), MockDHD.dhdGetGripperThumbPos
        )


    def test_getGripperFingerPos(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetGripperFingerPos, MockDHD.dhdGetGripperFingerPos
        )

        libdhd.dhdGetGripperFingerPos = (  # type: ignore
            MockDHD.dhdGetGripperFingerPos.mock
        )
        out = [0.0, 0.0, 0.0]

        for _ in range(100):
            MockDHD.dhdGetGripperFingerPos.px = random()
            MockDHD.dhdGetGripperFingerPos.py = random()
            MockDHD.dhdGetGripperFingerPos.pz = random()

            dhd.getGripperFingerPos(out)

            self.assertAlmostEqual(out[0], MockDHD.dhdGetGripperFingerPos.px)
            self.assertAlmostEqual(out[1], MockDHD.dhdGetGripperFingerPos.py)
            self.assertAlmostEqual(out[2], MockDHD.dhdGetGripperFingerPos.pz)

        self.assertIDImpl(
            lambda ID = -1: dhd.getGripperFingerPos(out, ID),
            MockDHD.dhdGetGripperFingerPos
        )
        self.assertRetImpl(
            lambda: dhd.getGripperFingerPos(out),
            MockDHD.dhdGetGripperFingerPos
        )

    def test_getComFreq(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetComFreq, MockDHD.dhdGetComFreq
        )

        libdhd.dhdGetComFreq = MockDHD.dhdGetComFreq.mock  # type: ignore

        for _ in range(100):
            MockDHD.dhdGetComFreq.ret = random()
            self.assertAlmostEqual(dhd.getComFreq(), MockDHD.dhdGetComFreq.ret)

        self.assertIDImpl(dhd.getComFreq, MockDHD.dhdGetComFreq)


    def test_setForceAndGripperForce(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetForceAndGripperForce,
            MockDHD.dhdSetForceAndGripperForce
        )

        libdhd.dhdSetForceAndGripperForce = ( # type: ignore
            MockDHD.dhdSetForceAndGripperForce.mock
        )

        f = [0.0, 0.0, 0.0]
        fg = 0.0

        for _ in range(100):
            f[0] = random()
            f[1] = random()
            f[2] = random()
            fg = random()

            dhd.setForceAndGripperForce(f, fg)

            self.assertAlmostEqual(f[0], MockDHD.dhdSetForceAndGripperForce.fx)
            self.assertAlmostEqual(f[1], MockDHD.dhdSetForceAndGripperForce.fy)
            self.assertAlmostEqual(f[2], MockDHD.dhdSetForceAndGripperForce.fz)

            self.assertAlmostEqual(fg, MockDHD.dhdSetForceAndGripperForce.fg)

        self.assertIDImpl(
            lambda ID = -1: dhd.setForceAndGripperForce(f, fg, ID),
            MockDHD.dhdSetForceAndGripperForce
        )
        self.assertRetImpl(
            lambda: dhd.setForceAndGripperForce(f, fg),
            MockDHD.dhdSetForceAndGripperForce
        )


    def test_setForceAndTorqueAndGripperForce(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetForceAndTorqueAndGripperForce,
            MockDHD.dhdSetForceAndTorqueAndGripperForce
        )

        libdhd.dhdSetForceAndTorqueAndGripperForce = (  # type: ignore
            MockDHD.dhdSetForceAndTorqueAndGripperForce.mock
        )

        f = [0.0, 0.0, 0.0]
        t = [0.0, 0.0, 0.0]
        fg = 0.0

        for _ in range(100):
            f[0] = random()
            f[1] = random()
            f[2] = random()

            t[0] = random()
            t[1] = random()
            t[2] = random()

            fg = random()

            dhd.setForceAndTorqueAndGripperForce(f, t, fg)

            self.assertAlmostEqual(
                f[0], MockDHD.dhdSetForceAndTorqueAndGripperForce.fx
            )
            self.assertAlmostEqual(
                f[1], MockDHD.dhdSetForceAndTorqueAndGripperForce.fy
            )
            self.assertAlmostEqual(
                f[2], MockDHD.dhdSetForceAndTorqueAndGripperForce.fz
            )

            self.assertAlmostEqual(
                t[0], MockDHD.dhdSetForceAndTorqueAndGripperForce.tx
            )
            self.assertAlmostEqual(
                t[1], MockDHD.dhdSetForceAndTorqueAndGripperForce.ty
            )
            self.assertAlmostEqual(
                t[2], MockDHD.dhdSetForceAndTorqueAndGripperForce.tz
            )

            self.assertAlmostEqual(
                fg, MockDHD.dhdSetForceAndTorqueAndGripperForce.fg
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.setForceAndTorqueAndGripperForce(f, t, fg, ID),
            MockDHD.dhdSetForceAndTorqueAndGripperForce
        )
        self.assertRetImpl(
            lambda: dhd.setForceAndTorqueAndGripperForce(f, t, fg),
            MockDHD.dhdSetForceAndTorqueAndGripperForce
        )


    def test_getForceAndTorqueAndGripperForce(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetForceAndTorqueAndGripperForce,
            MockDHD.dhdGetForceAndTorqueAndGripperForce
        )

        libdhd.dhdGetForceAndTorqueAndGripperForce = (  # type: ignore
            MockDHD.dhdGetForceAndTorqueAndGripperForce.mock
        )

        f_out = [0.0, 0.0, 0.0]
        t_out = [0.0, 0.0, 0.0]
        fg_out = c_double()

        for _ in range(100):
            MockDHD.dhdGetForceAndTorqueAndGripperForce.fx = random()
            MockDHD.dhdGetForceAndTorqueAndGripperForce.fy = random()
            MockDHD.dhdGetForceAndTorqueAndGripperForce.fz = random()

            MockDHD.dhdGetForceAndTorqueAndGripperForce.tx = random()
            MockDHD.dhdGetForceAndTorqueAndGripperForce.ty = random()
            MockDHD.dhdGetForceAndTorqueAndGripperForce.tz = random()


            dhd.getForceAndTorqueAndGripperForce(f_out, t_out, fg_out)

            self.assertAlmostEqual(
                f_out[0], MockDHD.dhdGetForceAndTorqueAndGripperForce.fx
            )
            self.assertAlmostEqual(
                f_out[1], MockDHD.dhdGetForceAndTorqueAndGripperForce.fy
            )
            self.assertAlmostEqual(
                f_out[2], MockDHD.dhdGetForceAndTorqueAndGripperForce.fz
            )

            self.assertAlmostEqual(
                t_out[0], MockDHD.dhdGetForceAndTorqueAndGripperForce.tx
            )
            self.assertAlmostEqual(
                t_out[1], MockDHD.dhdGetForceAndTorqueAndGripperForce.ty
            )
            self.assertAlmostEqual(
                t_out[2], MockDHD.dhdGetForceAndTorqueAndGripperForce.tz
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.getForceAndTorqueAndGripperForce(
                f_out, t_out, fg_out, ID
            ),
            MockDHD.dhdGetForceAndTorqueAndGripperForce
        )
        self.assertRetImpl(
            lambda: dhd.getForceAndTorqueAndGripperForce(f_out, t_out, fg_out),
            MockDHD.dhdGetForceAndTorqueAndGripperForce
        )


    def test_configLinearVelocity(self):
        self.assertSignaturesEqual(
            libdhd.dhdConfigLinearVelocity,
            MockDHD.dhdConfigLinearVelocity
        )

        libdhd.dhdConfigLinearVelocity = (  # type: ignore
            MockDHD.dhdConfigLinearVelocity.mock
        )

        for mode in VelocityEstimatorMode:
            dhd.configLinearVelocity(mode=mode)
            self.assertEqual(
                mode, MockDHD.dhdConfigLinearVelocity.mode
            )

        for _ in range(100):
            ms = randint(0, 100)
            dhd.configLinearVelocity(ms)
            self.assertEqual(ms, MockDHD.dhdConfigLinearVelocity.ms)

        self.assertIDImpl(
            lambda ID = -1: dhd.configLinearVelocity(ID=ID),
            MockDHD.dhdConfigLinearVelocity
        )

        self.assertRetImpl(
            dhd.configLinearVelocity,
            MockDHD.dhdConfigLinearVelocity
        )

    def test_getLinearVelocity(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetLinearVelocity,
            MockDHD.dhdGetLinearVelocity
        )

        libdhd.dhdGetLinearVelocity = (  # type: ignore
            MockDHD.dhdGetLinearVelocity.mock
        )
        out = [0.0, 0.0, 0.0]

        for _ in range(100):
            MockDHD.dhdGetLinearVelocity.vx = random()
            MockDHD.dhdGetLinearVelocity.vy = random()
            MockDHD.dhdGetLinearVelocity.vz = random()

            dhd.getLinearVelocity(out)

            self.assertAlmostEqual(out[0], MockDHD.dhdGetLinearVelocity.vx)
            self.assertAlmostEqual(out[1], MockDHD.dhdGetLinearVelocity.vy)
            self.assertAlmostEqual(out[2], MockDHD.dhdGetLinearVelocity.vz)

        self.assertIDImpl(
            lambda ID = -1: dhd.getLinearVelocity(out, ID),
            MockDHD.dhdGetLinearVelocity
        )
        self.assertRetImpl(
            lambda: dhd.getLinearVelocity(out),
            MockDHD.dhdGetLinearVelocity
        )

    def test_configAngularVelocity(self):
        self.assertSignaturesEqual(
            libdhd.dhdConfigAngularVelocity,
            MockDHD.dhdConfigAngularVelocity
        )

        libdhd.dhdConfigAngularVelocity = (  # type: ignore
            MockDHD.dhdConfigAngularVelocity.mock
        )

        for mode in VelocityEstimatorMode:
            dhd.configAngularVelocity(mode=mode)
            self.assertEqual(
                mode, MockDHD.dhdConfigAngularVelocity.mode
            )

        for _ in range(100):
            ms = randint(0, 100)
            dhd.configAngularVelocity(ms)
            self.assertEqual(ms, MockDHD.dhdConfigAngularVelocity.ms)

        self.assertIDImpl(
            lambda ID = -1: dhd.configAngularVelocity(ID=ID),
            MockDHD.dhdConfigAngularVelocity
        )

        self.assertRetImpl(
            dhd.configAngularVelocity,
            MockDHD.dhdConfigAngularVelocity
        )

    def test_getAngularVelocityRad(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetAngularVelocityRad,
            MockDHD.dhdGetAngularVelocityRad
        )

        libdhd.dhdGetAngularVelocityRad = (  # type: ignore
            MockDHD.dhdGetAngularVelocityRad.mock
        )
        out = [0.0, 0.0, 0.0]

        for _ in range(100):
            MockDHD.dhdGetAngularVelocityRad.wx = random()
            MockDHD.dhdGetAngularVelocityRad.wy = random()
            MockDHD.dhdGetAngularVelocityRad.wz = random()

            dhd.getAngularVelocityRad(out)

            self.assertAlmostEqual(out[0], MockDHD.dhdGetAngularVelocityRad.wx)
            self.assertAlmostEqual(out[1], MockDHD.dhdGetAngularVelocityRad.wy)
            self.assertAlmostEqual(out[2], MockDHD.dhdGetAngularVelocityRad.wz)

        self.assertIDImpl(
            lambda ID = -1: dhd.getAngularVelocityRad(out, ID),
            MockDHD.dhdGetAngularVelocityRad
        )
        self.assertRetImpl(
            lambda: dhd.getAngularVelocityRad(out),
            MockDHD.dhdGetAngularVelocityRad
        )


    def test_getAngularVelocityDeg(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetAngularVelocityDeg,
            MockDHD.dhdGetAngularVelocityDeg
        )

        libdhd.dhdGetAngularVelocityDeg = (  # type: ignore
            MockDHD.dhdGetAngularVelocityDeg.mock
        )
        out = [0.0, 0.0, 0.0]

        for _ in range(100):
            MockDHD.dhdGetAngularVelocityDeg.wx = random()
            MockDHD.dhdGetAngularVelocityDeg.wy = random()
            MockDHD.dhdGetAngularVelocityDeg.wz = random()

            dhd.getAngularVelocityDeg(out)

            self.assertAlmostEqual(out[0], MockDHD.dhdGetAngularVelocityDeg.wx)
            self.assertAlmostEqual(out[1], MockDHD.dhdGetAngularVelocityDeg.wy)
            self.assertAlmostEqual(out[2], MockDHD.dhdGetAngularVelocityDeg.wz)

        self.assertIDImpl(
            lambda ID = -1: dhd.getAngularVelocityDeg(out, ID),
            MockDHD.dhdGetAngularVelocityDeg
        )
        self.assertRetImpl(
            lambda: dhd.getAngularVelocityDeg(out),
            MockDHD.dhdGetAngularVelocityDeg
        )

    def test_configGripperVelocity(self):
        self.assertSignaturesEqual(
            libdhd.dhdConfigGripperVelocity,
            MockDHD.dhdConfigGripperVelocity
        )

        libdhd.dhdConfigGripperVelocity = (  # type: ignore
            MockDHD.dhdConfigGripperVelocity.mock
        )

        for mode in VelocityEstimatorMode:
            dhd.configGripperVelocity(mode=mode)
            self.assertAlmostEqual(
                mode, MockDHD.dhdConfigGripperVelocity.mode
            )

        for _ in range(100):
            ms = randint(0, 100)
            dhd.configGripperVelocity(ms)
            self.assertEqual(ms, MockDHD.dhdConfigGripperVelocity.ms)

        self.assertIDImpl(
            lambda ID = -1: dhd.configGripperVelocity(ID=ID),
            MockDHD.dhdConfigGripperVelocity
        )

        self.assertRetImpl(
            dhd.configGripperVelocity,
            MockDHD.dhdConfigGripperVelocity
        )

    def test_getGripperLinearVelocity(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetGripperLinearVelocity,
            MockDHD.dhdGetGripperLinearVelocity
        )

        libdhd.dhdGetGripperLinearVelocity = (  # type: ignore
            MockDHD.dhdGetGripperLinearVelocity.mock
        )

        out = c_double()

        for _ in range(100):
            MockDHD.dhdGetGripperLinearVelocity.vg = random()
            dhd.getGripperLinearVelocity(out)

            self.assertAlmostEqual(
                out.value,
                MockDHD.dhdGetGripperLinearVelocity.vg
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.getGripperLinearVelocity(out, ID),
            MockDHD.dhdGetGripperLinearVelocity
        )

        self.assertRetImpl(
            lambda: dhd.getGripperLinearVelocity(out),
            MockDHD.dhdGetGripperLinearVelocity
        )


    def test_getGripperAngularVelocityRad(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetGripperAngularVelocityRad,
            MockDHD.dhdGetGripperAngularVelocityRad
        )

        libdhd.dhdGetGripperAngularVelocityRad = (  # type: ignore
            MockDHD.dhdGetGripperAngularVelocityRad.mock
        )

        out = c_double()

        for _ in range(100):
            MockDHD.dhdGetGripperAngularVelocityRad.wg = random()
            dhd.getGripperAngularVelocityRad(out)

            self.assertAlmostEqual(
                out.value,
                MockDHD.dhdGetGripperAngularVelocityRad.wg
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.getGripperAngularVelocityRad(out, ID),
            MockDHD.dhdGetGripperAngularVelocityRad
        )

        self.assertRetImpl(
            lambda: dhd.getGripperAngularVelocityRad(out),
            MockDHD.dhdGetGripperAngularVelocityRad
        )

    def test_getGripperAngularVelocityDeg(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetGripperAngularVelocityDeg,
            MockDHD.dhdGetGripperAngularVelocityDeg
        )

        libdhd.dhdGetGripperAngularVelocityDeg = (  # type: ignore
            MockDHD.dhdGetGripperAngularVelocityDeg.mock
        )

        out = c_double()

        for _ in range(100):
            MockDHD.dhdGetGripperAngularVelocityDeg.wg = random()
            dhd.getGripperAngularVelocityDeg(out)

            self.assertAlmostEqual(
                out.value,
                MockDHD.dhdGetGripperAngularVelocityDeg.wg
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.getGripperAngularVelocityDeg(out, ID),
            MockDHD.dhdGetGripperAngularVelocityDeg
        )

        self.assertRetImpl(
            lambda: dhd.getGripperAngularVelocityDeg(out),
            MockDHD.dhdGetGripperAngularVelocityDeg
        )

    def test_emulateButton(self):
        self.assertSignaturesEqual(
            libdhd.dhdEmulateButton, MockDHD.dhdEmulateButton
        )

        libdhd.dhdEmulateButton = MockDHD.dhdEmulateButton.mock  # type: ignore

        dhd.emulateButton(True)
        self.assertTrue(MockDHD.dhdEmulateButton.enable)

        dhd.emulateButton(False)
        self.assertFalse(MockDHD.dhdEmulateButton.enable)

        self.assertIDImpl(
            lambda ID = -1: dhd.emulateButton(True, ID),
            MockDHD.dhdEmulateButton
        )

        self.assertRetImpl(
            lambda: dhd.emulateButton(True),
            MockDHD.dhdEmulateButton
        )


    def test_getBaseAngleXRad(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetBaseAngleXRad, MockDHD.dhdGetBaseAngleXRad
        )

        libdhd.dhdGetBaseAngleXRad = (  # type: ignore
            MockDHD.dhdGetBaseAngleXRad.mock
        )

        out = c_double()
        for _ in range(100):
            MockDHD.dhdGetBaseAngleXRad.base_angle_x = random()
            dhd.getBaseAngleXRad(out)
            self.assertAlmostEqual(
                out.value,
                MockDHD.dhdGetBaseAngleXRad.base_angle_x
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.getBaseAngleXRad(out, ID),
            MockDHD.dhdGetBaseAngleXRad
        )

        self.assertRetImpl(
            lambda: dhd.getBaseAngleXRad(out),
            MockDHD.dhdGetBaseAngleXRad
        )

    def test_getBaseAngleXDeg(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetBaseAngleXDeg, MockDHD.dhdGetBaseAngleXDeg
        )

        libdhd.dhdGetBaseAngleXDeg = (  # type: ignore
            MockDHD.dhdGetBaseAngleXDeg.mock
        )

        out = c_double()
        for _ in range(100):
            MockDHD.dhdGetBaseAngleXDeg.base_angle_x = random()
            dhd.getBaseAngleXDeg(out)
            self.assertAlmostEqual(
                out.value,
                MockDHD.dhdGetBaseAngleXDeg.base_angle_x
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.getBaseAngleXDeg(out, ID),
            MockDHD.dhdGetBaseAngleXDeg
        )

        self.assertRetImpl(
            lambda: dhd.getBaseAngleXDeg(out),
            MockDHD.dhdGetBaseAngleXDeg
        )

    def test_setBaseAngleXRad(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetBaseAngleXRad,
            MockDHD.dhdSetBaseAngleXRad
        )

        libdhd.dhdSetBaseAngleXRad = (  # type: ignore
            MockDHD.dhdSetBaseAngleXRad.mock
        )

        for _ in range(100):
            angle = random()
            dhd.setBaseAngleXRad(angle)
            self.assertAlmostEqual(
                angle, MockDHD.dhdSetBaseAngleXRad.base_angle_x
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.setBaseAngleXRad(0, ID),
            MockDHD.dhdSetBaseAngleXRad
        )

        self.assertRetImpl(
            lambda: dhd.setBaseAngleXRad(0),
            MockDHD.dhdSetBaseAngleXRad
        )

    def test_setBaseAngleXDeg(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetBaseAngleXDeg,
            MockDHD.dhdSetBaseAngleXDeg
        )

        libdhd.dhdSetBaseAngleXDeg = (  # type: ignore
            MockDHD.dhdSetBaseAngleXDeg.mock
        )

        for _ in range(100):
            angle = random()
            dhd.setBaseAngleXDeg(angle)
            self.assertAlmostEqual(
                angle, MockDHD.dhdSetBaseAngleXDeg.base_angle_x
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.setBaseAngleXDeg(0, ID),
            MockDHD.dhdSetBaseAngleXDeg
        )

        self.assertRetImpl(
            lambda: dhd.setBaseAngleXDeg(0),
            MockDHD.dhdSetBaseAngleXDeg
        )

    def test_getBaseAngleZRad(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetBaseAngleZRad, MockDHD.dhdGetBaseAngleZRad
        )

        libdhd.dhdGetBaseAngleZRad = (  # type: ignore
            MockDHD.dhdGetBaseAngleZRad.mock
        )

        out = c_double()
        for _ in range(100):
            MockDHD.dhdGetBaseAngleZRad.base_angle_z = random()
            dhd.getBaseAngleZRad(out)
            self.assertAlmostEqual(
                out.value,
                MockDHD.dhdGetBaseAngleZRad.base_angle_z
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.getBaseAngleZRad(out, ID),
            MockDHD.dhdGetBaseAngleZRad
        )

        self.assertRetImpl(
            lambda: dhd.getBaseAngleZRad(out),
            MockDHD.dhdGetBaseAngleZRad
        )

    def test_getBaseAngleZDeg(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetBaseAngleZDeg, MockDHD.dhdGetBaseAngleZDeg
        )

        libdhd.dhdGetBaseAngleZDeg = (  # type: ignore
            MockDHD.dhdGetBaseAngleZDeg.mock
        )

        out = c_double()
        for _ in range(100):
            MockDHD.dhdGetBaseAngleZDeg.base_angle_z = random()
            dhd.getBaseAngleZDeg(out)
            self.assertAlmostEqual(
                out.value,
                MockDHD.dhdGetBaseAngleZDeg.base_angle_z
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.getBaseAngleZDeg(out, ID),
            MockDHD.dhdGetBaseAngleZDeg
        )

        self.assertRetImpl(
            lambda: dhd.getBaseAngleZDeg(out),
            MockDHD.dhdGetBaseAngleZDeg
        )

    def test_setBaseAngleZRad(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetBaseAngleZRad,
            MockDHD.dhdSetBaseAngleZRad
        )

        libdhd.dhdSetBaseAngleZRad = (  # type: ignore
            MockDHD.dhdSetBaseAngleZRad.mock
        )

        for _ in range(100):
            angle = random()
            dhd.setBaseAngleZRad(angle)
            self.assertAlmostEqual(
                angle, MockDHD.dhdSetBaseAngleZRad.base_angle_z
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.setBaseAngleZRad(0, ID),
            MockDHD.dhdSetBaseAngleZRad
        )

        self.assertRetImpl(
            lambda: dhd.setBaseAngleZRad(0),
            MockDHD.dhdSetBaseAngleZRad
        )

    def test_setBaseAngleZDeg(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetBaseAngleZDeg,
            MockDHD.dhdSetBaseAngleZDeg
        )

        libdhd.dhdSetBaseAngleZDeg = (  # type: ignore
            MockDHD.dhdSetBaseAngleZDeg.mock
        )

        for _ in range(100):
            angle = random()
            dhd.setBaseAngleZDeg(angle)
            self.assertAlmostEqual(
                angle, MockDHD.dhdSetBaseAngleZDeg.base_angle_z
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.setBaseAngleZDeg(0, ID),
            MockDHD.dhdSetBaseAngleZDeg
        )

        self.assertRetImpl(
            lambda: dhd.setBaseAngleZDeg(0),
            MockDHD.dhdSetBaseAngleZDeg
        )

    def test_setVibration(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetVibration,
            MockDHD.dhdSetVibration
        )

        libdhd.dhdSetVibration = MockDHD.dhdSetVibration.mock  # type: ignore

        for _ in range(100):
            freq = random()
            amplitude = random()
            profile = randint(0, 100)

            dhd.setVibration(freq, amplitude, profile)

            self.assertAlmostEqual(freq, MockDHD.dhdSetVibration.freq)
            self.assertAlmostEqual(
                amplitude, MockDHD.dhdSetVibration.amplitude
            )

            self.assertEqual(profile, MockDHD.dhdSetVibration.profile)

        self.assertIDImpl(
            lambda ID = -1: dhd.setVibration(0, 0, 0, ID),
            MockDHD.dhdSetVibration
        )

        self.assertRetImpl(
            lambda: dhd.setVibration(0, 0, 0),
            MockDHD.dhdSetVibration
        )

    def test_setMaxForce(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetMaxForce,
            MockDHD.dhdSetMaxForce
        )

        libdhd.dhdSetMaxForce = (  # type: ignore
            MockDHD.dhdSetMaxForce.mock
        )

        for _ in range(100):
            limit = random()
            dhd.setMaxForce(limit)
            self.assertAlmostEqual(limit, MockDHD.dhdSetMaxForce.limit)

        self.assertIDImpl(
            lambda ID = -1: dhd.setMaxForce(0, ID),
            MockDHD.dhdSetMaxForce
        )

        self.assertRetImpl(
            lambda: dhd.setMaxForce(0),
            MockDHD.dhdSetMaxForce
        )

    def test_setMaxTorque(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetMaxTorque,
            MockDHD.dhdSetMaxTorque
        )

        libdhd.dhdSetMaxTorque = (  # type: ignore
            MockDHD.dhdSetMaxTorque.mock
        )

        for _ in range(100):
            limit = random()
            dhd.setMaxTorque(limit)
            self.assertAlmostEqual(limit, MockDHD.dhdSetMaxTorque.limit)

        self.assertIDImpl(
            lambda ID = -1: dhd.setMaxTorque(0, ID),
            MockDHD.dhdSetMaxTorque
        )

        self.assertRetImpl(
            lambda: dhd.setMaxTorque(0),
            MockDHD.dhdSetMaxTorque
        )

    def test_setMaxGripperForce(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetMaxGripperForce,
            MockDHD.dhdSetMaxGripperForce
        )

        libdhd.dhdSetMaxGripperForce = (  # type: ignore
            MockDHD.dhdSetMaxGripperForce.mock
        )

        for _ in range(100):
            limit = random()
            dhd.setMaxGripperForce(limit)
            self.assertAlmostEqual(limit, MockDHD.dhdSetMaxGripperForce.limit)

        self.assertIDImpl(
            lambda ID = -1: dhd.setMaxGripperForce(0, ID),
            MockDHD.dhdSetMaxGripperForce
        )

        self.assertRetImpl(
            lambda: dhd.setMaxGripperForce(0),
            MockDHD.dhdSetMaxGripperForce
        )

    def test_getMaxForce(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetMaxForce,
            MockDHD.dhdGetMaxForce
        )

        libdhd.dhdGetMaxForce = (  # type: ignore
            MockDHD.dhdGetMaxForce.mock
        )

        for _ in range(100):
            MockDHD.dhdGetMaxForce.ret = random()
            self.assertAlmostEqual(
                dhd.getMaxForce(), MockDHD.dhdGetMaxForce.ret
            )

        self.assertIDImpl(dhd.getMaxForce, MockDHD.dhdGetMaxForce)

    def test_getMaxTorque(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetMaxTorque,
            MockDHD.dhdGetMaxTorque
        )

        libdhd.dhdGetMaxTorque = (  # type: ignore
            MockDHD.dhdGetMaxTorque.mock
        )

        for _ in range(100):
            MockDHD.dhdGetMaxTorque.ret = random()
            self.assertAlmostEqual(
                dhd.getMaxTorque(), MockDHD.dhdGetMaxTorque.ret
            )

        self.assertIDImpl(dhd.getMaxTorque, MockDHD.dhdGetMaxTorque)

    def test_getMaxGripperForce(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetMaxGripperForce,
            MockDHD.dhdGetMaxGripperForce
        )

        libdhd.dhdGetMaxGripperForce = (  # type: ignore
            MockDHD.dhdGetMaxGripperForce.mock
        )

        for _ in range(100):
            MockDHD.dhdGetMaxGripperForce.ret = random()
            self.assertAlmostEqual(
                dhd.getMaxGripperForce(), MockDHD.dhdGetMaxGripperForce.ret
            )

        self.assertIDImpl(
            dhd.getMaxGripperForce,
            MockDHD.dhdGetMaxGripperForce
        )
