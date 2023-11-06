from typing import Dict
from typing import cast as _cast

from forcedimension_core import dhd
from forcedimension_core.constants import (
    ComMode, DeviceType, Handedness, VelocityEstimatorMode
)
from forcedimension_core.typing import ComModeStr


_error = [
    None,
    dhd.DHDError,
    dhd.DHDErrorCom,
    dhd.DHDErrorDHCBusy,
    dhd.DHDErrorNoDriverFound,
    dhd.DHDErrorNoDeviceFound,
    dhd.DHDErrorFeatureNotAvailable,
    dhd.DHDErrorTimeout,
    dhd.DHDErrorGeometry,
    dhd.DHDErrorExpertModeDisabled,
    dhd.DHDErrorNotImplemented,
    dhd.DHDErrorMemory,
    dhd.DHDErrorDeviceNotReady,
    dhd.DHDErrorFileNotFound,
    dhd.DHDErrorConfiguration,
    dhd.DHDErrorInvalidIndex,
    dhd.DHDErrorDeprecated,
    dhd.DHDErrorNullArgument,
    dhd.DHDErrorRedundantFail,
    dhd.DHDErrorFeatureNotEnabled,
    dhd.DHDErrorDeviceInUse,
    dhd.DHDErrorArgument,
    dhd.DHDErrorNoRegulation
]

_com_mode_strs = {
    ComMode.SYNC: 'sync',
    ComMode.ASYNC: 'async',
    ComMode.VIRTUAL: 'virtual',
    ComMode.NETWORK: 'network'
}

_com_modes: Dict[ComModeStr, ComMode] = {
    'sync': ComMode.SYNC,
    'async': ComMode.ASYNC,
    'virtual': ComMode.VIRTUAL,
    'network': ComMode.NETWORK,
}

_devtype_strs = {
    DeviceType.NONE: 'none',
    DeviceType.DELTA3: 'delta.3',
    DeviceType.OMEGA3: 'omega.3',
    DeviceType.OMEGA6_RIGHT: 'omega.6 right',
    DeviceType.OMEGA6_LEFT: 'omega.6 left',
    DeviceType.OMEGA7_RIGHT: 'omega.7 right',
    DeviceType.OMEGA7_LEFT: 'omega.7 left',
    DeviceType.CONTROLLER: 'controller',
    DeviceType.CONTROLLER_HR: 'controller hr',
    DeviceType.CUSTOM: 'custom',
    DeviceType.SIGMA3: 'sigma.3',
    DeviceType.SIGMA7_RIGHT: 'sigma.7 right',
    DeviceType.SIGMA7_LEFT: 'sigma.7 left',
    DeviceType.LAMBDA3: 'lambda.3',
    DeviceType.LAMBDA7_RIGHT: 'lambda.7 right',
    DeviceType.LAMBDA7_LEFT: 'lambda.7 left',
    DeviceType.FALCON: 'novint falcon',
}

_devtype_strs_pretty = {
    DeviceType.NONE: 'None',
    DeviceType.DELTA3: 'DELTA.3',
    DeviceType.OMEGA3: 'OMEGA.3',
    DeviceType.OMEGA6_RIGHT: 'OMEGA.6 Right',
    DeviceType.OMEGA6_LEFT: 'OMEGA.6 Left',
    DeviceType.OMEGA7_RIGHT: 'OMEGA.7 Right',
    DeviceType.OMEGA7_LEFT: 'OMEGA.7 Left',
    DeviceType.CONTROLLER: 'CONTROLLER',
    DeviceType.CONTROLLER_HR: 'CONTROLLER HR',
    DeviceType.CUSTOM: 'Custom',
    DeviceType.SIGMA3: 'SIGMA.3',
    DeviceType.SIGMA7_RIGHT: 'SIGMA.7 Right',
    DeviceType.SIGMA7_LEFT: 'SIGMA.7 Left',
    DeviceType.LAMBDA3: 'LAMBDA.3',
    DeviceType.LAMBDA7_RIGHT: 'LAMBDA.7 Right',
    DeviceType.LAMBDA7_LEFT: 'LAMBDA.7 Left',
    DeviceType.FALCON: 'Novint Falcon',
}

_handedness = {
    DeviceType.OMEGA6_RIGHT: Handedness.RIGHT,
    DeviceType.OMEGA6_LEFT: Handedness.LEFT,
    DeviceType.OMEGA7_RIGHT: Handedness.RIGHT,
    DeviceType.OMEGA7_LEFT: Handedness.LEFT,
    DeviceType.SIGMA7_RIGHT: Handedness.RIGHT,
    DeviceType.SIGMA7_LEFT: Handedness.LEFT,
    DeviceType.LAMBDA7_RIGHT: Handedness.RIGHT,
    DeviceType.LAMBDA7_LEFT: Handedness.LEFT,
}

_handedness_str = ['none', 'left', 'right']
_handedness_str_pretty = ['None', 'Left', 'Right']

_estimator_mode_str = {
    VelocityEstimatorMode.WINDOWING: "windowing"
}

_estimator_mode_str_pretty = {
    VelocityEstimatorMode.WINDOWING: "Windowing"
}

_dof = {
    DeviceType.DELTA3: 3,
    DeviceType.OMEGA3: 3,
    DeviceType.OMEGA6_RIGHT: 6,
    DeviceType.OMEGA6_LEFT: 6,
    DeviceType.OMEGA7_RIGHT: 7,
    DeviceType.OMEGA7_LEFT: 7,
    DeviceType.SIGMA3: 3,
    DeviceType.SIGMA7_RIGHT: 7,
    DeviceType.SIGMA7_LEFT: 7,
    DeviceType.LAMBDA3: 3,
    DeviceType.LAMBDA7_RIGHT: 7,
    DeviceType.LAMBDA7_LEFT: 7,
    DeviceType.FALCON: 3,
}


def com_mode_str(com_mode: ComMode) -> ComModeStr:
    return _cast(ComModeStr, _com_mode_strs[com_mode])


def com_mode_from_str(com_mode_str: ComModeStr) -> ComMode:
    return _com_modes[com_mode_str]


def num_dof(devtype: DeviceType) -> int:
    if devtype not in _dof:
        return 0

    return _dof[devtype]


def devtype_str(devtype: DeviceType, pretty: bool = False) -> str:
    if pretty:
        return _devtype_strs_pretty[devtype]

    return _devtype_strs[devtype]


def handedness(devtype: DeviceType) -> Handedness:
    if devtype in _handedness:
        return _handedness[devtype]

    return Handedness.NONE


def handedness_str(handedness: Handedness, pretty: bool = False) -> str:
    if pretty:
        return _handedness_str_pretty[handedness]

    return _handedness_str[handedness]


def velocity_estimator_mode_str(
    mode: VelocityEstimatorMode, pretty: bool = False
):
    if pretty:
        return _estimator_mode_str_pretty[mode]

    return _estimator_mode_str[mode]


def errno_to_exception(errno: int):
    """
    Convert a DHD error number to an exception.
    """
    return _error[errno]
