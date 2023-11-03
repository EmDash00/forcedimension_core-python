from typing import Any, Callable, Optional

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
        *args,
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

