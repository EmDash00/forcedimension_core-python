from array import array
from ctypes import CFUNCTYPE, POINTER, c_bool, c_byte, c_double, c_int, c_ubyte
from random import randint, random
from typing import Any
import unittest
from forcedimension_core import drd, runtime

from forcedimension_core.dhd.constants import MAX_DOF, ErrorNum


libdrd = runtime._libdrd

class MockDRD:
    class drdOpen:
        argtypes = []
        restype = c_int

        is_open = False
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock():
            MockDRD.drdOpen.is_open = True
            return MockDRD.drdOpen.ret

    class drdOpenID:
        argtypes = [c_byte]
        restype = c_int

        is_open = False
        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDRD.drdOpenID.ID = ID
            MockDRD.drdOpenID.is_open = True

            return MockDRD.drdOpenID.ret

    class drdSetDevice:
        argtypes = [c_byte]
        restype = c_int
        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDRD.drdSetDevice.ID = ID

            return MockDRD.drdSetDevice.ret

    class drdGetDeviceID:
        argtypes = []
        restype = c_int

        ID: int = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock():
            return MockDRD.drdGetDeviceID.ID

    class drdClose:
        argtypes = [c_byte]
        restype = c_int

        is_open: bool = True

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDRD.drdClose.ID = ID

            MockDRD.drdClose.is_open = False

            return MockDRD.drdClose.ret


    class drdIsSupported:
        argtypes = [c_byte]
        restype = c_bool

        ID = 0
        ret = False

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDRD.drdIsSupported.ID = ID

            return MockDRD.drdIsSupported.ret

    class drdIsRunning:
        argtypes = [c_byte]
        restype = c_bool

        ID = 0
        ret = False

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDRD.drdIsRunning.ID = ID

            return MockDRD.drdIsRunning.ret

    class drdIsMoving:
        argtypes = [c_byte]
        restype = c_bool

        ID = 0
        ret = False

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDRD.drdIsMoving.ID = ID

            return MockDRD.drdIsMoving.ret

    class drdIsFiltering:
        argtypes = [c_byte]
        restype = c_bool

        ID = 0
        ret = False

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDRD.drdIsFiltering.ID = ID

            return MockDRD.drdIsFiltering.ret

    class drdWaitForTick:
        argtypes = [c_byte]
        restype = None

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDRD.drdWaitForTick.ID = ID

    class drdIsInitialized:
        argtypes = [c_byte]
        restype = c_bool

        ID = 0
        ret = False

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDRD.drdIsInitialized.ID = ID

            return MockDRD.drdIsInitialized.ret

    class drdAutoInit:
        argtypes = [c_byte]
        restype = c_int

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDRD.drdAutoInit.ID = ID

            return MockDRD.drdAutoInit.ret

    class drdCheckInit:
        argtypes = [c_byte]
        restype = c_int

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDRD.drdCheckInit.ID = ID

            return MockDRD.drdCheckInit.ret

    class drdPrecisionInit:
        argtypes = [c_byte]
        restype = c_int

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDRD.drdPrecisionInit.ID = ID

            return MockDRD.drdPrecisionInit.ret


    class drdGetPositionAndOrientation:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double),
            POINTER(c_double), POINTER(c_double), POINTER(c_double),
            POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        px: float = 0
        py: float = 0
        pz: float = 0

        oa: float = 0
        ob: float = 0
        og: float = 0

        pg: float = 0

        frame = [[0.0] * 3] * 3

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(px, py, pz, oa, ob, og, pg, frame, ID):
            MockDRD.drdGetPositionAndOrientation.ID = ID

            px.contents.value = MockDRD.drdGetPositionAndOrientation.px
            py.contents.value = MockDRD.drdGetPositionAndOrientation.py
            pz.contents.value = MockDRD.drdGetPositionAndOrientation.pz

            pg.contents.value = MockDRD.drdGetPositionAndOrientation.pg

            oa.contents.value = MockDRD.drdGetPositionAndOrientation.oa
            ob.contents.value = MockDRD.drdGetPositionAndOrientation.ob
            og.contents.value = MockDRD.drdGetPositionAndOrientation.og

            for i in range(3):
                for j in range(3):
                    frame[3 * i + j] = MockDRD.drdGetPositionAndOrientation.frame[i][j]

            return MockDRD.drdGetPositionAndOrientation.ret

    class drdGetVelocity:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double),
            POINTER(c_double), POINTER(c_double), POINTER(c_double),
            POINTER(c_double), c_byte
        ]
        restype = c_int

        vx: float = 0
        vy: float = 0
        vz: float = 0

        wx: float = 0
        wy: float = 0
        wz: float = 0

        vg: float

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(vx, vy, vz, wx, wy, wz, vg, ID):
            MockDRD.drdGetVelocity.ID = ID

            vx.contents.value = MockDRD.drdGetVelocity.vx
            vy.contents.value = MockDRD.drdGetVelocity.vy
            vz.contents.value = MockDRD.drdGetVelocity.vz

            wx.contents.value = MockDRD.drdGetVelocity.wx
            wy.contents.value = MockDRD.drdGetVelocity.wy
            wz.contents.value = MockDRD.drdGetVelocity.wz

            vg.contents.value = MockDRD.drdGetVelocity.vg

            return MockDRD.drdGetVelocity.ret

    class drdGetCtrlFreq:
        argtypes = [c_byte]
        restype = c_double

        ID = 0
        ret: float = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDRD.drdGetCtrlFreq.ID = ID
            return MockDRD.drdGetCtrlFreq.ret

    class drdStart:
        argtypes = [c_byte]
        restype = c_int

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDRD.drdStart.ID = ID
            return MockDRD.drdStart.ret

    class drdRegulatePos:
        argtypes = [c_bool, c_byte]
        restype = c_int

        enable = False

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enable, ID):
            MockDRD.drdRegulatePos.ID = ID
            MockDRD.drdRegulatePos.enable = enable

            return MockDRD.drdRegulatePos.ret

    class drdRegulateRot:
        argtypes = [c_bool, c_byte]
        restype = c_int

        enable = False

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enable, ID):
            MockDRD.drdRegulateRot.ID = ID
            MockDRD.drdRegulateRot.enable = enable

            return MockDRD.drdRegulateRot.ret

    class drdRegulateGrip:
        argtypes = [c_bool, c_byte]
        restype = c_int

        enable = False

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enable, ID):
            MockDRD.drdRegulateGrip.ID = ID
            MockDRD.drdRegulateGrip.enable = enable

            return MockDRD.drdRegulateGrip.ret

    class drdSetForceAndTorqueAndGripperForce:
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
            MockDRD.drdSetForceAndTorqueAndGripperForce.ID = ID

            MockDRD.drdSetForceAndTorqueAndGripperForce.fx = fx
            MockDRD.drdSetForceAndTorqueAndGripperForce.fy = fy
            MockDRD.drdSetForceAndTorqueAndGripperForce.fz = fz

            MockDRD.drdSetForceAndTorqueAndGripperForce.tx = tx
            MockDRD.drdSetForceAndTorqueAndGripperForce.ty = ty
            MockDRD.drdSetForceAndTorqueAndGripperForce.tz = tz

            MockDRD.drdSetForceAndTorqueAndGripperForce.fg = fg

            return MockDRD.drdSetForceAndTorqueAndGripperForce.ret

    class drdSetForceAndWristJointTorquesAndGripperForce:
        argtypes = [
            c_double, c_double, c_double, c_double,
            c_double, c_double, c_double, c_byte
        ]
        restype = c_int

        fx: float = 0
        fy: float = 0
        fz: float = 0

        q0: float = 0
        q1: float = 0
        q2: float = 0

        fg = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(fx, fy, fz, t0, t1, t2, fg, ID):
            MockDRD.drdSetForceAndWristJointTorquesAndGripperForce.ID = ID

            MockDRD.drdSetForceAndWristJointTorquesAndGripperForce.fx = fx
            MockDRD.drdSetForceAndWristJointTorquesAndGripperForce.fy = fy
            MockDRD.drdSetForceAndWristJointTorquesAndGripperForce.fz = fz

            MockDRD.drdSetForceAndWristJointTorquesAndGripperForce.q0 = t0
            MockDRD.drdSetForceAndWristJointTorquesAndGripperForce.q1 = t1
            MockDRD.drdSetForceAndWristJointTorquesAndGripperForce.q2 = t2

            MockDRD.drdSetForceAndWristJointTorquesAndGripperForce.fg = fg

            return MockDRD.drdSetForceAndWristJointTorquesAndGripperForce.ret

    class drdEnableFilter:
        argtypes = [c_bool, c_byte]
        restype = c_int

        enable = False

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enable, ID):
            MockDRD.drdEnableFilter.ID = ID
            MockDRD.drdEnableFilter.enable = enable

            return MockDRD.drdEnableFilter.ret

    class drdMoveToPos:
        argtypes = [c_double, c_double, c_double, c_bool, c_byte]
        restype = c_int

        px = 0
        py = 0
        pz = 0

        block = False

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(px, py, pz, block, ID):
            MockDRD.drdMoveToPos.ID = ID

            MockDRD.drdMoveToPos.px = px
            MockDRD.drdMoveToPos.py = py
            MockDRD.drdMoveToPos.pz = pz

            MockDRD.drdMoveToPos.block = block

            return MockDRD.drdMoveToPos.ret

    class drdMoveToRot:
        argtypes = [c_double, c_double, c_double, c_bool, c_byte]
        restype = c_int

        oa = 0
        ob = 0
        og = 0

        block = False

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(oa, ob, og, block, ID):
            MockDRD.drdMoveToRot.ID = ID

            MockDRD.drdMoveToRot.oa = oa
            MockDRD.drdMoveToRot.ob = ob
            MockDRD.drdMoveToRot.og = og

            MockDRD.drdMoveToRot.block = block

            return MockDRD.drdMoveToRot.ret

    class drdMoveToGrip:
        argtypes = [c_double, c_bool, c_byte]
        restype = c_int

        pg = 0
        block = False

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(pg, block, ID):
            MockDRD.drdMoveToGrip.ID = ID

            MockDRD.drdMoveToGrip.pg = pg

            MockDRD.drdMoveToGrip.block = block

            return MockDRD.drdMoveToGrip.ret

    class drdMoveTo:
        argtypes = [POINTER(c_double), c_bool, c_byte]
        restype = c_int

        p = [0.0] * MAX_DOF
        block = False

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(p, block, ID):
            MockDRD.drdMoveTo.ID = ID

            for i in range(MAX_DOF):
                MockDRD.drdMoveTo.p[i] = p[i]

            MockDRD.drdMoveTo.block = block

            return MockDRD.drdMoveTo.ret

    class drdMoveToEnc:
        argtypes = [c_int, c_int, c_int, c_bool, c_byte]
        restype = c_int

        enc0 = 0
        enc1 = 0
        enc2 = 0

        block = False

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enc0, enc1, enc3, block, ID):
            MockDRD.drdMoveToEnc.ID = ID

            MockDRD.drdMoveToEnc.enc0 = enc0
            MockDRD.drdMoveToEnc.enc1 = enc1
            MockDRD.drdMoveToEnc.enc2 = enc3

            MockDRD.drdMoveToEnc.block = block

            return MockDRD.drdMoveToEnc.ret

    class drdMoveToAllEnc:
        argtypes = [POINTER(c_int), c_bool, c_byte]
        restype = c_int

        enc = array('i', (0 for _ in range(MAX_DOF)))
        block = False

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enc, block, ID):
            MockDRD.drdMoveToAllEnc.ID = ID

            for i in range(MAX_DOF):
                MockDRD.drdMoveToAllEnc.enc[i] = enc[i]

            MockDRD.drdMoveToAllEnc.block = block

            return MockDRD.drdMoveToAllEnc.ret

    class drdTrackPos:
        argtypes = [c_double, c_double, c_double, c_byte]
        restype = c_int

        px = 0
        py = 0
        pz = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(px, py, pz, ID):
            MockDRD.drdTrackPos.ID = ID

            MockDRD.drdTrackPos.px = px
            MockDRD.drdTrackPos.py = py
            MockDRD.drdTrackPos.pz = pz

            return MockDRD.drdTrackPos.ret

    class drdTrackRot:
        argtypes = [c_double, c_double, c_double, c_byte]
        restype = c_int

        oa = 0
        ob = 0
        og = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(oa, ob, og, ID):
            MockDRD.drdTrackRot.ID = ID

            MockDRD.drdTrackRot.oa = oa
            MockDRD.drdTrackRot.ob = ob
            MockDRD.drdTrackRot.og = og

            return MockDRD.drdTrackRot.ret

    class drdTrackGrip:
        argtypes = [c_double, c_byte]
        restype = c_int

        pg = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(pg, ID):
            MockDRD.drdTrackGrip.ID = ID

            MockDRD.drdTrackGrip.pg = pg

            return MockDRD.drdTrackGrip.ret

    class drdTrack:
        argtypes = [POINTER(c_double), c_byte]
        restype = c_int

        p = array('d', (0.0 for _ in range(MAX_DOF)))

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(p, ID):
            MockDRD.drdTrack.ID = ID

            for i in range(MAX_DOF):
                MockDRD.drdTrack.p[i] = p[i]

            return MockDRD.drdTrack.ret

    class drdTrackEnc:
        argtypes = [c_int, c_int, c_int, c_byte]
        restype = c_int

        enc0: int = 0
        enc1: int = 0
        enc2: int = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enc0, enc1, enc2, ID):
            MockDRD.drdTrackEnc.ID = ID

            MockDRD.drdTrackEnc.enc0 = enc0
            MockDRD.drdTrackEnc.enc1 = enc1
            MockDRD.drdTrackEnc.enc2 = enc2

            return MockDRD.drdTrackEnc.ret

    class drdTrackAllEnc:
        argtypes = [POINTER(c_int), c_byte]
        restype = c_int

        enc = array('i', (0 for _ in range(MAX_DOF)))

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(enc, ID):
            MockDRD.drdTrackAllEnc.ID = ID

            for i in range(MAX_DOF):
                MockDRD.drdTrackAllEnc.enc[i] = enc[i]

            return MockDRD.drdTrackAllEnc.ret

    class drdHold:
        argtypes = [c_byte]
        restype = c_int

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDRD.drdHold.ID = ID

            return MockDRD.drdHold.ret

    class drdLock:
        argtypes = [c_ubyte, c_bool, c_byte]
        restype = c_int

        mask = 0
        init = False

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(mask, init, ID):
            MockDRD.drdLock.ID = ID

            MockDRD.drdLock.mask = mask
            MockDRD.drdLock.init = init

            return MockDRD.drdLock.ret


    class drdStop:
        argtypes = [c_bool, c_byte]
        restype = c_int

        frc: bool = False

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(frc, ID):
            MockDRD.drdStop.ID = ID
            MockDRD.drdStop.frc = frc

            return MockDRD.drdStop.ret

    class drdGetPriorities:
        argtypes = [POINTER(c_int), POINTER(c_int), c_byte]
        restype = c_int

        prio = 0
        ctrlprio = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(prio, ctrlprio, ID):
            MockDRD.drdGetPriorities.ID = ID

            prio.contents.value = MockDRD.drdGetPriorities.prio
            ctrlprio.contents.value = MockDRD.drdGetPriorities.ctrlprio

            return MockDRD.drdGetPriorities.ret

    class drdSetPriorities:
        argtypes = [c_int, c_int, c_byte]
        restype = c_int

        prio = 0
        ctrlprio = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(prio, ctrlprio, ID):
            MockDRD.drdSetPriorities.ID = ID

            MockDRD.drdSetPriorities.prio = prio
            MockDRD.drdSetPriorities.ctrlprio = ctrlprio

            return MockDRD.drdSetPriorities.ret

    class drdSetEncPGain:
        argtypes = [c_double, c_byte]
        restype = c_int

        gain = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(gain, ID):
            MockDRD.drdSetEncPGain.ID = ID
            MockDRD.drdSetEncPGain.gain = gain

            return MockDRD.drdSetEncPGain.ret

    class drdGetEncPGain:
        argtypes = [c_byte]
        restype = c_double

        ID = 0
        gain: float = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDRD.drdGetEncPGain.ID = ID

            return MockDRD.drdGetEncPGain.gain


    class drdSetEncIGain:
        argtypes = [c_double, c_byte]
        restype = c_int

        gain = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(gain, ID):
            MockDRD.drdSetEncIGain.ID = ID
            MockDRD.drdSetEncIGain.gain = gain

            return MockDRD.drdSetEncIGain.ret

    class drdGetEncIGain:
        argtypes = [c_byte]
        restype = c_double

        ID = 0
        gain: float = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDRD.drdGetEncIGain.ID = ID

            return MockDRD.drdGetEncIGain.gain

    class drdSetEncDGain:
        argtypes = [c_double, c_byte]
        restype = c_int

        gain = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(gain, ID):
            MockDRD.drdSetEncDGain.ID = ID
            MockDRD.drdSetEncDGain.gain = gain

            return MockDRD.drdSetEncDGain.ret

    class drdGetEncDGain:
        argtypes = [c_byte]
        restype = c_double

        ID = 0
        gain: float = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDRD.drdGetEncDGain.ID = ID

            return MockDRD.drdGetEncDGain.gain

    class drdSetMotRatioMax:
        argtypes = [c_double, c_byte]
        restype = c_int

        scale = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(scale, ID):
            MockDRD.drdSetMotRatioMax.ID = ID
            MockDRD.drdSetMotRatioMax.scale = scale

            return MockDRD.drdSetMotRatioMax.ret

    class drdGetMotRatioMax:
        argtypes = [c_byte]
        restype = c_double

        ID = 0
        scale: float = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(ID):
            MockDRD.drdGetMotRatioMax.ID = ID

            return MockDRD.drdGetMotRatioMax.scale

    class drdSetEncMoveParam:
        argtypes = [c_double, c_double, c_double, c_byte]
        restype = c_int

        vmax = 0
        amax = 0
        jerk = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(amax, vmax, jerk, ID):
            MockDRD.drdSetEncMoveParam.ID = ID

            MockDRD.drdSetEncMoveParam.vmax = vmax
            MockDRD.drdSetEncMoveParam.amax = amax
            MockDRD.drdSetEncMoveParam.jerk = jerk

            return MockDRD.drdSetEncMoveParam.ret

    class drdSetEncTrackParam:
        argtypes = [c_double, c_double, c_double, c_byte]
        restype = c_int

        vmax = 0
        amax = 0
        jerk = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(amax, vmax, jerk, ID):
            MockDRD.drdSetEncTrackParam.ID = ID

            MockDRD.drdSetEncTrackParam.vmax = vmax
            MockDRD.drdSetEncTrackParam.amax = amax
            MockDRD.drdSetEncTrackParam.jerk = jerk

            return MockDRD.drdSetEncTrackParam.ret

    class drdSetPosMoveParam:
        argtypes = [c_double, c_double, c_double, c_byte]
        restype = c_int

        vmax = 0
        amax = 0
        jerk = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(amax, vmax, jerk, ID):
            MockDRD.drdSetPosMoveParam.ID = ID

            MockDRD.drdSetPosMoveParam.vmax = vmax
            MockDRD.drdSetPosMoveParam.amax = amax
            MockDRD.drdSetPosMoveParam.jerk = jerk

            return MockDRD.drdSetPosMoveParam.ret

    class drdSetPosTrackParam:
        argtypes = [c_double, c_double, c_double, c_byte]
        restype = c_int

        vmax = 0
        amax = 0
        jerk = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(amax, vmax, jerk, ID):
            MockDRD.drdSetPosTrackParam.ID = ID

            MockDRD.drdSetPosTrackParam.vmax = vmax
            MockDRD.drdSetPosTrackParam.amax = amax
            MockDRD.drdSetPosTrackParam.jerk = jerk

            return MockDRD.drdSetPosTrackParam.ret

    class drdSetRotMoveParam:
        argtypes = [c_double, c_double, c_double, c_byte]
        restype = c_int

        vmax = 0
        amax = 0
        jerk = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(amax, vmax, jerk, ID):
            MockDRD.drdSetRotMoveParam.ID = ID

            MockDRD.drdSetRotMoveParam.vmax = vmax
            MockDRD.drdSetRotMoveParam.amax = amax
            MockDRD.drdSetRotMoveParam.jerk = jerk

            return MockDRD.drdSetRotMoveParam.ret

    class drdSetRotTrackParam:
        argtypes = [c_double, c_double, c_double, c_byte]
        restype = c_int

        vmax = 0
        amax = 0
        jerk = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(amax, vmax, jerk, ID):
            MockDRD.drdSetRotTrackParam.ID = ID

            MockDRD.drdSetRotTrackParam.vmax = vmax
            MockDRD.drdSetRotTrackParam.amax = amax
            MockDRD.drdSetRotTrackParam.jerk = jerk

            return MockDRD.drdSetRotTrackParam.ret

    class drdSetGripMoveParam:
        argtypes = [c_double, c_double, c_double, c_byte]
        restype = c_int

        vmax = 0
        amax = 0
        jerk = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(amax, vmax, jerk, ID):
            MockDRD.drdSetGripMoveParam.ID = ID

            MockDRD.drdSetGripMoveParam.vmax = vmax
            MockDRD.drdSetGripMoveParam.amax = amax
            MockDRD.drdSetGripMoveParam.jerk = jerk

            return MockDRD.drdSetGripMoveParam.ret

    class drdSetGripTrackParam:
        argtypes = [c_double, c_double, c_double, c_byte]
        restype = c_int

        vmax = 0
        amax = 0
        jerk = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(amax, vmax, jerk, ID):
            MockDRD.drdSetGripTrackParam.ID = ID

            MockDRD.drdSetGripTrackParam.vmax = vmax
            MockDRD.drdSetGripTrackParam.amax = amax
            MockDRD.drdSetGripTrackParam.jerk = jerk

            return MockDRD.drdSetGripTrackParam.ret

    class drdGetEncMoveParam:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        vmax: float = 0
        amax: float = 0
        jerk: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(amax, vmax, jerk, ID):
            MockDRD.drdGetEncMoveParam.ID = ID

            vmax.contents.value = MockDRD.drdGetEncMoveParam.vmax
            amax.contents.value = MockDRD.drdGetEncMoveParam.amax
            jerk.contents.value = MockDRD.drdGetEncMoveParam.jerk

            return MockDRD.drdGetEncMoveParam.ret

    class drdGetEncTrackParam:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        vmax: float = 0
        amax: float = 0
        jerk: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(amax, vmax, jerk, ID):
            MockDRD.drdGetEncTrackParam.ID = ID

            vmax.contents.value = MockDRD.drdGetEncTrackParam.vmax
            amax.contents.value = MockDRD.drdGetEncTrackParam.amax
            jerk.contents.value = MockDRD.drdGetEncTrackParam.jerk

            return MockDRD.drdGetEncTrackParam.ret

    class drdGetPosMoveParam:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        vmax: float = 0
        amax: float = 0
        jerk: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(amax, vmax, jerk, ID):
            MockDRD.drdGetPosMoveParam.ID = ID

            vmax.contents.value = MockDRD.drdGetPosMoveParam.vmax
            amax.contents.value = MockDRD.drdGetPosMoveParam.amax
            jerk.contents.value = MockDRD.drdGetPosMoveParam.jerk

            return MockDRD.drdGetPosMoveParam.ret

    class drdGetPosTrackParam:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        vmax: float = 0
        amax: float = 0
        jerk: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(amax, vmax, jerk, ID):
            MockDRD.drdGetPosTrackParam.ID = ID

            vmax.contents.value = MockDRD.drdGetPosTrackParam.vmax
            amax.contents.value = MockDRD.drdGetPosTrackParam.amax
            jerk.contents.value = MockDRD.drdGetPosTrackParam.jerk

            return MockDRD.drdGetPosTrackParam.ret

    class drdGetRotMoveParam:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        vmax: float = 0
        amax: float = 0
        jerk: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(amax, vmax, jerk, ID):
            MockDRD.drdGetRotMoveParam.ID = ID

            vmax.contents.value = MockDRD.drdGetRotMoveParam.vmax
            amax.contents.value = MockDRD.drdGetRotMoveParam.amax
            jerk.contents.value = MockDRD.drdGetRotMoveParam.jerk

            return MockDRD.drdGetRotMoveParam.ret

    class drdGetRotTrackParam:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        vmax: float = 0
        amax: float = 0
        jerk: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(amax, vmax, jerk, ID):
            MockDRD.drdGetRotTrackParam.ID = ID

            vmax.contents.value = MockDRD.drdGetRotTrackParam.vmax
            amax.contents.value = MockDRD.drdGetRotTrackParam.amax
            jerk.contents.value = MockDRD.drdGetRotTrackParam.jerk

            return MockDRD.drdGetRotTrackParam.ret

    class drdGetGripMoveParam:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        vmax: float = 0
        amax: float = 0
        jerk: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(amax, vmax, jerk, ID):
            MockDRD.drdGetGripMoveParam.ID = ID

            vmax.contents.value = MockDRD.drdGetGripMoveParam.vmax
            amax.contents.value = MockDRD.drdGetGripMoveParam.amax
            jerk.contents.value = MockDRD.drdGetGripMoveParam.jerk

            return MockDRD.drdGetGripMoveParam.ret

    class drdGetGripTrackParam:
        argtypes = [
            POINTER(c_double), POINTER(c_double), POINTER(c_double), c_byte
        ]
        restype = c_int

        vmax: float = 0
        amax: float = 0
        jerk: float = 0

        ID = 0
        ret = 0

        @staticmethod
        @CFUNCTYPE(restype, *argtypes)
        def mock(amax, vmax, jerk, ID):
            MockDRD.drdGetGripTrackParam.ID = ID

            vmax.contents.value = MockDRD.drdGetGripTrackParam.vmax
            amax.contents.value = MockDRD.drdGetGripTrackParam.amax
            jerk.contents.value = MockDRD.drdGetGripTrackParam.jerk

            return MockDRD.drdGetGripTrackParam.ret

class TestRoboticSDK(unittest.TestCase):
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

    def test_open(self):
        self.assertSignaturesEqual(libdrd.drdOpen, MockDRD.drdOpen)
        libdrd.drdOpen = MockDRD.drdOpen.mock  # type: ignore

        drd.open()
        self.assertTrue(MockDRD.drdOpen.is_open)

        self.assertRetImpl(drd.open, MockDRD.drdOpen)


    def test_openID(self):
        self.assertSignaturesEqual(libdrd.drdOpenID, MockDRD.drdOpenID)
        libdrd.drdOpenID = MockDRD.drdOpenID.mock  # type: ignore

        drd.openID(0)
        self.assertTrue(MockDRD.drdOpenID.is_open)

        for ID in range(100):
            drd.openID(ID)
            self.assertEqual(ID, MockDRD.drdOpenID.ID)

        self.assertRetImpl(lambda: drd.openID(ID), MockDRD.drdOpenID)


    def test_setDevice(self):
        self.assertSignaturesEqual(
            libdrd.drdSetDevice, MockDRD.drdSetDevice
        )

        libdrd.drdSetDevice = MockDRD.drdSetDevice.mock  # type: ignore

        for ID in range(100):
            drd.setDevice(ID)
            self.assertEqual(ID, MockDRD.drdSetDevice.ID)

        self.assertRetImpl(lambda: drd.setDevice(0), MockDRD.drdSetDevice)


    def test_getDeviceID(self):
        self.assertSignaturesEqual(
            libdrd.drdGetDeviceID, MockDRD.drdGetDeviceID
        )

        libdrd.drdGetDeviceID = MockDRD.drdGetDeviceID.mock  # type: ignore

        for ID in range(100):
            MockDRD.drdGetDeviceID.ID = ID
            self.assertEqual(drd.getDeviceID(), ID)

    def test_close(self):
        self.assertSignaturesEqual(libdrd.drdClose, MockDRD.drdClose)

        libdrd.drdClose = MockDRD.drdClose.mock  # type: ignore
        MockDRD.drdClose.is_open = True
        drd.close()

        self.assertFalse(MockDRD.drdClose.is_open)

        self.assertIDImpl(drd.close, MockDRD.drdClose)
        self.assertRetImpl(lambda: drd.close(0), MockDRD.drdClose)

    def test_isSupported(self):
        self.assertSignaturesEqual(
            libdrd.drdIsSupported,
            MockDRD.drdIsSupported
        )

        libdrd.drdIsSupported = MockDRD.drdIsSupported.mock  # type: ignore

        MockDRD.drdIsSupported.ret = False
        self.assertFalse(drd.isSupported())

        MockDRD.drdIsSupported.ret = True
        self.assertTrue(drd.isSupported())

        self.assertIDImpl(drd.isSupported, MockDRD.drdIsSupported)

    def test_isRunning(self):
        self.assertSignaturesEqual(
            libdrd.drdIsRunning,
            MockDRD.drdIsRunning
        )

        libdrd.drdIsRunning = MockDRD.drdIsRunning.mock  # type: ignore

        MockDRD.drdIsRunning.ret = False
        self.assertFalse(drd.isRunning())

        MockDRD.drdIsRunning.ret = True
        self.assertTrue(drd.isRunning())

        self.assertIDImpl(drd.isRunning, MockDRD.drdIsRunning)

    def test_isMoving(self):
        self.assertSignaturesEqual(
            libdrd.drdIsMoving,
            MockDRD.drdIsMoving
        )

        libdrd.drdIsMoving = MockDRD.drdIsMoving.mock  # type: ignore

        MockDRD.drdIsMoving.ret = False
        self.assertFalse(drd.isMoving())

        MockDRD.drdIsMoving.ret = True
        self.assertTrue(drd.isMoving())

        self.assertIDImpl(drd.isMoving, MockDRD.drdIsMoving)

    def test_isFiltering(self):
        self.assertSignaturesEqual(
            libdrd.drdIsMoving,
            MockDRD.drdIsMoving
        )

        libdrd.drdIsMoving = MockDRD.drdIsMoving.mock  # type: ignore

        MockDRD.drdIsMoving.ret = False
        self.assertFalse(drd.isMoving())

        MockDRD.drdIsMoving.ret = True
        self.assertTrue(drd.isMoving())

        self.assertIDImpl(drd.isMoving, MockDRD.drdIsMoving)

    def test_waitForTick(self):
        self.assertSignaturesEqual(
            libdrd.drdWaitForTick,
            MockDRD.drdWaitForTick
        )

        libdrd.drdWaitForTick = MockDRD.drdWaitForTick.mock  # type: ignore

        self.assertIDImpl(
            drd.waitForTick,
            MockDRD.drdWaitForTick
        )

    def test_isIntialized(self):
        self.assertSignaturesEqual(
            libdrd.drdIsInitialized,
            MockDRD.drdIsInitialized
        )

        libdrd.drdIsInitialized = MockDRD.drdIsInitialized.mock  # type: ignore

        MockDRD.drdIsInitialized.ret = False
        self.assertFalse(drd.isInitialized())

        MockDRD.drdIsInitialized.ret = True
        self.assertTrue(drd.isInitialized())

        self.assertIDImpl(drd.isInitialized, MockDRD.drdIsInitialized)

    def test_autoInit(self):
        self.assertSignaturesEqual(
            libdrd.drdAutoInit,
            MockDRD.drdAutoInit
        )

        libdrd.drdAutoInit = MockDRD.drdAutoInit.mock  # type: ignore

        self.assertIDImpl(
            drd.autoInit,
            MockDRD.drdAutoInit
        )

        self.assertRetImpl(
            drd.autoInit,
            MockDRD.drdAutoInit
        )

    def test_checkInit(self):
        self.assertSignaturesEqual(
            libdrd.drdCheckInit,
            MockDRD.drdCheckInit
        )

        libdrd.drdCheckInit = MockDRD.drdCheckInit.mock  # type: ignore

        self.assertIDImpl(
            drd.checkInit,
            MockDRD.drdCheckInit
        )

        self.assertRetImpl(
            drd.checkInit,
            MockDRD.drdCheckInit
        )


    def test_precisionInit(self):
        self.assertSignaturesEqual(
            libdrd.drdPrecisionInit,
            MockDRD.drdPrecisionInit
        )

        libdrd.drdPrecisionInit = MockDRD.drdPrecisionInit.mock  # type: ignore

        self.assertIDImpl(
            drd.precisionInit,
            MockDRD.drdPrecisionInit
        )

        self.assertRetImpl(
            drd.precisionInit,
            MockDRD.drdPrecisionInit
        )

    def test_getPositionAndOrientation(self):
        self.assertSignaturesEqual(
            libdrd.drdGetPositionAndOrientation,
            MockDRD.drdGetPositionAndOrientation
        )

        libdrd.drdGetPositionAndOrientation = (  # type: ignore
            MockDRD.drdGetPositionAndOrientation.mock
        )

        p_out = [0.0, 0.0, 0.0]
        o_out = [0.0, 0.0, 0.0]
        pg_out = c_double()
        frame = [[0.0] * 3] * 3

        for _ in range(100):
            for i in range(3):
                for j in range(3):
                    MockDRD.drdGetPositionAndOrientation.frame[i][j] = (
                        random()
                    )

            MockDRD.drdGetPositionAndOrientation.oa = random()
            MockDRD.drdGetPositionAndOrientation.ob = random()
            MockDRD.drdGetPositionAndOrientation.og = random()

            MockDRD.drdGetPositionAndOrientation.px = random()
            MockDRD.drdGetPositionAndOrientation.py = random()
            MockDRD.drdGetPositionAndOrientation.pz = random()

            drd.getPositionAndOrientation(p_out, o_out, pg_out, frame)

            self.assertAlmostEqual(
                p_out[0], MockDRD.drdGetPositionAndOrientation.px
            )
            self.assertAlmostEqual(
                p_out[1], MockDRD.drdGetPositionAndOrientation.py
            )
            self.assertAlmostEqual(
                p_out[2], MockDRD.drdGetPositionAndOrientation.pz
            )

            self.assertAlmostEqual(
                o_out[0], MockDRD.drdGetPositionAndOrientation.oa
            )
            self.assertAlmostEqual(
                o_out[1], MockDRD.drdGetPositionAndOrientation.ob
            )
            self.assertAlmostEqual(
                o_out[2], MockDRD.drdGetPositionAndOrientation.og
            )

            for i in range(3):
                for j in range(3):
                    self.assertAlmostEqual(
                        frame[i][j],
                        MockDRD.drdGetPositionAndOrientation.frame[i][j]
                    )

        self.assertIDImpl(
            lambda ID = -1: drd.getPositionAndOrientation(
                p_out, o_out, pg_out, frame, ID
            ),
            MockDRD.drdGetPositionAndOrientation
        )
        self.assertRetImpl(
            lambda: drd.getPositionAndOrientation(p_out, o_out, pg_out, frame),
            MockDRD.drdGetPositionAndOrientation
        )

    def test_getVelocity(self):
        self.assertSignaturesEqual(
            libdrd.drdGetVelocity,
            MockDRD.drdGetVelocity
        )

        libdrd.drdGetVelocity = (  # type: ignore
            MockDRD.drdGetVelocity.mock
        )

        v_out = [0.0, 0.0, 0.0]
        w_out = [0.0, 0.0, 0.0]
        vg_out = c_double()

        for _ in range(100):
            MockDRD.drdGetVelocity.vx = random()
            MockDRD.drdGetVelocity.vy = random()
            MockDRD.drdGetVelocity.vz = random()

            MockDRD.drdGetVelocity.wx = random()
            MockDRD.drdGetVelocity.wy = random()
            MockDRD.drdGetVelocity.wz = random()

            MockDRD.drdGetVelocity.vg = random()

            drd.getVelocity(v_out, w_out, vg_out)

            self.assertEqual(v_out[0], MockDRD.drdGetVelocity.vx)
            self.assertEqual(v_out[1], MockDRD.drdGetVelocity.vy)
            self.assertEqual(v_out[2], MockDRD.drdGetVelocity.vz)

            self.assertEqual(w_out[0], MockDRD.drdGetVelocity.wx)
            self.assertEqual(w_out[1], MockDRD.drdGetVelocity.wy)
            self.assertEqual(w_out[2], MockDRD.drdGetVelocity.wz)

            self.assertEqual(vg_out.value, MockDRD.drdGetVelocity.vg)

        self.assertIDImpl(
            lambda ID = -1: drd.getVelocity(v_out, w_out, vg_out, ID),
            MockDRD.drdGetVelocity
        )
        self.assertRetImpl(
            lambda: drd.getVelocity(v_out, w_out, vg_out),
            MockDRD.drdGetVelocity
        )


    def test_getCtrlFreq(self):
        self.assertSignaturesEqual(
            libdrd.drdGetCtrlFreq, MockDRD.drdGetCtrlFreq
        )

        libdrd.drdGetCtrlFreq = MockDRD.drdGetCtrlFreq.mock  # type: ignore

        for _ in range(100):
            MockDRD.drdGetCtrlFreq.ret = random()
            self.assertEqual(drd.getCtrlFreq(), MockDRD.drdGetCtrlFreq.ret)

        self.assertIDImpl(drd.getCtrlFreq, MockDRD.drdGetCtrlFreq)

    def test_start(self):
        self.assertSignaturesEqual(
            libdrd.drdStart,
            MockDRD.drdStart
        )

        libdrd.drdStart = MockDRD.drdStart.mock  # type: ignore

        self.assertIDImpl(
            drd.start,
            MockDRD.drdStart
        )

        self.assertRetImpl(
            drd.start,
            MockDRD.drdStart
        )

    def test_regulatePos(self):
        self.assertSignaturesEqual(
            libdrd.drdRegulatePos, MockDRD.drdRegulatePos
        )

        libdrd.drdRegulatePos = MockDRD.drdRegulatePos.mock  # type: ignore

        drd.regulatePos(True)
        self.assertTrue(MockDRD.drdRegulatePos.enable)

        drd.regulatePos(False)
        self.assertFalse(MockDRD.drdRegulatePos.enable)

        self.assertIDImpl(
            lambda ID = -1: drd.regulatePos(True, ID),
            MockDRD.drdRegulatePos
        )

        self.assertRetImpl(
            lambda: drd.regulatePos(True),
            MockDRD.drdRegulatePos
        )

    def test_regulateRot(self):
        self.assertSignaturesEqual(
            libdrd.drdRegulateRot, MockDRD.drdRegulateRot
        )

        libdrd.drdRegulateRot = MockDRD.drdRegulateRot.mock  # type: ignore

        drd.regulateRot(True)
        self.assertTrue(MockDRD.drdRegulateRot.enable)

        drd.regulateRot(False)
        self.assertFalse(MockDRD.drdRegulateRot.enable)

        self.assertIDImpl(
            lambda ID = -1: drd.regulateRot(True, ID),
            MockDRD.drdRegulateRot
        )

        self.assertRetImpl(
            lambda: drd.regulateRot(True),
            MockDRD.drdRegulateRot
        )

    def test_regulateGrip(self):
        self.assertSignaturesEqual(
            libdrd.drdRegulateGrip, MockDRD.drdRegulateGrip
        )

        libdrd.drdRegulateGrip = MockDRD.drdRegulateGrip.mock  # type: ignore

        drd.regulateGrip(True)
        self.assertTrue(MockDRD.drdRegulateGrip.enable)

        drd.regulateGrip(False)
        self.assertFalse(MockDRD.drdRegulateGrip.enable)

        self.assertIDImpl(
            lambda ID = -1: drd.regulateGrip(True, ID),
            MockDRD.drdRegulateGrip
        )

        self.assertRetImpl(
            lambda: drd.regulateGrip(True),
            MockDRD.drdRegulateGrip
        )

    def test_setForceAndTorqueAndGripperForce(self):
        self.assertSignaturesEqual(
            libdrd.drdSetForceAndTorqueAndGripperForce,
            MockDRD.drdSetForceAndTorqueAndGripperForce
        )

        libdrd.drdSetForceAndTorqueAndGripperForce = (  # type: ignore
            MockDRD.drdSetForceAndTorqueAndGripperForce.mock
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

            drd.setForceAndTorqueAndGripperForce(f, t, fg)

            self.assertEqual(
                f[0], MockDRD.drdSetForceAndTorqueAndGripperForce.fx
            )
            self.assertEqual(
                f[1], MockDRD.drdSetForceAndTorqueAndGripperForce.fy
            )
            self.assertEqual(
                f[2], MockDRD.drdSetForceAndTorqueAndGripperForce.fz
            )

            self.assertEqual(
                t[0], MockDRD.drdSetForceAndTorqueAndGripperForce.tx
            )
            self.assertEqual(
                t[1], MockDRD.drdSetForceAndTorqueAndGripperForce.ty
            )
            self.assertEqual(
                t[2], MockDRD.drdSetForceAndTorqueAndGripperForce.tz
            )

            self.assertEqual(
                fg, MockDRD.drdSetForceAndTorqueAndGripperForce.fg
            )

        self.assertIDImpl(
            lambda ID = -1: drd.setForceAndTorqueAndGripperForce(f, t, fg, ID),
            MockDRD.drdSetForceAndTorqueAndGripperForce
        )
        self.assertRetImpl(
            lambda: drd.setForceAndTorqueAndGripperForce(f, t, fg),
            MockDRD.drdSetForceAndTorqueAndGripperForce
        )


    def test_setForceAndWristJointTorquesAndGripperForce(self):
        self.assertSignaturesEqual(
            libdrd.drdSetForceAndWristJointTorquesAndGripperForce,
            MockDRD.drdSetForceAndWristJointTorquesAndGripperForce
        )

        libdrd.drdSetForceAndWristJointTorquesAndGripperForce = (  # type: ignore
            MockDRD.drdSetForceAndWristJointTorquesAndGripperForce.mock
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

            drd.setForceAndWristJointTorquesAndGripperForce(f, t, fg)

            self.assertAlmostEqual(
                f[0],
                MockDRD.drdSetForceAndWristJointTorquesAndGripperForce.fx
            )
            self.assertAlmostEqual(
                f[1],
                MockDRD.drdSetForceAndWristJointTorquesAndGripperForce.fy
            )
            self.assertAlmostEqual(
                f[2],
                MockDRD.drdSetForceAndWristJointTorquesAndGripperForce.fz
            )

            self.assertAlmostEqual(
                t[0],
                MockDRD.drdSetForceAndWristJointTorquesAndGripperForce.q0
            )
            self.assertAlmostEqual(
                t[1],
                MockDRD.drdSetForceAndWristJointTorquesAndGripperForce.q1
            )
            self.assertAlmostEqual(
                t[2],
                MockDRD.drdSetForceAndWristJointTorquesAndGripperForce.q2
            )

            self.assertAlmostEqual(
                fg,
                MockDRD.drdSetForceAndWristJointTorquesAndGripperForce.fg
            )

        self.assertIDImpl(
            lambda ID = -1: drd.setForceAndWristJointTorquesAndGripperForce(
                f, t, fg, ID
            ),
            MockDRD.drdSetForceAndWristJointTorquesAndGripperForce
        )
        self.assertRetImpl(
            lambda: drd.setForceAndWristJointTorquesAndGripperForce(
                f, t, fg
            ),
            MockDRD.drdSetForceAndWristJointTorquesAndGripperForce
        )

    def test_enableFilter(self):
        self.assertSignaturesEqual(
            libdrd.drdEnableFilter, MockDRD.drdEnableFilter
        )

        libdrd.drdEnableFilter = MockDRD.drdEnableFilter.mock  # type: ignore

        drd.enableFilter(True)
        self.assertTrue(MockDRD.drdEnableFilter.enable)

        drd.enableFilter(False)
        self.assertFalse(MockDRD.drdEnableFilter.enable)

        self.assertIDImpl(
            lambda ID = -1: drd.enableFilter(True, ID),
            MockDRD.drdEnableFilter
        )

        self.assertRetImpl(
            lambda: drd.enableFilter(True),
            MockDRD.drdEnableFilter
        )


    def test_moveToPos(self):
        self.assertSignaturesEqual(
            libdrd.drdMoveToPos,
            MockDRD.drdMoveToPos
        )

        libdrd.drdMoveToPos = MockDRD.drdMoveToPos.mock  # type: ignore

        setval = [0.0, 0.0, 0.0]

        drd.moveToPos(setval, True)
        self.assertTrue(MockDRD.drdMoveToPos.block)

        drd.moveToPos(setval, False)
        self.assertFalse(MockDRD.drdMoveToPos.block)

        for _ in range(100):
            setval[0] = random()
            setval[1] = random()
            setval[2] = random()

            drd.moveToPos(setval, False)

            self.assertAlmostEqual(setval[0], MockDRD.drdMoveToPos.px)
            self.assertAlmostEqual(setval[1], MockDRD.drdMoveToPos.py)
            self.assertAlmostEqual(setval[2], MockDRD.drdMoveToPos.pz)

        self.assertIDImpl(
            lambda ID = -1: drd.moveToPos(setval, True, ID),
            MockDRD.drdMoveToPos
        )
        self.assertRetImpl(
            lambda: drd.moveToPos(setval, True), MockDRD.drdMoveToPos
        )

    def test_moveToRot(self):
        self.assertSignaturesEqual(
            libdrd.drdMoveToRot,
            MockDRD.drdMoveToRot
        )

        libdrd.drdMoveToRot = MockDRD.drdMoveToRot.mock  # type: ignore

        setval = [0.0, 0.0, 0.0]

        drd.moveToRot(setval, True)
        self.assertTrue(MockDRD.drdMoveToRot.block)

        drd.moveToRot(setval, False)
        self.assertFalse(MockDRD.drdMoveToRot.block)

        for _ in range(100):
            setval[0] = random()
            setval[1] = random()
            setval[2] = random()

            drd.moveToRot(setval, False)

            self.assertAlmostEqual(setval[0], MockDRD.drdMoveToRot.oa)
            self.assertAlmostEqual(setval[1], MockDRD.drdMoveToRot.ob)
            self.assertAlmostEqual(setval[2], MockDRD.drdMoveToRot.og)

        self.assertIDImpl(
            lambda ID = -1: drd.moveToRot(setval, True, ID),
            MockDRD.drdMoveToRot
        )
        self.assertRetImpl(
            lambda: drd.moveToRot(setval, True), MockDRD.drdMoveToRot
        )

    def test_moveToGrip(self):
        self.assertSignaturesEqual(
            libdrd.drdMoveToGrip,
            MockDRD.drdMoveToGrip
        )

        libdrd.drdMoveToGrip = MockDRD.drdMoveToGrip.mock  # type: ignore

        setval = 0.0

        drd.moveToGrip(setval, True)
        self.assertTrue(MockDRD.drdMoveToGrip.block)

        drd.moveToGrip(setval, False)
        self.assertFalse(MockDRD.drdMoveToGrip.block)

        for _ in range(100):
            setval = random()

            drd.moveToGrip(setval, False)

            self.assertAlmostEqual(setval, MockDRD.drdMoveToGrip.pg)

        self.assertIDImpl(
            lambda ID = -1: drd.moveToGrip(setval, True, ID),
            MockDRD.drdMoveToGrip
        )
        self.assertRetImpl(
            lambda: drd.moveToGrip(setval, True), MockDRD.drdMoveToGrip
        )

    def test_moveTo(self):
        self.assertSignaturesEqual(
            libdrd.drdMoveTo, MockDRD.drdMoveTo
        )

        libdrd.drdMoveTo = MockDRD.drdMoveTo.mock  # type: ignore

        setval = [0.0] * MAX_DOF

        drd.moveTo(setval, True)
        self.assertTrue(MockDRD.drdMoveTo.block)

        drd.moveTo(setval,False)
        self.assertFalse(MockDRD.drdMoveTo.block)

        for _ in range(100):
            for i in range(MAX_DOF):
                setval[i] = random()

            drd.moveTo(setval, True)

            for i in range(MAX_DOF):
                self.assertAlmostEqual(setval[i], MockDRD.drdMoveTo.p[i])

        self.assertIDImpl(
            lambda ID = -1: drd.moveTo(setval, True, ID),
            MockDRD.drdMoveTo
        )

        self.assertRetImpl(
            lambda: drd.moveTo(setval,True),
            MockDRD.drdMoveTo
        )


    def test_moveToEnc(self):
        self.assertSignaturesEqual(
            libdrd.drdMoveToEnc,
            MockDRD.drdMoveToEnc
        )

        libdrd.drdMoveToEnc = MockDRD.drdMoveToEnc.mock  # type: ignore

        setval = [0, 0, 0]

        drd.moveToEnc(setval, True)
        self.assertTrue(MockDRD.drdMoveToEnc.block)

        drd.moveToEnc(setval, False)
        self.assertFalse(MockDRD.drdMoveToEnc.block)

        for _ in range(100):
            setval[0] = randint(0, 100)
            setval[1] = randint(0, 100)
            setval[2] = randint(0, 100)

            drd.moveToEnc(setval, False)

            self.assertEqual(setval[0], MockDRD.drdMoveToEnc.enc0)
            self.assertEqual(setval[1], MockDRD.drdMoveToEnc.enc1)
            self.assertEqual(setval[2], MockDRD.drdMoveToEnc.enc2)

        self.assertIDImpl(
            lambda ID = -1: drd.moveToEnc(setval, True, ID),
            MockDRD.drdMoveToEnc
        )
        self.assertRetImpl(
            lambda: drd.moveToEnc(setval, True), MockDRD.drdMoveToEnc
        )


    def test_moveToAllEnc(self):
        self.assertSignaturesEqual(
            libdrd.drdMoveToAllEnc, MockDRD.drdMoveToAllEnc
        )

        libdrd.drdMoveToAllEnc = MockDRD.drdMoveToAllEnc.mock  # type: ignore

        setval = [0] * MAX_DOF

        drd.moveToAllEnc(setval, True)
        self.assertTrue(MockDRD.drdMoveToAllEnc.block)

        drd.moveToAllEnc(setval,False)
        self.assertFalse(MockDRD.drdMoveToAllEnc.block)

        for _ in range(100):
            for i in range(MAX_DOF):
                setval[i] = randint(0, 100)

            drd.moveToAllEnc(setval, True)

            for i in range(MAX_DOF):
                self.assertEqual(
                    setval[i], MockDRD.drdMoveToAllEnc.enc[i]
                )

        self.assertIDImpl(
            lambda ID = -1: drd.moveToAllEnc(setval, True, ID),
            MockDRD.drdMoveToAllEnc
        )

        self.assertRetImpl(
            lambda: drd.moveToAllEnc(setval,True),
            MockDRD.drdMoveToAllEnc
        )

    def test_trackPos(self):
        self.assertSignaturesEqual(
            libdrd.drdTrackPos,
            MockDRD.drdTrackPos
        )

        libdrd.drdTrackPos = MockDRD.drdTrackPos.mock  # type: ignore

        setval = [0.0, 0.0, 0.0]

        for _ in range(100):
            setval[0] = random()
            setval[1] = random()
            setval[2] = random()

            drd.trackPos(setval, False)

            self.assertAlmostEqual(setval[0], MockDRD.drdTrackPos.px)
            self.assertAlmostEqual(setval[1], MockDRD.drdTrackPos.py)
            self.assertAlmostEqual(setval[2], MockDRD.drdTrackPos.pz)

        self.assertIDImpl(
            lambda ID = -1: drd.trackPos(setval, ID),
            MockDRD.drdTrackPos
        )
        self.assertRetImpl(
            lambda: drd.trackPos(setval), MockDRD.drdTrackPos
        )

    def test_trackRot(self):
        self.assertSignaturesEqual(
            libdrd.drdTrackRot,
            MockDRD.drdTrackRot
        )

        libdrd.drdTrackRot = MockDRD.drdTrackRot.mock  # type: ignore

        setval = [0.0, 0.0, 0.0]

        for _ in range(100):
            setval[0] = random()
            setval[1] = random()
            setval[2] = random()

            drd.trackRot(setval, False)

            self.assertAlmostEqual(setval[0], MockDRD.drdTrackRot.oa)
            self.assertAlmostEqual(setval[1], MockDRD.drdTrackRot.ob)
            self.assertAlmostEqual(setval[2], MockDRD.drdTrackRot.og)

        self.assertIDImpl(
            lambda ID = -1: drd.trackRot(setval, ID),
            MockDRD.drdTrackRot
        )
        self.assertRetImpl(
            lambda: drd.trackRot(setval), MockDRD.drdTrackRot
        )


    def test_trackGrip(self):
        self.assertSignaturesEqual(
            libdrd.drdTrackGrip,
            MockDRD.drdTrackGrip
        )

        libdrd.drdTrackGrip = MockDRD.drdTrackGrip.mock  # type: ignore

        setval = 0.0

        for _ in range(100):
            setval = random()

            drd.trackGrip(setval, False)

            self.assertAlmostEqual(setval, MockDRD.drdTrackGrip.pg)

        self.assertIDImpl(
            lambda ID = -1: drd.trackGrip(setval, ID),
            MockDRD.drdTrackGrip
        )
        self.assertRetImpl(
            lambda: drd.trackGrip(setval), MockDRD.drdTrackGrip
        )

    def test_track(self):
        self.assertSignaturesEqual(
            libdrd.drdTrack, MockDRD.drdTrack
        )

        libdrd.drdTrack = MockDRD.drdTrack.mock  # type: ignore

        setval = [0.0] * MAX_DOF

        for _ in range(100):
            for i in range(MAX_DOF):
                setval[i] = random()

            drd.track(setval, True)

            for i in range(MAX_DOF):
                self.assertAlmostEqual(setval[i], MockDRD.drdTrack.p[i])

        self.assertIDImpl(
            lambda ID = -1: drd.track(setval, ID),
            MockDRD.drdTrack
        )

        self.assertRetImpl(
            lambda: drd.track(setval),
            MockDRD.drdTrack
        )

    def test_trackEnc(self):
        self.assertSignaturesEqual(
            libdrd.drdTrackEnc,
            MockDRD.drdTrackEnc
        )

        libdrd.drdTrackEnc = MockDRD.drdTrackEnc.mock  # type: ignore

        setval = [0, 0, 0]

        for _ in range(100):
            setval[0] = randint(0, 100)
            setval[1] = randint(0, 100)
            setval[2] = randint(0, 100)

            drd.trackEnc(setval)

            self.assertEqual(setval[0], MockDRD.drdTrackEnc.enc0)
            self.assertEqual(setval[1], MockDRD.drdTrackEnc.enc1)
            self.assertEqual(setval[2], MockDRD.drdTrackEnc.enc2)

        self.assertIDImpl(
            lambda ID = -1: drd.trackEnc(setval, ID),
            MockDRD.drdTrackEnc
        )
        self.assertRetImpl(
            lambda: drd.trackEnc(setval), MockDRD.drdTrackEnc
        )

    def test_trackAllEnc(self):
        self.assertSignaturesEqual(
            libdrd.drdTrackAllEnc, MockDRD.drdTrackAllEnc
        )

        libdrd.drdTrackAllEnc = MockDRD.drdTrackAllEnc.mock  # type: ignore

        setval = [0] * MAX_DOF

        for _ in range(100):
            for i in range(MAX_DOF):
                setval[i] = randint(0, 100)

            drd.trackAllEnc(setval, True)

            for i in range(MAX_DOF):
                self.assertEqual(
                    setval[i], MockDRD.drdTrackAllEnc.enc[i]
                )

        self.assertIDImpl(
            lambda ID = -1: drd.trackAllEnc(setval, ID),
            MockDRD.drdTrackAllEnc
        )

        self.assertRetImpl(
            lambda: drd.trackAllEnc(setval),
            MockDRD.drdTrackAllEnc
        )

    def test_hold(self):
        self.assertSignaturesEqual(
            libdrd.drdHold,
            MockDRD.drdHold
        )

        libdrd.drdHold = MockDRD.drdHold.mock  # type: ignore

        self.assertIDImpl(
            drd.hold,
            MockDRD.drdHold
        )

        self.assertRetImpl(
            drd.hold,
            MockDRD.drdHold
        )


    def test_lock(self):
        self.assertSignaturesEqual(
            libdrd.drdLock,
            MockDRD.drdLock
        )

        libdrd.drdLock = MockDRD.drdLock.mock  # type: ignore


        drd.lock(0, True)
        self.assertTrue(MockDRD.drdLock.init)

        drd.lock(0, False)
        self.assertFalse(MockDRD.drdLock.init)

        for mask in range(255):
            drd.lock(mask, False)
            self.assertFalse(MockDRD.drdLock.init)

        self.assertIDImpl(
            lambda ID = -1: drd.lock(0, True, ID),
            MockDRD.drdLock
        )

        self.assertRetImpl(
            lambda: drd.lock(0, True),
            MockDRD.drdLock
        )


    def test_stop(self):
        self.assertSignaturesEqual(
            libdrd.drdStop,
            MockDRD.drdStop
        )

        libdrd.drdStop = MockDRD.drdStop.mock  # type: ignore

        drd.stop(True)
        self.assertTrue(MockDRD.drdStop.frc)

        drd.stop(False)
        self.assertFalse(MockDRD.drdStop.frc)

        self.assertIDImpl(
            lambda ID = -1: drd.stop(True, ID),
            MockDRD.drdStop
        )

        self.assertRetImpl(
            lambda: drd.stop(True),
            MockDRD.drdStop
        )

    def test_getPriorities(self):
        self.assertSignaturesEqual(
            libdrd.drdGetPriorities,
            MockDRD.drdGetPriorities
        )

        libdrd.drdGetPriorities = MockDRD.drdGetPriorities.mock  # type: ignore

        for _ in range(100):
            MockDRD.drdGetPriorities.prio = randint(0, 100)
            MockDRD.drdGetPriorities.ctrlprio = randint(0, 100)

            prio, ctrlprio, _ = drd.getPriorities()

            self.assertEqual(prio, MockDRD.drdGetPriorities.prio)
            self.assertEqual(ctrlprio, MockDRD.drdGetPriorities.ctrlprio)

        self.assertIDImpl(
            drd.getPriorities,
            MockDRD.drdGetPriorities
        )

        self.assertRetImpl(
            lambda: drd.getPriorities()[-1],
            MockDRD.drdGetPriorities
        )

    def test_setPriorities(self):
        self.assertSignaturesEqual(
            libdrd.drdSetPriorities,
            MockDRD.drdSetPriorities
        )

        libdrd.drdSetPriorities = MockDRD.drdSetPriorities.mock  # type: ignore

        for _ in range(100):
            prio = randint(0, 100)
            ctrlprio = randint(0, 100)

            drd.setPriorities(prio, ctrlprio)

            self.assertEqual(prio, MockDRD.drdSetPriorities.prio)
            self.assertEqual(ctrlprio, MockDRD.drdSetPriorities.ctrlprio)

        self.assertIDImpl(
            lambda ID = -1: drd.setPriorities(prio, ctrlprio, ID),
            MockDRD.drdSetPriorities
        )

        self.assertRetImpl(
            lambda: drd.setPriorities(prio, ctrlprio),
            MockDRD.drdSetPriorities
        )

    def test_setEncPGain(self):
        self.assertSignaturesEqual(
            libdrd.drdSetEncPGain,
            MockDRD.drdSetEncPGain
        )

        libdrd.drdSetEncPGain = (  # type: ignore
            MockDRD.drdSetEncPGain.mock
        )

        for _ in range(100):
            gain = random()
            drd.setEncPGain(gain)

            self.assertAlmostEqual(gain, MockDRD.drdSetEncPGain.gain)

        self.assertIDImpl(
            lambda ID = -1: drd.setEncPGain(0, ID),
            MockDRD.drdSetEncPGain
        )

        self.assertRetImpl(
            lambda: drd.setEncPGain(0),
            MockDRD.drdSetEncPGain
        )

    def test_getEncPGain(self):
        self.assertSignaturesEqual(
            libdrd.drdGetEncPGain,
            MockDRD.drdGetEncPGain
        )

        libdrd.drdGetEncPGain = (  # type: ignore
            MockDRD.drdGetEncPGain.mock
        )

        for _ in range(100):
            MockDRD.drdGetEncPGain.gain = random()

            self.assertAlmostEqual(
                drd.getEncPGain(),
                MockDRD.drdGetEncPGain.gain
            )

        self.assertIDImpl(
            drd.getEncPGain,
            MockDRD.drdGetEncPGain
        )

    def test_setEncIGain(self):
        self.assertSignaturesEqual(
            libdrd.drdSetEncIGain,
            MockDRD.drdSetEncIGain
        )

        libdrd.drdSetEncIGain = (  # type: ignore
            MockDRD.drdSetEncIGain.mock
        )

        for _ in range(100):
            gain = random()
            drd.setEncIGain(gain)

            self.assertAlmostEqual(gain, MockDRD.drdSetEncIGain.gain)

        self.assertIDImpl(
            lambda ID = -1: drd.setEncIGain(0, ID),
            MockDRD.drdSetEncIGain
        )

        self.assertRetImpl(
            lambda: drd.setEncIGain(0),
            MockDRD.drdSetEncIGain
        )

    def test_getEncIGain(self):
        self.assertSignaturesEqual(
            libdrd.drdGetEncIGain,
            MockDRD.drdGetEncIGain
        )

        libdrd.drdGetEncIGain = (  # type: ignore
            MockDRD.drdGetEncIGain.mock
        )

        for _ in range(100):
            MockDRD.drdGetEncIGain.gain = random()

            self.assertAlmostEqual(
                drd.getEncIGain(),
                MockDRD.drdGetEncIGain.gain
            )

        self.assertIDImpl(
            drd.getEncIGain,
            MockDRD.drdGetEncIGain
        )

    def test_setEncDGain(self):
        self.assertSignaturesEqual(
            libdrd.drdSetEncDGain,
            MockDRD.drdSetEncDGain
        )

        libdrd.drdSetEncDGain = (  # type: ignore
            MockDRD.drdSetEncDGain.mock
        )

        for _ in range(100):
            gain = random()
            drd.setEncDGain(gain)

            self.assertAlmostEqual(gain, MockDRD.drdSetEncDGain.gain)

        self.assertIDImpl(
            lambda ID = -1: drd.setEncDGain(0, ID),
            MockDRD.drdSetEncDGain
        )

        self.assertRetImpl(
            lambda: drd.setEncDGain(0),
            MockDRD.drdSetEncDGain
        )

    def test_getEncDGain(self):
        self.assertSignaturesEqual(
            libdrd.drdGetEncDGain,
            MockDRD.drdGetEncDGain
        )

        libdrd.drdGetEncDGain = (  # type: ignore
            MockDRD.drdGetEncDGain.mock
        )

        for _ in range(100):
            MockDRD.drdGetEncDGain.gain = random()

            self.assertAlmostEqual(
                drd.getEncDGain(),
                MockDRD.drdGetEncDGain.gain
            )

        self.assertIDImpl(
            drd.getEncDGain,
            MockDRD.drdGetEncDGain
        )

    def test_setMotRatioMax(self):
        self.assertSignaturesEqual(
            libdrd.drdSetMotRatioMax,
            MockDRD.drdSetMotRatioMax
        )

        libdrd.drdSetMotRatioMax = (  # type: ignore
            MockDRD.drdSetMotRatioMax.mock
        )

        for _ in range(100):
            scale = random()
            drd.setMotRatioMax(scale)

            self.assertAlmostEqual(scale, MockDRD.drdSetMotRatioMax.scale)

        self.assertIDImpl(
            lambda ID = -1: drd.setMotRatioMax(0, ID),
            MockDRD.drdSetMotRatioMax
        )

        self.assertRetImpl(
            lambda: drd.setMotRatioMax(0),
            MockDRD.drdSetMotRatioMax
        )

    def test_getMotRatioMax(self):
        self.assertSignaturesEqual(
            libdrd.drdGetMotRatioMax,
            MockDRD.drdGetMotRatioMax
        )

        libdrd.drdGetMotRatioMax = (  # type: ignore
            MockDRD.drdGetMotRatioMax.mock
        )

        for _ in range(100):
            MockDRD.drdGetMotRatioMax.scale = random()

            self.assertAlmostEqual(
                drd.getMotRatioMax(),
                MockDRD.drdGetMotRatioMax.scale
            )

        self.assertIDImpl(
            drd.getMotRatioMax,
            MockDRD.drdGetMotRatioMax
        )

    def test_setEncMoveParam(self):
        self.assertSignaturesEqual(
            libdrd.drdSetEncMoveParam,
            MockDRD.drdSetEncMoveParam
        )

        libdrd.drdSetEncMoveParam = (  # type: ignore
            MockDRD.drdSetEncMoveParam.mock
        )

        vmax = 0.0
        amax = 0.0
        jerk = 0.0

        for _ in range(100):
            vmax = random()
            amax = random()
            jerk = random()

            drd.setEncMoveParam(vmax, amax, jerk)

            self.assertAlmostEqual(
                vmax, MockDRD.drdSetEncMoveParam.vmax
            )

            self.assertAlmostEqual(
                amax, MockDRD.drdSetEncMoveParam.amax
            )

            self.assertAlmostEqual(
                jerk, MockDRD.drdSetEncMoveParam.jerk
            )

        self.assertIDImpl(
            lambda ID = -1: drd.setEncMoveParam(0, 0, 0, ID),
            MockDRD.drdSetEncMoveParam
        )

        self.assertRetImpl(
            lambda: drd.setEncMoveParam(0, 0, 0),
            MockDRD.drdSetEncMoveParam
        )

    def test_setEncTrackParam(self):
        self.assertSignaturesEqual(
            libdrd.drdSetEncTrackParam,
            MockDRD.drdSetEncTrackParam
        )

        libdrd.drdSetEncTrackParam = (  # type: ignore
            MockDRD.drdSetEncTrackParam.mock
        )

        vmax = 0.0
        amax = 0.0
        jerk = 0.0

        for _ in range(100):
            vmax = random()
            amax = random()
            jerk = random()

            drd.setEncTrackParam(vmax, amax, jerk)

            self.assertAlmostEqual(
                vmax, MockDRD.drdSetEncTrackParam.vmax
            )

            self.assertAlmostEqual(
                amax, MockDRD.drdSetEncTrackParam.amax
            )

            self.assertAlmostEqual(
                jerk, MockDRD.drdSetEncTrackParam.jerk
            )

        self.assertIDImpl(
            lambda ID = -1: drd.setEncTrackParam(0, 0, 0, ID),
            MockDRD.drdSetEncTrackParam
        )

        self.assertRetImpl(
            lambda: drd.setEncTrackParam(0, 0, 0),
            MockDRD.drdSetEncTrackParam
        )

    def test_setPosMoveParam(self):
        self.assertSignaturesEqual(
            libdrd.drdSetPosMoveParam,
            MockDRD.drdSetPosMoveParam
        )

        libdrd.drdSetPosMoveParam = (  # type: ignore
            MockDRD.drdSetPosMoveParam.mock
        )

        vmax = 0.0
        amax = 0.0
        jerk = 0.0

        for _ in range(100):
            vmax = random()
            amax = random()
            jerk = random()

            drd.setPosMoveParam(vmax, amax, jerk)

            self.assertAlmostEqual(
                vmax, MockDRD.drdSetPosMoveParam.vmax
            )

            self.assertAlmostEqual(
                amax, MockDRD.drdSetPosMoveParam.amax
            )

            self.assertAlmostEqual(
                jerk, MockDRD.drdSetPosMoveParam.jerk
            )

        self.assertIDImpl(
            lambda ID = -1: drd.setPosMoveParam(0, 0, 0, ID),
            MockDRD.drdSetPosMoveParam
        )

        self.assertRetImpl(
            lambda: drd.setPosMoveParam(0, 0, 0),
            MockDRD.drdSetPosMoveParam
        )

    def test_setPosTrackParam(self):
        self.assertSignaturesEqual(
            libdrd.drdSetPosTrackParam,
            MockDRD.drdSetPosTrackParam
        )

        libdrd.drdSetPosTrackParam = (  # type: ignore
            MockDRD.drdSetPosTrackParam.mock
        )

        vmax = 0.0
        amax = 0.0
        jerk = 0.0

        for _ in range(100):
            vmax = random()
            amax = random()
            jerk = random()

            drd.setPosTrackParam(vmax, amax, jerk)

            self.assertAlmostEqual(
                vmax, MockDRD.drdSetPosTrackParam.vmax
            )

            self.assertAlmostEqual(
                amax, MockDRD.drdSetPosTrackParam.amax
            )

            self.assertAlmostEqual(
                jerk, MockDRD.drdSetPosTrackParam.jerk
            )

        self.assertIDImpl(
            lambda ID = -1: drd.setPosTrackParam(0, 0, 0, ID),
            MockDRD.drdSetPosTrackParam
        )

        self.assertRetImpl(
            lambda: drd.setPosTrackParam(0, 0, 0),
            MockDRD.drdSetPosTrackParam
        )

    def test_setRotMoveParam(self):
        self.assertSignaturesEqual(
            libdrd.drdSetRotMoveParam,
            MockDRD.drdSetRotMoveParam
        )

        libdrd.drdSetRotMoveParam = (  # type: ignore
            MockDRD.drdSetRotMoveParam.mock
        )

        vmax = 0.0
        amax = 0.0
        jerk = 0.0

        for _ in range(100):
            vmax = random()
            amax = random()
            jerk = random()

            drd.setRotMoveParam(vmax, amax, jerk)

            self.assertAlmostEqual(
                vmax, MockDRD.drdSetRotMoveParam.vmax
            )

            self.assertAlmostEqual(
                amax, MockDRD.drdSetRotMoveParam.amax
            )

            self.assertAlmostEqual(
                jerk, MockDRD.drdSetRotMoveParam.jerk
            )

        self.assertIDImpl(
            lambda ID = -1: drd.setRotMoveParam(0, 0, 0, ID),
            MockDRD.drdSetRotMoveParam
        )

        self.assertRetImpl(
            lambda: drd.setRotMoveParam(0, 0, 0),
            MockDRD.drdSetRotMoveParam
        )

    def test_setRotTrackParam(self):
        self.assertSignaturesEqual(
            libdrd.drdSetRotTrackParam,
            MockDRD.drdSetRotTrackParam
        )

        libdrd.drdSetRotTrackParam = (  # type: ignore
            MockDRD.drdSetRotTrackParam.mock
        )

        vmax = 0.0
        amax = 0.0
        jerk = 0.0

        for _ in range(100):
            vmax = random()
            amax = random()
            jerk = random()

            drd.setRotTrackParam(vmax, amax, jerk)

            self.assertAlmostEqual(
                vmax, MockDRD.drdSetRotTrackParam.vmax
            )

            self.assertAlmostEqual(
                amax, MockDRD.drdSetRotTrackParam.amax
            )

            self.assertAlmostEqual(
                jerk, MockDRD.drdSetRotTrackParam.jerk
            )

        self.assertIDImpl(
            lambda ID = -1: drd.setRotTrackParam(0, 0, 0, ID),
            MockDRD.drdSetRotTrackParam
        )

        self.assertRetImpl(
            lambda: drd.setRotTrackParam(0, 0, 0),
            MockDRD.drdSetRotTrackParam
        )

    def test_setGripMoveParam(self):
        self.assertSignaturesEqual(
            libdrd.drdSetGripMoveParam,
            MockDRD.drdSetGripMoveParam
        )

        libdrd.drdSetGripMoveParam = (  # type: ignore
            MockDRD.drdSetGripMoveParam.mock
        )

        vmax = 0.0
        amax = 0.0
        jerk = 0.0

        for _ in range(100):
            vmax = random()
            amax = random()
            jerk = random()

            drd.setGripMoveParam(vmax, amax, jerk)

            self.assertAlmostEqual(
                vmax, MockDRD.drdSetGripMoveParam.vmax
            )

            self.assertAlmostEqual(
                amax, MockDRD.drdSetGripMoveParam.amax
            )

            self.assertAlmostEqual(
                jerk, MockDRD.drdSetGripMoveParam.jerk
            )

        self.assertIDImpl(
            lambda ID = -1: drd.setGripMoveParam(0, 0, 0, ID),
            MockDRD.drdSetGripMoveParam
        )

        self.assertRetImpl(
            lambda: drd.setGripMoveParam(0, 0, 0),
            MockDRD.drdSetGripMoveParam
        )

    def test_setGripTrackParam(self):
        self.assertSignaturesEqual(
            libdrd.drdSetGripTrackParam,
            MockDRD.drdSetGripTrackParam
        )

        libdrd.drdSetGripTrackParam = (  # type: ignore
            MockDRD.drdSetGripTrackParam.mock
        )

        vmax = 0.0
        amax = 0.0
        jerk = 0.0

        for _ in range(100):
            vmax = random()
            amax = random()
            jerk = random()

            drd.setGripTrackParam(vmax, amax, jerk)

            self.assertAlmostEqual(
                vmax, MockDRD.drdSetGripTrackParam.vmax
            )

            self.assertAlmostEqual(
                amax, MockDRD.drdSetGripTrackParam.amax
            )

            self.assertAlmostEqual(
                jerk, MockDRD.drdSetGripTrackParam.jerk
            )

        self.assertIDImpl(
            lambda ID = -1: drd.setGripTrackParam(0, 0, 0, ID),
            MockDRD.drdSetGripTrackParam
        )

        self.assertRetImpl(
            lambda: drd.setGripTrackParam(0, 0, 0),
            MockDRD.drdSetGripTrackParam
        )

    def test_getEncMoveParam(self):
        self.assertSignaturesEqual(
            libdrd.drdGetEncMoveParam,
            MockDRD.drdGetEncMoveParam
        )

        libdrd.drdGetEncMoveParam = (  # type: ignore
            MockDRD.drdGetEncMoveParam.mock
        )

        for _ in range(100):
            MockDRD.drdGetEncMoveParam.vmax = random()
            MockDRD.drdGetEncMoveParam.amax = random()
            MockDRD.drdGetEncMoveParam.jerk = random()

            vmax, amax, jerk, _ = drd.getEncMoveParam()

            self.assertAlmostEqual(
                vmax, MockDRD.drdGetEncMoveParam.vmax
            )

            self.assertAlmostEqual(
                amax, MockDRD.drdGetEncMoveParam.amax
            )

            self.assertAlmostEqual(
                jerk, MockDRD.drdGetEncMoveParam.jerk
            )

        self.assertIDImpl(
            drd.getEncMoveParam,
            MockDRD.drdGetEncMoveParam
        )

        self.assertRetImpl(
            lambda: drd.getEncMoveParam()[-1],
            MockDRD.drdGetEncMoveParam
        )

    def test_getEncTrackParam(self):
        self.assertSignaturesEqual(
            libdrd.drdGetEncTrackParam,
            MockDRD.drdGetEncTrackParam
        )

        libdrd.drdGetEncTrackParam = (  # type: ignore
            MockDRD.drdGetEncTrackParam.mock
        )

        for _ in range(100):
            MockDRD.drdGetEncTrackParam.vmax = random()
            MockDRD.drdGetEncTrackParam.amax = random()
            MockDRD.drdGetEncTrackParam.jerk = random()

            vmax, amax, jerk, _ = drd.getEncTrackParam()

            self.assertAlmostEqual(
                vmax, MockDRD.drdGetEncTrackParam.vmax
            )

            self.assertAlmostEqual(
                amax, MockDRD.drdGetEncTrackParam.amax
            )

            self.assertAlmostEqual(
                jerk, MockDRD.drdGetEncTrackParam.jerk
            )

        self.assertIDImpl(
            drd.getEncTrackParam,
            MockDRD.drdGetEncTrackParam
        )

        self.assertRetImpl(
            lambda: drd.getEncTrackParam()[-1],
            MockDRD.drdGetEncTrackParam
        )

    def test_getPosMoveParam(self):
        self.assertSignaturesEqual(
            libdrd.drdGetPosMoveParam,
            MockDRD.drdGetPosMoveParam
        )

        libdrd.drdGetPosMoveParam = (  # type: ignore
            MockDRD.drdGetPosMoveParam.mock
        )

        for _ in range(100):
            MockDRD.drdGetPosMoveParam.vmax = random()
            MockDRD.drdGetPosMoveParam.amax = random()
            MockDRD.drdGetPosMoveParam.jerk = random()

            vmax, amax, jerk, _ = drd.getPosMoveParam()

            self.assertAlmostEqual(
                vmax, MockDRD.drdGetPosMoveParam.vmax
            )

            self.assertAlmostEqual(
                amax, MockDRD.drdGetPosMoveParam.amax
            )

            self.assertAlmostEqual(
                jerk, MockDRD.drdGetPosMoveParam.jerk
            )

        self.assertIDImpl(
            drd.getPosMoveParam,
            MockDRD.drdGetPosMoveParam
        )

        self.assertRetImpl(
            lambda: drd.getPosMoveParam()[-1],
            MockDRD.drdGetPosMoveParam
        )

    def test_getPosTrackParam(self):
        self.assertSignaturesEqual(
            libdrd.drdGetPosTrackParam,
            MockDRD.drdGetPosTrackParam
        )

        libdrd.drdGetPosTrackParam = (  # type: ignore
            MockDRD.drdGetPosTrackParam.mock
        )

        for _ in range(100):
            MockDRD.drdGetPosTrackParam.vmax = random()
            MockDRD.drdGetPosTrackParam.amax = random()
            MockDRD.drdGetPosTrackParam.jerk = random()

            vmax, amax, jerk, _ = drd.getPosTrackParam()

            self.assertAlmostEqual(
                vmax, MockDRD.drdGetPosTrackParam.vmax
            )

            self.assertAlmostEqual(
                amax, MockDRD.drdGetPosTrackParam.amax
            )

            self.assertAlmostEqual(
                jerk, MockDRD.drdGetPosTrackParam.jerk
            )

        self.assertIDImpl(
            drd.getPosTrackParam,
            MockDRD.drdGetPosTrackParam
        )

        self.assertRetImpl(
            lambda: drd.getPosTrackParam()[-1],
            MockDRD.drdGetPosTrackParam
        )

    def test_getRotMoveParam(self):
        self.assertSignaturesEqual(
            libdrd.drdGetRotMoveParam,
            MockDRD.drdGetRotMoveParam
        )

        libdrd.drdGetRotMoveParam = (  # type: ignore
            MockDRD.drdGetRotMoveParam.mock
        )

        for _ in range(100):
            MockDRD.drdGetRotMoveParam.vmax = random()
            MockDRD.drdGetRotMoveParam.amax = random()
            MockDRD.drdGetRotMoveParam.jerk = random()

            vmax, amax, jerk, _ = drd.getRotMoveParam()

            self.assertAlmostEqual(
                vmax, MockDRD.drdGetRotMoveParam.vmax
            )

            self.assertAlmostEqual(
                amax, MockDRD.drdGetRotMoveParam.amax
            )

            self.assertAlmostEqual(
                jerk, MockDRD.drdGetRotMoveParam.jerk
            )

        self.assertIDImpl(
            drd.getRotMoveParam,
            MockDRD.drdGetRotMoveParam
        )

        self.assertRetImpl(
            lambda: drd.getRotMoveParam()[-1],
            MockDRD.drdGetRotMoveParam
        )

    def test_getRotTrackParam(self):
        self.assertSignaturesEqual(
            libdrd.drdGetRotTrackParam,
            MockDRD.drdGetRotTrackParam
        )

        libdrd.drdGetRotTrackParam = (  # type: ignore
            MockDRD.drdGetRotTrackParam.mock
        )

        for _ in range(100):
            MockDRD.drdGetRotTrackParam.vmax = random()
            MockDRD.drdGetRotTrackParam.amax = random()
            MockDRD.drdGetRotTrackParam.jerk = random()

            vmax, amax, jerk, _ = drd.getRotTrackParam()

            self.assertAlmostEqual(
                vmax, MockDRD.drdGetRotTrackParam.vmax
            )

            self.assertAlmostEqual(
                amax, MockDRD.drdGetRotTrackParam.amax
            )

            self.assertAlmostEqual(
                jerk, MockDRD.drdGetRotTrackParam.jerk
            )

        self.assertIDImpl(
            drd.getRotTrackParam,
            MockDRD.drdGetRotTrackParam
        )

        self.assertRetImpl(
            lambda: drd.getRotTrackParam()[-1],
            MockDRD.drdGetRotTrackParam
        )

    def test_getGripMoveParam(self):
        self.assertSignaturesEqual(
            libdrd.drdGetGripMoveParam,
            MockDRD.drdGetGripMoveParam
        )

        libdrd.drdGetGripMoveParam = (  # type: ignore
            MockDRD.drdGetGripMoveParam.mock
        )

        for _ in range(100):
            MockDRD.drdGetGripMoveParam.vmax = random()
            MockDRD.drdGetGripMoveParam.amax = random()
            MockDRD.drdGetGripMoveParam.jerk = random()

            vmax, amax, jerk, _ = drd.getGripMoveParam()

            self.assertAlmostEqual(
                vmax, MockDRD.drdGetGripMoveParam.vmax
            )

            self.assertAlmostEqual(
                amax, MockDRD.drdGetGripMoveParam.amax
            )

            self.assertAlmostEqual(
                jerk, MockDRD.drdGetGripMoveParam.jerk
            )

        self.assertIDImpl(
            drd.getGripMoveParam,
            MockDRD.drdGetGripMoveParam
        )

        self.assertRetImpl(
            lambda: drd.getGripMoveParam()[-1],
            MockDRD.drdGetGripMoveParam
        )

    def test_getGripTrackParam(self):
        self.assertSignaturesEqual(
            libdrd.drdGetGripTrackParam,
            MockDRD.drdGetGripTrackParam
        )

        libdrd.drdGetGripTrackParam = (  # type: ignore
            MockDRD.drdGetGripTrackParam.mock
        )

        for _ in range(100):
            MockDRD.drdGetGripTrackParam.vmax = random()
            MockDRD.drdGetGripTrackParam.amax = random()
            MockDRD.drdGetGripTrackParam.jerk = random()

            vmax, amax, jerk, _ = drd.getGripTrackParam()

            self.assertAlmostEqual(
                vmax, MockDRD.drdGetGripTrackParam.vmax
            )

            self.assertAlmostEqual(
                amax, MockDRD.drdGetGripTrackParam.amax
            )

            self.assertAlmostEqual(
                jerk, MockDRD.drdGetGripTrackParam.jerk
            )

        self.assertIDImpl(
            drd.getGripTrackParam,
            MockDRD.drdGetGripTrackParam
        )

        self.assertRetImpl(
            lambda: drd.getGripTrackParam()[-1],
            MockDRD.drdGetGripTrackParam
        )
