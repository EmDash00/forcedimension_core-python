import unittest
from ctypes import c_int

import forcedimension_core


class TestConstants(unittest.TestCase):
    def test_device_types(self):
        self.assertEqual(forcedimension_core.DeviceType.NONE, 0)

        self.assertEqual(forcedimension_core.DeviceType.DELTA3, 63)
        self.assertEqual(forcedimension_core.DeviceType.OMEGA3, 33)

        self.assertEqual(forcedimension_core.DeviceType.OMEGA6_RIGHT, 34)
        self.assertEqual(forcedimension_core.DeviceType.OMEGA6_LEFT, 36)

        self.assertEqual(forcedimension_core.DeviceType.OMEGA7_RIGHT, 35)
        self.assertEqual(forcedimension_core.DeviceType.OMEGA7_LEFT, 37)

        self.assertEqual(forcedimension_core.DeviceType.CONTROLLER, 81)
        self.assertEqual(forcedimension_core.DeviceType.CONTROLLER_HR, 82)

        self.assertEqual(forcedimension_core.DeviceType.CUSTOM, 91)

        self.assertEqual(forcedimension_core.DeviceType.SIGMA3, 206)
        self.assertEqual(forcedimension_core.DeviceType.SIGMA7_RIGHT, 104)
        self.assertEqual(forcedimension_core.DeviceType.SIGMA7_LEFT, 105)

        self.assertEqual(forcedimension_core.DeviceType.LAMBDA3, 203)

        self.assertEqual(forcedimension_core.DeviceType.LAMBDA7_RIGHT, 108)
        self.assertEqual(forcedimension_core.DeviceType.LAMBDA7_LEFT, 109)

        self.assertEqual(forcedimension_core.DeviceType.FALCON, 60)

        self.assertEqual(
            forcedimension_core.DeviceType.OMEGA6_RIGHT,
            forcedimension_core.dhd.deprecated.DeviceType.OMEGA33
        )

        self.assertEqual(
            forcedimension_core.DeviceType.OMEGA7_LEFT,
            forcedimension_core.dhd.deprecated.DeviceType.OMEGA331_LEFT
        )

        self.assertEqual(
            forcedimension_core.DeviceType.OMEGA7_RIGHT,
            forcedimension_core.dhd.deprecated.DeviceType.OMEGA331
        )

        self.assertEqual(
            forcedimension_core.DeviceType.OMEGA7_LEFT,
            forcedimension_core.dhd.deprecated.DeviceType.OMEGA331_LEFT
        )

        self.assertEqual(
            forcedimension_core.DeviceType.SIGMA7_RIGHT,
            forcedimension_core.dhd.deprecated.DeviceType.SIGMA331
        )

        self.assertEqual(
            forcedimension_core.DeviceType.SIGMA7_LEFT,
            forcedimension_core.dhd.deprecated.DeviceType.SIGMA331_LEFT
        )

        self.assertEqual(
            forcedimension_core.DeviceType.LAMBDA7_RIGHT,
            forcedimension_core.dhd.deprecated.DeviceType.LAMBDA331
        )

        self.assertEqual(
            forcedimension_core.DeviceType.LAMBDA7_LEFT,
            forcedimension_core.dhd.deprecated.DeviceType.LAMBDA331_LEFT
        )

    def test_dofs(self):
        self.assertEqual(forcedimension_core.MAX_DOF, 8)

        self.assertEqual(forcedimension_core.DELTA_IDX, (0, 1, 2))
        self.assertEqual(forcedimension_core.WRIST_IDX, (3, 4, 5))

    def test_return_codes(self):
        self.assertEqual(forcedimension_core.TIMEGUARD, 1)
        self.assertEqual(forcedimension_core.MOTOR_SATURATED, 2)

    def test_status(self):
        status = forcedimension_core.containers.Status()

        self.assertEqual(forcedimension_core.MAX_STATUS, 17)
        self.assertEqual(
            len(status._fields_) - 1, forcedimension_core.MAX_STATUS
        )

        self.assertEqual(
            status._fields_[:-1],
            (
                ('power', c_int),
                ('connected', c_int),
                ('started', c_int),
                ('reset', c_int),
                ('idle', c_int),
                ('force', c_int),
                ('brake', c_int),
                ('torque', c_int),
                ('wrist_detected', c_int),
                ('error', c_int),
                ('gravity', c_int),
                ('timeguard', c_int),
                ('wrist_init', c_int),
                ('redundancy', c_int),
                ('forceoffcause', c_int),
                ('locks', c_int),
                ('axis_checked', c_int),
            )
        )

    def test_max_buttons(self):
        self.assertEqual(forcedimension_core.MAX_BUTTONS, 32)

    def test_velocity_config(self):
        self.assertEqual(
            forcedimension_core.VelocityEstimatorMode.WINDOWING, 0
        )

        self.assertEqual(
            forcedimension_core.DEFAULT_VELOCITY_WINDOW, 20
        )

    def test_com_mode(self):
        self.assertEqual(forcedimension_core.ComMode.SYNC, 0)
        self.assertEqual(forcedimension_core.ComMode.ASYNC, 1)
        self.assertEqual(forcedimension_core.ComMode.VIRTUAL, 3)
        self.assertEqual(forcedimension_core.ComMode.NETWORK, 4)

    def test_thread_priority(self):
        self.assertEqual(forcedimension_core.ThreadPriority.DEFAULT, 0)
        self.assertEqual(forcedimension_core.ThreadPriority.HIGH, 1)
        self.assertEqual(forcedimension_core.ThreadPriority.LOW, 2)
        self.assertEqual(forcedimension_core.ComMode.NETWORK, 4)

    def test_error(self):
        self.assertEqual(forcedimension_core.ErrorNum.NO_ERROR, 0)
        self.assertEqual(forcedimension_core.ErrorNum.ERROR, 1)
        self.assertEqual(forcedimension_core.ErrorNum.COM, 2)
        self.assertEqual(forcedimension_core.ErrorNum.DHC_BUSY, 3)
        self.assertEqual(forcedimension_core.ErrorNum.NO_DRIVER_FOUND, 4)
        self.assertEqual(forcedimension_core.ErrorNum.NO_DEVICE_FOUND, 5)
        self.assertEqual(forcedimension_core.ErrorNum.NOT_AVAILABLE, 6)
        self.assertEqual(forcedimension_core.ErrorNum.TIMEOUT, 7)
        self.assertEqual(forcedimension_core.ErrorNum.GEOMETRY, 8)
        self.assertEqual(forcedimension_core.ErrorNum.EXPERT_MODE_DISABLED, 9)
        self.assertEqual(forcedimension_core.ErrorNum.NOT_IMPLEMENTED, 10)
        self.assertEqual(forcedimension_core.ErrorNum.OUT_OF_MEMORY, 11)
        self.assertEqual(forcedimension_core.ErrorNum.DEVICE_NOT_READY, 12)
        self.assertEqual(forcedimension_core.ErrorNum.FILE_NOT_FOUND, 13)
        self.assertEqual(forcedimension_core.ErrorNum.CONFIGURATION, 14)
        self.assertEqual(forcedimension_core.ErrorNum.INVALID_INDEX, 15)
        self.assertEqual(forcedimension_core.ErrorNum.DEPRECATED, 16)
        self.assertEqual(forcedimension_core.ErrorNum.NULL_ARGUMENT, 17)
        self.assertEqual(forcedimension_core.ErrorNum.REDUNDANT_FAIL, 18)
        self.assertEqual(forcedimension_core.ErrorNum.NOT_ENABLED, 19)
        self.assertEqual(forcedimension_core.ErrorNum.DEVICE_IN_USE, 20)
        self.assertEqual(forcedimension_core.ErrorNum.INVALID, 21)
        self.assertEqual(forcedimension_core.ErrorNum.NO_REGULATION, 22)


if __name__ == "__main__":
    unittest.main()
