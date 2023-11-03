import unittest
from ctypes import c_int

import forcedimension_core as fdsdk_core


class TestConstants(unittest.TestCase):
    def test_device_types(self):
        self.assertEqual(fdsdk_core.constants.DeviceType.NONE, 0)

        self.assertEqual(fdsdk_core.constants.DeviceType.DELTA3, 63)
        self.assertEqual(fdsdk_core.constants.DeviceType.OMEGA3, 33)

        self.assertEqual(fdsdk_core.constants.DeviceType.OMEGA6_RIGHT, 34)
        self.assertEqual(fdsdk_core.constants.DeviceType.OMEGA6_LEFT, 36)

        self.assertEqual(fdsdk_core.constants.DeviceType.OMEGA7_RIGHT, 35)
        self.assertEqual(fdsdk_core.constants.DeviceType.OMEGA7_LEFT, 37)

        self.assertEqual(fdsdk_core.constants.DeviceType.CONTROLLER, 81)
        self.assertEqual(fdsdk_core.constants.DeviceType.CONTROLLER_HR, 82)

        self.assertEqual(fdsdk_core.constants.DeviceType.CUSTOM, 91)

        self.assertEqual(fdsdk_core.constants.DeviceType.SIGMA3, 206)
        self.assertEqual(fdsdk_core.constants.DeviceType.SIGMA7_RIGHT, 104)
        self.assertEqual(fdsdk_core.constants.DeviceType.SIGMA7_LEFT, 105)

        self.assertEqual(fdsdk_core.constants.DeviceType.LAMBDA3, 203)

        self.assertEqual(fdsdk_core.constants.DeviceType.LAMBDA7_RIGHT, 108)
        self.assertEqual(fdsdk_core.constants.DeviceType.LAMBDA7_LEFT, 109)

        self.assertEqual(fdsdk_core.constants.DeviceType.FALCON, 60)

        self.assertEqual(
            fdsdk_core.constants.DeviceType.OMEGA6_RIGHT,
            fdsdk_core.deprecated.constants.DeviceType.OMEGA33
        )

        self.assertEqual(
            fdsdk_core.constants.DeviceType.OMEGA7_LEFT,
            fdsdk_core.deprecated.constants.DeviceType.OMEGA331_LEFT
        )

        self.assertEqual(
            fdsdk_core.constants.DeviceType.OMEGA7_RIGHT,
            fdsdk_core.deprecated.constants.DeviceType.OMEGA331
        )

        self.assertEqual(
            fdsdk_core.constants.DeviceType.OMEGA7_LEFT,
            fdsdk_core.deprecated.constants.DeviceType.OMEGA331_LEFT
        )

        self.assertEqual(
            fdsdk_core.constants.DeviceType.SIGMA7_RIGHT,
            fdsdk_core.deprecated.constants.DeviceType.SIGMA331
        )

        self.assertEqual(
            fdsdk_core.constants.DeviceType.SIGMA7_LEFT,
            fdsdk_core.deprecated.constants.DeviceType.SIGMA331_LEFT
        )

        self.assertEqual(
            fdsdk_core.constants.DeviceType.LAMBDA7_RIGHT,
            fdsdk_core.deprecated.constants.DeviceType.LAMBDA331
        )

        self.assertEqual(
            fdsdk_core.constants.DeviceType.LAMBDA7_LEFT,
            fdsdk_core.deprecated.constants.DeviceType.LAMBDA331_LEFT
        )

    def test_dofs(self):
        self.assertEqual(fdsdk_core.constants.MAX_DOF, 8)

        self.assertEqual(fdsdk_core.constants.DELTA_IDX, (0, 1, 2))
        self.assertEqual(fdsdk_core.constants.WRIST_IDX, (3, 4, 5))

    def test_return_codes(self):
        self.assertEqual(fdsdk_core.constants.TIMEGUARD, 1)
        self.assertEqual(fdsdk_core.constants.MOTOR_SATURATED, 2)

    def test_status(self):
        status = fdsdk_core.containers.Status()

        self.assertEqual(fdsdk_core.constants.MAX_STATUS, 17)
        self.assertEqual(
            len(status._fields_) - 1, fdsdk_core.constants.MAX_STATUS
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
        self.assertEqual(fdsdk_core.constants.MAX_BUTTONS, 32)

    def test_velocity_config(self):
        self.assertEqual(
            fdsdk_core.constants.VelocityEstimatorMode.WINDOWING, 0
        )

        self.assertEqual(
            fdsdk_core.constants.DEFAULT_VELOCITY_WINDOW, 20
        )

    def test_com_mode(self):
        self.assertEqual(fdsdk_core.constants.ComMode.SYNC, 0)
        self.assertEqual(fdsdk_core.constants.ComMode.ASYNC, 1)
        self.assertEqual(fdsdk_core.constants.ComMode.VIRTUAL, 3)
        self.assertEqual(fdsdk_core.constants.ComMode.NETWORK, 4)

    def test_thread_priority(self):
        self.assertEqual(fdsdk_core.constants.ThreadPriority.DEFAULT, 0)
        self.assertEqual(fdsdk_core.constants.ThreadPriority.HIGH, 1)
        self.assertEqual(fdsdk_core.constants.ThreadPriority.LOW, 2)
        self.assertEqual(fdsdk_core.constants.ComMode.NETWORK, 4)

    def test_error(self):
        self.assertEqual(fdsdk_core.constants.ErrorNum.NO_ERROR, 0)
        self.assertEqual(fdsdk_core.constants.ErrorNum.ERROR, 1)
        self.assertEqual(fdsdk_core.constants.ErrorNum.COM, 2)
        self.assertEqual(fdsdk_core.constants.ErrorNum.DHC_BUSY, 3)
        self.assertEqual(fdsdk_core.constants.ErrorNum.NO_DRIVER_FOUND, 4)
        self.assertEqual(fdsdk_core.constants.ErrorNum.NO_DEVICE_FOUND, 5)
        self.assertEqual(fdsdk_core.constants.ErrorNum.NOT_AVAILABLE, 6)
        self.assertEqual(fdsdk_core.constants.ErrorNum.TIMEOUT, 7)
        self.assertEqual(fdsdk_core.constants.ErrorNum.GEOMETRY, 8)
        self.assertEqual(fdsdk_core.constants.ErrorNum.EXPERT_MODE_DISABLED, 9)
        self.assertEqual(fdsdk_core.constants.ErrorNum.NOT_IMPLEMENTED, 10)
        self.assertEqual(fdsdk_core.constants.ErrorNum.OUT_OF_MEMORY, 11)
        self.assertEqual(fdsdk_core.constants.ErrorNum.DEVICE_NOT_READY, 12)
        self.assertEqual(fdsdk_core.constants.ErrorNum.FILE_NOT_FOUND, 13)
        self.assertEqual(fdsdk_core.constants.ErrorNum.CONFIGURATION, 14)
        self.assertEqual(fdsdk_core.constants.ErrorNum.INVALID_INDEX, 15)
        self.assertEqual(fdsdk_core.constants.ErrorNum.DEPRECATED, 16)
        self.assertEqual(fdsdk_core.constants.ErrorNum.NULL_ARGUMENT, 17)
        self.assertEqual(fdsdk_core.constants.ErrorNum.REDUNDANT_FAIL, 18)
        self.assertEqual(fdsdk_core.constants.ErrorNum.NOT_ENABLED, 19)
        self.assertEqual(fdsdk_core.constants.ErrorNum.DEVICE_IN_USE, 20)
        self.assertEqual(fdsdk_core.constants.ErrorNum.INVALID, 21)
        self.assertEqual(fdsdk_core.constants.ErrorNum.NO_REGULATION, 22)


if __name__ == "__main__":
    unittest.main()
