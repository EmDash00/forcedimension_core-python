from random import randint, random
from typing import Any
import unittest
from array import array
from ctypes import (CFUNCTYPE, POINTER, c_byte, c_char_p, c_double, c_int,
                    c_ubyte, c_uint, c_ushort)
import warnings
from forcedimension_core import containers

import forcedimension_core.dhd as dhd
import forcedimension_core.runtime as runtime
from forcedimension_core.dhd.constants import MAX_DOF, ComMode, DeviceType, ErrorNum

libdhd = runtime._libdhd


class MockDHD:
    class dhdEnableExpertMode:
        argtypes = []
        restype = c_int

        enable = False

        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock():
            MockDHD.dhdEnableExpertMode.enable = True
            return MockDHD.dhdEnableExpertMode.ret

    class dhdDisableExpertMode:
        argtypes = []
        restype = c_int

        enable = True

        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock():
            MockDHD.dhdDisableExpertMode.enable = False
            return MockDHD.dhdDisableExpertMode.ret

    class dhdPreset:
        argtypes = [POINTER(c_int), c_ubyte, c_byte]
        restype = c_int

        val = array('i', (0 for _ in range(MAX_DOF)))

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(val, mask, ID):
            MockDHD.dhdPreset.ID = ID

            for i in range(MAX_DOF):
                MockDHD.dhdPreset.val[i] = val[i]

            return MockDHD.dhdPreset.ret

    class dhdSetTimeGuard:
        argtypes = [c_int, c_byte]
        restype = c_int

        timeguard_us = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(timeguard_us, ID):
            MockDHD.dhdSetTimeGuard.ID = ID
            MockDHD.dhdSetTimeGuard.timeguard_us = timeguard_us
            return MockDHD.dhdSetTimeGuard.ret

    class dhdSetVelocityThreshold:
        argtypes = [c_uint, c_byte]
        restype = c_int

        thresh = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(thresh, ID):
            MockDHD.dhdSetVelocityThreshold.ID = ID
            MockDHD.dhdSetVelocityThreshold.thresh = thresh
            return MockDHD.dhdSetVelocityThreshold.ret

    class dhdGetVelocityThreshold:
        argtypes = [POINTER(c_uint), c_byte]
        restype = c_int

        thresh = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(thresh, ID):
            MockDHD.dhdGetVelocityThreshold.ID = ID
            thresh.contents.value = MockDHD.dhdGetVelocityThreshold.thresh

            return MockDHD.dhdGetVelocityThreshold.ret

    class dhdUpdateEncoders:
        argtypes = [c_byte]
        restype = c_int

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDHD.dhdUpdateEncoders.ID = ID
            return MockDHD.dhdUpdateEncoders.ret

    class dhdGetDeltaEncoders:
        argtypes = [
            POINTER(c_int), POINTER(c_int), POINTER(c_int), c_byte
        ]
        restype = c_int

        enc0: int = 0
        enc1: int = 0
        enc2: int = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enc0, enc1, enc2, ID):
            MockDHD.dhdGetDeltaEncoders.ID = ID

            enc0.contents.value = MockDHD.dhdGetDeltaEncoders.enc0
            enc1.contents.value = MockDHD.dhdGetDeltaEncoders.enc1
            enc2.contents.value = MockDHD.dhdGetDeltaEncoders.enc2

            return MockDHD.dhdGetDeltaEncoders.ret

    class dhdGetWristEncoders:
        argtypes = [
            POINTER(c_int), POINTER(c_int), POINTER(c_int), c_byte
        ]
        restype = c_int

        enc0 = 0
        enc1 = 0
        enc2 = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enc0, enc1, enc2, ID):
            MockDHD.dhdGetWristEncoders.ID = ID

            enc0.contents.value = MockDHD.dhdGetWristEncoders.enc0
            enc1.contents.value = MockDHD.dhdGetWristEncoders.enc1
            enc2.contents.value = MockDHD.dhdGetWristEncoders.enc2

            return MockDHD.dhdGetWristEncoders.ret

    class dhdGetGripperEncoder:
        argtypes = [POINTER(c_int), c_byte]
        restype = c_int

        enc = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enc, ID):
            MockDHD.dhdGetGripperEncoder.ID = ID
            enc.contents.value = MockDHD.dhdGetGripperEncoder.enc
            return MockDHD.dhdGetGripperEncoder.ret

    class dhdGetEncoder:
        argtypes = [c_int, c_byte]
        restype = c_int

        index: int = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(index, ID):
            MockDHD.dhdGetEncoder.ID = ID
            MockDHD.dhdGetEncoder.index = index

            return MockDHD.dhdGetEncoder.ret

    class dhdSetMotor:
        argtypes = [c_int, c_ushort, c_byte]
        restype = c_int

        index: int = 0
        output: int = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(index, mot, ID):
            MockDHD.dhdSetMotor.ID = ID

            MockDHD.dhdSetMotor.index = index
            MockDHD.dhdSetMotor.output = mot

            return MockDHD.dhdSetMotor.ret

    class dhdSetDeltaMotor:
        argtypes = [c_ushort, c_ushort, c_ushort, c_byte]
        restype = c_int

        mot0: int = 0
        mot1: int = 0
        mot2: int = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(mot0, mot1, mot2, ID):
            MockDHD.dhdSetDeltaMotor.ID = ID

            MockDHD.dhdSetDeltaMotor.mot0 = mot0
            MockDHD.dhdSetDeltaMotor.mot1 = mot1
            MockDHD.dhdSetDeltaMotor.mot2 = mot2

            return MockDHD.dhdSetDeltaMotor.ret


    class dhdSetWristMotor:
        argtypes = [c_ushort, c_ushort, c_ushort, c_byte]
        restype = c_int

        mot0 = 0
        mot1 = 0
        mot2 = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(mot0, mot1, mot2, ID):
            MockDHD.dhdSetWristMotor.ID = ID

            MockDHD.dhdSetWristMotor.mot0 = mot0
            MockDHD.dhdSetWristMotor.mot1 = mot1
            MockDHD.dhdSetWristMotor.mot2 = mot2

            return MockDHD.dhdSetWristMotor.ret

    class dhdSetGripperMotor:
        argtypes = [c_ushort, c_byte]
        restype = c_int

        mot: int = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(mot, ID):
            MockDHD.dhdSetGripperMotor.ID = ID
            MockDHD.dhdSetGripperMotor.mot = mot
            return MockDHD.dhdSetGripperMotor.ret

    class dhdDeltaEncoderToPosition:
        argtypes = [
            c_int, c_int, c_int,
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        enc0: int = 0
        enc1: int = 0
        enc2: int = 0

        px: float = 0
        py: float = 0
        pz: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enc0, enc1, enc2, px, py, pz, ID):
            MockDHD.dhdDeltaEncoderToPosition.ID = ID


            MockDHD.dhdDeltaEncoderToPosition.enc0 = enc0
            MockDHD.dhdDeltaEncoderToPosition.enc1 = enc1
            MockDHD.dhdDeltaEncoderToPosition.enc2 = enc2

            px.contents.value = MockDHD.dhdDeltaEncoderToPosition.px
            py.contents.value = MockDHD.dhdDeltaEncoderToPosition.py
            pz.contents.value = MockDHD.dhdDeltaEncoderToPosition.pz

            return MockDHD.dhdDeltaEncoderToPosition.ret

    class dhdDeltaPositionToEncoder:
        argtypes = [
            c_double, c_double, c_double,
            POINTER(c_int), POINTER(c_int), POINTER(c_int), c_byte
        ]
        restype = c_int

        enc0 = 0
        enc1 = 0
        enc2 = 0

        px = 0
        py = 0
        pz = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(px, py, pz, enc0, enc1, enc2, ID):
            MockDHD.dhdDeltaPositionToEncoder.ID = ID

            MockDHD.dhdDeltaPositionToEncoder.px = px
            MockDHD.dhdDeltaPositionToEncoder.py = py
            MockDHD.dhdDeltaPositionToEncoder.pz = pz

            enc0.contents.value = MockDHD.dhdDeltaPositionToEncoder.enc0
            enc1.contents.value = MockDHD.dhdDeltaPositionToEncoder.enc1
            enc2.contents.value = MockDHD.dhdDeltaPositionToEncoder.enc2

            return MockDHD.dhdDeltaPositionToEncoder.ret

    class dhdDeltaMotorToForce:
        argtypes = [
            c_ushort, c_ushort, c_ushort,
            c_int, c_int, c_int,
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        mot0: int = 0
        mot1: int = 0
        mot2: int = 0

        enc0: int = 0
        enc1: int = 0
        enc2: int = 0

        fx: float = 0
        fy: float = 0
        fz: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(mot0, mot1, mot2, enc0, enc1, enc2, fx, fy, fz, ID):
            MockDHD.dhdDeltaMotorToForce.ID = ID

            MockDHD.dhdDeltaMotorToForce.mot0 = mot0
            MockDHD.dhdDeltaMotorToForce.mot1 = mot1
            MockDHD.dhdDeltaMotorToForce.mot2 = mot2

            MockDHD.dhdDeltaMotorToForce.enc0 = enc0
            MockDHD.dhdDeltaMotorToForce.enc1 = enc1
            MockDHD.dhdDeltaMotorToForce.enc2 = enc2

            fx.contents.value = MockDHD.dhdDeltaMotorToForce.fx
            fy.contents.value = MockDHD.dhdDeltaMotorToForce.fy
            fz.contents.value = MockDHD.dhdDeltaMotorToForce.fz

            return MockDHD.dhdDeltaMotorToForce.ret

    class dhdDeltaForceToMotor:
        argtypes = [
            c_double, c_double, c_double,
            c_int, c_int, c_int,
            POINTER(c_ushort), POINTER(c_ushort), POINTER(c_ushort), c_byte
        ]
        restype = c_int

        mot0: int = 0
        mot1: int = 0
        mot2: int = 0

        enc0: int = 0
        enc1: int = 0
        enc2: int = 0

        fx: float = 0
        fy: float = 0
        fz: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(fx, fy, fz, enc0, enc1, enc2, mot0, mot1, mot2, ID):
            MockDHD.dhdDeltaForceToMotor.ID = ID

            MockDHD.dhdDeltaForceToMotor.fx = fx
            MockDHD.dhdDeltaForceToMotor.fy = fy
            MockDHD.dhdDeltaForceToMotor.fz = fz

            MockDHD.dhdDeltaForceToMotor.enc0 = enc0
            MockDHD.dhdDeltaForceToMotor.enc1 = enc1
            MockDHD.dhdDeltaForceToMotor.enc2 = enc2

            mot0.contents.value = MockDHD.dhdDeltaForceToMotor.mot0
            mot1.contents.value = MockDHD.dhdDeltaForceToMotor.mot1
            mot2.contents.value = MockDHD.dhdDeltaForceToMotor.mot2

            return MockDHD.dhdDeltaForceToMotor.ret

    class dhdWristEncoderToOrientation:
        argtypes = [
            c_int, c_int, c_int,
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        enc0: int = 0
        enc1: int = 0
        enc2: int = 0

        oa: float = 0
        ob: float = 0
        og: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enc0, enc1, enc2, oa, ob, og, ID):
            MockDHD.dhdWristEncoderToOrientation.ID = ID

            MockDHD.dhdWristEncoderToOrientation.enc0 = enc0
            MockDHD.dhdWristEncoderToOrientation.enc1 = enc1
            MockDHD.dhdWristEncoderToOrientation.enc2 = enc2

            oa.contents.value = MockDHD.dhdWristEncoderToOrientation.oa
            ob.contents.value = MockDHD.dhdWristEncoderToOrientation.ob
            og.contents.value = MockDHD.dhdWristEncoderToOrientation.og

            return MockDHD.dhdWristEncoderToOrientation.ret



    class dhdWristOrientationToEncoder:
        argtypes = [
            c_double, c_double, c_double,
            POINTER(c_int), POINTER(c_int), POINTER(c_int), c_byte
        ]
        restype = c_int

        enc0 = 0
        enc1 = 0
        enc2 = 0

        oa = 0
        ob = 0
        og = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(oa, ob, og, enc0, enc1, enc2, ID):
            MockDHD.dhdWristOrientationToEncoder.ID = ID

            MockDHD.dhdWristOrientationToEncoder.oa = oa
            MockDHD.dhdWristOrientationToEncoder.ob = ob
            MockDHD.dhdWristOrientationToEncoder.og = og

            enc0.contents.value = MockDHD.dhdWristOrientationToEncoder.enc0
            enc1.contents.value = MockDHD.dhdWristOrientationToEncoder.enc1
            enc2.contents.value = MockDHD.dhdWristOrientationToEncoder.enc2

            return MockDHD.dhdWristOrientationToEncoder.ret

    class dhdWristMotorToTorque:
        argtypes = [
            c_ushort, c_ushort, c_ushort,
            c_int, c_int, c_int,
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        mot0: int = 0
        mot1: int = 0
        mot2: int = 0

        enc0: int = 0
        enc1: int = 0
        enc2: int = 0

        tx: float = 0
        ty: float = 0
        tz: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(mot0, mot1, mot2, enc0, enc1, enc2, tx, ty, tz, ID):
            MockDHD.dhdWristMotorToTorque.ID = ID

            MockDHD.dhdWristMotorToTorque.mot0 = mot0
            MockDHD.dhdWristMotorToTorque.mot1 = mot1
            MockDHD.dhdWristMotorToTorque.mot2 = mot2

            MockDHD.dhdWristMotorToTorque.enc0 = enc0
            MockDHD.dhdWristMotorToTorque.enc1 = enc1
            MockDHD.dhdWristMotorToTorque.enc2 = enc2

            tx.contents.value = MockDHD.dhdWristMotorToTorque.tx
            ty.contents.value = MockDHD.dhdWristMotorToTorque.ty
            tz.contents.value = MockDHD.dhdWristMotorToTorque.tz

            return MockDHD.dhdWristMotorToTorque.ret


    class dhdWristTorqueToMotor:
        argtypes = [
            c_double, c_double, c_double,
            c_int, c_int, c_int,
            POINTER(c_ushort), POINTER(c_ushort), POINTER(c_ushort), c_byte
        ]
        restype = c_int

        mot0: int = 0
        mot1: int = 0
        mot2: int = 0

        enc0: int = 0
        enc1: int = 0
        enc2: int = 0

        tx: float = 0
        ty: float = 0
        tz: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(tx, ty, tz, enc0, enc1, enc2, mot0, mot1, mot2, ID):
            MockDHD.dhdWristTorqueToMotor.ID = ID

            MockDHD.dhdWristTorqueToMotor.tx = tx
            MockDHD.dhdWristTorqueToMotor.ty = ty
            MockDHD.dhdWristTorqueToMotor.tz = tz

            MockDHD.dhdWristTorqueToMotor.enc0 = enc0
            MockDHD.dhdWristTorqueToMotor.enc1 = enc1
            MockDHD.dhdWristTorqueToMotor.enc2 = enc2

            mot0.contents.value = MockDHD.dhdWristTorqueToMotor.mot0
            mot1.contents.value = MockDHD.dhdWristTorqueToMotor.mot1
            mot2.contents.value = MockDHD.dhdWristTorqueToMotor.mot2

            return MockDHD.dhdWristTorqueToMotor.ret


    class dhdGripperEncoderToAngleRad:
        argtypes = [c_int, POINTER(c_double), c_byte]
        restype = c_int

        enc: int = 0
        angle: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enc, angle, ID):
            MockDHD.dhdGripperEncoderToAngleRad.ID = ID

            MockDHD.dhdGripperEncoderToAngleRad.enc = enc
            angle.contents.value = MockDHD.dhdGripperEncoderToAngleRad.angle

            return MockDHD.dhdGripperEncoderToAngleRad.ret

    class dhdGripperEncoderToGap:
        argtypes = [c_int, POINTER(c_double), c_byte]
        restype = c_int

        enc: int = 0
        gap: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enc, gap, ID):
            MockDHD.dhdGripperEncoderToGap.ID = ID

            MockDHD.dhdGripperEncoderToGap.enc = enc
            gap.contents.value = MockDHD.dhdGripperEncoderToGap.gap

            return MockDHD.dhdGripperEncoderToGap.ret

    class dhdGripperAngleRadToEncoder:
        argtypes = [c_double, POINTER(c_int), c_byte]
        restype = c_int

        enc: int = 0
        angle: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(angle, enc, ID):
            MockDHD.dhdGripperAngleRadToEncoder.ID = ID

            MockDHD.dhdGripperAngleRadToEncoder.angle = angle
            enc.contents.value = MockDHD.dhdGripperAngleRadToEncoder.enc

            return MockDHD.dhdGripperAngleRadToEncoder.ret

    class dhdGripperGapToEncoder:
        argtypes = [c_double, POINTER(c_int), c_byte]
        restype = c_int

        enc = 0
        gap = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(gap, enc, ID):
            MockDHD.dhdGripperGapToEncoder.ID = ID

            MockDHD.dhdGripperGapToEncoder.gap = gap
            enc.contents.value = MockDHD.dhdGripperGapToEncoder.enc

            return MockDHD.dhdGripperGapToEncoder.ret

    class dhdGripperMotorToForce:
        argtypes = [
            c_ushort, POINTER(c_double), POINTER(c_int), c_byte
        ]
        restype = c_int

        mot:int = 0
        f: float = 0
        enc = array('i', (0 for _ in range(4)))

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(mot, f, enc, ID):
            MockDHD.dhdGripperMotorToForce.ID = ID


            MockDHD.dhdGripperMotorToForce.mot = mot
            for i in range(4):
                MockDHD.dhdGripperMotorToForce.enc[i] = enc[i]
            f.contents.value = MockDHD.dhdGripperMotorToForce.f

            return MockDHD.dhdGripperMotorToForce.ret

    class dhdGripperForceToMotor:
        argtypes = [c_double, POINTER(c_ushort), POINTER(c_int), c_byte]
        restype = c_int

        mot: int = 0
        f: float = 0
        enc = array('i', (0 for _ in range(4)))

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(f, mot, enc, ID):
            MockDHD.dhdGripperForceToMotor.ID = ID

            MockDHD.dhdGripperForceToMotor.f = f

            for i in range(4):
                MockDHD.dhdGripperForceToMotor.enc[i] = enc[i]

            mot.contents.value = MockDHD.dhdGripperForceToMotor.mot

            return MockDHD.dhdGripperForceToMotor.ret


    class dhdSetMot:
        argtypes = [POINTER(c_ushort), c_ubyte, c_byte]
        restype = c_int

        mot = [0] * MAX_DOF
        mask = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(mot, mask, ID):
            MockDHD.dhdSetMot.ID = ID

            MockDHD.dhdSetMot.mask = mask
            for i in range(MAX_DOF):
                MockDHD.dhdSetMot.mot[i] = mot[i]

            return MockDHD.dhdSetMot.ret

    class dhdSetJointTorques:
        argtypes = [POINTER(c_double), c_ubyte, c_byte]
        restype = c_int

        q = [0.0] * MAX_DOF
        mask = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(q, mask, ID):
            MockDHD.dhdSetJointTorques.ID = ID

            MockDHD.dhdSetJointTorques.mask = mask
            for i in range(MAX_DOF):
                MockDHD.dhdSetJointTorques.q[i] = q[i]

            return MockDHD.dhdSetJointTorques.ret

    class dhdPreloadMot:
        argtypes = [POINTER(c_ushort), c_ubyte, c_byte]
        restype = c_int

        mot = [0] * MAX_DOF
        mask = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(mot, mask, ID):
            MockDHD.dhdPreloadMot.ID = ID

            MockDHD.dhdPreloadMot.mask = mask
            for i in range(MAX_DOF):
                MockDHD.dhdPreloadMot.mot[i] = mot[i]

            return MockDHD.dhdPreloadMot.ret

    class dhdGetEnc:
        argtypes = [POINTER(c_int), c_ubyte, c_byte]
        restype = c_int

        enc = [0] * MAX_DOF
        mask = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enc, mask, ID):
            MockDHD.dhdGetEnc.ID = ID

            MockDHD.dhdGetEnc.mask = mask
            for i in range(MAX_DOF):
                enc[i] = MockDHD.dhdGetEnc.enc[i]

            return MockDHD.dhdGetEnc.ret

    class dhdSetBrk:
        argtypes = [c_ubyte, c_byte]
        restype = c_int

        mask = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(mask, ID):
            MockDHD.dhdSetBrk.ID = ID
            MockDHD.dhdSetBrk.mask = mask
            return MockDHD.dhdSetBrk.ret

    class dhdGetDeltaJointAngles:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        j0: float = 0
        j1: float = 0
        j2: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(j0, j1, j2, ID):
            MockDHD.dhdGetDeltaJointAngles.ID = ID

            j0.contents.value = MockDHD.dhdGetDeltaJointAngles.j0
            j1.contents.value = MockDHD.dhdGetDeltaJointAngles.j1
            j2.contents.value = MockDHD.dhdGetDeltaJointAngles.j2

            return MockDHD.dhdGetDeltaJointAngles.ret

    class dhdGetDeltaJacobian:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        jcb = [[0.0] * 3] * 3

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(jcb, ID):
            MockDHD.dhdGetDeltaJacobian.ID = ID

            for i in range(3):
                for j in range(3):
                    jcb[3 * i + j] = MockDHD.dhdGetDeltaJacobian.jcb[i][j]

            return MockDHD.dhdGetDeltaJacobian.ret

    class dhdDeltaJointAnglesToJacobian:
        argtypes = [c_double, c_double, c_double, POINTER(c_double), c_byte]
        restype = c_int

        j0 = 0
        j1 = 0
        j2 = 0

        jcb = [[0.0] * 3 for _ in range(3)]

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(j0, j1, j2, jcb, ID):
            MockDHD.dhdDeltaJointAnglesToJacobian.ID = ID

            MockDHD.dhdDeltaJointAnglesToJacobian.j0 = j0
            MockDHD.dhdDeltaJointAnglesToJacobian.j1 = j1
            MockDHD.dhdDeltaJointAnglesToJacobian.j2 = j2

            for i in range(3):
                for j in range(3):
                    jcb[3 * i + j] = MockDHD.dhdDeltaJointAnglesToJacobian.jcb[i][j]

            return MockDHD.dhdDeltaJointAnglesToJacobian.ret

    class dhdDeltaJointTorquesExtrema:
        argtypes = [
            c_double, c_double, c_double,
            POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        j0 = 0
        j1 = 0
        j2 = 0

        minq = [0.0, 0.0, 0.0]
        maxq = [0.0, 0.0, 0.0]

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(j0, j1, j2, minq, maxq, ID):
           MockDHD.dhdDeltaJointTorquesExtrema.ID = ID

           MockDHD.dhdDeltaJointTorquesExtrema.j0 = j0
           MockDHD.dhdDeltaJointTorquesExtrema.j1 = j1
           MockDHD.dhdDeltaJointTorquesExtrema.j2 = j2

           for i in range(3):
                minq[i] = MockDHD.dhdDeltaJointTorquesExtrema.minq[i]

           for i in range(3):
                maxq[i] = MockDHD.dhdDeltaJointTorquesExtrema.maxq[i]

           return MockDHD.dhdDeltaJointTorquesExtrema.ret


    class dhdSetDeltaJointTorques:
        argtypes = [c_double, c_double, c_double, c_byte]
        restype = c_int

        q0 = 0
        q1 = 0
        q2 = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(q0, q1, q2, ID):
           MockDHD.dhdSetDeltaJointTorques.ID = ID

           MockDHD.dhdSetDeltaJointTorques.q0 = q0
           MockDHD.dhdSetDeltaJointTorques.q1 = q1
           MockDHD.dhdSetDeltaJointTorques.q2 = q2

           return MockDHD.dhdSetDeltaJointTorques.ret

    class dhdDeltaEncodersToJointAngles:
        argtypes = [
            c_int, c_int, c_int,
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        enc0: int = 0
        enc1: int = 0
        enc2: int = 0

        j0: float = 0
        j1: float = 0
        j2: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enc0, enc1, enc2, j0, j1, j2, ID):
            MockDHD.dhdDeltaEncodersToJointAngles.ID = ID

            MockDHD.dhdDeltaEncodersToJointAngles.enc0 = enc0
            MockDHD.dhdDeltaEncodersToJointAngles.enc1 = enc1
            MockDHD.dhdDeltaEncodersToJointAngles.enc2 = enc2

            j0.contents.value = MockDHD.dhdDeltaEncodersToJointAngles.j0
            j1.contents.value = MockDHD.dhdDeltaEncodersToJointAngles.j1
            j2.contents.value = MockDHD.dhdDeltaEncodersToJointAngles.j2

            return MockDHD.dhdDeltaEncodersToJointAngles.ret


    class dhdDeltaJointAnglesToEncoders:
        argtypes = [
            c_double, c_double, c_double,
            POINTER(c_int), POINTER(c_int), POINTER(c_int), c_byte
        ]
        restype = c_int

        enc0: int = 0
        enc1: int = 0
        enc2: int = 0

        j0: float = 0
        j1: float = 0
        j2: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(j0, j1, j2, enc0, enc1, enc2, ID):
            MockDHD.dhdDeltaJointAnglesToEncoders.ID = ID

            MockDHD.dhdDeltaJointAnglesToEncoders.j0 = j0
            MockDHD.dhdDeltaJointAnglesToEncoders.j1 = j1
            MockDHD.dhdDeltaJointAnglesToEncoders.j2 = j2

            enc0.contents.value = MockDHD.dhdDeltaJointAnglesToEncoders.enc0
            enc1.contents.value = MockDHD.dhdDeltaJointAnglesToEncoders.enc1
            enc2.contents.value = MockDHD.dhdDeltaJointAnglesToEncoders.enc2

            return MockDHD.dhdDeltaJointAnglesToEncoders.ret


    class dhdGetWristJointAngles:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        j0: float = 0
        j1: float = 0
        j2: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(j0, j1, j2, ID):
            MockDHD.dhdGetWristJointAngles.ID = ID

            j0.contents.value = MockDHD.dhdGetWristJointAngles.j0
            j1.contents.value = MockDHD.dhdGetWristJointAngles.j1
            j2.contents.value = MockDHD.dhdGetWristJointAngles.j2

            return MockDHD.dhdGetWristJointAngles.ret


    class dhdGetWristJacobian:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        jcb = [[0.0] * 3] * 3

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(jcb, ID):
            MockDHD.dhdGetWristJacobian.ID = ID

            for i in range(3):
                for j in range(3):
                    jcb[3 * i + j] = MockDHD.dhdGetWristJacobian.jcb[i][j]

            return MockDHD.dhdGetWristJacobian.ret

    class dhdWristJointAnglesToJacobian:
        argtypes = [c_double, c_double, c_double, POINTER(c_double), c_byte]
        restype = c_int

        j0 = 0
        j1 = 0
        j2 = 0

        jcb = [[0.0] * 3 for _ in range(3)]

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(j0, j1, j2, jcb, ID):
            MockDHD.dhdWristJointAnglesToJacobian.ID = ID

            MockDHD.dhdWristJointAnglesToJacobian.j0 = j0
            MockDHD.dhdWristJointAnglesToJacobian.j1 = j1
            MockDHD.dhdWristJointAnglesToJacobian.j2 = j2

            for i in range(3):
                for j in range(3):
                    jcb[3 * i + j] = MockDHD.dhdWristJointAnglesToJacobian.jcb[i][j]

            return MockDHD.dhdWristJointAnglesToJacobian.ret

    class dhdWristJointTorquesExtrema:
        argtypes = [
            c_double, c_double, c_double,
            POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        j0 = 0
        j1 = 0
        j2 = 0

        minq = [0.0, 0.0, 0.0]
        maxq = [0.0, 0.0, 0.0]

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(j0, j1, j2, minq, maxq, ID):
           MockDHD.dhdWristJointTorquesExtrema.ID = ID

           MockDHD.dhdWristJointTorquesExtrema.j0 = j0
           MockDHD.dhdWristJointTorquesExtrema.j1 = j1
           MockDHD.dhdWristJointTorquesExtrema.j2 = j2

           for i in range(3):
                minq[i] = MockDHD.dhdWristJointTorquesExtrema.minq[i]

           for i in range(3):
                maxq[i] = MockDHD.dhdWristJointTorquesExtrema.maxq[i]

           return MockDHD.dhdWristJointTorquesExtrema.ret

    class dhdSetWristJointTorques:
        argtypes = [
            c_double, c_double, c_double, c_byte
        ]
        restype = c_int

        q0 = 0
        q1 = 0
        q2 = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(q0, q1, q2, ID):
            MockDHD.dhdSetWristJointTorques.ID = ID

            MockDHD.dhdSetWristJointTorques.q0 = q0
            MockDHD.dhdSetWristJointTorques.q1 = q1
            MockDHD.dhdSetWristJointTorques.q2 = q2

            return MockDHD.dhdSetWristJointTorques.ret

    class dhdSetForceAndWristJointTorques:
        argtypes = [
            c_double, c_double, c_double, c_double, c_double, c_double, c_byte
        ]
        restype = c_int

        fx = 0
        fy = 0
        fz = 0

        q0 = 0
        q1 = 0
        q2 = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(fx, fy, fz, q0, q1, q2, ID):
            MockDHD.dhdSetForceAndWristJointTorques.ID = ID

            MockDHD.dhdSetForceAndWristJointTorques.fx = fx
            MockDHD.dhdSetForceAndWristJointTorques.fy = fy
            MockDHD.dhdSetForceAndWristJointTorques.fz = fz

            MockDHD.dhdSetForceAndWristJointTorques.q0 = q0
            MockDHD.dhdSetForceAndWristJointTorques.q1 = q1
            MockDHD.dhdSetForceAndWristJointTorques.q2 = q2

            return MockDHD.dhdSetForceAndWristJointTorques.ret


    class dhdSetForceAndWristJointTorquesAndGripperForce:
        argtypes = [
            c_double, c_double, c_double,
            c_double, c_double, c_double,
            c_double, c_byte
        ]
        restype = c_int

        fx: float = 0
        fy: float = 0
        fz: float = 0

        fg: float = 0

        q0: float = 0
        q1: float = 0
        q2: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(fx, fy, fz, q0, q1, q2, fg, ID):
            MockDHD.dhdSetForceAndWristJointTorquesAndGripperForce.ID = ID

            MockDHD.dhdSetForceAndWristJointTorquesAndGripperForce.fx = fx
            MockDHD.dhdSetForceAndWristJointTorquesAndGripperForce.fy = fy
            MockDHD.dhdSetForceAndWristJointTorquesAndGripperForce.fz = fz

            MockDHD.dhdSetForceAndWristJointTorquesAndGripperForce.q0 = q0
            MockDHD.dhdSetForceAndWristJointTorquesAndGripperForce.q1 = q1
            MockDHD.dhdSetForceAndWristJointTorquesAndGripperForce.q2 = q2

            MockDHD.dhdSetForceAndWristJointTorquesAndGripperForce.fg = fg

            return MockDHD.dhdSetForceAndWristJointTorquesAndGripperForce.ret

    class dhdWristEncodersToJointAngles:
        argtypes = [
            c_int, c_int, c_int,
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        enc0: int = 0
        enc1: int = 0
        enc2: int = 0

        j0: float = 0
        j1: float = 0
        j2: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enc0, enc1, enc2, j0, j1, j2, ID):
            MockDHD.dhdWristEncodersToJointAngles.ID = ID

            MockDHD.dhdWristEncodersToJointAngles.enc0 = enc0
            MockDHD.dhdWristEncodersToJointAngles.enc1 = enc1
            MockDHD.dhdWristEncodersToJointAngles.enc2 = enc2

            j0.contents.value = MockDHD.dhdWristEncodersToJointAngles.j0
            j1.contents.value = MockDHD.dhdWristEncodersToJointAngles.j1
            j2.contents.value = MockDHD.dhdWristEncodersToJointAngles.j2

            return MockDHD.dhdWristEncodersToJointAngles.ret

    class dhdWristJointAnglesToEncoders:
        argtypes = [
            c_double, c_double, c_double,
            POINTER(c_int), POINTER(c_int), POINTER(c_int), c_byte
        ]
        restype = c_int

        enc0 = 0
        enc1 = 0
        enc2 = 0

        j0 = 0
        j1 = 0
        j2 = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(j0, j1, j2, enc0, enc1, enc2, ID):
            MockDHD.dhdWristJointAnglesToEncoders.ID = ID

            MockDHD.dhdWristJointAnglesToEncoders.j0 = j0
            MockDHD.dhdWristJointAnglesToEncoders.j1 = j1
            MockDHD.dhdWristJointAnglesToEncoders.j2 = j2

            enc0.contents.value = MockDHD.dhdWristJointAnglesToEncoders.enc0
            enc1.contents.value = MockDHD.dhdWristJointAnglesToEncoders.enc1
            enc2.contents.value = MockDHD.dhdWristJointAnglesToEncoders.enc2

            return MockDHD.dhdWristJointAnglesToEncoders.ret


    class dhdGetJointAngles:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        joint_angles = array('d', (0.0 for _ in range(MAX_DOF)))

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(joint_angles, ID):
            MockDHD.dhdGetJointAngles.ID = ID

            for i in range(MAX_DOF):
                joint_angles[i] = MockDHD.dhdGetJointAngles.joint_angles[i]

            return MockDHD.dhdGetJointAngles.ret


    class dhdGetJointVelocities:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        joint_v = array('d', (0.0 for _ in range(MAX_DOF)))

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(joint_v, ID):
            MockDHD.dhdGetJointVelocities.ID = ID

            for i in range(MAX_DOF):
                joint_v[i] = MockDHD.dhdGetJointVelocities.joint_v[i]

            return MockDHD.dhdGetJointVelocities.ret

    class dhdGetEncVelocities:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        enc_v = array('d', (0.0 for _ in range(MAX_DOF)))

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enc_v, ID):
            MockDHD.dhdGetEncVelocities.ID = ID

            for i in range(MAX_DOF):
                enc_v[i] = MockDHD.dhdGetEncVelocities.enc_v[i]

            return MockDHD.dhdGetEncVelocities.ret

    class dhdJointAnglesToInertiaMatrix:
        argtypes = [POINTER(c_double), POINTER(c_double), c_byte]
        restype = c_int

        joint_angles = [0.0] * MAX_DOF
        inertia_matrix = [[0.0] * 6] * 6

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(joint_angles, inertia_matrix, ID):
            MockDHD.dhdJointAnglesToInertiaMatrix.ID = ID

            for i in range(MAX_DOF):
                MockDHD.dhdJointAnglesToInertiaMatrix.joint_angles[i] = joint_angles[i]

            for i in range(6):
                for j in range(6):
                    inertia_matrix[6 * i + j] = MockDHD.dhdJointAnglesToInertiaMatrix.inertia_matrix[i][j]


            return MockDHD.dhdJointAnglesToInertiaMatrix.ret

    class dhdJointAnglesToGravityJointTorques:
        argtypes = [POINTER(c_double), POINTER(c_double), c_ubyte, c_byte]
        restype = c_int

        joint_angles = [0.0] * MAX_DOF
        q = [0.0] * MAX_DOF
        mask = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(joint_angles, q, mask, ID):
            MockDHD.dhdJointAnglesToGravityJointTorques.ID = ID

            MockDHD.dhdJointAnglesToGravityJointTorques.mask = mask

            for i in range(MAX_DOF):
                 MockDHD.dhdJointAnglesToGravityJointTorques.joint_angles[i] = joint_angles[i]

            for i in range(MAX_DOF):
                q[i] = MockDHD.dhdJointAnglesToGravityJointTorques.q[i]

            return MockDHD.dhdJointAnglesToGravityJointTorques.ret

    class dhdSetComMode:
        argtypes = [c_int, c_byte]
        restype = c_int

        mode = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(mode, ID):
            MockDHD.dhdSetComMode.ID = ID
            MockDHD.dhdSetComMode.mode = mode

            return MockDHD.dhdSetComMode.ret

    class dhdSetComModePriority:
        argtypes = [c_int, c_byte]
        restype = c_int

        priority = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(priority, ID):
            MockDHD.dhdSetComModePriority.ID = ID
            MockDHD.dhdSetComModePriority.priority = priority

            return MockDHD.dhdSetComModePriority.ret

    class dhdSetWatchdog:
        argtypes = [c_ubyte, c_byte]
        restype = c_int

        duration = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(duration, ID):
            MockDHD.dhdSetWatchdog.ID = ID
            MockDHD.dhdSetWatchdog.duration = duration

            return MockDHD.dhdSetWatchdog.ret

    class dhdGetWatchdog:
        argtypes = [POINTER(c_ubyte), c_byte]
        restype = c_int
        duration = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(duration, ID):
            MockDHD.dhdGetWatchdog.ID = ID
            duration.contents.value = MockDHD.dhdGetWatchdog.duration

            return MockDHD.dhdGetWatchdog.ret

    class dhdGetEncRange:
        argtypes = [POINTER(c_int), POINTER(c_int), c_byte]
        restype = c_int

        enc_min = [0] * MAX_DOF
        enc_max = [0] * MAX_DOF

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enc_min, enc_max, ID):
            MockDHD.dhdGetEncRange.ID = ID

            for i in range(MAX_DOF):
                enc_min[i] = MockDHD.dhdGetEncRange.enc_min[i]
                enc_max[i] = MockDHD.dhdGetEncRange.enc_max[i]

            return MockDHD.dhdGetEncRange.ret

    class dhdGetJointAngleRange:
        argtypes = [POINTER(c_double), POINTER(c_double), c_byte]
        restype = c_int

        jmin = [0] * MAX_DOF
        jmax = [0] * MAX_DOF

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(jmin, jmax, ID):
            MockDHD.dhdGetJointAngleRange.ID = ID

            for i in range(MAX_DOF):
                jmin[i] = MockDHD.dhdGetJointAngleRange.jmin[i]
                jmax[i] = MockDHD.dhdGetJointAngleRange.jmax[i]

            return MockDHD.dhdGetJointAngleRange.ret

    class dhdControllerSetDevice:
        argtypes = [c_int, c_byte]
        restype = c_int

        device = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(device, ID):
            MockDHD.dhdControllerSetDevice.ID = ID
            MockDHD.dhdControllerSetDevice.device = device

            return MockDHD.dhdControllerSetDevice.ret

    class dhdReadConfigFromFile:
        argtypes = [c_char_p, c_byte]
        restype = c_int

        filename = ""

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(filename, ID):
            MockDHD.dhdReadConfigFromFile.ID = ID
            MockDHD.dhdReadConfigFromFile.filename = filename.decode('utf-8')

            return MockDHD.dhdReadConfigFromFile.ret

    class dhdDeltaGravityJointTorques:
        argtypes = [
            c_double, c_double, c_double,
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        j0: float = 0.
        j1: float = 0.
        j2: float = 0.

        q0: float = 0.
        q1: float = 0.
        q2: float = 0.

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(j0, j1, j2, q0, q1, q2, ID):
            MockDHD.dhdDeltaGravityJointTorques.ID = ID

            MockDHD.dhdDeltaGravityJointTorques.j0 = j0
            MockDHD.dhdDeltaGravityJointTorques.j1 = j1
            MockDHD.dhdDeltaGravityJointTorques.j2 = j2

            q0.contents.value = MockDHD.dhdDeltaGravityJointTorques.q0
            q1.contents.value = MockDHD.dhdDeltaGravityJointTorques.q1
            q2.contents.value = MockDHD.dhdDeltaGravityJointTorques.q2

            return MockDHD.dhdDeltaGravityJointTorques.ret

    class dhdWristGravityJointTorques:
        argtypes = [
            c_double, c_double, c_double,
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        j0: float = 0.
        j1: float = 0.
        j2: float = 0.

        q0: float = 0.
        q1: float = 0.
        q2: float = 0.

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(j0, j1, j2, q0, q1, q2, ID):
            MockDHD.dhdWristGravityJointTorques.ID = ID

            MockDHD.dhdWristGravityJointTorques.j0 = j0
            MockDHD.dhdWristGravityJointTorques.j1 = j1
            MockDHD.dhdWristGravityJointTorques.j2 = j2

            q0.contents.value = MockDHD.dhdWristGravityJointTorques.q0
            q1.contents.value = MockDHD.dhdWristGravityJointTorques.q1
            q2.contents.value = MockDHD.dhdWristGravityJointTorques.q2

            return MockDHD.dhdWristGravityJointTorques.ret

class TestExpertSDK(unittest.TestCase):
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

    def test_enableExpertMode(self):
        self.assertSignaturesEqual(
            libdhd.dhdEnableExpertMode, MockDHD.dhdEnableExpertMode
        )

        libdhd.dhdEnableExpertMode = ( # type: ignore
            MockDHD.dhdEnableExpertMode.mock
        )

        dhd.expert.enableExpertMode()
        self.assertTrue(MockDHD.dhdEnableExpertMode.enable)

    def test_disableExpertMode(self):
        self.assertSignaturesEqual(
            libdhd.dhdDisableExpertMode, MockDHD.dhdDisableExpertMode
        )

        libdhd.dhdDisableExpertMode = ( # type: ignore
            MockDHD.dhdDisableExpertMode.mock
        )

        dhd.expert.disableExpertMode()
        self.assertFalse(MockDHD.dhdDisableExpertMode.enable)

    def test_preset(self):
        self.assertSignaturesEqual(
            libdhd.dhdPreset, MockDHD.dhdPreset
        )

        libdhd.dhdPreset = MockDHD.dhdPreset.mock  # type: ignore

        val = [0] * MAX_DOF
        mask = 0

        for _ in range(100):
            for i in range(MAX_DOF):
                val[i] = randint(0, 100)

            mask = randint(0, 100)

            dhd.expert.preset(val, mask)

            self.assertSequenceEqual(val, MockDHD.dhdPreset.val)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.preset(val, 0, ID),
            MockDHD.dhdPreset
        )

        self.assertRetImpl(
            lambda: dhd.expert.preset(val),
            MockDHD.dhdPreset
        )

    def test_setTimeGuard(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetTimeGuard,
            MockDHD.dhdSetTimeGuard
        )

        libdhd.dhdSetTimeGuard = (  # type: ignore
            MockDHD.dhdSetTimeGuard.mock
        )

        for _ in range(100):
            value = randint(0, 100)
            dhd.expert.setTimeGuard(value)

            self.assertEqual(
                value, MockDHD.dhdSetTimeGuard.timeguard_us
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.setTimeGuard(0, ID),
            MockDHD.dhdSetTimeGuard
        )

        self.assertRetImpl(
            lambda: dhd.expert.setTimeGuard(0),
            MockDHD.dhdSetTimeGuard
        )

    def test_setVelocityThreshold(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetVelocityThreshold,
            MockDHD.dhdSetVelocityThreshold
        )

        libdhd.dhdSetVelocityThreshold = (  # type: ignore
            MockDHD.dhdSetVelocityThreshold.mock
        )

        for _ in range(100):
            value = randint(0, 100)
            dhd.expert.setVelocityThreshold(value)

            self.assertEqual(
                value, MockDHD.dhdSetVelocityThreshold.thresh
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.setVelocityThreshold(0, ID),
            MockDHD.dhdSetVelocityThreshold
        )

        self.assertRetImpl(
            lambda: dhd.expert.setVelocityThreshold(0),
            MockDHD.dhdSetVelocityThreshold
        )

    def test_getVelocityThreshold(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetVelocityThreshold,
            MockDHD.dhdGetVelocityThreshold
        )

        libdhd.dhdGetVelocityThreshold = (  # type: ignore
            MockDHD.dhdGetVelocityThreshold.mock
        )

        for _ in range(100):
            MockDHD.dhdGetVelocityThreshold.thresh = randint(0, 100)

            self.assertEqual(
                dhd.expert.getVelocityThreshold(),
                MockDHD.dhdGetVelocityThreshold.thresh
            )

        self.assertIDImpl(
            dhd.expert.getVelocityThreshold,
            MockDHD.dhdGetVelocityThreshold
        )

        MockDHD.dhdGetVelocityThreshold.ret = -1
        self.assertEqual(dhd.expert.getVelocityThreshold(), -1)


    def test_updateEncoders(self):
        self.assertSignaturesEqual(
            libdhd.dhdUpdateEncoders, MockDHD.dhdEnableExpertMode
        )

        libdhd.dhdUpdateEncoders = ( # type: ignore
            MockDHD.dhdUpdateEncoders.mock
        )

        self.assertIDImpl(
            dhd.expert.updateEncoders,
            MockDHD.dhdUpdateEncoders
        )

        self.assertRetImpl(
            dhd.expert.updateEncoders,
            MockDHD.dhdUpdateEncoders
        )

    def test_getDeltaEncoders(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetDeltaEncoders, MockDHD.dhdGetDeltaEncoders
        )

        libdhd.dhdGetDeltaEncoders = (  # type: ignore
            MockDHD.dhdGetDeltaEncoders.mock
        )
        out = [0, 0, 0]

        for _ in range(100):
            MockDHD.dhdGetDeltaEncoders.enc0 = randint(0, 100)
            MockDHD.dhdGetDeltaEncoders.enc1 = randint(0, 100)
            MockDHD.dhdGetDeltaEncoders.enc2 = randint(0, 100)

            dhd.expert.getDeltaEncoders(out)

            self.assertEqual(out[0], MockDHD.dhdGetDeltaEncoders.enc0)
            self.assertEqual(out[1], MockDHD.dhdGetDeltaEncoders.enc1)
            self.assertEqual(out[2], MockDHD.dhdGetDeltaEncoders.enc2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.getDeltaEncoders(out, ID),
            MockDHD.dhdGetDeltaEncoders
        )
        self.assertRetImpl(
            lambda: dhd.expert.getDeltaEncoders(out),
            MockDHD.dhdGetDeltaEncoders
        )

    def test_getDeltaEncodersDirect(self):
        libdhd.dhdGetDeltaEncoders = (  # type: ignore
            MockDHD.dhdGetDeltaEncoders.mock
        )
        out = containers.Enc3()

        for _ in range(100):
            MockDHD.dhdGetDeltaEncoders.enc0 = randint(0, 100)
            MockDHD.dhdGetDeltaEncoders.enc1 = randint(0, 100)
            MockDHD.dhdGetDeltaEncoders.enc2 = randint(0, 100)

            dhd.expert.direct.getDeltaEncoders(out)

            self.assertEqual(out[0], MockDHD.dhdGetDeltaEncoders.enc0)
            self.assertEqual(out[1], MockDHD.dhdGetDeltaEncoders.enc1)
            self.assertEqual(out[2], MockDHD.dhdGetDeltaEncoders.enc2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.getDeltaEncoders(out, ID),
            MockDHD.dhdGetDeltaEncoders
        )
        self.assertRetImpl(
            lambda: dhd.expert.direct.getDeltaEncoders(out),
            MockDHD.dhdGetDeltaEncoders
        )

    def test_getWristEncoders(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetWristEncoders, MockDHD.dhdGetWristEncoders
        )

        libdhd.dhdGetWristEncoders = (  # type: ignore
            MockDHD.dhdGetWristEncoders.mock
        )
        out = [0, 0, 0]

        for _ in range(100):
            MockDHD.dhdGetWristEncoders.enc0 = randint(0, 100)
            MockDHD.dhdGetWristEncoders.enc1 = randint(0, 100)
            MockDHD.dhdGetWristEncoders.enc2 = randint(0, 100)

            dhd.expert.getWristEncoders(out)

            self.assertEqual(out[0], MockDHD.dhdGetWristEncoders.enc0)
            self.assertEqual(out[1], MockDHD.dhdGetWristEncoders.enc1)
            self.assertEqual(out[2], MockDHD.dhdGetWristEncoders.enc2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.getWristEncoders(out, ID),
            MockDHD.dhdGetWristEncoders
        )
        self.assertRetImpl(
            lambda: dhd.expert.getWristEncoders(out),
            MockDHD.dhdGetWristEncoders
        )

    def test_getWristEncodersDirect(self):
        libdhd.dhdGetWristEncoders = (  # type: ignore
            MockDHD.dhdGetWristEncoders.mock
        )
        out = containers.Enc3()

        for _ in range(100):
            MockDHD.dhdGetWristEncoders.enc0 = randint(0, 100)
            MockDHD.dhdGetWristEncoders.enc1 = randint(0, 100)
            MockDHD.dhdGetWristEncoders.enc2 = randint(0, 100)

            dhd.expert.direct.getWristEncoders(out)

            self.assertEqual(out[0], MockDHD.dhdGetWristEncoders.enc0)
            self.assertEqual(out[1], MockDHD.dhdGetWristEncoders.enc1)
            self.assertEqual(out[2], MockDHD.dhdGetWristEncoders.enc2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.getWristEncoders(out, ID),
            MockDHD.dhdGetWristEncoders
        )
        self.assertRetImpl(
            lambda: dhd.expert.direct.getWristEncoders(out),
            MockDHD.dhdGetWristEncoders
        )

    def test_getGripperEncoder(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetGripperEncoder,
            MockDHD.dhdGetGripperEncoder
        )

        libdhd.dhdGetGripperEncoder = (  # type: ignore
            MockDHD.dhdGetGripperEncoder.mock
        )

        out = c_int()

        for _ in range(100):
            MockDHD.dhdGetGripperEncoder.enc = randint(0, 100)

            dhd.expert.getGripperEncoder(out)
            self.assertEqual(out.value, MockDHD.dhdGetGripperEncoder.enc)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.getGripperEncoder(out, ID),
            MockDHD.dhdGetGripperEncoder
        )

        self.assertRetImpl(
            lambda: dhd.expert.getGripperEncoder(out),
            MockDHD.dhdGetGripperEncoder
        )

    def test_getEncoder(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetEncoder,
            MockDHD.dhdGetEncoder
        )

        libdhd.dhdGetEncoder = (  # type: ignore
            MockDHD.dhdGetEncoder.mock
        )

        for _ in range(100):
            index = randint(0, 100)
            MockDHD.dhdGetEncoder.ret = randint(0, 100)

            self.assertEqual(
                dhd.expert.getEncoder(index),
                MockDHD.dhdGetEncoder.ret
            )

            self.assertEqual(
                index,
                MockDHD.dhdGetEncoder.index
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.getEncoder(0, ID),
            MockDHD.dhdGetEncoder
        )

    def test_setMotor(self):
        self.assertSignaturesEqual(libdhd.dhdSetMotor, MockDHD.dhdSetMotor)

        libdhd.dhdSetMotor = MockDHD.dhdSetMotor.mock  # type: ignore

        for _ in range(100):
            index = randint(0, 100)
            output = randint(0, 100)

            dhd.expert.setMotor(index, output)

            self.assertEqual(index, MockDHD.dhdSetMotor.index)
            self.assertEqual(output, MockDHD.dhdSetMotor.output)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.setMotor(0, 0, ID),
            MockDHD.dhdSetMotor
        )

        self.assertRetImpl(
            lambda: dhd.expert.setMotor(0, 0),
            MockDHD.dhdSetMotor
        )


    def test_setWristMotor(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetWristMotor, MockDHD.dhdSetWristMotor
        )

        libdhd.dhdSetWristMotor = (  # type: ignore
            MockDHD.dhdSetWristMotor.mock
        )

        mot = [0, 0, 0]
        for _ in range(100):
            mot[0] = randint(0, 100)
            mot[1] = randint(0, 100)
            mot[2] = randint(0, 100)

            dhd.expert.setWristMotor(mot)

            self.assertEqual(mot[0], MockDHD.dhdSetWristMotor.mot0)
            self.assertEqual(mot[1], MockDHD.dhdSetWristMotor.mot1)
            self.assertEqual(mot[2], MockDHD.dhdSetWristMotor.mot2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.setWristMotor(mot, ID),
            MockDHD.dhdSetWristMotor
        )

        self.assertRetImpl(
            lambda: dhd.expert.setWristMotor(mot),
            MockDHD.dhdSetWristMotor
        )

    def test_setGripperMotor(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetGripperMotor, MockDHD.dhdSetGripperMotor
        )

        libdhd.dhdSetGripperMotor = (  # type: ignore
            MockDHD.dhdSetGripperMotor.mock
        )

        mot = 0
        for _ in range(100):
            mot = randint(0, 100)

            dhd.expert.setGripperMotor(mot)

            self.assertEqual(mot, MockDHD.dhdSetGripperMotor.mot)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.setGripperMotor(mot, ID),
            MockDHD.dhdSetGripperMotor
        )

        self.assertRetImpl(
            lambda: dhd.expert.setGripperMotor(mot),
            MockDHD.dhdSetGripperMotor
        )

    def test_setDeltaMotor(self):
        libdhd.dhdSetDeltaMotor = (  # type: ignore
            MockDHD.dhdSetDeltaMotor.mock
        )

        mot = [0, 0, 0]
        for _ in range(100):
            mot[0] = randint(0, 100)
            mot[1] = randint(0, 100)
            mot[2] = randint(0, 100)

            dhd.expert.setDeltaMotor(mot)

            self.assertEqual(mot[0], MockDHD.dhdSetDeltaMotor.mot0)
            self.assertEqual(mot[1], MockDHD.dhdSetDeltaMotor.mot1)
            self.assertEqual(mot[2], MockDHD.dhdSetDeltaMotor.mot2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.setDeltaMotor(mot, ID),
            MockDHD.dhdSetDeltaMotor
        )

        self.assertRetImpl(
            lambda: dhd.expert.setDeltaMotor(mot),
            MockDHD.dhdSetDeltaMotor
        )

    def test_deltaEncoderToPosition(self):
        self.assertSignaturesEqual(
            libdhd.dhdDeltaEncoderToPosition,
            MockDHD.dhdDeltaEncoderToPosition
        )

        libdhd.dhdDeltaEncoderToPosition = (  # type: ignore
            MockDHD.dhdDeltaEncoderToPosition.mock
        )

        enc = [0, 0, 0]
        out = [0.0, 0.0, 0.0]

        for _ in range(100):
            MockDHD.dhdDeltaEncoderToPosition.px = random()
            MockDHD.dhdDeltaEncoderToPosition.py = random()
            MockDHD.dhdDeltaEncoderToPosition.pz = random()

            enc[0] = randint(0, 100)
            enc[1] = randint(0, 100)
            enc[2] = randint(0, 100)

            dhd.expert.deltaEncoderToPosition(enc, out)

            self.assertAlmostEqual(
                out[0], MockDHD.dhdDeltaEncoderToPosition.px
            )
            self.assertAlmostEqual(
                out[1], MockDHD.dhdDeltaEncoderToPosition.py
            )
            self.assertAlmostEqual(
                out[2], MockDHD.dhdDeltaEncoderToPosition.pz
            )

            self.assertEqual(enc[0], MockDHD.dhdDeltaEncoderToPosition.enc0)
            self.assertEqual(enc[1], MockDHD.dhdDeltaEncoderToPosition.enc1)
            self.assertEqual(enc[2], MockDHD.dhdDeltaEncoderToPosition.enc2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.deltaEncoderToPosition(enc, out, ID),
            MockDHD.dhdDeltaEncoderToPosition
        )

        self.assertRetImpl(
            lambda: dhd.expert.deltaEncoderToPosition(enc, out),
            MockDHD.dhdDeltaEncoderToPosition
        )

    def test_deltaEncoderToPositionDirect(self):
        libdhd.dhdDeltaEncoderToPosition = (  # type: ignore
            MockDHD.dhdDeltaEncoderToPosition.mock
        )

        enc = containers.Enc3()
        out = containers.Vector3()

        for _ in range(100):
            MockDHD.dhdDeltaEncoderToPosition.px = random()
            MockDHD.dhdDeltaEncoderToPosition.py = random()
            MockDHD.dhdDeltaEncoderToPosition.pz = random()

            enc[0] = randint(0, 100)
            enc[1] = randint(0, 100)
            enc[2] = randint(0, 100)

            dhd.expert.direct.deltaEncoderToPosition(enc, out)

            self.assertAlmostEqual(
                out[0], MockDHD.dhdDeltaEncoderToPosition.px
            )
            self.assertAlmostEqual(
                out[1], MockDHD.dhdDeltaEncoderToPosition.py
            )
            self.assertAlmostEqual(
                out[2], MockDHD.dhdDeltaEncoderToPosition.pz
            )

            self.assertEqual(enc[0], MockDHD.dhdDeltaEncoderToPosition.enc0)
            self.assertEqual(enc[1], MockDHD.dhdDeltaEncoderToPosition.enc1)
            self.assertEqual(enc[2], MockDHD.dhdDeltaEncoderToPosition.enc2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.deltaEncoderToPosition(enc, out, ID),
            MockDHD.dhdDeltaEncoderToPosition
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.deltaEncoderToPosition(enc, out),
            MockDHD.dhdDeltaEncoderToPosition
        )

    def test_deltaPositionToEncoder(self):
        self.assertSignaturesEqual(
            libdhd.dhdDeltaPositionToEncoder,
            MockDHD.dhdDeltaPositionToEncoder
        )

        libdhd.dhdDeltaPositionToEncoder = (  # type: ignore
            MockDHD.dhdDeltaPositionToEncoder.mock
        )

        pos = [0.0, 0.0, 0.0]
        out = [0, 0, 0]

        for _ in range(100):
            MockDHD.dhdDeltaPositionToEncoder.enc0 = randint(0, 100)
            MockDHD.dhdDeltaPositionToEncoder.enc1 = randint(0, 100)
            MockDHD.dhdDeltaPositionToEncoder.enc2 = randint(0, 100)

            pos[0] = random()
            pos[1] = random()
            pos[2] = random()

            dhd.expert.deltaPositionToEncoder(pos, out)

            self.assertAlmostEqual(
                pos[0], MockDHD.dhdDeltaPositionToEncoder.px
            )
            self.assertAlmostEqual(
                pos[1], MockDHD.dhdDeltaPositionToEncoder.py
            )
            self.assertAlmostEqual(
                pos[2], MockDHD.dhdDeltaPositionToEncoder.pz
            )

            self.assertEqual(out[0], MockDHD.dhdDeltaPositionToEncoder.enc0)
            self.assertEqual(out[1], MockDHD.dhdDeltaPositionToEncoder.enc1)
            self.assertEqual(out[2], MockDHD.dhdDeltaPositionToEncoder.enc2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.deltaPositionToEncoder(pos, out, ID),
            MockDHD.dhdDeltaPositionToEncoder
        )

        self.assertRetImpl(
            lambda: dhd.expert.deltaPositionToEncoder(pos, out),
            MockDHD.dhdDeltaPositionToEncoder
        )

    def test_deltaPositionToEncoderDirect(self):
        libdhd.dhdDeltaPositionToEncoder = (  # type: ignore
            MockDHD.dhdDeltaPositionToEncoder.mock
        )

        pos = containers.Vector3()
        out = containers.Enc3()

        for _ in range(100):
            MockDHD.dhdDeltaPositionToEncoder.enc0 = randint(0, 100)
            MockDHD.dhdDeltaPositionToEncoder.enc1 = randint(0, 100)
            MockDHD.dhdDeltaPositionToEncoder.enc2 = randint(0, 100)

            pos[0] = random()
            pos[1] = random()
            pos[2] = random()

            dhd.expert.direct.deltaPositionToEncoder(pos, out)

            self.assertAlmostEqual(
                pos[0], MockDHD.dhdDeltaPositionToEncoder.px
            )
            self.assertAlmostEqual(
                pos[1], MockDHD.dhdDeltaPositionToEncoder.py
            )
            self.assertAlmostEqual(
                pos[2], MockDHD.dhdDeltaPositionToEncoder.pz
            )

            self.assertEqual(out[0], MockDHD.dhdDeltaPositionToEncoder.enc0)
            self.assertEqual(out[1], MockDHD.dhdDeltaPositionToEncoder.enc1)
            self.assertEqual(out[2], MockDHD.dhdDeltaPositionToEncoder.enc2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.deltaPositionToEncoder(pos, out, ID),
            MockDHD.dhdDeltaPositionToEncoder
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.deltaPositionToEncoder(pos, out),
            MockDHD.dhdDeltaPositionToEncoder
        )

    def test_deltaMotorToForce(self):
        self.assertSignaturesEqual(
            libdhd.dhdDeltaMotorToForce,
            MockDHD.dhdDeltaMotorToForce
        )

        libdhd.dhdDeltaMotorToForce = (  # type: ignore
            MockDHD.dhdDeltaMotorToForce.mock
        )

        mot = [0, 0, 0]
        enc = [0, 0, 0]

        out = [0.0, 0.0, 0.0]

        for _ in range(100):
            MockDHD.dhdDeltaMotorToForce.fx = random()
            MockDHD.dhdDeltaMotorToForce.fy = random()
            MockDHD.dhdDeltaMotorToForce.fz = random()

            mot[0] = randint(0, 100)
            mot[1] = randint(0, 100)
            mot[2] = randint(0, 100)

            enc[0] = randint(0, 100)
            enc[1] = randint(0, 100)
            enc[2] = randint(0, 100)

            dhd.expert.deltaMotorToForce(mot, enc, out)

            self.assertAlmostEqual(
                out[0], MockDHD.dhdDeltaMotorToForce.fx
            )
            self.assertAlmostEqual(
                out[1], MockDHD.dhdDeltaMotorToForce.fy
            )
            self.assertAlmostEqual(
                out[2], MockDHD.dhdDeltaMotorToForce.fz
            )

            self.assertEqual(mot[0], MockDHD.dhdDeltaMotorToForce.mot0)
            self.assertEqual(mot[1], MockDHD.dhdDeltaMotorToForce.mot1)
            self.assertEqual(mot[2], MockDHD.dhdDeltaMotorToForce.mot2)

            self.assertEqual(enc[0], MockDHD.dhdDeltaMotorToForce.enc0)
            self.assertEqual(enc[1], MockDHD.dhdDeltaMotorToForce.enc1)
            self.assertEqual(enc[2], MockDHD.dhdDeltaMotorToForce.enc2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.deltaMotorToForce(mot, enc, out, ID),
            MockDHD.dhdDeltaMotorToForce
        )

        self.assertRetImpl(
            lambda: dhd.expert.deltaMotorToForce(mot, enc, out),
            MockDHD.dhdDeltaMotorToForce
        )

    def test_deltaMotorToForceDirect(self):
        libdhd.dhdDeltaMotorToForce = (  # type: ignore
            MockDHD.dhdDeltaMotorToForce.mock
        )

        mot = containers.Mot3()
        enc = containers.Enc3()

        out = containers.Vector3()

        for _ in range(100):
            MockDHD.dhdDeltaMotorToForce.fx = random()
            MockDHD.dhdDeltaMotorToForce.fy = random()
            MockDHD.dhdDeltaMotorToForce.fz = random()

            mot[0] = randint(0, 100)
            mot[1] = randint(0, 100)
            mot[2] = randint(0, 100)

            enc[0] = randint(0, 100)
            enc[1] = randint(0, 100)
            enc[2] = randint(0, 100)

            dhd.expert.direct.deltaMotorToForce(mot, enc, out)

            self.assertAlmostEqual(
                out[0], MockDHD.dhdDeltaMotorToForce.fx
            )
            self.assertAlmostEqual(
                out[1], MockDHD.dhdDeltaMotorToForce.fy
            )
            self.assertAlmostEqual(
                out[2], MockDHD.dhdDeltaMotorToForce.fz
            )

            self.assertEqual(mot[0], MockDHD.dhdDeltaMotorToForce.mot0)
            self.assertEqual(mot[1], MockDHD.dhdDeltaMotorToForce.mot1)
            self.assertEqual(mot[2], MockDHD.dhdDeltaMotorToForce.mot2)

            self.assertEqual(enc[0], MockDHD.dhdDeltaMotorToForce.enc0)
            self.assertEqual(enc[1], MockDHD.dhdDeltaMotorToForce.enc1)
            self.assertEqual(enc[2], MockDHD.dhdDeltaMotorToForce.enc2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.deltaMotorToForce(
                mot, enc, out, ID
            ),
            MockDHD.dhdDeltaMotorToForce
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.deltaMotorToForce(mot, enc, out),
            MockDHD.dhdDeltaMotorToForce
        )

    def test_deltaForceToMotor(self):
        self.assertSignaturesEqual(
            libdhd.dhdDeltaForceToMotor,
            MockDHD.dhdDeltaForceToMotor
        )

        libdhd.dhdDeltaForceToMotor = (  # type: ignore
            MockDHD.dhdDeltaForceToMotor.mock
        )

        f = [0.0, 0.0, 0.0]
        enc = [0, 0, 0]

        out = [0, 0, 0]

        for _ in range(100):
            MockDHD.dhdDeltaForceToMotor.mot0 = randint(0, 100)
            MockDHD.dhdDeltaForceToMotor.mot1 = randint(0, 100)
            MockDHD.dhdDeltaForceToMotor.mot2 = randint(0, 100)

            f[0] = random()
            f[1] = random()
            f[2] = random()

            enc[0] = randint(0, 100)
            enc[1] = randint(0, 100)
            enc[2] = randint(0, 100)

            dhd.expert.deltaForceToMotor(f, enc, out)

            self.assertAlmostEqual(
                f[0], MockDHD.dhdDeltaForceToMotor.fx
            )
            self.assertAlmostEqual(
                f[1], MockDHD.dhdDeltaForceToMotor.fy
            )
            self.assertAlmostEqual(
                f[2], MockDHD.dhdDeltaForceToMotor.fz
            )

            self.assertEqual(out[0], MockDHD.dhdDeltaForceToMotor.mot0)
            self.assertEqual(out[1], MockDHD.dhdDeltaForceToMotor.mot1)
            self.assertEqual(out[2], MockDHD.dhdDeltaForceToMotor.mot2)

            self.assertEqual(enc[0], MockDHD.dhdDeltaForceToMotor.enc0)
            self.assertEqual(enc[1], MockDHD.dhdDeltaForceToMotor.enc1)
            self.assertEqual(enc[2], MockDHD.dhdDeltaForceToMotor.enc2)


        self.assertIDImpl(
            lambda ID = -1: dhd.expert.deltaForceToMotor(f, enc, out, ID),
            MockDHD.dhdDeltaForceToMotor
        )

        self.assertRetImpl(
            lambda: dhd.expert.deltaForceToMotor(f, enc, out),
            MockDHD.dhdDeltaForceToMotor
        )

    def test_deltaMotorToForceDirectDirect(self):
        libdhd.dhdDeltaForceToMotor = (  # type: ignore
            MockDHD.dhdDeltaForceToMotor.mock
        )

        f = [0.0, 0.0, 0.0]
        enc = [0, 0, 0]

        out = containers.Mot3()

        for _ in range(100):
            MockDHD.dhdDeltaForceToMotor.mot0 = randint(0, 100)
            MockDHD.dhdDeltaForceToMotor.mot1 = randint(0, 100)
            MockDHD.dhdDeltaForceToMotor.mot2 = randint(0, 100)

            f[0] = random()
            f[1] = random()
            f[2] = random()

            enc[0] = randint(0, 100)
            enc[1] = randint(0, 100)
            enc[2] = randint(0, 100)

            dhd.expert.direct.deltaForceToMotor(
                f, enc, out
            )

            self.assertAlmostEqual(
                f[0], MockDHD.dhdDeltaForceToMotor.fx
            )
            self.assertAlmostEqual(
                f[1], MockDHD.dhdDeltaForceToMotor.fy
            )
            self.assertAlmostEqual(
                f[2], MockDHD.dhdDeltaForceToMotor.fz
            )

            self.assertEqual(out[0], MockDHD.dhdDeltaForceToMotor.mot0)
            self.assertEqual(out[1], MockDHD.dhdDeltaForceToMotor.mot1)
            self.assertEqual(out[2], MockDHD.dhdDeltaForceToMotor.mot2)

            self.assertEqual(enc[0], MockDHD.dhdDeltaForceToMotor.enc0)
            self.assertEqual(enc[1], MockDHD.dhdDeltaForceToMotor.enc1)
            self.assertEqual(enc[2], MockDHD.dhdDeltaForceToMotor.enc2)


        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.deltaForceToMotor(
                f, enc, out, ID
            ),
            MockDHD.dhdDeltaForceToMotor
        )

        self.assertRetImpl(
            lambda: dhd.expert.deltaForceToMotor(f, enc, out),
            MockDHD.dhdDeltaForceToMotor
        )

    def test_wristEncoderToOrientation(self):
        self.assertSignaturesEqual(
            libdhd.dhdWristEncoderToOrientation,
            MockDHD.dhdWristEncoderToOrientation
        )

        libdhd.dhdWristEncoderToOrientation = (  # type: ignore
            MockDHD.dhdWristEncoderToOrientation.mock
        )

        enc = [0, 0, 0]
        out = [0.0, 0.0, 0.0]

        for _ in range(100):
            MockDHD.dhdWristEncoderToOrientation.oa = random()
            MockDHD.dhdWristEncoderToOrientation.ob = random()
            MockDHD.dhdWristEncoderToOrientation.og = random()

            enc[0] = randint(0, 100)
            enc[1] = randint(0, 100)
            enc[2] = randint(0, 100)

            dhd.expert.wristEncoderToOrientation(enc, out)

            self.assertAlmostEqual(
                out[0], MockDHD.dhdWristEncoderToOrientation.oa
            )
            self.assertAlmostEqual(
                out[1], MockDHD.dhdWristEncoderToOrientation.ob
            )
            self.assertAlmostEqual(
                out[2], MockDHD.dhdWristEncoderToOrientation.og
            )

            self.assertEqual(enc[0], MockDHD.dhdWristEncoderToOrientation.enc0)
            self.assertEqual(enc[1], MockDHD.dhdWristEncoderToOrientation.enc1)
            self.assertEqual(enc[2], MockDHD.dhdWristEncoderToOrientation.enc2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.wristEncoderToOrientation(enc, out, ID),
            MockDHD.dhdWristEncoderToOrientation
        )

        self.assertRetImpl(
            lambda: dhd.expert.wristEncoderToOrientation(enc, out),
            MockDHD.dhdWristEncoderToOrientation
        )

    def test_wristEncoderToOrientationDirect(self):
        libdhd.dhdWristEncoderToOrientation = (  # type: ignore
            MockDHD.dhdWristEncoderToOrientation.mock
        )

        enc = [0, 0, 0]
        out = containers.Vector3()

        for _ in range(100):
            MockDHD.dhdWristEncoderToOrientation.oa = random()
            MockDHD.dhdWristEncoderToOrientation.ob = random()
            MockDHD.dhdWristEncoderToOrientation.og = random()

            enc[0] = randint(0, 100)
            enc[1] = randint(0, 100)
            enc[2] = randint(0, 100)

            dhd.expert.direct.wristEncoderToOrientation(enc, out)

            self.assertAlmostEqual(
                out[0], MockDHD.dhdWristEncoderToOrientation.oa
            )
            self.assertAlmostEqual(
                out[1], MockDHD.dhdWristEncoderToOrientation.ob
            )
            self.assertAlmostEqual(
                out[2], MockDHD.dhdWristEncoderToOrientation.og
            )

            self.assertEqual(enc[0], MockDHD.dhdWristEncoderToOrientation.enc0)
            self.assertEqual(enc[1], MockDHD.dhdWristEncoderToOrientation.enc1)
            self.assertEqual(enc[2], MockDHD.dhdWristEncoderToOrientation.enc2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.wristEncoderToOrientation(
                enc, out, ID
            ),
            MockDHD.dhdWristEncoderToOrientation
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.wristEncoderToOrientation(enc, out),
            MockDHD.dhdWristEncoderToOrientation
        )

    def test_wristOrientationToEncoder(self):
        self.assertSignaturesEqual(
            libdhd.dhdWristOrientationToEncoder,
            MockDHD.dhdWristOrientationToEncoder
        )

        libdhd.dhdWristOrientationToEncoder = (  # type: ignore
            MockDHD.dhdWristOrientationToEncoder.mock
        )

        orientation = [0.0, 0.0, 0.0]
        out = [0, 0, 0]

        for _ in range(100):
            MockDHD.dhdWristOrientationToEncoder.enc0 = randint(0, 100)
            MockDHD.dhdWristOrientationToEncoder.enc1 = randint(0, 100)
            MockDHD.dhdWristOrientationToEncoder.enc2 = randint(0, 100)

            orientation[0] = random()
            orientation[1] = random()
            orientation[2] = random()

            dhd.expert.wristOrientationToEncoder(orientation, out)

            self.assertAlmostEqual(
                orientation[0], MockDHD.dhdWristOrientationToEncoder.oa
            )
            self.assertAlmostEqual(
                orientation[1], MockDHD.dhdWristOrientationToEncoder.ob
            )
            self.assertAlmostEqual(
                orientation[2], MockDHD.dhdWristOrientationToEncoder.og
            )

            self.assertEqual(out[0], MockDHD.dhdWristOrientationToEncoder.enc0)
            self.assertEqual(out[1], MockDHD.dhdWristOrientationToEncoder.enc1)
            self.assertEqual(out[2], MockDHD.dhdWristOrientationToEncoder.enc2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.wristOrientationToEncoder(
                orientation, out, ID
            ),
            MockDHD.dhdWristOrientationToEncoder
        )

        self.assertRetImpl(
            lambda: dhd.expert.wristOrientationToEncoder(orientation, out),
            MockDHD.dhdWristOrientationToEncoder
        )

    def test_wristOrientationToEncoderDirect(self):
        libdhd.dhdWristOrientationToEncoder = (  # type: ignore
            MockDHD.dhdWristOrientationToEncoder.mock
        )

        orientation = [0.0, 0.0, 0.0]
        out = containers.Enc3()

        for _ in range(100):
            MockDHD.dhdWristOrientationToEncoder.enc0 = randint(0, 100)
            MockDHD.dhdWristOrientationToEncoder.enc1 = randint(0, 100)
            MockDHD.dhdWristOrientationToEncoder.enc2 = randint(0, 100)

            orientation[0] = random()
            orientation[1] = random()
            orientation[2] = random()

            dhd.expert.direct.wristOrientationToEncoder(orientation, out)

            self.assertAlmostEqual(
                orientation[0], MockDHD.dhdWristOrientationToEncoder.oa
            )
            self.assertAlmostEqual(
                orientation[1], MockDHD.dhdWristOrientationToEncoder.ob
            )
            self.assertAlmostEqual(
                orientation[2], MockDHD.dhdWristOrientationToEncoder.og
            )

            self.assertEqual(out[0], MockDHD.dhdWristOrientationToEncoder.enc0)
            self.assertEqual(out[1], MockDHD.dhdWristOrientationToEncoder.enc1)
            self.assertEqual(out[2], MockDHD.dhdWristOrientationToEncoder.enc2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.wristOrientationToEncoder(
                orientation, out, ID
            ),
            MockDHD.dhdWristOrientationToEncoder
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.wristOrientationToEncoder(
                orientation, out
            ),
            MockDHD.dhdWristOrientationToEncoder
        )


    def test_wristMotorToTorque(self):
        self.assertSignaturesEqual(
            libdhd.dhdWristMotorToTorque,
            MockDHD.dhdWristMotorToTorque
        )

        libdhd.dhdWristMotorToTorque = (  # type: ignore
            MockDHD.dhdWristMotorToTorque.mock
        )

        mot = [0, 0, 0]
        enc = [0, 0, 0]

        out = [0.0, 0.0, 0.0]

        for _ in range(100):
            MockDHD.dhdWristMotorToTorque.tx = random()
            MockDHD.dhdWristMotorToTorque.ty = random()
            MockDHD.dhdWristMotorToTorque.tz = random()

            mot[0] = randint(0, 100)
            mot[1] = randint(0, 100)
            mot[2] = randint(0, 100)

            enc[0] = randint(0, 100)
            enc[1] = randint(0, 100)
            enc[2] = randint(0, 100)

            dhd.expert.wristMotorToTorque(mot, enc, out)

            self.assertAlmostEqual(
                out[0], MockDHD.dhdWristMotorToTorque.tx
            )
            self.assertAlmostEqual(
                out[1], MockDHD.dhdWristMotorToTorque.ty
            )
            self.assertAlmostEqual(
                out[2], MockDHD.dhdWristMotorToTorque.tz
            )

            self.assertEqual(mot[0], MockDHD.dhdWristMotorToTorque.mot0)
            self.assertEqual(mot[1], MockDHD.dhdWristMotorToTorque.mot1)
            self.assertEqual(mot[2], MockDHD.dhdWristMotorToTorque.mot2)

            self.assertEqual(enc[0], MockDHD.dhdWristMotorToTorque.enc0)
            self.assertEqual(enc[1], MockDHD.dhdWristMotorToTorque.enc1)
            self.assertEqual(enc[2], MockDHD.dhdWristMotorToTorque.enc2)


        self.assertIDImpl(
            lambda ID = -1: dhd.expert.wristMotorToTorque(mot, enc, out, ID),
            MockDHD.dhdWristMotorToTorque
        )

        self.assertRetImpl(
            lambda: dhd.expert.wristMotorToTorque(mot, enc, out),
            MockDHD.dhdWristMotorToTorque
        )

    def test_wristMotorToTorqueDirect(self):
        libdhd.dhdWristMotorToTorque = (  # type: ignore
            MockDHD.dhdWristMotorToTorque.mock
        )

        mot = [0, 0, 0]
        enc = [0, 0, 0]

        out = containers.Vector3()

        for _ in range(100):
            MockDHD.dhdWristMotorToTorque.tx = random()
            MockDHD.dhdWristMotorToTorque.ty = random()
            MockDHD.dhdWristMotorToTorque.tz = random()

            mot[0] = randint(0, 100)
            mot[1] = randint(0, 100)
            mot[2] = randint(0, 100)

            enc[0] = randint(0, 100)
            enc[1] = randint(0, 100)
            enc[2] = randint(0, 100)

            dhd.expert.direct.wristMotorToTorque(mot, enc, out)

            self.assertAlmostEqual(
                out[0], MockDHD.dhdWristMotorToTorque.tx
            )
            self.assertAlmostEqual(
                out[1], MockDHD.dhdWristMotorToTorque.ty
            )
            self.assertAlmostEqual(
                out[2], MockDHD.dhdWristMotorToTorque.tz
            )

            self.assertEqual(mot[0], MockDHD.dhdWristMotorToTorque.mot0)
            self.assertEqual(mot[1], MockDHD.dhdWristMotorToTorque.mot1)
            self.assertEqual(mot[2], MockDHD.dhdWristMotorToTorque.mot2)

            self.assertEqual(enc[0], MockDHD.dhdWristMotorToTorque.enc0)
            self.assertEqual(enc[1], MockDHD.dhdWristMotorToTorque.enc1)
            self.assertEqual(enc[2], MockDHD.dhdWristMotorToTorque.enc2)


        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.wristMotorToTorque(
                mot, enc, out, ID
            ),
            MockDHD.dhdWristMotorToTorque
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.wristMotorToTorque(mot, enc, out),
            MockDHD.dhdWristMotorToTorque
        )

    def test_wristTorqueToMotor(self):
        self.assertSignaturesEqual(
            libdhd.dhdWristTorqueToMotor,
            MockDHD.dhdWristTorqueToMotor
        )

        libdhd.dhdWristTorqueToMotor = (  # type: ignore
            MockDHD.dhdWristTorqueToMotor.mock
        )

        t = [0.0, 0.0, 0.0]
        enc = [0, 0, 0]

        out = [0, 0, 0]

        for _ in range(100):
            MockDHD.dhdWristTorqueToMotor.mot0 = randint(0, 100)
            MockDHD.dhdWristTorqueToMotor.mot1 = randint(0, 100)
            MockDHD.dhdWristTorqueToMotor.mot2 = randint(0, 100)

            t[0] = random()
            t[1] = random()
            t[2] = random()

            enc[0] = randint(0, 100)
            enc[1] = randint(0, 100)
            enc[2] = randint(0, 100)

            dhd.expert.wristTorqueToMotor(t, enc, out)

            self.assertAlmostEqual(
                t[0], MockDHD.dhdWristTorqueToMotor.tx
            )
            self.assertAlmostEqual(
                t[1], MockDHD.dhdWristTorqueToMotor.ty
            )
            self.assertAlmostEqual(
                t[2], MockDHD.dhdWristTorqueToMotor.tz
            )

            self.assertEqual(out[0], MockDHD.dhdWristTorqueToMotor.mot0)
            self.assertEqual(out[1], MockDHD.dhdWristTorqueToMotor.mot1)
            self.assertEqual(out[2], MockDHD.dhdWristTorqueToMotor.mot2)

            self.assertEqual(enc[0], MockDHD.dhdWristTorqueToMotor.enc0)
            self.assertEqual(enc[1], MockDHD.dhdWristTorqueToMotor.enc1)
            self.assertEqual(enc[2], MockDHD.dhdWristTorqueToMotor.enc2)


        self.assertIDImpl(
            lambda ID = -1: dhd.expert.wristTorqueToMotor(t, enc, out, ID),
            MockDHD.dhdWristTorqueToMotor
        )

        self.assertRetImpl(
            lambda: dhd.expert.wristTorqueToMotor(t, enc, out),
            MockDHD.dhdWristTorqueToMotor
        )

    def test_wristTorqueToMotorDirect(self):
        libdhd.dhdWristTorqueToMotor = (  # type: ignore
            MockDHD.dhdWristTorqueToMotor.mock
        )

        t = [0.0, 0.0, 0.0]
        enc = [0, 0, 0]

        out = containers.Mot3()

        for _ in range(100):
            MockDHD.dhdWristTorqueToMotor.mot0 = randint(0, 100)
            MockDHD.dhdWristTorqueToMotor.mot1 = randint(0, 100)
            MockDHD.dhdWristTorqueToMotor.mot2 = randint(0, 100)

            t[0] = random()
            t[1] = random()
            t[2] = random()

            enc[0] = randint(0, 100)
            enc[1] = randint(0, 100)
            enc[2] = randint(0, 100)

            dhd.expert.direct.wristTorqueToMotor(t, enc, out)

            self.assertAlmostEqual(
                t[0], MockDHD.dhdWristTorqueToMotor.tx
            )
            self.assertAlmostEqual(
                t[1], MockDHD.dhdWristTorqueToMotor.ty
            )
            self.assertAlmostEqual(
                t[2], MockDHD.dhdWristTorqueToMotor.tz
            )

            self.assertEqual(out[0], MockDHD.dhdWristTorqueToMotor.mot0)
            self.assertEqual(out[1], MockDHD.dhdWristTorqueToMotor.mot1)
            self.assertEqual(out[2], MockDHD.dhdWristTorqueToMotor.mot2)

            self.assertEqual(enc[0], MockDHD.dhdWristTorqueToMotor.enc0)
            self.assertEqual(enc[1], MockDHD.dhdWristTorqueToMotor.enc1)
            self.assertEqual(enc[2], MockDHD.dhdWristTorqueToMotor.enc2)


        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.wristTorqueToMotor(
                t, enc, out, ID
            ),
            MockDHD.dhdWristTorqueToMotor
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.wristTorqueToMotor(t, enc, out),
            MockDHD.dhdWristTorqueToMotor
        )


    def test_gripperEncoderToAngleRad(self):
        self.assertSignaturesEqual(
            libdhd.dhdGripperEncoderToAngleRad,
            MockDHD.dhdGripperEncoderToAngleRad
        )

        libdhd.dhdGripperEncoderToAngleRad = (  # type: ignore
            MockDHD.dhdGripperEncoderToAngleRad.mock
        )

        out = c_double()
        for _ in range(100):
            enc = randint(0, 100)
            MockDHD.dhdGripperEncoderToAngleRad.angle = random()

            dhd.expert.gripperEncoderToAngleRad(enc, out)

            self.assertAlmostEqual(
                out.value,
                MockDHD.dhdGripperEncoderToAngleRad.angle
            )

            self.assertEqual(enc, MockDHD.dhdGripperEncoderToAngleRad.enc)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.gripperEncoderToAngleRad(0, out, ID),
            MockDHD.dhdGripperEncoderToAngleRad
        )

        self.assertRetImpl(
            lambda: dhd.expert.gripperEncoderToAngleRad(0, out),
            MockDHD.dhdGripperEncoderToAngleRad
        )

    def test_gripperEncoderToGap(self):
        self.assertSignaturesEqual(
            libdhd.dhdGripperEncoderToGap,
            MockDHD.dhdGripperEncoderToGap
        )

        libdhd.dhdGripperEncoderToGap = (  # type: ignore
            MockDHD.dhdGripperEncoderToGap.mock
        )

        out = c_double()
        for _ in range(100):
            enc = randint(0, 100)
            MockDHD.dhdGripperEncoderToGap.gap = random()

            dhd.expert.gripperEncoderToGap(enc, out)

            self.assertAlmostEqual(
                out.value,
                MockDHD.dhdGripperEncoderToGap.gap
            )

            self.assertEqual(enc, MockDHD.dhdGripperEncoderToGap.enc)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.gripperEncoderToGap(enc, out, ID),
            MockDHD.dhdGripperEncoderToGap
        )

        self.assertRetImpl(
            lambda: dhd.expert.gripperEncoderToGap(0, out),
            MockDHD.dhdGripperEncoderToGap
        )

    def test_gripperAngleRadToEncoder(self):
        self.assertSignaturesEqual(
            libdhd.dhdGripperAngleRadToEncoder,
            MockDHD.dhdGripperAngleRadToEncoder
        )

        libdhd.dhdGripperAngleRadToEncoder = (  # type: ignore
            MockDHD.dhdGripperAngleRadToEncoder.mock
        )

        out = c_int()
        for _ in range(100):
            angle = random()

            dhd.expert.gripperAngleRadToEncoder(angle, out)

            self.assertAlmostEqual(
                out.value,
                MockDHD.dhdGripperAngleRadToEncoder.enc
            )

            self.assertAlmostEqual(
                angle, MockDHD.dhdGripperAngleRadToEncoder.angle
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.gripperAngleRadToEncoder(angle, out, ID),
            MockDHD.dhdGripperAngleRadToEncoder
        )

        self.assertRetImpl(
            lambda: dhd.expert.gripperAngleRadToEncoder(angle, out),
            MockDHD.dhdGripperAngleRadToEncoder
        )


    def test_gripperGapToEncoder(self):
        self.assertSignaturesEqual(
            libdhd.dhdGripperGapToEncoder,
            MockDHD.dhdGripperGapToEncoder
        )

        libdhd.dhdGripperGapToEncoder = (  # type: ignore
            MockDHD.dhdGripperGapToEncoder.mock
        )

        out = c_int()
        for _ in range(100):
            gap = random()

            dhd.expert.gripperGapToEncoder(gap, out)

            self.assertAlmostEqual(
                out.value,
                MockDHD.dhdGripperGapToEncoder.enc
            )

            self.assertAlmostEqual(gap, MockDHD.dhdGripperGapToEncoder.gap)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.gripperGapToEncoder(gap, out, ID),
            MockDHD.dhdGripperGapToEncoder
        )

        self.assertRetImpl(
            lambda: dhd.expert.gripperGapToEncoder(gap, out),
            MockDHD.dhdGripperGapToEncoder
        )

    def test_gripperMotorToForce(self):
        self.assertSignaturesEqual(
            libdhd.dhdGripperMotorToForce,
            MockDHD.dhdGripperMotorToForce
        )

        libdhd.dhdGripperMotorToForce = (  # type: ignore
            MockDHD.dhdGripperMotorToForce.mock
        )

        out = c_double()
        enc = [0, 0, 0]
        enc_grip = 0

        for _ in range(100):
            MockDHD.dhdGripperMotorToForce.f = random()
            enc_grip = randint(0, 100)
            enc_grip = randint(0, 100)

            mot = randint(0, 100)

            for i in range(3):
                enc[i] = randint(0, 100)

            dhd.expert.gripperMotorToForce(mot, enc, enc_grip, out)

            for i in range(3):
                self.assertAlmostEqual(
                    enc[i], MockDHD.dhdGripperMotorToForce.enc[i]
                )

            self.assertAlmostEqual(
                enc_grip,
                MockDHD.dhdGripperMotorToForce.enc[3]
            )


            self.assertEqual(mot, MockDHD.dhdGripperMotorToForce.mot)

            self.assertAlmostEqual(
                out.value,
                MockDHD.dhdGripperMotorToForce.f
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.gripperMotorToForce(0, enc, 0, out, ID),
            MockDHD.dhdGripperMotorToForce
        )

        self.assertRetImpl(
            lambda: dhd.expert.gripperMotorToForce(0, enc, 0, out),
            MockDHD.dhdGripperMotorToForce
        )

    def test_gripperMotorToForceDirect(self):
        self.assertSignaturesEqual(
            libdhd.dhdGripperMotorToForce,
            MockDHD.dhdGripperMotorToForce
        )

        libdhd.dhdGripperMotorToForce = (  # type: ignore
            MockDHD.dhdGripperMotorToForce.mock
        )

        out = c_double()
        enc_wrist_grip = containers.Enc4()

        for _ in range(100):
            MockDHD.dhdGripperMotorToForce.f = random()

            mot = randint(0, 100)

            for i in range(4):
                enc_wrist_grip[i] = randint(0, 100)

            dhd.expert.direct.gripperMotorToForce(mot, enc_wrist_grip, out)

            for i in range(4):
                self.assertEqual(
                    enc_wrist_grip[i], MockDHD.dhdGripperMotorToForce.enc[i]
                )

            self.assertEqual(mot, MockDHD.dhdGripperMotorToForce.mot)

            self.assertAlmostEqual(
                out.value,
                MockDHD.dhdGripperMotorToForce.f
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.gripperMotorToForce(
                0, enc_wrist_grip, out, ID
            ),
            MockDHD.dhdGripperMotorToForce
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.gripperMotorToForce(0, enc_wrist_grip, out),
            MockDHD.dhdGripperMotorToForce
        )

    def test_gripperForceToMotor(self):
        self.assertSignaturesEqual(
            libdhd.dhdGripperForceToMotor,
            MockDHD.dhdGripperForceToMotor
        )

        libdhd.dhdGripperForceToMotor = (  # type: ignore
            MockDHD.dhdGripperForceToMotor.mock
        )

        out = c_ushort()
        enc = [0, 0, 0]
        enc_grip = 0

        for _ in range(100):
            MockDHD.dhdGripperForceToMotor.mot = randint(0, 100)
            enc_grip = randint(0, 100)
            f = random()

            for i in range(3):
                enc[i] = randint(0, 100)

            dhd.expert.gripperForceToMotor(f, enc, enc_grip, out)

            for i in range(3):
                self.assertEqual(
                    enc[i], MockDHD.dhdGripperForceToMotor.enc[i]
                )

            self.assertEqual(
                enc_grip,
                MockDHD.dhdGripperForceToMotor.enc[3]
            )

            self.assertAlmostEqual(f, MockDHD.dhdGripperForceToMotor.f)

            self.assertEqual(
                out.value,
                MockDHD.dhdGripperForceToMotor.mot
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.gripperForceToMotor(0, enc, 0, out, ID),
            MockDHD.dhdGripperForceToMotor
        )

        self.assertRetImpl(
            lambda: dhd.expert.gripperForceToMotor(0, enc, 0, out),
            MockDHD.dhdGripperForceToMotor
        )

    def test_gripperForceToMotorDirect(self):
        self.assertSignaturesEqual(
            libdhd.dhdGripperForceToMotor,
            MockDHD.dhdGripperForceToMotor
        )

        libdhd.dhdGripperForceToMotor = (  # type: ignore
            MockDHD.dhdGripperForceToMotor.mock
        )

        out = c_ushort()
        enc_wrist_grip = containers.Enc4()

        for _ in range(100):
            MockDHD.dhdGripperForceToMotor.mot = randint(0, 100)
            f = random()

            for i in range(4):
                enc_wrist_grip[i] = randint(0, 100)

            dhd.expert.direct.gripperForceToMotor(f, enc_wrist_grip, out)

            for i in range(4):
                self.assertEqual(
                    enc_wrist_grip[i], MockDHD.dhdGripperForceToMotor.enc[i]
                )

            self.assertAlmostEqual(f, MockDHD.dhdGripperForceToMotor.f)

            self.assertAlmostEqual(
                out.value,
                MockDHD.dhdGripperForceToMotor.mot
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.gripperForceToMotor(
                0, enc_wrist_grip, out, ID
            ),
            MockDHD.dhdGripperForceToMotor
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.gripperForceToMotor(
                0, enc_wrist_grip, out
            ),
            MockDHD.dhdGripperForceToMotor
        )


    def test_setMot(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetMot, MockDHD.dhdSetMot
        )

        libdhd.dhdSetMot = MockDHD.dhdSetMot.mock  # type: ignore

        cmds = [0] * MAX_DOF

        for _ in range(100):
            for i in range(MAX_DOF):
                cmds[i] = randint(0, 100)

            mask = randint(0, 100)

            dhd.expert.setMot(cmds, mask)

            self.assertListEqual(cmds, MockDHD.dhdSetMot.mot)
            self.assertEqual(mask, MockDHD.dhdSetMot.mask)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.setMot(cmds, 0, ID),
            MockDHD.dhdSetMot
        )

        self.assertRetImpl(
            lambda: dhd.expert.setMot(cmds, 0),
            MockDHD.dhdSetMot
        )

    def test_setJointTorques(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetJointTorques, MockDHD.dhdSetJointTorques
        )

        libdhd.dhdSetJointTorques = MockDHD.dhdSetJointTorques.mock  # type: ignore

        q = [0.0] * MAX_DOF

        for _ in range(100):
            for i in range(MAX_DOF):
                q[i] = random()

            mask = randint(0, 100)

            dhd.expert.setJointTorques(q, mask)

            self.assertListEqual(q, MockDHD.dhdSetJointTorques.q)
            self.assertEqual(mask, MockDHD.dhdSetJointTorques.mask)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.setJointTorques(q, 0, ID),
            MockDHD.dhdSetJointTorques
        )

        self.assertRetImpl(
            lambda: dhd.expert.setJointTorques(q, 0),
            MockDHD.dhdSetJointTorques
        )

    def test_preloadMot(self):
        self.assertSignaturesEqual(
            libdhd.dhdPreloadMot, MockDHD.dhdPreloadMot
        )

        libdhd.dhdPreloadMot = MockDHD.dhdPreloadMot.mock  # type: ignore

        cmds = [0] * MAX_DOF

        for _ in range(100):
            for i in range(MAX_DOF):
                cmds[i] = randint(0, 100)

            mask = randint(0, 100)

            dhd.expert.preloadMot(cmds, mask)

            self.assertListEqual(cmds, MockDHD.dhdPreloadMot.mot)
            self.assertEqual(mask, MockDHD.dhdPreloadMot.mask)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.preloadMot(cmds, 0, ID),
            MockDHD.dhdPreloadMot
        )

        self.assertRetImpl(
            lambda: dhd.expert.preloadMot(cmds, 0),
            MockDHD.dhdPreloadMot
        )


    def test_getEnc(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetEnc, MockDHD.dhdGetEnc
        )

        libdhd.dhdGetEnc = MockDHD.dhdGetEnc.mock  # type: ignore

        mask = 0
        enc = [0] * MAX_DOF

        for _ in range(100):
            dhd.expert.getEnc(enc, mask)

            self.assertListEqual(enc, MockDHD.dhdGetEnc.enc)
            self.assertEqual(mask, MockDHD.dhdGetEnc.mask)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.getEnc(enc, mask, ID),
            MockDHD.dhdGetEnc
        )

        self.assertRetImpl(
            lambda: dhd.expert.getEnc(enc, mask),
            MockDHD.dhdGetEnc
        )

    def test_getEncDirect(self):
        libdhd.dhdGetEnc = MockDHD.dhdGetEnc.mock  # type: ignore

        mask = 0
        enc = containers.DOFInt()

        for _ in range(100):
            dhd.expert.direct.getEnc(enc, mask)

            for i in range(MAX_DOF):
                self.assertEqual(enc[i], MockDHD.dhdGetEnc.enc[i])

            self.assertEqual(mask, MockDHD.dhdGetEnc.mask)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.getEnc(enc, mask, ID),
            MockDHD.dhdGetEnc
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.getEnc(enc, mask),
            MockDHD.dhdGetEnc
        )

    def test_setBrk(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetBrk, MockDHD.dhdSetBrk
        )

        libdhd.dhdSetBrk = MockDHD.dhdSetBrk.mock  # type: ignore

        mask = 0

        for _ in range(100):
            dhd.expert.setBrk(mask)

            self.assertEqual(mask, MockDHD.dhdSetBrk.mask)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.setBrk(mask, ID),
            MockDHD.dhdSetBrk
        )

        self.assertRetImpl(
            lambda: dhd.expert.setBrk(mask),
            MockDHD.dhdSetBrk
        )

    def test_getDeltaJointAngles(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetDeltaJointAngles, MockDHD.dhdGetDeltaJointAngles
        )

        libdhd.dhdGetDeltaJointAngles = (  # type: ignore
            MockDHD.dhdGetDeltaJointAngles.mock
        )
        out = [0.0, 0.0, 0.0]

        for _ in range(100):
            MockDHD.dhdGetDeltaJointAngles.j0 = random()
            MockDHD.dhdGetDeltaJointAngles.j1 = random()
            MockDHD.dhdGetDeltaJointAngles.j2 = random()

            dhd.expert.getDeltaJointAngles(out)

            self.assertAlmostEqual(out[0], MockDHD.dhdGetDeltaJointAngles.j0)
            self.assertAlmostEqual(out[1], MockDHD.dhdGetDeltaJointAngles.j1)
            self.assertAlmostEqual(out[2], MockDHD.dhdGetDeltaJointAngles.j2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.getDeltaJointAngles(out, ID),
            MockDHD.dhdGetDeltaJointAngles
        )
        self.assertRetImpl(
            lambda: dhd.expert.getDeltaJointAngles(out),
            MockDHD.dhdGetDeltaJointAngles
        )

    def test_getDeltaJointAnglesDirect(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetDeltaJointAngles, MockDHD.dhdGetDeltaJointAngles
        )

        libdhd.dhdGetDeltaJointAngles = (  # type: ignore
            MockDHD.dhdGetDeltaJointAngles.mock
        )
        out = containers.Vector3()

        for _ in range(100):
            MockDHD.dhdGetDeltaJointAngles.j0 = random()
            MockDHD.dhdGetDeltaJointAngles.j1 = random()
            MockDHD.dhdGetDeltaJointAngles.j2 = random()

            dhd.expert.direct.getDeltaJointAngles(out)

            self.assertAlmostEqual(out[0], MockDHD.dhdGetDeltaJointAngles.j0)
            self.assertAlmostEqual(out[1], MockDHD.dhdGetDeltaJointAngles.j1)
            self.assertAlmostEqual(out[2], MockDHD.dhdGetDeltaJointAngles.j2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.getDeltaJointAngles(out, ID),
            MockDHD.dhdGetDeltaJointAngles
        )
        self.assertRetImpl(
            lambda: dhd.expert.direct.getDeltaJointAngles(out),
            MockDHD.dhdGetDeltaJointAngles
        )

    def test_getDeltaJacobian(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetDeltaJacobian, MockDHD.dhdGetDeltaJacobian
        )

        libdhd.dhdGetDeltaJacobian = (  # type: ignore
            MockDHD.dhdGetDeltaJacobian.mock
        )
        out = [[0.0] * 3] * 3

        for _ in range(100):
            for i in range(3):
                for j in range(3):
                    MockDHD.dhdGetDeltaJacobian.jcb[i][j] = random()

            dhd.expert.getDeltaJacobian(out)

            self.assertListEqual(out, MockDHD.dhdGetDeltaJacobian.jcb)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.getDeltaJacobian(out, ID),
            MockDHD.dhdGetDeltaJacobian
        )
        self.assertRetImpl(
            lambda: dhd.expert.getDeltaJacobian(out),
            MockDHD.dhdGetDeltaJacobian
        )

    def test_getDeltaJacobianDirect(self):
        libdhd.dhdGetDeltaJacobian = (  # type: ignore
            MockDHD.dhdGetDeltaJacobian.mock
        )
        out = containers.Mat3x3()

        for _ in range(100):
            for i in range(3):
                for j in range(3):
                    MockDHD.dhdGetDeltaJacobian.jcb[i][j] = random()

            dhd.expert.direct.getDeltaJacobian(out)

            for i in range(3):
                for j in range(3):
                    self.assertAlmostEqual(
                        out[i, j], MockDHD.dhdGetDeltaJacobian.jcb[i][j]
                    )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.getDeltaJacobian(out, ID),
            MockDHD.dhdGetDeltaJacobian
        )
        self.assertRetImpl(
            lambda: dhd.expert.direct.getDeltaJacobian(out),
            MockDHD.dhdGetDeltaJacobian
        )

    def test_wristJointAnglesToJacobian(self):
        self.assertSignaturesEqual(
            libdhd.dhdWristJointAnglesToJacobian,
            MockDHD.dhdWristJointAnglesToJacobian
        )

        libdhd.dhdWristJointAnglesToJacobian = (  # type: ignore
            MockDHD.dhdWristJointAnglesToJacobian.mock
        )

        joint_angles = [0.0, 0.0, 0.0]
        out = [[0.0] * 3 for _ in range(3)]

        for _ in range(100):
            for i in range(3):
                joint_angles[i] = random()

            for i in range(3):
                for j in range(3):
                    MockDHD.dhdWristJointAnglesToJacobian.jcb[i][j] = random()


            dhd.expert.wristJointAnglesToJacobian(joint_angles, out)

            self.assertAlmostEqual(
                joint_angles[0],
                MockDHD.dhdWristJointAnglesToJacobian.j0
            )

            self.assertAlmostEqual(
                joint_angles[1],
                MockDHD.dhdWristJointAnglesToJacobian.j1
            )

            self.assertAlmostEqual(
                joint_angles[2],
                MockDHD.dhdWristJointAnglesToJacobian.j2
            )
            for i in range(3):
                for j in range(3):
                    self.assertAlmostEqual(
                        out[i][j],
                        MockDHD.dhdWristJointAnglesToJacobian.jcb[i][j]
                    )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.wristJointAnglesToJacobian(
                joint_angles, out, ID
            ),
            MockDHD.dhdWristJointAnglesToJacobian
        )

        self.assertRetImpl(
            lambda: dhd.expert.wristJointAnglesToJacobian(
                joint_angles, out,
            ),
            MockDHD.dhdWristJointAnglesToJacobian
        )

    def test_wristJointAnglesToJacobianDirect(self):
        libdhd.dhdWristJointAnglesToJacobian = (  # type: ignore
            MockDHD.dhdWristJointAnglesToJacobian.mock
        )

        joint_angles = [0.0, 0.0, 0.0]
        out = containers.Mat3x3()

        for _ in range(100):
            for i in range(3):
                joint_angles[i] = random()

            for i in range(3):
                for j in range(3):
                    MockDHD.dhdWristJointAnglesToJacobian.jcb[i][j] = random()


            dhd.expert.direct.wristJointAnglesToJacobian(joint_angles, out)

            self.assertAlmostEqual(
                joint_angles[0],
                MockDHD.dhdWristJointAnglesToJacobian.j0
            )

            self.assertAlmostEqual(
                joint_angles[1],
                MockDHD.dhdWristJointAnglesToJacobian.j1
            )

            self.assertAlmostEqual(
                joint_angles[2],
                MockDHD.dhdWristJointAnglesToJacobian.j2
            )
            for i in range(3):
                for j in range(3):
                    self.assertAlmostEqual(
                        out[i, j],
                        MockDHD.dhdWristJointAnglesToJacobian.jcb[i][j]
                    )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.wristJointAnglesToJacobian(
                joint_angles, out, ID
            ),
            MockDHD.dhdWristJointAnglesToJacobian
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.wristJointAnglesToJacobian(
                joint_angles, out,
            ),
            MockDHD.dhdWristJointAnglesToJacobian
        )


    def test_deltaJointTorquesExtrema(self):
        self.assertSignaturesEqual(
            libdhd.dhdDeltaJointTorquesExtrema,
            MockDHD.dhdDeltaJointTorquesExtrema
        )

        libdhd.dhdDeltaJointTorquesExtrema = (  # type: ignore
            MockDHD.dhdDeltaJointTorquesExtrema.mock
        )

        joint_angles = [0.0, 0.0, 0.0]

        minq = [0.0, 0.0, 0.0]
        maxq = [0.0, 0.0, 0.0]

        for _ in range(100):
            for i in range(3):
                MockDHD.dhdDeltaJointTorquesExtrema.minq[i] = random()
                MockDHD.dhdDeltaJointTorquesExtrema.maxq[i] = random()
                joint_angles[i] = random()

            dhd.expert.deltaJointTorquesExtrema(joint_angles, minq, maxq)


            for i in range(3):
                self.assertAlmostEqual(
                    minq[i], MockDHD.dhdDeltaJointTorquesExtrema.minq[i]
                )
                self.assertAlmostEqual(
                    maxq[i], MockDHD.dhdDeltaJointTorquesExtrema.maxq[i]
                )

            self.assertAlmostEqual(
                joint_angles[0], MockDHD.dhdDeltaJointTorquesExtrema.j0
            )

            self.assertAlmostEqual(
                joint_angles[1], MockDHD.dhdDeltaJointTorquesExtrema.j1
            )

            self.assertAlmostEqual(
                joint_angles[2], MockDHD.dhdDeltaJointTorquesExtrema.j2
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.deltaJointTorquesExtrema(
                joint_angles, minq, maxq, ID
            ),
            MockDHD.dhdDeltaJointTorquesExtrema
        )

        self.assertRetImpl(
            lambda: dhd.expert.deltaJointTorquesExtrema(
                joint_angles, minq, maxq
            ),
            MockDHD.dhdDeltaJointTorquesExtrema
        )

    def test_deltaJointTorquesExtremaDirect(self):
        joint_angles = [0.0, 0.0, 0.0]

        minq = containers.Vector3()
        maxq = containers.Vector3()

        for _ in range(100):
            for i in range(3):
                MockDHD.dhdDeltaJointTorquesExtrema.minq[i] = random()
                MockDHD.dhdDeltaJointTorquesExtrema.maxq[i] = random()
                joint_angles[i] = random()

            dhd.expert.direct.deltaJointTorquesExtrema(joint_angles, minq, maxq)


            for i in range(3):
                self.assertAlmostEqual(
                    minq[i], MockDHD.dhdDeltaJointTorquesExtrema.minq[i]
                )
                self.assertAlmostEqual(
                    maxq[i], MockDHD.dhdDeltaJointTorquesExtrema.maxq[i]
                )

            self.assertAlmostEqual(
                joint_angles[0], MockDHD.dhdDeltaJointTorquesExtrema.j0
            )

            self.assertAlmostEqual(
                joint_angles[1], MockDHD.dhdDeltaJointTorquesExtrema.j1
            )

            self.assertAlmostEqual(
                joint_angles[2], MockDHD.dhdDeltaJointTorquesExtrema.j2
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.deltaJointTorquesExtrema(
                joint_angles, minq, maxq, ID
            ),
            MockDHD.dhdDeltaJointTorquesExtrema
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.deltaJointTorquesExtrema(
                joint_angles, minq, maxq
            ),
            MockDHD.dhdDeltaJointTorquesExtrema
        )


    def test_setDeltaJointTorques(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetDeltaJointTorques,
            MockDHD.dhdSetDeltaJointTorques
        )

        libdhd.dhdSetDeltaJointTorques = (  # type: ignore
            MockDHD.dhdSetDeltaJointTorques.mock
        )

        q = [0.0, 0.0, 0.0]
        for _ in range(100):
            for i in range(3):
                q[i] = random()

            dhd.expert.setDeltaJointTorques(q)

            self.assertAlmostEqual(q[0], MockDHD.dhdSetDeltaJointTorques.q0)
            self.assertAlmostEqual(q[1], MockDHD.dhdSetDeltaJointTorques.q1)
            self.assertAlmostEqual(q[2], MockDHD.dhdSetDeltaJointTorques.q2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.setDeltaJointTorques(q, ID),
            MockDHD.dhdSetDeltaJointTorques
        )

        self.assertRetImpl(
            lambda: dhd.expert.setDeltaJointTorques(q),
            MockDHD.dhdSetDeltaJointTorques
        )

    def test_deltaEncodersToJointAngles(self):
        self.assertSignaturesEqual(
            libdhd.dhdDeltaEncodersToJointAngles,
            MockDHD.dhdDeltaEncodersToJointAngles
        )

        libdhd.dhdDeltaEncodersToJointAngles = (  # type: ignore
            MockDHD.dhdDeltaEncodersToJointAngles.mock
        )

        enc = [0, 0, 0]
        out = [0.0, 0.0, 0.0]
        for _ in range(100):
            MockDHD.dhdDeltaEncodersToJointAngles.j0 = random()
            MockDHD.dhdDeltaEncodersToJointAngles.j1 = random()
            MockDHD.dhdDeltaEncodersToJointAngles.j2 = random()

            dhd.expert.deltaEncodersToJointAngles(enc, out)

            self.assertAlmostEqual(
                out[0], MockDHD.dhdDeltaEncodersToJointAngles.j0
            )

            self.assertAlmostEqual(
                out[1], MockDHD.dhdDeltaEncodersToJointAngles.j1
            )

            self.assertAlmostEqual(
                out[2], MockDHD.dhdDeltaEncodersToJointAngles.j2
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.deltaEncodersToJointAngles(
                enc, out, ID
            ),
            MockDHD.dhdDeltaEncodersToJointAngles
        )

        self.assertRetImpl(
            lambda: dhd.expert.deltaEncodersToJointAngles(enc, out),
            MockDHD.dhdDeltaEncodersToJointAngles
        )

    def test_deltaEncodersToJointAnglesDirect(self):
        libdhd.dhdDeltaEncodersToJointAngles = (  # type: ignore
            MockDHD.dhdDeltaEncodersToJointAngles.mock
        )

        enc = [0, 0, 0]
        out = containers.Vector3()

        for _ in range(100):
            MockDHD.dhdDeltaEncodersToJointAngles.j0 = random()
            MockDHD.dhdDeltaEncodersToJointAngles.j1 = random()
            MockDHD.dhdDeltaEncodersToJointAngles.j2 = random()

            dhd.expert.direct.deltaEncodersToJointAngles(enc, out)

            self.assertAlmostEqual(
                out[0], MockDHD.dhdDeltaEncodersToJointAngles.j0
            )

            self.assertAlmostEqual(
                out[1], MockDHD.dhdDeltaEncodersToJointAngles.j1
            )

            self.assertAlmostEqual(
                out[2], MockDHD.dhdDeltaEncodersToJointAngles.j2
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.deltaEncodersToJointAngles(
                enc, out, ID
            ),
            MockDHD.dhdDeltaEncodersToJointAngles
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.deltaEncodersToJointAngles(enc, out),
            MockDHD.dhdDeltaEncodersToJointAngles
        )

    def test_deltaJointAnglesToEncoders(self):
        self.assertSignaturesEqual(
            libdhd.dhdDeltaJointAnglesToEncoders,
            MockDHD.dhdDeltaJointAnglesToEncoders
        )

        libdhd.dhdDeltaJointAnglesToEncoders = (  # type: ignore
            MockDHD.dhdDeltaJointAnglesToEncoders.mock
        )

        joint_angles = [0.0, 0.0, 0.0]
        out = [0, 0, 0]

        for _ in range(100):
            MockDHD.dhdDeltaJointAnglesToEncoders.enc0 = randint(0, 100)
            MockDHD.dhdDeltaJointAnglesToEncoders.enc1 = randint(0, 100)
            MockDHD.dhdDeltaJointAnglesToEncoders.enc2 = randint(0, 100)

            dhd.expert.deltaJointAnglesToEncoders(joint_angles, out)

            self.assertAlmostEqual(
                out[0], MockDHD.dhdDeltaJointAnglesToEncoders.enc0
            )

            self.assertAlmostEqual(
                out[1], MockDHD.dhdDeltaJointAnglesToEncoders.enc1
            )

            self.assertAlmostEqual(
                out[2], MockDHD.dhdDeltaJointAnglesToEncoders.enc2
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.deltaJointAnglesToEncoders(
                joint_angles, out, ID
            ),
            MockDHD.dhdDeltaJointAnglesToEncoders
        )

        self.assertRetImpl(
            lambda: dhd.expert.deltaJointAnglesToEncoders(joint_angles, out),
            MockDHD.dhdDeltaJointAnglesToEncoders
        )

    def test_deltaJointAnglesToEncodersDirect(self):
        libdhd.dhdDeltaJointAnglesToEncoders = (  # type: ignore
            MockDHD.dhdDeltaJointAnglesToEncoders.mock
        )

        joint_angles = [0.0, 0.0, 0.0]
        out = containers.Enc3()

        for _ in range(100):
            MockDHD.dhdDeltaJointAnglesToEncoders.enc0 = randint(0, 100)
            MockDHD.dhdDeltaJointAnglesToEncoders.enc1 = randint(0, 100)
            MockDHD.dhdDeltaJointAnglesToEncoders.enc2 = randint(0, 100)

            dhd.expert.direct.deltaJointAnglesToEncoders(joint_angles, out)

            self.assertAlmostEqual(
                out[0], MockDHD.dhdDeltaJointAnglesToEncoders.enc0
            )

            self.assertAlmostEqual(
                out[1], MockDHD.dhdDeltaJointAnglesToEncoders.enc1
            )

            self.assertAlmostEqual(
                out[2], MockDHD.dhdDeltaJointAnglesToEncoders.enc2
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.deltaJointAnglesToEncoders(
                joint_angles, out, ID
            ),
            MockDHD.dhdDeltaJointAnglesToEncoders
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.deltaJointAnglesToEncoders(joint_angles, out),
            MockDHD.dhdDeltaJointAnglesToEncoders
        )

    def test_getWristJointAngles(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetWristJointAngles, MockDHD.dhdGetWristJointAngles
        )

        libdhd.dhdGetWristJointAngles = (  # type: ignore
            MockDHD.dhdGetWristJointAngles.mock
        )
        out = [0.0, 0.0, 0.0]

        for _ in range(100):
            MockDHD.dhdGetWristJointAngles.j0 = random()
            MockDHD.dhdGetWristJointAngles.j1 = random()
            MockDHD.dhdGetWristJointAngles.j2 = random()

            dhd.expert.getWristJointAngles(out)

            self.assertAlmostEqual(out[0], MockDHD.dhdGetWristJointAngles.j0)
            self.assertAlmostEqual(out[1], MockDHD.dhdGetWristJointAngles.j1)
            self.assertAlmostEqual(out[2], MockDHD.dhdGetWristJointAngles.j2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.getWristJointAngles(out, ID),
            MockDHD.dhdGetWristJointAngles
        )
        self.assertRetImpl(
            lambda: dhd.expert.getWristJointAngles(out),
            MockDHD.dhdGetWristJointAngles
        )

    def test_getWristJointAnglesDirect(self):
        libdhd.dhdGetWristJointAngles = (  # type: ignore
            MockDHD.dhdGetWristJointAngles.mock
        )
        out = containers.Vector3()

        for _ in range(100):
            MockDHD.dhdGetWristJointAngles.j0 = random()
            MockDHD.dhdGetWristJointAngles.j1 = random()
            MockDHD.dhdGetWristJointAngles.j2 = random()

            dhd.expert.direct.getWristJointAngles(out)

            self.assertAlmostEqual(out[0], MockDHD.dhdGetWristJointAngles.j0)
            self.assertAlmostEqual(out[1], MockDHD.dhdGetWristJointAngles.j1)
            self.assertAlmostEqual(out[2], MockDHD.dhdGetWristJointAngles.j2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.getWristJointAngles(out, ID),
            MockDHD.dhdGetWristJointAngles
        )
        self.assertRetImpl(
            lambda: dhd.expert.direct.getWristJointAngles(out),
            MockDHD.dhdGetWristJointAngles
        )

    def test_getWristJacobian(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetWristJacobian, MockDHD.dhdGetWristJacobian
        )

        libdhd.dhdGetWristJacobian = (  # type: ignore
            MockDHD.dhdGetWristJacobian.mock
        )
        out = [[0.0] * 3] * 3

        for _ in range(100):
            for i in range(3):
                for j in range(3):
                    MockDHD.dhdGetWristJacobian.jcb[i][j] = random()

            dhd.expert.getWristJacobian(out)

            self.assertListEqual(out, MockDHD.dhdGetWristJacobian.jcb)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.getWristJacobian(out, ID),
            MockDHD.dhdGetWristJacobian
        )
        self.assertRetImpl(
            lambda: dhd.expert.getWristJacobian(out),
            MockDHD.dhdGetWristJacobian
        )

    def test_getWristJacobianDirect(self):
        libdhd.dhdGetWristJacobian = (  # type: ignore
            MockDHD.dhdGetWristJacobian.mock
        )
        out = containers.Mat3x3()

        for _ in range(100):
            for i in range(3):
                for j in range(3):
                    MockDHD.dhdGetWristJacobian.jcb[i][j] = random()

            dhd.expert.direct.getWristJacobian(out)

            for i in range(3):
                for j in range(3):
                    self.assertAlmostEqual(
                        out[i, j], MockDHD.dhdGetWristJacobian.jcb[i][j]
                    )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.getWristJacobian(out, ID),
            MockDHD.dhdGetWristJacobian
        )
        self.assertRetImpl(
            lambda: dhd.expert.direct.getWristJacobian(out),
            MockDHD.dhdGetWristJacobian
        )

    def test_deltaJointAnglesToJacobian(self):
        self.assertSignaturesEqual(
            libdhd.dhdDeltaJointAnglesToJacobian,
            MockDHD.dhdDeltaJointAnglesToJacobian
        )

        libdhd.dhdDeltaJointAnglesToJacobian = (  # type: ignore
            MockDHD.dhdDeltaJointAnglesToJacobian.mock
        )

        joint_angles = [0.0, 0.0, 0.0]
        out = [[0.0] * 3 for _ in range(3)]

        for _ in range(100):
            for i in range(3):
                joint_angles[i] = random()

            for i in range(3):
                for j in range(3):
                    MockDHD.dhdDeltaJointAnglesToJacobian.jcb[i][j] = random()


            dhd.expert.deltaJointAnglesToJacobian(joint_angles, out)

            self.assertAlmostEqual(
                joint_angles[0],
                MockDHD.dhdDeltaJointAnglesToJacobian.j0
            )

            self.assertAlmostEqual(
                joint_angles[1],
                MockDHD.dhdDeltaJointAnglesToJacobian.j1
            )

            self.assertAlmostEqual(
                joint_angles[2],
                MockDHD.dhdDeltaJointAnglesToJacobian.j2
            )
            for i in range(3):
                for j in range(3):
                    self.assertAlmostEqual(
                        out[i][j],
                        MockDHD.dhdDeltaJointAnglesToJacobian.jcb[i][j]
                    )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.deltaJointAnglesToJacobian(
                joint_angles, out, ID
            ),
            MockDHD.dhdDeltaJointAnglesToJacobian
        )

        self.assertRetImpl(
            lambda: dhd.expert.deltaJointAnglesToJacobian(
                joint_angles, out,
            ),
            MockDHD.dhdDeltaJointAnglesToJacobian
        )

    def test_wristJointTorquesExtrema(self):
        self.assertSignaturesEqual(
            libdhd.dhdWristJointTorquesExtrema,
            MockDHD.dhdWristJointTorquesExtrema
        )

        libdhd.dhdWristJointTorquesExtrema = (  # type: ignore
            MockDHD.dhdWristJointTorquesExtrema.mock
        )

        joint_angles = [0.0, 0.0, 0.0]

        minq = [0.0, 0.0, 0.0]
        maxq = [0.0, 0.0, 0.0]

        for _ in range(100):
            for i in range(3):
                MockDHD.dhdWristJointTorquesExtrema.minq[i] = random()
                MockDHD.dhdWristJointTorquesExtrema.maxq[i] = random()
                joint_angles[i] = random()

            dhd.expert.wristJointTorquesExtrema(joint_angles, minq, maxq)


            for i in range(3):
                self.assertAlmostEqual(
                    minq[i], MockDHD.dhdWristJointTorquesExtrema.minq[i]
                )
                self.assertAlmostEqual(
                    maxq[i], MockDHD.dhdWristJointTorquesExtrema.maxq[i]
                )

            self.assertAlmostEqual(
                joint_angles[0], MockDHD.dhdWristJointTorquesExtrema.j0
            )

            self.assertAlmostEqual(
                joint_angles[1], MockDHD.dhdWristJointTorquesExtrema.j1
            )

            self.assertAlmostEqual(
                joint_angles[2], MockDHD.dhdWristJointTorquesExtrema.j2
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.wristJointTorquesExtrema(
                joint_angles, minq, maxq, ID
            ),
            MockDHD.dhdWristJointTorquesExtrema
        )

        self.assertRetImpl(
            lambda: dhd.expert.wristJointTorquesExtrema(
                joint_angles, minq, maxq
            ),
            MockDHD.dhdWristJointTorquesExtrema
        )

    def test_wristJointTorquesExtremaDirect(self):
        joint_angles = [0.0, 0.0, 0.0]

        minq = containers.Vector3()
        maxq = containers.Vector3()

        for _ in range(100):
            for i in range(3):
                MockDHD.dhdWristJointTorquesExtrema.minq[i] = random()
                MockDHD.dhdWristJointTorquesExtrema.maxq[i] = random()
                joint_angles[i] = random()

            dhd.expert.direct.wristJointTorquesExtrema(joint_angles, minq, maxq)


            for i in range(3):
                self.assertAlmostEqual(
                    minq[i], MockDHD.dhdWristJointTorquesExtrema.minq[i]
                )
                self.assertAlmostEqual(
                    maxq[i], MockDHD.dhdWristJointTorquesExtrema.maxq[i]
                )

            self.assertAlmostEqual(
                joint_angles[0], MockDHD.dhdWristJointTorquesExtrema.j0
            )

            self.assertAlmostEqual(
                joint_angles[1], MockDHD.dhdWristJointTorquesExtrema.j1
            )

            self.assertAlmostEqual(
                joint_angles[2], MockDHD.dhdWristJointTorquesExtrema.j2
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.wristJointTorquesExtrema(
                joint_angles, minq, maxq, ID
            ),
            MockDHD.dhdWristJointTorquesExtrema
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.wristJointTorquesExtrema(
                joint_angles, minq, maxq
            ),
            MockDHD.dhdWristJointTorquesExtrema
        )

    def test_setWristJointTorques(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetWristJointTorques,
            MockDHD.dhdSetWristJointTorques
        )

        libdhd.dhdSetWristJointTorques = (  # type: ignore
            MockDHD.dhdSetWristJointTorques.mock
        )

        q = [0.0, 0.0, 0.0]
        for _ in range(100):
            for i in range(3):
                q[i] = random()

            dhd.expert.setWristJointTorques(q)

            self.assertAlmostEqual(q[0], MockDHD.dhdSetWristJointTorques.q0)
            self.assertAlmostEqual(q[1], MockDHD.dhdSetWristJointTorques.q1)
            self.assertAlmostEqual(q[2], MockDHD.dhdSetWristJointTorques.q2)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.setWristJointTorques(q, ID),
            MockDHD.dhdSetWristJointTorques
        )

        self.assertRetImpl(
            lambda: dhd.expert.setWristJointTorques(q),
            MockDHD.dhdSetWristJointTorques
        )

    def test_setForceAndWristJointTorques(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetForceAndWristJointTorques,
            MockDHD.dhdSetForceAndWristJointTorques
        )

        libdhd.dhdSetForceAndWristJointTorques = (  # type: ignore
            MockDHD.dhdSetForceAndWristJointTorques.mock
        )

        f = [0.0, 0.0, 0.0]
        t = [0.0, 0.0, 0.0]

        for _ in range(100):
            f[0] = random()
            f[1] = random()
            f[2] = random()

            t[0] = random()
            t[1] = random()
            t[2] = random()

            dhd.expert.setForceAndWristJointTorques(f, t)

            self.assertAlmostEqual(
                f[0], MockDHD.dhdSetForceAndWristJointTorques.fx
            )
            self.assertAlmostEqual(
                f[1], MockDHD.dhdSetForceAndWristJointTorques.fy
            )
            self.assertAlmostEqual(
                f[2], MockDHD.dhdSetForceAndWristJointTorques.fz
            )

            self.assertAlmostEqual(

                t[0], MockDHD.dhdSetForceAndWristJointTorques.q0)
            self.assertAlmostEqual(
                t[1], MockDHD.dhdSetForceAndWristJointTorques.q1
            )
            self.assertAlmostEqual(
                t[2], MockDHD.dhdSetForceAndWristJointTorques.q2
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.setForceAndWristJointTorques(f, t, ID),
            MockDHD.dhdSetForceAndWristJointTorques
        )
        self.assertRetImpl(
            lambda: dhd.expert.setForceAndWristJointTorques(f, t),
            MockDHD.dhdSetForceAndWristJointTorques
        )

    def test_setForceAndWristJointTorquesAndGripperForce(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetForceAndWristJointTorquesAndGripperForce,
            MockDHD.dhdSetForceAndWristJointTorquesAndGripperForce
        )

        libdhd.dhdSetForceAndWristJointTorquesAndGripperForce = (  # type: ignore
            MockDHD.dhdSetForceAndWristJointTorquesAndGripperForce.mock
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

            dhd.expert.setForceAndWristJointTorquesAndGripperForce(f, t, fg)

            self.assertAlmostEqual(
                f[0],
                MockDHD.dhdSetForceAndWristJointTorquesAndGripperForce.fx
            )
            self.assertAlmostEqual(
                f[1],
                MockDHD.dhdSetForceAndWristJointTorquesAndGripperForce.fy
            )
            self.assertAlmostEqual(
                f[2],
                MockDHD.dhdSetForceAndWristJointTorquesAndGripperForce.fz
            )

            self.assertAlmostEqual(
                t[0],
                MockDHD.dhdSetForceAndWristJointTorquesAndGripperForce.q0
            )
            self.assertAlmostEqual(
                t[1],
                MockDHD.dhdSetForceAndWristJointTorquesAndGripperForce.q1
            )
            self.assertAlmostEqual(
                t[2],
                MockDHD.dhdSetForceAndWristJointTorquesAndGripperForce.q2
            )

            self.assertAlmostEqual(
                fg,
                MockDHD.dhdSetForceAndWristJointTorquesAndGripperForce.fg
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.setForceAndWristJointTorquesAndGripperForce(
                f, t, fg, ID
            ),
            MockDHD.dhdSetForceAndWristJointTorquesAndGripperForce
        )
        self.assertRetImpl(
            lambda: dhd.expert.setForceAndWristJointTorquesAndGripperForce(
                f, t, fg
            ),
            MockDHD.dhdSetForceAndWristJointTorquesAndGripperForce
        )

    def test_wristEncodersToJointAngles(self):
        self.assertSignaturesEqual(
            libdhd.dhdWristEncodersToJointAngles,
            MockDHD.dhdWristEncodersToJointAngles
        )

        libdhd.dhdWristEncodersToJointAngles = (  # type: ignore
            MockDHD.dhdWristEncodersToJointAngles.mock
        )

        enc = [0, 0, 0]
        out = [0.0, 0.0, 0.0]
        for _ in range(100):
            MockDHD.dhdWristEncodersToJointAngles.j0 = random()
            MockDHD.dhdWristEncodersToJointAngles.j1 = random()
            MockDHD.dhdWristEncodersToJointAngles.j2 = random()

            dhd.expert.wristEncodersToJointAngles(enc, out)

            self.assertAlmostEqual(
                out[0], MockDHD.dhdWristEncodersToJointAngles.j0
            )

            self.assertAlmostEqual(
                out[1], MockDHD.dhdWristEncodersToJointAngles.j1
            )

            self.assertAlmostEqual(
                out[2], MockDHD.dhdWristEncodersToJointAngles.j2
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.wristEncodersToJointAngles(
                enc, out, ID
            ),
            MockDHD.dhdWristEncodersToJointAngles
        )

        self.assertRetImpl(
            lambda: dhd.expert.wristEncodersToJointAngles(enc, out),
            MockDHD.dhdWristEncodersToJointAngles
        )

    def test_wristEncodersToJointAnglesDirect(self):
        libdhd.dhdWristEncodersToJointAngles = (  # type: ignore
            MockDHD.dhdWristEncodersToJointAngles.mock
        )

        enc = [0, 0, 0]
        out = containers.Vector3()

        for _ in range(100):
            MockDHD.dhdWristEncodersToJointAngles.j0 = random()
            MockDHD.dhdWristEncodersToJointAngles.j1 = random()
            MockDHD.dhdWristEncodersToJointAngles.j2 = random()

            dhd.expert.direct.wristEncodersToJointAngles(enc, out)

            self.assertAlmostEqual(
                out[0], MockDHD.dhdWristEncodersToJointAngles.j0
            )

            self.assertAlmostEqual(
                out[1], MockDHD.dhdWristEncodersToJointAngles.j1
            )

            self.assertAlmostEqual(
                out[2], MockDHD.dhdWristEncodersToJointAngles.j2
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.wristEncodersToJointAngles(
                enc, out, ID
            ),
            MockDHD.dhdWristEncodersToJointAngles
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.wristEncodersToJointAngles(enc, out),
            MockDHD.dhdWristEncodersToJointAngles
        )

    def test_wristJointAnglesToEncoders(self):
        self.assertSignaturesEqual(
            libdhd.dhdWristJointAnglesToEncoders,
            MockDHD.dhdWristJointAnglesToEncoders
        )

        libdhd.dhdWristJointAnglesToEncoders = (  # type: ignore
            MockDHD.dhdWristJointAnglesToEncoders.mock
        )

        joint_angles = [0.0, 0.0, 0.0]
        out = [0, 0, 0]

        for _ in range(100):
            MockDHD.dhdWristJointAnglesToEncoders.enc0 = randint(0, 100)
            MockDHD.dhdWristJointAnglesToEncoders.enc1 = randint(0, 100)
            MockDHD.dhdWristJointAnglesToEncoders.enc2 = randint(0, 100)

            dhd.expert.wristJointAnglesToEncoders(joint_angles, out)

            self.assertAlmostEqual(
                out[0], MockDHD.dhdWristJointAnglesToEncoders.enc0
            )

            self.assertAlmostEqual(
                out[1], MockDHD.dhdWristJointAnglesToEncoders.enc1
            )

            self.assertAlmostEqual(
                out[2], MockDHD.dhdWristJointAnglesToEncoders.enc2
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.wristJointAnglesToEncoders(
                joint_angles, out, ID
            ),
            MockDHD.dhdWristJointAnglesToEncoders
        )

        self.assertRetImpl(
            lambda: dhd.expert.wristJointAnglesToEncoders(joint_angles, out),
            MockDHD.dhdWristJointAnglesToEncoders
        )

    def test_wristJointAnglesToEncodersDirect(self):
        libdhd.dhdWristJointAnglesToEncoders = (  # type: ignore
            MockDHD.dhdWristJointAnglesToEncoders.mock
        )

        joint_angles = [0.0, 0.0, 0.0]
        out = containers.Enc3()

        for _ in range(100):
            MockDHD.dhdWristJointAnglesToEncoders.enc0 = randint(0, 100)
            MockDHD.dhdWristJointAnglesToEncoders.enc1 = randint(0, 100)
            MockDHD.dhdWristJointAnglesToEncoders.enc2 = randint(0, 100)

            dhd.expert.direct.wristJointAnglesToEncoders(joint_angles, out)

            self.assertAlmostEqual(
                out[0], MockDHD.dhdWristJointAnglesToEncoders.enc0
            )

            self.assertAlmostEqual(
                out[1], MockDHD.dhdWristJointAnglesToEncoders.enc1
            )

            self.assertAlmostEqual(
                out[2], MockDHD.dhdWristJointAnglesToEncoders.enc2
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.wristJointAnglesToEncoders(
                joint_angles, out, ID
            ),
            MockDHD.dhdWristJointAnglesToEncoders
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.wristJointAnglesToEncoders(joint_angles, out),
            MockDHD.dhdWristJointAnglesToEncoders
        )


    def test_getJointAngles(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetJointAngles, MockDHD.dhdGetJointAngles
        )

        libdhd.dhdGetJointAngles = MockDHD.dhdGetJointAngles.mock  # type: ignore

        joint_angles = [0.0] * MAX_DOF

        for _ in range(100):
            dhd.expert.getJointAngles(joint_angles)

            for i in range(MAX_DOF):
                self.assertAlmostEqual(
                    joint_angles[i], MockDHD.dhdGetJointAngles.joint_angles[i]
                )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.getJointAngles(joint_angles, ID),
            MockDHD.dhdGetJointAngles
        )

        self.assertRetImpl(
            lambda: dhd.expert.getJointAngles(joint_angles),
            MockDHD.dhdGetJointAngles
        )

    def test_getJointAnglesDirect(self):
        libdhd.dhdGetJointAngles = MockDHD.dhdGetJointAngles.mock  # type: ignore

        joint_angles = containers.DOFFloat()

        for _ in range(100):
            dhd.expert.direct.getJointAngles(joint_angles)

            for i in range(MAX_DOF):
                self.assertAlmostEqual(
                    joint_angles[i], MockDHD.dhdGetJointAngles.joint_angles[i]
                )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.getJointAngles(joint_angles, ID),
            MockDHD.dhdGetJointAngles
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.getJointAngles(joint_angles),
            MockDHD.dhdGetJointAngles
        )


    def test_getJointVelocities(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetJointVelocities, MockDHD.dhdGetJointVelocities
        )

        libdhd.dhdGetJointVelocities = MockDHD.dhdGetJointVelocities.mock  # type: ignore

        joint_v = [0.0] * MAX_DOF

        for _ in range(100):
            dhd.expert.getJointVelocities(joint_v)

            for i in range(MAX_DOF):
                self.assertAlmostEqual(
                    joint_v[i], MockDHD.dhdGetJointVelocities.joint_v[i]
                )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.getJointVelocities(joint_v, ID),
            MockDHD.dhdGetJointVelocities
        )

        self.assertRetImpl(
            lambda: dhd.expert.getJointVelocities(joint_v),
            MockDHD.dhdGetJointVelocities
        )

    def test_getJointVelocitiesDirect(self):
        libdhd.dhdGetJointVelocities = MockDHD.dhdGetJointVelocities.mock  # type: ignore

        joint_v = containers.DOFFloat()

        for _ in range(100):
            dhd.expert.direct.getJointVelocities(joint_v)

            for i in range(MAX_DOF):
                self.assertAlmostEqual(
                    joint_v[i], MockDHD.dhdGetJointVelocities.joint_v[i]
                )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.getJointVelocities(joint_v, ID),
            MockDHD.dhdGetJointVelocities
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.getJointVelocities(joint_v),
            MockDHD.dhdGetJointVelocities
        )

    def test_getEncVelocities(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetEncVelocities, MockDHD.dhdGetEncVelocities
        )

        libdhd.dhdGetEncVelocities = MockDHD.dhdGetEncVelocities.mock  # type: ignore

        enc_v = [0.0] * MAX_DOF

        for _ in range(100):
            dhd.expert.getEncVelocities(enc_v)

            for i in range(MAX_DOF):
                self.assertAlmostEqual(
                    enc_v[i], MockDHD.dhdGetEncVelocities.enc_v[i]
                )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.getEncVelocities(enc_v, ID),
            MockDHD.dhdGetEncVelocities
        )

        self.assertRetImpl(
            lambda: dhd.expert.getEncVelocities(enc_v),
            MockDHD.dhdGetEncVelocities
        )

    def test_getEncVelocitiesDirect(self):
        libdhd.dhdGetEncVelocities = MockDHD.dhdGetEncVelocities.mock  # type: ignore

        enc_v = containers.DOFFloat()

        for _ in range(100):
            dhd.expert.direct.getEncVelocities(enc_v)

            for i in range(MAX_DOF):
                self.assertAlmostEqual(
                    enc_v[i], MockDHD.dhdGetEncVelocities.enc_v[i]
                )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.getEncVelocities(enc_v, ID),
            MockDHD.dhdGetEncVelocities
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.getEncVelocities(enc_v),
            MockDHD.dhdGetEncVelocities
        )

    def test_jointAnglesToInertiaMatrix(self):
        self.assertSignaturesEqual(
            libdhd.dhdJointAnglesToInertiaMatrix,
            MockDHD.dhdJointAnglesToInertiaMatrix
        )

        libdhd.dhdJointAnglesToInertiaMatrix = (  # type: ignore
            MockDHD.dhdJointAnglesToInertiaMatrix.mock
        )

        joint_angles = [0.0] * MAX_DOF
        out = [[0.0] * 6] * 6

        for _ in range(100):
            for i in range(MAX_DOF):
                joint_angles[i] = random()

            for i in range(6):
                for j in range(6):
                    MockDHD.dhdJointAnglesToInertiaMatrix.inertia_matrix[i][j] = random()


            dhd.expert.jointAnglesToIntertiaMatrix(joint_angles, out)

            for i in range(MAX_DOF):
                self.assertAlmostEqual(
                    joint_angles[i],
                    MockDHD.dhdJointAnglesToInertiaMatrix.joint_angles[i]
                )

            for i in range(6):
                for j in range(6):
                    self.assertAlmostEqual(
                        out[i][j],
                        MockDHD.dhdJointAnglesToInertiaMatrix.inertia_matrix[i][j]
                    )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.jointAnglesToIntertiaMatrix(
                joint_angles, out, ID
            ),
            MockDHD.dhdJointAnglesToInertiaMatrix
        )

        self.assertRetImpl(
            lambda: dhd.expert.jointAnglesToIntertiaMatrix(
                joint_angles, out,
            ),
            MockDHD.dhdJointAnglesToInertiaMatrix
        )

    def test_jointAnglesToInertiaMatrixDirect(self):
        libdhd.dhdJointAnglesToInertiaMatrix = (  # type: ignore
            MockDHD.dhdJointAnglesToInertiaMatrix.mock
        )

        joint_angles = containers.DOFFloat()
        out = containers.Mat6x6()

        for _ in range(100):
            for i in range(MAX_DOF):
                joint_angles[i] = random()

            for i in range(6):
                for j in range(6):
                    MockDHD.dhdJointAnglesToInertiaMatrix.inertia_matrix[i][j] = random()


            dhd.expert.direct.jointAnglesToIntertiaMatrix(joint_angles, out)

            for i in range(MAX_DOF):
                self.assertAlmostEqual(
                    joint_angles[i],
                    MockDHD.dhdJointAnglesToInertiaMatrix.joint_angles[i]
                )

            for i in range(6):
                for j in range(6):
                    self.assertAlmostEqual(
                        out[i, j],
                        MockDHD.dhdJointAnglesToInertiaMatrix.inertia_matrix[i][j]
                    )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.jointAnglesToIntertiaMatrix(
                joint_angles, out, ID
            ),
            MockDHD.dhdJointAnglesToInertiaMatrix
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.jointAnglesToIntertiaMatrix(
                joint_angles, out,
            ),
            MockDHD.dhdJointAnglesToInertiaMatrix
        )

    def test_jointAnglesToGravityJointTorques(self):
        self.assertSignaturesEqual(
            libdhd.dhdJointAnglesToGravityJointTorques,
            MockDHD.dhdJointAnglesToGravityJointTorques
        )

        libdhd.dhdJointAnglesToGravityJointTorques = (  # type: ignore
            MockDHD.dhdJointAnglesToGravityJointTorques.mock
        )

        joint_angles = [0.0] * MAX_DOF
        out = [0.0] * MAX_DOF

        for _ in range(100):
            mask = randint(0, 100)

            for i in range(MAX_DOF):
                joint_angles[i] = random()
                MockDHD.dhdJointAnglesToGravityJointTorques.q[i] = random()

            dhd.expert.jointAnglesToGravityJointTorques(
                joint_angles, out, mask
            )

            for i in range(MAX_DOF):
                self.assertAlmostEqual(
                    joint_angles[i],
                    MockDHD.dhdJointAnglesToGravityJointTorques.joint_angles[i]
                )

                self.assertAlmostEqual(
                    out[i],
                    MockDHD.dhdJointAnglesToGravityJointTorques.q[i]
                )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.jointAnglesToGravityJointTorques(
                joint_angles, out, 0, ID
            ),
            MockDHD.dhdJointAnglesToGravityJointTorques
        )

        self.assertRetImpl(
            lambda: dhd.expert.jointAnglesToGravityJointTorques(
                joint_angles, out, 0
            ),
            MockDHD.dhdJointAnglesToGravityJointTorques
        )

    def test_jointAnglesToGravityJointTorquesDirect(self):
        libdhd.dhdJointAnglesToGravityJointTorques = (  # type: ignore
            MockDHD.dhdJointAnglesToGravityJointTorques.mock
        )

        joint_angles = containers.DOFFloat()
        out = containers.DOFFloat()

        for _ in range(100):
            mask = randint(0, 100)

            for i in range(MAX_DOF):
                joint_angles[i] = random()
                MockDHD.dhdJointAnglesToGravityJointTorques.q[i] = random()

            dhd.expert.direct.jointAnglesToGravityJointTorques(
                joint_angles, out, mask
            )

            for i in range(MAX_DOF):
                self.assertAlmostEqual(
                    joint_angles[i],
                    MockDHD.dhdJointAnglesToGravityJointTorques.joint_angles[i]
                )

                self.assertAlmostEqual(
                    out[i],
                    MockDHD.dhdJointAnglesToGravityJointTorques.q[i]
                )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.direct.jointAnglesToGravityJointTorques(
                joint_angles, out, 0, ID
            ),
            MockDHD.dhdJointAnglesToGravityJointTorques
        )

        self.assertRetImpl(
            lambda: dhd.expert.direct.jointAnglesToGravityJointTorques(
                joint_angles, out, 0
            ),
            MockDHD.dhdJointAnglesToGravityJointTorques
        )

    def test_setComMode(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetComMode,
            MockDHD.dhdSetComMode
        )

        libdhd.dhdSetComMode = MockDHD.dhdSetComMode.mock  # type: ignore

        for mode in ComMode:
            dhd.expert.setComMode(mode)
            self.assertEqual(mode, MockDHD.dhdSetComMode.mode)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.setComMode(ComMode.SYNC, ID),
            MockDHD.dhdSetComMode
        )

        self.assertRetImpl(
            lambda: dhd.expert.setComMode(ComMode.SYNC),
            MockDHD.dhdSetComMode
        )

    # TODO: Fix this
    def test_setComModePriority(self):
        ...

    def test_setWatchdog(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetWatchdog,
            MockDHD.dhdSetWatchdog
        )

        libdhd.dhdSetWatchdog = MockDHD.dhdSetWatchdog.mock  # type: ignore

        for duration in range(100):
            dhd.expert.setWatchdog(duration)
            self.assertEqual(duration, MockDHD.dhdSetWatchdog.duration)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.setWatchdog(0, ID),
            MockDHD.dhdSetWatchdog
        )

        self.assertRetImpl(
            lambda: dhd.expert.setWatchdog(0),
            MockDHD.dhdSetWatchdog
        )

    def test_getWatchdog(self):
        self.assertSignaturesEqual(
            libdhd.dhdSetWatchdog,
            MockDHD.dhdSetWatchdog
        )

        libdhd.dhdGetWatchdog = MockDHD.dhdGetWatchdog.mock  # type: ignore

        for duration in range(100):
            MockDHD.dhdGetWatchdog.duration = duration

            self.assertEqual(
                dhd.expert.getWatchdog(), MockDHD.dhdGetWatchdog.duration
            )

        self.assertIDImpl(
            dhd.expert.getWatchdog,
            MockDHD.dhdGetWatchdog
        )

        MockDHD.dhdGetWatchdog.ret = -1

        self.assertEqual(
            dhd.expert.getWatchdog(), -1
        )

    def test_getEncRange(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetEncRange,
            MockDHD.dhdGetEncRange
        )

        libdhd.dhdGetEncRange = MockDHD.dhdGetEncRange.mock  # type: ignore

        encMin_out = [0] * MAX_DOF
        encMax_out = [0] * MAX_DOF

        for _ in range(100):
            for i in range(MAX_DOF):
                MockDHD.dhdGetEncRange.enc_min[i] = randint(0, 100)
                MockDHD.dhdGetEncRange.enc_max[i] = randint(0, 100)

            dhd.expert.getEncRange(encMin_out, encMax_out)

            self.assertListEqual(
                encMin_out,
                MockDHD.dhdGetEncRange.enc_min
            )

            self.assertListEqual(
                encMax_out,
                MockDHD.dhdGetEncRange.enc_max
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.getEncRange(encMin_out, encMax_out, ID),
            MockDHD.dhdGetEncRange
        )

        self.assertRetImpl(
            lambda: dhd.expert.getEncRange(encMin_out, encMax_out),
            MockDHD.dhdGetEncRange
        )


    def test_getJointAngleRange(self):
        self.assertSignaturesEqual(
            libdhd.dhdGetJointAngleRange,
            MockDHD.dhdGetJointAngleRange
        )

        libdhd.dhdGetJointAngleRange = MockDHD.dhdGetJointAngleRange.mock  # type: ignore

        jmin_out = [0.0] * MAX_DOF
        jmax_out = [0.0] * MAX_DOF

        for _ in range(100):
            for i in range(MAX_DOF):
                MockDHD.dhdGetJointAngleRange.jmin[i] = randint(0, 100)
                MockDHD.dhdGetJointAngleRange.jmax[i] = randint(0, 100)

            dhd.expert.getJointAngleRange(jmin_out, jmax_out)

            self.assertListEqual(
                jmin_out,
                MockDHD.dhdGetJointAngleRange.jmin
            )

            self.assertListEqual(
                jmax_out,
                MockDHD.dhdGetJointAngleRange.jmax
            )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.getJointAngleRange(
                jmin_out, jmax_out, ID
            ),
            MockDHD.dhdGetJointAngleRange
        )

        self.assertRetImpl(
            lambda: dhd.expert.getJointAngleRange(jmin_out, jmax_out),
            MockDHD.dhdGetJointAngleRange
        )

    def test_controllerSetDevice(self):
        self.assertSignaturesEqual(
            libdhd.dhdControllerSetDevice,
            MockDHD.dhdControllerSetDevice
        )

        libdhd.dhdControllerSetDevice = (  # type: ignore
            MockDHD.dhdControllerSetDevice.mock
        )

        for devtype in DeviceType:
            dhd.expert.controllerSetDevice(devtype)
            self.assertEqual(devtype, MockDHD.dhdControllerSetDevice.device)

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.controllerSetDevice(
                DeviceType.NONE, ID
            ),
            MockDHD.dhdControllerSetDevice
        )

        self.assertRetImpl(
            lambda: dhd.expert.controllerSetDevice(DeviceType.NONE),
            MockDHD.dhdControllerSetDevice
        )

    def test_readConfigFromFile(self):
        self.assertSignaturesEqual(
            libdhd.dhdReadConfigFromFile,
            MockDHD.dhdReadConfigFromFile
        )

        libdhd.dhdReadConfigFromFile = (  # type: ignore
            MockDHD.dhdReadConfigFromFile.mock
        )

        dhd.expert.readConfigFromFile("lorem ipsem")
        self.assertEqual(
            "lorem ipsem",
            MockDHD.dhdReadConfigFromFile.filename
        )

        self.assertIDImpl(
            lambda ID = -1: dhd.expert.readConfigFromFile("", ID),
            MockDHD.dhdReadConfigFromFile
        )

        self.assertRetImpl(
            lambda ID = -1: dhd.expert.readConfigFromFile("", ID),
            MockDHD.dhdReadConfigFromFile
        )

    def test_deltaGravityJointTorques(self):
        self.assertSignaturesEqual(
            libdhd.dhdDeltaGravityJointTorques,
            MockDHD.dhdDeltaGravityJointTorques
        )

        libdhd.dhdDeltaGravityJointTorques = (  # type: ignore
            MockDHD.dhdDeltaGravityJointTorques.mock
        )

        joint_angles = [0.0] * 3
        out = [0.0] * 3

        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=DeprecationWarning)

            for _ in range(100):
                mask = randint(0, 100)

                for i in range(3):
                    joint_angles[i] = random()

                MockDHD.dhdDeltaGravityJointTorques.q0 = random()
                MockDHD.dhdDeltaGravityJointTorques.q1 = random()
                MockDHD.dhdDeltaGravityJointTorques.q2 = random()

                dhd.expert.deltaGravityJointTorques(
                    joint_angles, out, mask
                )

                self.assertAlmostEqual(
                    joint_angles[0],
                    MockDHD.dhdDeltaGravityJointTorques.j0
                )

                self.assertAlmostEqual(
                    joint_angles[1],
                    MockDHD.dhdDeltaGravityJointTorques.j1
                )

                self.assertAlmostEqual(
                    joint_angles[2],
                    MockDHD.dhdDeltaGravityJointTorques.j2
                )

                self.assertAlmostEqual(
                    out[0],
                    MockDHD.dhdDeltaGravityJointTorques.q0
                )

                self.assertAlmostEqual(
                    out[1],
                    MockDHD.dhdDeltaGravityJointTorques.q1
                )

                self.assertAlmostEqual(
                    out[2],
                    MockDHD.dhdDeltaGravityJointTorques.q2
                )

            self.assertIDImpl(
                lambda ID = -1: dhd.expert.deltaGravityJointTorques(
                    joint_angles, out, ID
                ),
                MockDHD.dhdDeltaGravityJointTorques
            )

            self.assertRetImpl(
                lambda: dhd.expert.deltaGravityJointTorques(
                    joint_angles, out
                ),
                MockDHD.dhdDeltaGravityJointTorques
            )

    def test_wristGravityJointTorques(self):
        self.assertSignaturesEqual(
            libdhd.dhdWristGravityJointTorques,
            MockDHD.dhdWristGravityJointTorques
        )

        libdhd.dhdWristGravityJointTorques = (  # type: ignore
            MockDHD.dhdWristGravityJointTorques.mock
        )

        joint_angles = [0.0] * 3
        out = [0.0] * 3

        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=DeprecationWarning)

            for _ in range(100):
                mask = randint(0, 100)

                for i in range(3):
                    joint_angles[i] = random()

                MockDHD.dhdWristGravityJointTorques.q0 = random()
                MockDHD.dhdWristGravityJointTorques.q1 = random()
                MockDHD.dhdWristGravityJointTorques.q2 = random()

                dhd.expert.wristGravityJointTorques(
                    joint_angles, out, mask
                )

                self.assertAlmostEqual(
                    joint_angles[0],
                    MockDHD.dhdWristGravityJointTorques.j0
                )

                self.assertAlmostEqual(
                    joint_angles[1],
                    MockDHD.dhdWristGravityJointTorques.j1
                )

                self.assertAlmostEqual(
                    joint_angles[2],
                    MockDHD.dhdWristGravityJointTorques.j2
                )

                self.assertAlmostEqual(
                    out[0],
                    MockDHD.dhdWristGravityJointTorques.q0
                )

                self.assertAlmostEqual(
                    out[1],
                    MockDHD.dhdWristGravityJointTorques.q1
                )

                self.assertAlmostEqual(
                    out[2],
                    MockDHD.dhdWristGravityJointTorques.q2
                )

            self.assertIDImpl(
                lambda ID = -1: dhd.expert.wristGravityJointTorques(
                    joint_angles, out, ID
                ),
                MockDHD.dhdWristGravityJointTorques
            )

            self.assertRetImpl(
                lambda: dhd.expert.wristGravityJointTorques(
                    joint_angles, out
                ),
                MockDHD.dhdWristGravityJointTorques
            )
