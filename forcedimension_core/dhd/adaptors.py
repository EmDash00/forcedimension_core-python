from collections.abc import Callable
from typing import Any


class DHDError(Exception):
    """Represents an internal DHD library error."""

    def __init__(
        self, msg: str | None = "An undocumented error has occurred.", **kwargs
    ):
        if msg is not None:
            return super().__init__(msg)
        return super().__init__()


class DHDFeatureError(DHDError):
    """Represents a DHD library error where a feature was
    attempted to be used when it is not available on the
    device.
    """

    def __init__(
        self,
        *,
        reason: str,
        ID: int | None = None,
        op: Callable[[Any], Any] | None,
        **kwargs,
    ):
        op_seg = "A op" if op is None else str(op)
        id_seg = "" if ID is None else f" on device {ID} "

        return super().__init__(f"{op_seg} is not available{id_seg}because {reason}.")


class DHDErrorExpertModeDisabled(DHDFeatureError):
    """Reprseents the internal DHD error raised when an expert
    mode function is attempted to be used when it is not
    enabled.
    """

    def __init__(self, *args, op: Callable[[Any], Any] | None = None, **kwargs):
        if "ID" in kwargs:
            kwargs.pop("ID")

        return super().__init__(
            reason="expert mode is disabled", ID=None, op=op, **kwargs
        )


class DHDErrorFeatureNotAvailable(DHDFeatureError):
    """Represents a DHD library error where a feature was
    attempted to be used when it is not supported on the
    device.
    """

    def __init__(
        self, *args, op: Callable[[Any], Any] | None, ID: int | None = None, **kwargs
    ):
        return super().__init__(
            reason="it is not supported on this device", ID=ID, op=op, **kwargs
        )


class DHDErrorFeatureNotEnabled(DHDFeatureError):
    """Represents a DHD library error where a feature was
    attempted to be used when it is not enabled on the device.
    """

    def __init__(
        self,
        *args,
        op: Callable[[Any], Any] | None = None,
        ID: int | None = None,
        **kwargs,
    ):
        return super().__init__(
            reason="it was previously disabled for this device", ID=ID, op=op, **kwargs
        )


class DHDErrorDeviceNotReady(DHDFeatureError):
    """Represents a DHD library error where a device was
    attempted to be used when it is not yet ready to process a
    new command.
    """

    def __init__(
        self, *args, op: Callable[[Any], Any] | None, ID: int | None = None, **kwargs
    ):
        return super().__init__(
            reason="the device isn't ready to process a new command",
            op=op,
            ID=ID,
            **kwargs,
        )


class DHDErrorRedundantFail(DHDError):
    """Represents a DHD library error where a device's internal
    redundant encoder integrity test failed.
    """

    def __init__(self, *, ID: int | None = None, **kwargs):
        spec = f" on device ID {ID}" if ID is not None else ""

        super().__init__(f"The redundant encoder integrity test failed{spec}", **kwargs)


class DHDIOError(DHDError, OSError):
    """Represents a generic DHD library IO error where a device's
    internal redundant encoder integrity test failed.
    """

    def __init__(
        self, *args, err: str, ID: int | None = None, op: str | None = None, **kwargs
    ):
        op_seg = "" if op is None else f"{op} failed. "
        id_seg = "" if ID is None else f" occurred on device {ID}"

        return super().__init__(f"{op_seg}{err}{id_seg}")


class DHDErrorTimeout(DHDIOError):
    """Represents a timeout error when communicating with a
    device.
    """

    def __init__(self, *args, op: str | None = None, ID: int | None = None, **kwargs):
        return super().__init__(err="timeout", ID=ID, op=op, **kwargs)


class DHDErrorCom(DHDIOError):
    """Represents a communication error when communicating with a
    device.
    """

    def __init__(self, *args, ID: int | None = None, **kwargs):
        return super().__init__(
            err="A communication error between the host and the HapticDevice",
            ID=ID,
            **kwargs,
        )


class DHDErrorDHCBusy(DHDIOError):
    """Represents an error where the device controller is
    busy.
    """

    def __init__(self, *, ID: int | None = None, **kwargs):
        return super().__init__(err="The device controller is busy.", ID=ID, **kwargs)


class DHDErrorNoDeviceFound(DHDIOError):
    """Represents an error when attempting to open a device when
    no devices are found.
    """

    def __init__(self, **kwargs):
        return super().__init__(
            err="No compatible Force Dimension devices found", **kwargs
        )


class DHDErrorDeviceInUse(DHDIOError):
    """Represents an error when attempting to open a device when
    the requested device is in use.
    """

    def __init__(self, *, ID: int | None = None, **kwargs):
        super().__init__(
            err="Open error (because the device is already in use)", ID=ID, **kwargs
        )


class DHDErrorNoDriverFound(DHDIOError):
    """Represents an error when attempting to open a device when
    the requested device's drivers were unable to be found.
    """

    def __init__(self, *, ID: int | None = None, **kwargs):
        return super().__init__(
            err="A required driver is not installed (see device manual fordetails)",
            ID=ID,
            **kwargs,
        )


class DHDErrorConfiguration(DHDIOError):
    """Represents an error where a device's firmware or internal
    configuration health check has failed.
    """

    def __init__(self, *, ID: int | None = None, **kwargs):
        super().__init__(
            err="The firmware or internal configuration health check failed",
            ID=ID,
            **kwargs,
        )


class DHDErrorGeometry(DHDError):
    """Represents an error that has occurred within a device's
    internal geometric model.
    """

    def __init__(self, ID: int | None = None, *args, **kwargs):
        spec = f"device ID {ID}'s" if ID is not None else "the device's"

        return super().__init__(f"An error has occurred within {spec} geometric model")


class DHDErrorMemory(DHDError, MemoryError):
    """Represents an error that has occurred when an operation
    with DHD is unable to be completed because the system has run
    out of memory.
    """

    def __init__(self, *args, **kwargs):
        return super().__init__("DHD ran out of memory.")


class DHDErrorNotImplemented(DHDError, NotImplementedError):
    """Represents an error that has occurred when a requested
    operation has not yet been implemented.
    """

    def __init__(self, *args, **kwargs):
        return super().__init__("The command or op is currently not implemented.")


class DHDErrorFileNotFound(DHDError, FileNotFoundError):
    """Represents an error that has occurred when a requested
    operation needs a file but could not find the file.
    """

    def __init__(self, *args, **kwargs):
        return super().__init__()


class DHDErrorDeprecated(DHDError):
    """Represents an error that has occurred due to the use of a
    deprecated operation, function, or device.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            "This op, function, or current device is marked as deprecated."
        )


class DHDErrorInvalidIndex(DHDError, IndexError):
    """Represents an error that has occurred when an index passed
    to a function is outside the expected range for that
    index.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            "An index passed to the function is outside the expected valid range. "
        )


class DHDErrorArgument(DHDError, ValueError):
    """Represents an error that has occurred when a function was
    passed an invalid or null pointer argument.
    """

    def __init__(self, null: bool = False, *args, **kwargs):
        if not null:
            super().__init__(
                "The function producing this error was passed an invalid argument."
            )
        else:
            super().__init__(
                "The function producing this error was passed an unexpected "
                "null pointer argument."
            )


class DHDErrorNullArgument(DHDErrorArgument):
    """Represents an error that has occurred when a function was
    passed a null argument.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(null=True)


class DHDErrorNoRegulation(DHDError):
    """Represents an error that has occurred because the robotic
    regulation thread is not running.

    This error only applies to functions from the robotic SDK
    (DRD).

    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            "The robotic regulation thread is not running. This only applies "
            "to functions from the robotic SDK (DRD)."
        )
