from ctypes import CFUNCTYPE, POINTER, c_byte, c_double, c_int


class MockDHD:
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

