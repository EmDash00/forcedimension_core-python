from ctypes import c_bool, c_byte, c_double
from forcedimension_core import runtime as _runtime


_runtime._libdhd.dhdKbHit.argtypes = []
_runtime._libdhd.dhdKbHit.restype = c_bool


def kbHit() -> bool:
    """
    Check keyboard for a key hit. This function is OS
    independent.

    :returns:
        `True` if a key on the keyboard was hit, and `False`
        otherwise.
    """
    return _runtime._libdhd.dhdKbHit()


_runtime._libdhd.dhdKbGet.argtypes = []
_runtime._libdhd.dhdKbGet.restype = c_byte


def kbGet() -> str:
    """
    Retrieve a character from the keyboard. This function is OS
    independent.

    :returns:
        The character hit on the keyboard.
    """
    return chr(_runtime._libdhd.dhdKbGet())


_runtime._libdhd.dhdGetTime.argtypes = []
_runtime._libdhd.dhdGetTime.restype = c_double


def getTime() -> float:
    """
    Returns the current value from the high-resolution system
    counter in [s]. The resolution of the system counter may be
    machine-dependent, as it is usually derived from one of the
    CPU clock signals. The time returned, however, is guarunteed
    to be monotonic.

    :returns:
        The current monotonic time in [s] from the
        high-resolution system counter.
    """
    return _runtime._libdhd.dhdGetTime()


_runtime._libdhd.dhdSleep.argtypes = [c_double]
_runtime._libdhd.dhdSleep.restype = None


def sleep(sec: float) -> None:
    """
    Sleep for a given period of time in [s]. This function is OS
    independent.
    """
    _runtime._libdhd.dhdSleep(sec)
