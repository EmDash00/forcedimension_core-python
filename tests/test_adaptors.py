from math import nan
import unittest

import pydantic

import forcedimension_core as fd
from forcedimension_core.dhd.adaptors import (
    DHDError, DHDErrorArgument,
    DHDErrorCom,
    DHDErrorConfiguration,
    DHDErrorDeprecated,
    DHDErrorDeviceInUse,
    DHDErrorDeviceNotReady,
    DHDErrorDHCBusy,
    DHDErrorExpertModeDisabled,
    DHDErrorFeatureNotAvailable,
    DHDErrorFeatureNotEnabled,
    DHDErrorFileNotFound,
    DHDErrorGeometry,
    DHDErrorInvalidIndex,
    DHDErrorMemory,
    DHDErrorNoDeviceFound,
    DHDErrorNoDriverFound,
    DHDErrorNoRegulation,
    DHDErrorNotImplemented,
    DHDErrorNullArgument,
    DHDErrorRedundantFail,
    DHDErrorTimeout, Handedness
)
from forcedimension_core.constants import (ComMode, DeviceType, ErrorNum,
                                               VelocityEstimatorMode)

from forcedimension_core.drd.adaptors import TrajectoryGenParams


class TestAdaptors(unittest.TestCase):
    def test_com_mode_str(self):
        self.assertEqual(fd.com_mode_str(ComMode.SYNC), 'sync')
        self.assertEqual(fd.com_mode_str(ComMode.ASYNC), 'async')
        self.assertEqual(fd.com_mode_str(ComMode.VIRTUAL), 'virtual')
        self.assertEqual(fd.com_mode_str(ComMode.NETWORK), 'network')

    def test_com_mode_from_str(self):
        self.assertEqual(fd.com_mode_from_str('sync'), ComMode.SYNC)
        self.assertEqual(fd.com_mode_from_str('async'), ComMode.ASYNC)
        self.assertEqual(
            fd.com_mode_from_str('virtual'), ComMode.VIRTUAL
        )
        self.assertEqual(
            fd.com_mode_from_str('network'), ComMode.NETWORK
        )

    def test_num_dof(self):
        self.assertEqual(fd.num_dof(DeviceType.DELTA3), 3)
        self.assertEqual(fd.num_dof(DeviceType.OMEGA3), 3)
        self.assertEqual(fd.num_dof(DeviceType.SIGMA3), 3)
        self.assertEqual(fd.num_dof(DeviceType.LAMBDA3), 3)
        self.assertEqual(fd.num_dof(DeviceType.FALCON), 3)

        self.assertEqual(fd.num_dof(DeviceType.SIGMA7_LEFT), 7)
        self.assertEqual(fd.num_dof(DeviceType.SIGMA7_RIGHT), 7)

        self.assertEqual(fd.num_dof(DeviceType.OMEGA6_LEFT), 6)
        self.assertEqual(fd.num_dof(DeviceType.OMEGA6_RIGHT), 6)

        self.assertEqual(fd.num_dof(DeviceType.OMEGA7_LEFT), 7)
        self.assertEqual(fd.num_dof(DeviceType.OMEGA7_RIGHT), 7)

        self.assertEqual(fd.num_dof(DeviceType.LAMBDA7_LEFT), 7)
        self.assertEqual(fd.num_dof(DeviceType.LAMBDA7_RIGHT), 7)

        self.assertEqual(fd.num_dof(DeviceType.CONTROLLER), 0)
        self.assertEqual(fd.num_dof(DeviceType.CONTROLLER_HR), 0)
        self.assertEqual(fd.num_dof(DeviceType.NONE), 0)

    def test_devtype_str(self):
        # Regular str tests

        self.assertEqual(fd.devtype_str(DeviceType.DELTA3), 'delta.3')
        self.assertEqual(fd.devtype_str(DeviceType.OMEGA3), 'omega.3')
        self.assertEqual(fd.devtype_str(DeviceType.SIGMA3), 'sigma.3')
        self.assertEqual(fd.devtype_str(DeviceType.LAMBDA3), 'lambda.3')
        self.assertEqual(fd.devtype_str(DeviceType.FALCON), 'novint falcon')

        self.assertEqual(fd.devtype_str(DeviceType.SIGMA7_LEFT),'sigma.7 left')
        self.assertEqual(
            fd.devtype_str(DeviceType.SIGMA7_RIGHT), 'sigma.7 right'
        )

        self.assertEqual(
            fd.devtype_str(DeviceType.OMEGA6_LEFT), 'omega.6 left'
        )
        self.assertEqual(
            fd.devtype_str(DeviceType.OMEGA6_RIGHT), 'omega.6 right'
        )

        self.assertEqual(
            fd.devtype_str(DeviceType.OMEGA7_LEFT), 'omega.7 left'
        )
        self.assertEqual(
            fd.devtype_str(DeviceType.OMEGA7_RIGHT),
            'omega.7 right'
        )

        self.assertEqual(
            fd.devtype_str(DeviceType.LAMBDA7_LEFT), 'lambda.7 left'
        )
        self.assertEqual(
            fd.devtype_str(DeviceType.LAMBDA7_RIGHT), 'lambda.7 right'
        )

        self.assertEqual(
            fd.devtype_str(DeviceType.CONTROLLER), 'controller'
        )

        self.assertEqual(
            fd.devtype_str(DeviceType.CONTROLLER_HR), 'controller hr'
        )

        self.assertEqual(fd.devtype_str(DeviceType.NONE), 'none')
        self.assertEqual(fd.devtype_str(DeviceType.CUSTOM), 'custom')

        # Pretty str tests

        self.assertEqual(
            fd.devtype_str(DeviceType.DELTA3, pretty=True), 'DELTA.3'
        )
        self.assertEqual(
            fd.devtype_str(DeviceType.OMEGA3, pretty=True), 'OMEGA.3'
        )

        self.assertEqual(
            fd.devtype_str(DeviceType.SIGMA3, pretty=True), 'SIGMA.3'
        )

        self.assertEqual(
            fd.devtype_str(DeviceType.LAMBDA3, pretty=True), 'LAMBDA.3'
        )
        self.assertEqual(
            fd.devtype_str(DeviceType.FALCON, pretty=True),
            'Novint Falcon'
        )

        self.assertEqual(
            fd.devtype_str(DeviceType.SIGMA7_LEFT, pretty=True),
            'SIGMA.7 Left'
        )
        self.assertEqual(
            fd.devtype_str(DeviceType.SIGMA7_RIGHT, pretty=True),
            'SIGMA.7 Right'
        )

        self.assertEqual(
            fd.devtype_str(DeviceType.OMEGA6_LEFT, pretty=True),
            'OMEGA.6 Left'
        )
        self.assertEqual(
            fd.devtype_str(DeviceType.OMEGA6_RIGHT, pretty=True),
            'OMEGA.6 Right'
        )

        self.assertEqual(
            fd.devtype_str(DeviceType.OMEGA7_LEFT, pretty=True),
            'OMEGA.7 Left'
        )
        self.assertEqual(
            fd.devtype_str(DeviceType.OMEGA7_RIGHT, pretty=True),
            'OMEGA.7 Right'
        )

        self.assertEqual(
            fd.devtype_str(DeviceType.LAMBDA7_LEFT, pretty=True),
            'LAMBDA.7 Left'
        )
        self.assertEqual(
            fd.devtype_str(DeviceType.LAMBDA7_RIGHT, pretty=True),
            'LAMBDA.7 Right'
        )

        self.assertEqual(
            fd.devtype_str(DeviceType.CONTROLLER, pretty=True),
            'CONTROLLER'
        )
        self.assertEqual(
            fd.devtype_str(DeviceType.CONTROLLER_HR, pretty=True),
            'CONTROLLER HR'
        )
        self.assertEqual(fd.devtype_str(DeviceType.NONE), 'none')
        self.assertEqual(fd.devtype_str(DeviceType.CUSTOM), 'custom')

    def test_handedness(self):
        self.assertEqual(fd.handedness(DeviceType.DELTA3), Handedness.NONE)
        self.assertEqual(fd.handedness(DeviceType.OMEGA3), Handedness.NONE)
        self.assertEqual(fd.handedness(DeviceType.SIGMA3), Handedness.NONE)
        self.assertEqual(fd.handedness(DeviceType.LAMBDA3), Handedness.NONE)
        self.assertEqual(fd.handedness(DeviceType.FALCON), Handedness.NONE)

        self.assertEqual(
            fd.handedness(DeviceType.SIGMA7_LEFT), Handedness.LEFT
        )
        self.assertEqual(
            fd.handedness(DeviceType.SIGMA7_RIGHT), Handedness.RIGHT
        )

        self.assertEqual(
            fd.handedness(DeviceType.OMEGA6_LEFT),
            Handedness.LEFT
        )
        self.assertEqual(
            fd.handedness(DeviceType.OMEGA6_RIGHT),
            Handedness.RIGHT
        )

        self.assertEqual(
            fd.handedness(DeviceType.OMEGA7_LEFT),
            Handedness.LEFT
        )
        self.assertEqual(
            fd.handedness(DeviceType.OMEGA7_RIGHT),
            Handedness.RIGHT
        )

        self.assertEqual(
            fd.handedness(DeviceType.LAMBDA7_LEFT),
            Handedness.LEFT
        )
        self.assertEqual(
            fd.handedness(DeviceType.LAMBDA7_RIGHT),
            Handedness.RIGHT
        )

        self.assertEqual(fd.handedness(DeviceType.CONTROLLER), Handedness.NONE)
        self.assertEqual(
            fd.handedness(DeviceType.CONTROLLER_HR), Handedness.NONE
        )
        self.assertEqual(fd.handedness(DeviceType.NONE), Handedness.NONE)

    def test_handedness_str(self):
        # Regular strs

        self.assertEqual(fd.handedness_str(Handedness.NONE), 'none')
        self.assertEqual(fd.handedness_str(Handedness.LEFT), 'left')
        self.assertEqual(fd.handedness_str(Handedness.RIGHT), 'right')

        # Pretty strs

        self.assertEqual(
            fd.handedness_str(Handedness.NONE, pretty=True), 'None'
        )

        self.assertEqual(
            fd.handedness_str(Handedness.LEFT, pretty=True), 'Left'
        )
        self.assertEqual(
            fd.handedness_str(Handedness.RIGHT, pretty=True), 'Right'
        )

    def test_estimator_mode_str(self):
        # Regular strs

        self.assertEqual(
            fd.velocity_estimator_mode_str(VelocityEstimatorMode.WINDOWING),
            'windowing'
        )

        # Pretty strs

        self.assertEqual(
            fd.velocity_estimator_mode_str(
                VelocityEstimatorMode.WINDOWING, pretty=True
            ),
            'Windowing'
        )

    def test_errno_to_exception(self):
        self.assertIs(fd.errno_to_exception(ErrorNum.NO_ERROR), None)

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.ERROR)(op='', ID=1),
            DHDError
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.ERROR)(op='', ID=1, msg=None),
            DHDError
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.COM)(op='', ID=1, msg=None),
            DHDErrorCom
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.DHC_BUSY)(op='', ID=1),
            DHDErrorDHCBusy
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.NO_DRIVER_FOUND)(op='', ID=1),
            DHDErrorNoDriverFound
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.NO_DEVICE_FOUND)(op='', ID=1),
            DHDErrorNoDeviceFound
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.NOT_AVAILABLE)(op='', ID=1),
            DHDErrorFeatureNotAvailable
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.TIMEOUT)(op='', ID=1),
            DHDErrorTimeout
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.GEOMETRY)(op='', ID=1),
            DHDErrorGeometry
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.GEOMETRY)(op=''),
            DHDErrorGeometry
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.EXPERT_MODE_DISABLED)(op='', ID=1),
            DHDErrorExpertModeDisabled
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.EXPERT_MODE_DISABLED)(op=''),
            DHDErrorExpertModeDisabled
        )


        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.NOT_IMPLEMENTED)(op='', ID=1),
            DHDErrorNotImplemented
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.NOT_IMPLEMENTED)(),
            DHDErrorNotImplemented
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.OUT_OF_MEMORY)(op='', ID=1),
            DHDErrorMemory
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.DEVICE_NOT_READY)(op='', ID=1),
            DHDErrorDeviceNotReady
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.FILE_NOT_FOUND)(op='', ID=1),
            DHDErrorFileNotFound
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.CONFIGURATION)(op='', ID=1),
            DHDErrorConfiguration
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.INVALID_INDEX)(op='', ID=1),
            DHDErrorInvalidIndex
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.DEPRECATED)(op='', ID=1),
            DHDErrorDeprecated
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.NULL_ARGUMENT)(op='', ID=1),
            DHDErrorNullArgument
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.REDUNDANT_FAIL)(op='', ID=1),
            DHDErrorRedundantFail
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.REDUNDANT_FAIL)(op=''),
            DHDErrorRedundantFail
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.NOT_ENABLED)(op='', ID=1),
            DHDErrorFeatureNotEnabled
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.DEVICE_IN_USE)(op='', ID=1),
            DHDErrorDeviceInUse
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.INVALID)(op='', ID=1),
            DHDErrorArgument
        )

        self.assertIsInstance(
            fd.errno_to_exception(ErrorNum.NO_REGULATION)(op='', ID=1),
            DHDErrorNoRegulation
        )

    def test_TrajectoryGenParams(self):
        class Model(pydantic.BaseModel):
            params: TrajectoryGenParams = pydantic.Field(
                default_factory=TrajectoryGenParams
            )

        params = TrajectoryGenParams()
        self.assertTupleEqual(tuple(params), (nan, nan, nan))

        params.vmax = 0.
        params.amax = 1.
        params.jerk = 2.

        self.assertEqual(
            params.pretty_str(0., 0., 0.),
            f"vmax={params.vmax} (default) amax={params.amax} jerk={params.jerk}"
        )

        self.assertEqual(
            params.pretty_str(0., 1., 2.),
            f"vmax={params.vmax} (default) amax={params.amax} (default) "
            f"jerk={params.jerk} (default)"
        )

        model = Model(params=TrajectoryGenParams(vmax=0., amax=1., jerk=2.))

        self.assertRaises(ValueError, lambda: TrajectoryGenParams(vmax=-1))
        self.assertRaises(ValueError, lambda: TrajectoryGenParams(amax=-1))
        self.assertRaises(ValueError, lambda: TrajectoryGenParams(jerk=-1))

        dct = model.model_dump()
        self.assertAlmostEqual(dct['params']['vmax'], 0.0)
        self.assertAlmostEqual(dct['params']['amax'], 1.0)
        self.assertAlmostEqual(dct['params']['jerk'], 2.0)
