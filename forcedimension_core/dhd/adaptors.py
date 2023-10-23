from enum import IntEnum
from typing import Any, Callable, Dict, Literal, Optional
import typing

from forcedimension_core.typing import ComModeStr
from forcedimension_core.dhd.constants import (
    DEFAULT_VELOCITY_WINDOW, MAX_STATUS,
    ComMode, DeviceType, ErrorNum, VelocityEstimatorMode
)

class Handedness(IntEnum):
    NONE = 0
    LEFT = 1
    RIGHT = 2


class DHDError(Exception):
    def __init__(
        self, msg: Optional[str] = "An undocumented error has occured.",
        **kwargs
    ):
        if msg is not None:
            return super().__init__(msg)
        else:
            return super().__init__()


class DHDFeatureError(DHDError):
    def __init__(
        self,
        *,
        reason: str,
        ID: Optional[int] = None,
        op: Optional[Callable[[Any], Any]],
        **kwargs
    ):
        op_seg = (
            "A op" if op is None else str(op)
        )
        id_seg = "" if ID is None else f" on device {ID} "

        return super().__init__(
            f"{op_seg} is not available{id_seg}because {reason}."
        )


class DHDErrorExpertModeDisabled(DHDFeatureError):
    def __init__(
        self,
        *args,
        op: Optional[Callable[[Any], Any]] = None,
        **kwargs
    ):
        if 'ID' in kwargs:
            kwargs.pop('ID')

        return super().__init__(
            reason="expert mode is disabled",
            ID=None,
            op=op,
            **kwargs
        )


class DHDErrorFeatureNotAvailable(DHDFeatureError):
    def __init__(
        self,
        *args,
        op: Optional[Callable[[Any], Any]],
        ID: Optional[int] = None,
        **kwargs
    ):

        return super().__init__(
            reason="it is not supported on this device",
            ID=ID,
            op=op,
            **kwargs
        )


class DHDErrorFeatureNotEnabled(DHDFeatureError):
    def __init__(
        self,
        *args,
        op: Optional[Callable[[Any], Any]] = None,
        ID: Optional[int] = None,
        **kwargs
    ):

        return super().__init__(
            reason="it was previously disabled for this device",
            ID=ID,
            op=op,
            **kwargs
        )


class DHDErrorDeviceNotReady(DHDFeatureError):
    def __init__(
        self,
        *,
        op: Optional[Callable[[Any], Any]],
        ID: Optional[int] = None,
        **kwargs
    ):
        return super().__init__(
            reason="the device isn't ready to proccess a new command",
            op=op,
            ID=ID,
            **kwargs
        )


class DHDErrorRedundantFail(DHDError):
    def __init__(self, *, ID: Optional[int] = None, **kwargs):
        if ID is not None:
            spec = f" on device ID {ID}"
        else:
            spec = ""

        super().__init__(
            f"The redundant encoder integrity test failed{spec}",
            **kwargs
        )


class DHDIOError(DHDError, OSError):
    def __init__(
        self,
        *args,
        err: str,
        ID: Optional[int] = None,
        op: Optional[str] = None,
        **kwargs
    ):
        op_seg = "" if op is None else f"{op} failed. "
        id_seg = "" if ID is None else f" occured on device {ID}"

        return super().__init__(f"{op_seg}{err}{id_seg}")


class DHDErrorTimeout(DHDIOError):
    def __init__(
        self,
        *args,
        op: Optional[str] = None,
        ID: Optional[int] = None,
        **kwargs
    ):

        return super().__init__(
            err="timeout",
            ID=ID,
            op=op,
            **kwargs
        )


class DHDErrorCom(DHDIOError):
    def __init__(
        self,
        *args,
        ID: Optional[int] = None,
        **kwargs
    ):
        return super().__init__(
            err="A communication error between the host and the HapticDevice",
            ID=ID,
            **kwargs
        )


class DHDErrorDHCBusy(DHDIOError):
    def __init__(self, *, ID: Optional[int] = None, **kwargs):
        return super().__init__(
            err="The device controller is busy.",
            ID=ID,
            **kwargs
        )


class DHDErrorNoDeviceFound(DHDIOError):
    def __init__(self, **kwargs):
        return super().__init__(
            err="No compatible Force Dimension devices found",
            **kwargs
        )


class DHDErrorDeviceInUse(DHDIOError):
    def __init__(self, *, ID: Optional[int] = None, **kwargs):
        super().__init__(
            err="Open error (because the device is already in use)",
            ID=ID,
            **kwargs
        )


class DHDErrorNoDriverFound(DHDIOError):
    def __init__(self, *, ID: Optional[int] = None, **kwargs):
        return super().__init__(
            err="A required driver is not installed (see device manual for"
                "details)",
            ID=ID,
            **kwargs
        )


class DHDErrorConfiguration(DHDIOError):
    def __init__(self, *, ID: Optional[int] = None, **kwargs):
        super().__init__(
            err="The firmware or internal configuration health check failed",
            ID=ID,
            **kwargs
        )


class DHDErrorGeometry(DHDError):
    def __init__(self, ID: Optional[int] = None, *args, **kwargs):

        if (ID is not None):
            spec = f"device ID {ID}'s"
        else:
            spec = "the device's"

        return super().__init__(
            f"An error has occured within {spec} geometric model"
        )


class DHDErrorMemory(DHDError, MemoryError):
    def __init__(self, *args, **kwargs):
        return super().__init__(
            "DHD ran out of memory."
        )


class DHDErrorNotImplemented(DHDError, NotImplementedError):
    def __init__(self, *args, **kwargs):
        return super().__init__(
            "The command or op is currently not implemented."
        )


class DHDErrorFileNotFound(DHDError, FileNotFoundError):
    def __init__(self, *args, **kwargs):
        return super().__init__()


class DHDErrorDeprecated(DHDError):
    def __init__(self, *args, **kwargs):
        super().__init__(
            "This op, function, or current device is marked as "
            "deprecated."
        )


class DHDErrorInvalidIndex(DHDError, IndexError):
    def __init__(self, *args, **kwargs):
        super().__init__(
            "An index passed to the function is outside the expected valid "
            "range. "
        )


class DHDErrorArgument(DHDError, ValueError):
    def __init__(self, null: bool = False, *args, **kwargs):
        if not null:
            super().__init__(
                "The function producing this error was passed an invalid or "
                "argument."
            )
        else:
            super().__init__(
                "The function producing this error was passed an unexpected "
                "null pointer argument."
            )


class DHDErrorNullArgument(DHDErrorArgument):
    def __init__(self, *args, **kwargs):
        super().__init__(null=True)


class DHDErrorNoRegulation(DHDError):
    def __init__(self, *args, **kwargs):
        super().__init__(
            "The robotic regulation thread is not running. This only applies "
            "to functions from the robotic SDK (DRD)."
        )


_error = [
    None,
    DHDError,
    DHDErrorCom,
    DHDErrorDHCBusy,
    DHDErrorNoDriverFound,
    DHDErrorNoDeviceFound,
    DHDErrorFeatureNotAvailable,
    DHDErrorTimeout,
    DHDErrorGeometry,
    DHDErrorExpertModeDisabled,
    DHDErrorNotImplemented,
    DHDErrorMemory,
    DHDErrorDeviceNotReady,
    DHDErrorFileNotFound,
    DHDErrorConfiguration,
    DHDErrorInvalidIndex,
    DHDErrorDeprecated,
    DHDErrorNullArgument,
    DHDErrorRedundantFail,
    DHDErrorFeatureNotEnabled,
    DHDErrorDeviceInUse,
    DHDErrorArgument,
    DHDErrorNoRegulation
]

_com_mode_strs = [
    'sync',
    'async',
    'virtual',
    'network'
]

_com_modes: Dict[ComModeStr, ComMode] = {
    'sync': ComMode.SYNC,
    'async': ComMode.ASYNC,
    'virtual': ComMode.VIRTUAL,
    'network': ComMode.NETWORK,
}

_devtype_strs = {
    DeviceType.NONE: 'None',
    DeviceType.DELTA3: 'DELTA.3',
    DeviceType.OMEGA3: 'OMEGA.3',
    DeviceType.OMEGA6_RIGHT: 'OMEGA.6 right',
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

_handedness_str = ['None', 'Left', 'Right']

_estimator_mode_str = {
    VelocityEstimatorMode.WINDOWING: "Windowing"
}

_dof = {
    DeviceType.DELTA3: 3,
    DeviceType.OMEGA3: 3,
    DeviceType.OMEGA6_RIGHT: 6,
    DeviceType.OMEGA6_LEFT: 6,
    DeviceType.OMEGA7_RIGHT: 7,
    DeviceType.OMEGA7_LEFT: 6,
    DeviceType.SIGMA3: 3,
    DeviceType.SIGMA7_RIGHT: 7,
    DeviceType.SIGMA7_LEFT: 7,
    DeviceType.LAMBDA3: 3,
    DeviceType.LAMBDA7_RIGHT: 7,
    DeviceType.LAMBDA7_LEFT: 7,
    DeviceType.FALCON: 3,
}

def com_mode_str(com_mode: int) -> ComModeStr:
    return typing.cast(ComModeStr, _com_mode_strs[com_mode])


def com_mode_from_str(com_mode_str: ComModeStr) -> ComMode:
    return _com_modes[com_mode_str]


def num_dof(devtype: DeviceType) -> int:
    if devtype not in _dof:
        return 0

    return _dof[devtype]

def devtype_str(devtype: DeviceType) -> str:
    return _devtype_strs[devtype]


def handedness(devtype: DeviceType) -> Handedness:
    if devtype in _handedness:
        return _handedness[devtype]

    return Handedness.NONE

def handedness_str(handedness: Handedness) -> str:
    return _handedness_str[handedness]


def velocity_estimator_mode_str(mode: VelocityEstimatorMode):
    return _estimator_mode_str[mode]



def errno_to_exception(errno: int):
    """
    Convert a DHD error number to an exception.
    """
    return _error[errno]
