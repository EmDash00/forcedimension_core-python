import ctypes as ct
from ctypes import c_byte, c_char_p, c_double, c_int, c_ubyte, c_uint, c_ushort
from typing import Tuple
import typing_extensions

from forcedimension_core.dhd.constants import ComMode, MAX_DOF, DeviceType
import forcedimension_core.runtime as _runtime
from forcedimension_core.typing import (
    IntDOFTuple,
    FloatDOFTuple,
    Array,
    MutableArray,
    c_double_ptr,
    c_int_ptr,
    c_ushort_ptr,
    c_ubyte_ptr,
    c_uint_ptr
)

from . import direct_expert as direct


_runtime._libdhd.dhdEnableExpertMode.argtypes = []
_runtime._libdhd.dhdEnableExpertMode.restype = c_int


def enableExpertMode() -> int:
    """
    Enable expert mode.

    :returns: 0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.disableExpertMode()`
    """
    return _runtime._libdhd.dhdEnableExpertMode()


_runtime._libdhd.dhdDisableExpertMode.argtypes = []
_runtime._libdhd.dhdDisableExpertMode.restype = c_int


def disableExpertMode() -> int:
    """
    Disable expert mode.

    :returns: 0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.disableExpertMode()`
    """
    return _runtime._libdhd.dhdDisableExpertMode()


_runtime._libdhd.dhdPreset.argtypes = [c_int_ptr, c_ubyte, c_byte]
_runtime._libdhd.dhdPreset.restype = c_int


def preset(val: Array[int, int], mask: int = 0xff, ID: int = -1) -> int:
    """
    Set selected encoder offsets to a given value. Intended for use with the
    generic controller when no RESET button is available.

    :param Array[int, int] val:
        Vector of encoder offsets refering to each DOF with length
        :data:`forcedimension_core.dhd.constants.MAX_DOF`.

    :param int mask:
        Bitwise mask of which encoder should be set.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``val`` is not implicitly convertible to a C char.

    :raises IndexError:
        If ``len(val) < MAX_DOF``.

    :raises TypeError:
        If ``val`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``mask`` is not implicitly convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns: 0 on success, -1 otherwise
    """
    vals = (c_int * MAX_DOF)(
            val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7]
        )

    return _runtime._libdhd.dhdPreset(
        ct.cast(vals, c_int_ptr),
        mask,
        ID
    )

_runtime._libdhd.dhdSetTimeGuard.argtypes = [c_int, c_byte]
_runtime._libdhd.dhdSetTimeGuard.restype = c_int


def setTimeGuard(min_period: int, ID: int = -1) -> int:
    """
    Enable/disable the :ref:timeguard: feature with an arbitrary minimum
    period.

    :param int min_period:
        Minimum refresh period (in [us]). A value of 0.
        disables the TimeGuard feature, while a value of -1 resets the default
        recommended value.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``min_period`` is not implicitly convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns: 0 on success, -1 otherwise.
    """

    return _runtime._libdhd.dhdSetTimeGuard(min_period, ID)


_runtime._libdhd.dhdSetVelocityThreshold.argtypes = [c_uint, c_byte]
_runtime._libdhd.dhdSetVelocityThreshold.restype = c_int


def setVelocityThreshold(thresh: int, ID: int = -1) -> int:
    """
    Adjust the :ref:`velocity_threshold` of the device (in [m/s]). The velocity
    threshold  is a safety feature that prevents the device from accelerating
    to high  velocities without control. If the velocity of one of the device
    axis passes the threshold, the device enters BRAKE mode.

    Warning
    -------
    Since the range of threshold values is device dependent, it is
    recommended NOT to modify factory settings.


    :param int thresh:
        An arbitrary value of velocity threshold (in [m/s]).

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``thresh`` is not implicitly convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns: 0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.getVelocityThreshold()`
    """

    return _runtime._libdhd.dhdSetVelocityThreshold(thresh, ID)


_runtime._libdhd.dhdGetVelocityThreshold.argtypes = [c_uint_ptr, c_byte]
_runtime._libdhd.dhdGetVelocityThreshold.restype = c_int


def getVelocityThreshold(ID: int = -1) -> int:
    """
    Get the velocity threshold of the device. Velocity threshold is a safety
    feature that prevents the device from accelerating to high velocities
    without control. If the velocity of one of the device axis passes the
    threshold, the device enters BRAKE mode.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        The non-negative velocity threshold on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.setVelocityThreshold()`
    """

    thresh = c_uint()

    if _runtime._libdhd.dhdGetVelocityThreshold(thresh, ID):
        return -1

    return thresh.value


_runtime._libdhd.dhdUpdateEncoders.argtypes = [c_byte]
_runtime._libdhd.dhdUpdateEncoders.restype = c_int


def updateEncoders(ID: int = -1) -> int:
    """
    Force an update of the internal encoder values in the state vector. This
    call retrieves the encoder values from the device and places them into
    the state vector. No kinematic model is called.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns: 0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.getEnc()`
    """
    return _runtime._libdhd.dhdUpdateEncoders(ID)


_runtime._libdhd.dhdGetDeltaEncoders.argtypes = [
    c_int_ptr,
    c_int_ptr,
    c_int_ptr,
    c_byte
]
_runtime._libdhd.dhdGetDeltaEncoders.restype = c_int


def getDeltaEncoders(out: MutableArray[int, int], ID: int = -1) -> int:
    """
    Read all encoders values of the DELTA structure

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param Array[int, int] out:
        An output buffer to store the raw encoder values.

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD` on success, and
        -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.deltaEncodersToJointAngles()`
    | :func:`forcedimension_core.dhd.expert.deltaEncoderToPosition()`


    """

    enc0 = c_int()
    enc1 = c_int()
    enc2 = c_int()

    err = _runtime._libdhd.dhdGetDeltaEncoders(enc0, enc1, enc2, ID)

    out[0] = enc0.value
    out[1] = enc1.value
    out[2] = enc2.value

    return err


_runtime._libdhd.dhdGetWristEncoders.argtypes = [
    c_int_ptr,
    c_int_ptr,
    c_int_ptr,
    c_byte
]
_runtime._libdhd.dhdGetWristEncoders.restype = c_int


def getWristEncoders(out: MutableArray[int, int], ID: int = -1) -> int:
    """
    Read all encoders values of the wrist structure.

    Note
    ----
    This feature only applies to devices with a wrist. See
    the :ref:`device_types` section for more details.


    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :param Array[int, int] out:
        An output buffer to store the raw wrist encoder values.

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.wristEncodersToOrientation()`
    | :func:`forcedimension_core.dhd.wristEncodersToJointAngles()`
    | :func:`forcedimension_core.dhd.wristOrientationToEncoder()`
    """

    enc0 = c_int()
    enc1 = c_int()
    enc2 = c_int()

    err = _runtime._libdhd.dhdGetWristEncoders(
        enc0,
        enc1,
        enc2,
        ID
    )

    out[0] = enc0.value
    out[1] = enc1.value
    out[2] = enc2.value

    return err


_runtime._libdhd.dhdGetGripperEncoder.argtypes = [c_int_ptr, c_byte]
_runtime._libdhd.dhdGetGripperEncoder.restype = c_int


def getGripperEncoder(out: c_int, ID: int = -1) -> int:
    """
    Read the encoder value of the force gripper.

    Note
    ----
    This feature only applies to devices with a gripper. See
    the :ref:`device_types` section for more details.


    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param c_int out:
        Output buffer to store the encoder value of the force gripper.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        Tuple of (enc, err). enc is the encoder value of the force gripper.
        err is  0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.
    """

    return _runtime._libdhd.dhdGetGripperEncoder(out, ID)


_runtime._libdhd.dhdGetEncoder.argtypes = [c_int, c_byte]
_runtime._libdhd.dhdGetEncoder.restype = c_int


def getEncoder(index: int, ID: int = -1) -> int:
    """
    Read a single encoder value from the haptic device.

    :param int index:
        The motor index number as defined by
        :data:`forcedimension_core.dhd.constants.MAX_DOF`

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``index`` is not implicitly convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns: The (positive) encoder reading on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.getEnc()`
    """

    return _runtime._libdhd.dhdGetEncoder(index, ID)


_runtime._libdhd.dhdSetMotor.argtypes = [c_int, c_ushort, c_byte]
_runtime._libdhd.dhdSetMotor.restype = c_int


def setMotor(index: int, output: int, ID: int = -1) -> int:
    """
    Program a command to a single motor channel.

    :param int index:
        The motor index number as defined by
        :data:`forcedimension_core.dhd.constants.MAX_DOF`

    :param int output:
        The motor DAa C char.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``index`` is not implicitly convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``output`` is not implicitly convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns: 0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.setMot()`
    | :func:`forcedimension_core.dhd.expert.setDeltaMotor()`
    | :func:`forcedimension_core.dhd.expert.setWristMotor()`
    """

    return _runtime._libdhd.dhdSetMotor(index, output, ID)


_runtime._libdhd.dhdSetDeltaMotor.argtypes = [c_ushort, c_ushort, c_ushort, c_byte]
_runtime._libdhd.dhdSetDeltaMotor.restype = c_int


def setDeltaMotor(mot: Array[int, int], ID: int = -1) -> int:
    """
    Set desired motor commands to the amplifier channels commanding the DELTA
    motors.

    :param Array[int, int] mot:
        Sequence of ``(mot0, mot1, mot2)`` where ``mot0``, ``mot1``,
        and ``mot2`` are the axis 0, 1, and 2 DELTA motor commands,
        respectively.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If any element of ``mot`` is not implicitly convertible to a C ushort.

    :raises IndexError:
        If ``len(mot) < 3``.

    :raises TypeError:
        If ``mot`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns: 0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.setMot()`
    | :func:`forcedimension_core.dhd.expert.setMotor()`
    | :func:`forcedimension_core.dhd.expert.setWristMotor()`
    """
    return _runtime._libdhd.dhdSetDeltaMotor(mot[0], mot[1], mot[2], ID)


_runtime._libdhd.dhdSetWristMotor.argtypes = [
    c_ushort, c_ushort, c_ushort, c_byte
]
_runtime._libdhd.dhdSetWristMotor.restype = c_int


def setWristMotor(output: Array[int, int], ID: int = -1) -> int:
    """
    Set desired motor commands to the amplifier channels commanding the wrist
    motors.

    Note
    ----
    This feature only applies to the following devices:

    :data:`forcedimension_core.dhd.constants.DeviceType.SIGMA7_RIGHT`
    :data:`forcedimension_core.dhd.constants.DeviceType.SIGMA7_LEFT`


    :param Array[int, int] output:
        Sequence of (output0, output1, output2) where ``output0``, ``output1``,
        and ``output2`` are the axis 0, 1, and 2 wrist motor commands,
        respectively.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If any element of ``output`` is not implicitly convertible to a C char.

    :raises IndexError:
        If ``len(output) < 3``.

    :raises TypeError:
        If ``output`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns: 0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.setMot()`
    | :func:`forcedimension_core.dhd.setMotor()`
    | :func:`forcedimension_core.dhd.setDeltaMotor()`
    | :func:`forcedimension_core.dhd.setGripperMotor()`
    """
    return _runtime._libdhd.dhdSetWristMotor(output[0], output[1], output[2], ID)


_runtime._libdhd.dhdSetGripperMotor.argtypes = [c_ushort, c_byte]
_runtime._libdhd.dhdSetGripperMotor.restype = c_int


def setGripperMotor(output: int, ID: int = -1) -> int:
    """
    Set desired motor commands to the amplifier channels commanding the force
    gripper.

    :param int output:
        Gripper motor command.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``output`` is not implicitly convertible to a C ushort.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns: 0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.setMot()`
    | :func:`forcedimension_core.dhd.setMotor()`
    | :func:`forcedimension_core.dhd.setDeltaMotor()`
    | :func:`forcedimension_core.dhd.setWristMotor()`
    """
    return _runtime._libdhd.dhdSetWristMotor(output, ID)


_runtime._libdhd.dhdDeltaEncoderToPosition.argtypes = [
    c_int,
    c_int,
    c_int,
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_byte
]
_runtime._libdhd.dhdDeltaEncoderToPosition.restype = c_int


def deltaEncoderToPosition(
    enc: Array[int, int],
    out: MutableArray[int, float],
    ID: int = -1
) -> int:
    """
    Compute and return the position of the end-effector
    (in [m]) about the X, Y, and Z axes for a given set of encoder values.

    :param Array[int, int] enc:
        Sequence of ``(enc0, enc1, enc2)`` where ``enc0``, ``enc1``, and
        ``enc2`` refer to raw encoder values on axis 0, 1, and 2,
        respectively.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param Array[int, int] out:
        An output buffer to store the end-effector position (in [m]).

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :raises ctypes.ArgumentError:
        If any element of ``enc`` is not implicitly convertible to a C int.

    :raises IndexError:
        If ``len(enc) < 3``.

    :raises TypeError:
        If ``enc`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.getDeltaEncoders()`
    | :func:`forcedimension_core.dhd.expert.deltaPositionToEncoder()`
    | :func:`forcedimension_core.dhd.expert.deltaEncodersToJointAngles()`
    """

    px = c_double()
    py = c_double()
    pz = c_double()

    err = _runtime._libdhd.dhdDeltaEncoderToPosition(
        enc[0],
        enc[1],
        enc[2],
        px,
        py,
        pz,
        ID
    )

    out[0] = px.value
    out[1] = py.value
    out[2] = pz.value

    return err


_runtime._libdhd.dhdDeltaPositionToEncoder.argtypes = [
    c_double,
    c_double,
    c_double,
    c_int_ptr,
    c_int_ptr,
    c_int_ptr,
    c_byte
]
_runtime._libdhd.dhdDeltaPositionToEncoder.restype = c_int


def deltaPositionToEncoder(
    pos: Array[int, float],
    out: MutableArray[int, int],
    ID: int = -1,
) -> int:
    """
    Computes and returns the encoder values of the end-effector
    for a given end-effector position.

    :param Array[int, float] pos:
        Sequence of ``(px, py, pz)`` where ``px``, ``py``, and ``pz``
        refer to the end-effector position on the X, Y, and Z axes,
        respectively (in [m]).

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param Array[int, int] out:
        An output buffer to store the raw encoder values.

    :raises TypeError:
        If ``out`` does not support item
        assignment either because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :raises ctypes.ArgumentError:
        If any element of ``pos`` is not implicitly convertible to a C double.

    :raises IndexError:
        If ``len(pos) < 3``.

    :raises TypeError:
        If ``pos`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.getDeltaEncoders()`
    | :func:`forcedimension_core.dhd.expert.deltaEncoderToPosition()`
    | :func:`forcedimension_core.dhd.expert.deltaEncodersToJointAngles()`
    """

    enc0 = c_int()
    enc1 = c_int()
    enc2 = c_int()

    err = _runtime._libdhd.dhdDeltaPositionToEncoder(
        pos[0],
        pos[1],
        pos[2],
        enc0,
        enc1,
        enc2,
        ID
    )

    out[0] = enc0.value
    out[1] = enc1.value
    out[2] = enc2.value

    return err


_runtime._libdhd.dhdDeltaMotorToForce.argtypes = [
    c_ushort,
    c_ushort,
    c_ushort,
    c_int,
    c_int,
    c_int,
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_byte
]
_runtime._libdhd.dhdDeltaMotorToForce.restype = c_int


def deltaMotorToForce(
    mot: Array[int, int],
    enc: Array[int, int],
    out: MutableArray[int, float],
    ID: int = -1
) -> int:
    """
    Compute and return the force applied to the end-effector for
    a given set of motor commands at a given position (defined by encoder
    readings)

    :param Array[int, int] mot:
        Sequence of ``(mot0, mot1, mot2)`` where ``mot0``, ``mot1``,
        and ``mot2`` are the axis 0, 1, and 2 DELTA motor commands,
        respectively.

    :param Array[int, int] enc:
        Sequence of ``(enc0, enc1, enc2)`` where ``enc0``, ``enc1``, and
        ``enc2`` refer to encoder values on axis 0, 1, and 2,
        respectively.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param MutableArray[int, float] out:
        An output buffer to store the applied force to the end effector.

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :raises ctypes.ArgumentError:
        If any element of ``output`` is not implicitly convertible to a C
        ushort.

    :raises IndexError:
        If ``len(output) < 3``.

    :raises TypeError:
        If ``output`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If any element of ``enc`` is not implicitly convertible to a C char.

    :raises IndexError:
        If ``len(enc) < 3``

    :raises TypeError:
        If ``enc`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.deltaForceToMotor()`
    """

    fx = c_double()
    fy = c_double()
    fz = c_double()

    err = _runtime._libdhd.dhdDeltaMotorToForce(
        mot[0],
        mot[1],
        mot[2],
        enc[0],
        enc[1],
        enc[2],
        fx,
        fy,
        fz,
        ID
    )

    out[0] = fx.value
    out[1] = fy.value
    out[2] = fz.value

    return err


_runtime._libdhd.dhdDeltaForceToMotor.argtypes = [
    c_double,
    c_double,
    c_double,
    c_int,
    c_int,
    c_int,
    c_ushort_ptr,
    c_ushort_ptr,
    c_ushort_ptr,
    c_byte
]
_runtime._libdhd.dhdDeltaForceToMotor.restype = c_int


def deltaForceToMotor(
    f: Array[int, float],
    enc: Array[int, int],
    out: MutableArray[int, int],
    ID: int = -1
) -> int:
    """
    Compute and return the motor commands necessary to obtain a
    given force on the end-effector at a given position (defined by encoder
    readings).

    :param Array[int, float] f:
        Sequence of ``(fx, fy, fz)`` where ``fx``, ``fy``, and ``fz`` are the
        force on the DELTA end-effector on the X, Y, and Z axes, respectively
        (in [N]).

    :param Array[int, int] enc:
        Sequence of ``(enc0, enc1, enc2)`` where ``enc0``, ``enc1``, and
        ``enc2`` refer to encoder values on axis 0, 1, and 2, respectively.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param Array[int, int] out:
        An output buffer to store the applied force to the end-effector.

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :raises ctypes.ArgumentError:
        If any element of ``f`` is not implicitly convertible to a C char.

    :raises IndexError:
        If ``len(f) < 3``.

    :raises TypeError:
        If ``f`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 or :data:`forcedimension_core.dhd.constants.MOTOR_SATURATED` on success,
        and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.deltaMotorToForce()`
    """

    output0 = c_ushort()
    output1 = c_ushort()
    output2 = c_ushort()

    err = _runtime._libdhd.dhdDeltaForceToMotor(
        f[0],
        f[1],
        f[2],
        enc[0],
        enc[1],
        enc[2],
        output0,
        output1,
        output2,
        ID
    )

    out[0] = output0.value
    out[1] = output1.value
    out[2] = output2.value

    return err


_runtime._libdhd.dhdWristEncoderToOrientation.argtypes = [
    c_int,
    c_int,
    c_int,
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_byte
]
_runtime._libdhd.dhdWristEncoderToOrientation.restype = c_int


def wristEncoderToOrientation(
    enc: Array[int, int],
    out: MutableArray[int, float],
    ID: int = -1,
) -> int:
    """
    For devices with a wrist structure, compute the individual angle of each
    joint, starting with the one located nearest to the wrist base plate.

    Note
    ----
    For the :data:`forcedimension_core.dhd.constants.DeviceType.OMEGA6_RIGHT`
    and the :data:`forcedimension_core.dhd.constants.DeviceType.OMEGA6_LEFT`
    devices, angles are computed with respect to their internal reference
    frame, which is rotated 45 degrees or π/4 radians about the Y axis. Please
    refer to your device user manual for more information on your device
    coordinate system.


    Note
    ----
    This feature only applies to devices with a wrist. See
    the :ref:`device_types` section for more details.


    :param Array[int, int] enc:
        Sequence of ``(enc0, enc1, enc2)`` where ``enc0``, ``enc1``, and
        ``enc2`` refer to wrist encoder values on the first, second, and
        third joint, respectively

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param MutableArray[int, float] out:
        An output buffer to store the joint angles.

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises ctypes.ArgumentError:
        If any element of ``enc`` is not implicitly convertible
        to a C char.

    :raises IndexError:
        If ``len(enc) < 3``.

    :raises TypeError:
        If ``enc`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.wristEncodersToJointAngles()`
    | :func:`forcedimension_core.dhd.expert.wristOrientationToEncoder()`
    | :func:`forcedimension_core.dhd.expert.wristJointAnglesToEncoders()`
    """
    px = c_double()
    py = c_double()
    pz = c_double()

    err = _runtime._libdhd.dhdWristEncoderToOrientation(
        enc[0],
        enc[1],
        enc[2],
        px,
        py,
        pz,
        ID
    )

    out[0] = px.value
    out[1] = py.value
    out[2] = pz.value

    return err


_runtime._libdhd.dhdWristOrientationToEncoder.argtypes = [
    c_double,
    c_double,
    c_double,
    c_int_ptr,
    c_int_ptr,
    c_int_ptr,
    c_byte
]
_runtime._libdhd.dhdWristOrientationToEncoder.restype = c_int


def wristOrientationToEncoder(
    orientation: Array[int, float],
    out: MutableArray[int, int],
    ID: int = -1,
) -> int:
    """
    For devices with a wrist structure, compute the encoder values from the
    individual angle of each joint, starting witht he one located nearest to
    the wrist plate base.

    Note
    ----
    For the
    :data:`forcedimension_core.dhd.constants.DeviceType.OMEGA6` and
    :data:`forcedimension_core.dhd.constants.DeviceType.OMEGA6_LEFT` devices,
    angles must be expressed with respect to their internal reference frame,
    which is rotated 45 degrees or π/4 radians about the Y axis. Please refer
    to  your device user manual for more information on your device coordinate
    system.


    Note
    ----
    This feature only applies to devices with a wrist. See
    the :ref:`device_types` section for more details.


    :param Array[int, float] orientation:
        Sequence of ``(oa, ob, og)`` where ``oa``, ``ob``, and ``og`` refer to
        wrist end effector orientation around the X, Y, and Z axes,
        respectively (in [rad]).

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param Array[int, int] out:
        An output buffer to store the encoder values.

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises ctypes.ArgumentError:
        If any element of ``orientation`` is not implicitly convertible to a C
        double.

    :raises IndexError:
        If ``len(orientation) < 3``.

    :raises TypeError:
        If ``orientation`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.wristEncodersToJointAngles()`
    | :func:`forcedimension_core.dhd.expert.wristEncodersToOrientation()`
    | :func:`forcedimension_core.dhd.expert.wristJointAnglesToEncoders()`


    """

    enc0 = c_int()
    enc1 = c_int()
    enc2 = c_int()

    err = _runtime._libdhd.dhdWristOrientationToEncoder(
        orientation[0],
        orientation[1],
        orientation[2],
        enc0,
        enc1,
        enc2,
        ID
    )

    out[0] = enc0.value
    out[1] = enc1.value
    out[2] = enc2.value

    return err


_runtime._libdhd.dhdWristMotorToTorque.argtypes = [
    c_ushort,
    c_ushort,
    c_ushort,
    c_int,
    c_int,
    c_int,
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_byte
]
_runtime._libdhd.dhdWristMotorToTorque.restype = c_int


def wristMotorToTorque(
    output: Array[int, int],
    enc: Array[int, int],
    out: MutableArray[int, float]
) -> int:
    """
    Compute and return the torque applied to the wrist
    end-effector for a given set of motor commands at a given orientation
    (defined by encoder values)

    Note
    ----
    This feature only applies to the following devices:

    :data:`forcedimension_core.dhd.constants.DeviceType.SIGMA7_RIGHT`
    :data:`forcedimension_core.dhd.constants.DeviceType.SIGMA7_LEFT`


    :param Array[int, int] cmd:
        Sequence of ``(cmd0, cmd1, cmd2)`` where ``cmd0``, ``cmd1``,
        and ``cmd2`` are the axis 0, 1, and 2 DELTA motor commands,
        respectively.

    :param Array[int, int] enc:
        Sequence of ``(enc0, enc1, enc2)`` where ``enc0``, ``enc1``, and
        ``enc2`` refer to encoder values on axis 0, 1, and 2, respectively.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param MutableArray[int, float] out:
        An output buffer to store the torques applied to the wrist.

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises ctypes.ArgumentError:
        If any element of ``cmd`` is not implicitly convertible to a C ushort.

    :raises IndexError:
        If ``len(cmd) < 3``.

    :raises TypeError:
        If ``cmd`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If any element of ``enc`` is not implicitly convertible to a C char.

    :raises IndexError:
        If ``len(enc) < 3``.

    :raises TypeError:
        If ``enc`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1, otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.wristTorqueToMotor()`
    | :func:`forcedimension_core.dhd.expert.wristJointTorquesExtrema()`
    """

    tx = c_double()
    ty = c_double()
    tz = c_double()

    err = _runtime._libdhd.dhdWristMotorToTorque(
        output[0],
        output[1],
        output[2],
        enc[0],
        enc[1],
        enc[2],
        tx,
        ty,
        tz,
        ID
    )

    out[0] = tx.value
    out[1] = ty.value
    out[2] = tz.value

    return err


_runtime._libdhd.dhdWristTorqueToMotor.argtypes = [
    c_double,
    c_double,
    c_double,
    c_int,
    c_int,
    c_int,
    c_ushort_ptr,
    c_ushort_ptr,
    c_ushort_ptr,
    c_byte
]
_runtime._libdhd.dhdWristTorqueToMotor.restype = c_int


def wristTorqueToMotor(
    t: Array[int, float],
    enc: Array[int, int],
    out: MutableArray[int, int],
    ID: int = -1
) -> int:
    """
    Compute and return the wrist motor commands necessary to
    obtain a given torque (in [Nm]) on the wrist end-effector at a given
    orientation (defined by encoder values).

    Note
    ----
    This feature only applies to the following devices:

    :data:`forcedimension_core.dhd.constants.DeviceType.SIGMA7_RIGHT`
    :data:`forcedimension_core.dhd.constants.DeviceType.SIGMA7_LEFT`


    :param Array[int, float] t:
        Sequence of ``(t0, t1, t2)`` where ``t0``, ``t1``, and ``t2`` are the
        DELTA axis torque commands for axes 0, 1, and 2, respectively
        (in [Nm]).

    :param Array[int, int] enc:
        Sequence of ``(enc0, enc1, enc2)`` where ``enc0``, ``enc1``, and
        ``enc2`` refer to encoder values on axis 0, 1, and 2, respectively.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param Array[int, int] out:
        An output buffer to store the wrist motor commands.

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises ctypes.ArgumentError:
        If any element of ``t`` is not implicitly convertible to a C double.

    :raises IndexError:
        If ``len(t) < 3``.

    :raises TypeError:
        If ``t`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If any element of ``enc`` is not implicitly convertible to a C int.

    :raises IndexError:
        If ``len(enc) < 3``.

    :raises TypeError:
        If ``enc`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.wristTorqueToMotor()`
    """

    output0 = c_ushort()
    output1 = c_ushort()
    output2 = c_ushort()

    err = _runtime._libdhd.dhdWristTorqueToMotor(
        t[0],
        t[1],
        t[2],
        enc[0],
        enc[1],
        enc[2],
        output0,
        output1,
        output2,
        ID
    )

    out[0] = output0.value
    out[1] = output1.value
    out[2] = output2.value

    return err


_runtime._libdhd.dhdGripperEncoderToAngleRad.argtypes = [
    c_int,
    c_double_ptr,
    c_byte
]
_runtime._libdhd.dhdGripperEncoderToAngleRad.restype = c_int


def gripperEncoderToAngleRad(enc: int, out: c_double, ID: int = -1) -> int:
    """
    Compute the gripper angle (in [rad]) for a given encoder value.

    Note
    ----
    This feature only applies to devices with a gripper. See
    the :ref:`device_types` section for more details.


    :param int enc:
        Gripper encoder reading.

    :param c_int out:
        Output buffer to store the gripper angle (in [rad]).

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``enc`` is not implicitly convertible to a C char.

    :raises IndexError:
        If ``len(enc) < 3``

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.gripperAngleRadToEncoder()`
    | :func:`forcedimension_core.dhd.expert.gripperEncoderToGap()`
    """

    return _runtime._libdhd.dhdGripperEncoderToAngleRad(enc, out, ID)


_runtime._libdhd.dhdGripperEncoderToGap.argtypes = [
    c_int,
    c_double_ptr,
    c_byte
]
_runtime._libdhd.dhdGripperEncoderToGap.restype = c_int


def gripperEncoderToGap(enc: int, out: c_double, ID: int = -1) -> int:
    """
    Compute and return the gripper opening (in [m]) for a
    given encoder reading.

    Note
    ----
    This feature only applies to devices with a gripper. See
    the :ref:`device_types` section for more details.


    :param int enc:
        Gripper encoder reading.

    :param c_double out:
        Buffer to store the griper opening (in [m]).

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``enc`` is not implicitly convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        A tuple in the form ``(gap, err)``. ``gap`` is the gripper opening in
        [m] ``err`` is 0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.gripperGapToEncoder()`
    | :func:`forcedimension_core.dhd.expert.gripperEncoderToAngleRad()`
    """

    return _runtime._libdhd.dhdGripperEncoderToGap(enc, out, ID)


_runtime._libdhd.dhdGripperAngleRadToEncoder.argtypes = [
    c_double,
    c_int_ptr,
    c_byte
]
_runtime._libdhd.dhdGripperAngleRadToEncoder.restype = c_int


def gripperAngleRadToEncoder(angle: float, out: c_int, ID: int = -1) -> int:
    """
    Computes and return the gripper encoder value for a given
    gripper opening distance (in [rad]).

    Note
    ----
    This feature only applies to devices with a gripper. See
    the :ref:`device_types` section for more details.


    :param float angle:
        Gripper opening as an angle (in [rad]).

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``angle`` is not implicitly convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        A tuple in the form ``(enc, err)``. ``enc`` is the gripper raw encoder
        reading. ``err`` is 0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.gripperEncoderToAngleRad()`
    | :func:`forcedimension_core.dhd.expert.gripperEncoderToGap()`
    """

    return _runtime._libdhd.dhdGripperAngleRadToEncoder(angle, out, ID)


_runtime._libdhd.dhdGripperGapToEncoder.argtypes = [
    c_double,
    c_int_ptr,
    c_byte
]
_runtime._libdhd.dhdGripperGapToEncoder.restype = c_int


def gripperGapToEncoder(gap: float, out: c_int, ID: int = -1) -> int:
    """
    Compute and return the gripper encoder value for a given
    gripper opening distance (in [m]).

    Note
    ----
    This feature only applies to devices with a gripper. See
    the :ref:`device_types` section for more details.

    :param float gap:
        Gripper opening distance (in [m]).

    :param c_int out:
        Outpu buffer to store the gripper encoder value.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``gap`` is not implicitly convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        A tuple in the form ``(enc, err)``. ``enc`` is the gripper encoder
        reading. ``err`` is 0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.gripperEncoderToAngleRad()`
    | :func:`forcedimension_core.dhd.expert.gripperAngleRadToEncoder()`
    | :func:`forcedimension_core.dhd.expert.gripperEncoderToGap()`
    """

    return  _runtime._libdhd.dhdGripperGapToEncoder(gap, out, ID)


_runtime._libdhd.dhdGripperMotorToForce.argtypes = [
    c_ushort,
    c_double_ptr,
    c_int_ptr,
    c_byte
]
_runtime._libdhd.dhdGripperMotorToForce.restype = c_int


def gripperMotorToForce(
    cmd: int,
    enc_wrist: Array[int, int],
    enc_gripper: int,
    out: c_double,
    ID: int = -1
) -> int:
    """
    Compute the force applied to the end-effector for a given
    motor command.

    Note
    ----
    This feature only applies to devices with an active gripper. See
    the :ref:`device_types` section for more details.


    :param int output:
        Motor command on gripper axis.

    :param Array[int, int] enc_wrist:
        Sequence of ``(enc0, enc1, enc2)`` where ``enc0``, ``enc1``, ``enc2``
        are encoder values about wrist joints 0, 1, and 2, respectively.

    :param int enc_gripper:
        Encoder reading for the gripper.

    :param c_double out:
        Output buffer to store the force applied to the end effector (in [N]).

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``cmd`` is not implicitly convertible to a C ushort.

    :raises ctypes.ArgumentError:
        If any element of ``enc_wrist`` is not implicitly convertible to a C
        int.

    :raises IndexError:
        If ``len(enc_wrist) < 3``.

    :raises TypeError:
        If ``enc_wrist`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``enc_gripper`` is not implicitly convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        A tuple in the form ``(force, err)``. ``force`` is the force on the
        gripper end-effector (in [N]). ``err`` is 0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.gripperForceToMotor()`
    """

    enc = (c_int * 4)(enc_wrist[0], enc_wrist[1], enc_wrist[2], enc_gripper)
    return _runtime._libdhd.dhdGripperMotorToForce(cmd, out, enc, ID)


_runtime._libdhd.dhdGripperForceToMotor.argtypes = [
    c_double,
    c_ushort_ptr,
    c_int_ptr,
    c_byte
]
_runtime._libdhd.dhdGripperForceToMotor.restype = c_int


def gripperForceToMotor(
    f: float,
    enc_wrist: Array[int, int],
    enc_gripper: int,
    out: c_ushort,
    ID: int = -1
) -> int:
    """
    Given a desired force (in [N]) to be displayed by the force gripper,
    compute and return the refering motor command.

    Note
    ----
    This feature only applies to devices with an active gripper. See
    the :ref:`device_types` section for more details.


    :param int f:
        Force on the gripper end-effector (in [N]).

    :param Array[int, int] enc_wrist:
        An output buffer to store the wrist encoding readings.

    :param c_ushort out:
        Output buffer to store the motor command.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``f`` is not implicitly convertible to a C double.

    :raises ctypes.ArgumentError:
        If any member of ``enc_wrist`` is not implicitly convertible to a C
        ushort.

    :raises IndexError:
        If ``len(enc_wrist) < 3``.

    :raises TypeError:
        If ``enc_wrist`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``enc_gripper`` is not implicitly convertible to a C ushort.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        A tuple in the form ``(cmd, err)``.  ``cmd`` is the motor command on
        the gripper axis. ``err`` is 0 or
        :data:`forcedimension_core.dhd.constants.MOTOR_SATURATED` on success,
        -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.gripperForceToMotor()`
    """

    enc = (c_int * 4)(enc_wrist[0], enc_wrist[1], enc_wrist[2], enc_gripper)

    return _runtime._libdhd.dhdGripperForceToMotor(f, out, enc, ID)



_runtime._libdhd.dhdSetMot.argtypes = [c_ushort_ptr, c_ubyte, c_byte]
_runtime._libdhd.dhdSetMot.restype = c_int


def setMot(cmds: Array[int, int], mask: int = 0xff, ID: int = -1) -> int:
    """
    Program motor commands to a selection of motor channels. Particularly
    useful when using the generic controller directly, without a device model
    attached.

    :param Array[int, int] cmds:
        List of motor command values.

    :param int mask:
        Bitwise mask of which motor should be set.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If any element of ``cmds`` is not implicitly convertible to a C
        ushort.

    :raises IndexError:
        If ``len(cmds) < MAX_DOF``.

    :raises TypeError:
        If ``cmds`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``mask`` is not implicitly convertible to a C uchar.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns: 0 on success, -1 otherwise

    See Also
    --------
    | :data:`forcedimension_core.dhd.expert.setMotor()`
    | :data:`forcedimension_core.dhd.expert.setDeltaMotor()`
    | :data:`forcedimension_core.dhd.expert.setWristMotor()`
    | :data:`forcedimension_core.dhd.expert.setGripperMotor()`

    """
    cmd_arr = (c_ushort * MAX_DOF)(
            cmds[0],
            cmds[1],
            cmds[2],
            cmds[3],
            cmds[4],
            cmds[5],
            cmds[6],
            cmds[7]
        )

    return _runtime._libdhd.dhdSetMot(
        ct.cast(cmd_arr, c_ushort_ptr),
        mask,
        ID
    )


_runtime._libdhd.dhdSetJointTorques.argtypes = [
    c_double_ptr, c_ubyte, c_byte
]
_runtime._libdhd.dhdSetJointTorques.restype = c_int


def setJointTorques(q: Array[int, float], mask: int = 0xff, ID: int = -1):
    """
    Sets all joint torques on all active axes.

    :param Array[int, float] q:
        Joint torques for each degree-of-freedom (in [Nm]).

    :param int mask:
        Bitwise mask of which joints should be set

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If any element of ``cmds`` is not implicitly convertible to a C
        double.

    :raises IndexError:
        If ``len(cmds) < MAX_DOF``.

    :raises TypeError:
        If ``cmds`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``mask`` is not implicitly convertible to a C uchar.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.setDeltaJointTorques()`
    | :func:`forcedimension_core.dhd.expert.setWristJointTorques()`
    | :func:`forcedimension_core.dhd.expert.setForceAndWristJointTorques()`
    | :func:`forcedimension_core.dhd.expert.setForceAndWristJointTorquesAndGripperForce()`
    """

    cmd_arr = (c_double * MAX_DOF)(
            q[0],
            q[1],
            q[2],
            q[3],
            q[4],
            q[5],
            q[6],
            q[7]
        )

    return _runtime._libdhd.dhdSetJointTorques(
        ct.cast(cmd_arr, c_double_ptr),
        mask,
        ID
    )


_runtime._libdhd.dhdPreloadMot.argtypes = [c_ushort_ptr, c_ubyte, c_byte]
_runtime._libdhd.dhdPreloadMot.restype = c_int


def preloadMot(cmds: Array[int, int], mask: int = 0xff, ID: int = -1) -> int:
    """
    Program motor commands to a selection of motor channels. Unlike
    forcedimension_core.dhd.expert.setMot, this function saves the requested
    commands internally for later application by calling
    :func:`forcedimension_core.dhd.setForce()` and the friends.

    :param Array[int, int] outputs:
        List of motor command values.

    :param int mask:
        Bitwise mask of which motor should be set.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If any element of ``cmds`` is not implicitly convertible to a C ushort.

    :raises IndexError:
        If ``len(cmds) < MAX_DOF``.

    :raises TypeError:
        If ``cmds`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``mask`` is not implicitly convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns: 0 on success, -1 otherwise

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.setMot()`
    """

    cmd_arr = (c_ushort * MAX_DOF)(
            cmds[0],
            cmds[1],
            cmds[2],
            cmds[3],
            cmds[4],
            cmds[5],
            cmds[6],
            cmds[7]
        )

    return _runtime._libdhd.dhdPreloadMot(
        ct.cast(cmd_arr, c_ushort_ptr),
        mask,
        ID
    )


_runtime._libdhd.dhdGetEnc.argtypes = [c_int_ptr, c_ubyte, c_byte]
_runtime._libdhd.dhdGetEnc.restype = c_int


def getEnc(out: MutableArray[int, int], mask: int=0xff, ID: int = -1) -> int:
    """
    Get a selective list of encoder values. Particularly useful when using the
    generic controller directly, without a device model attached.

    :param int mask:
        Bitwise mask of which motor should be set.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param Array[int, int] out:
        An output buffer to store the encoder values.

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < MAX_DOF``

    :raises ctypes.ArgumentError:
        If ``mask`` is not implicitly convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD` on success, -1
        otherwise.

    See Also
    --------
    | :data:`forcedimension_core.dhd.expert.getEncoder()`
    | :data:`forcedimension_core.dhd.expert.getEncVelocities()`
    """
    enc = (c_int * MAX_DOF)()

    err = _runtime._libdhd.dhdGetEnc(ct.cast(enc, c_int_ptr), mask, ID)

    for i in range(MAX_DOF):
        out[i] = enc[i]

    return err


_runtime._libdhd.dhdSetBrk.argtypes = [c_ubyte, c_byte]
_runtime._libdhd.dhdSetBrk.restype = c_int


def setBrk(mask: int = 0xff, ID: int = -1) -> int:
    """
    Set electromagnetic braking status on selective motor groups. Only applies
    when using the generic controller directly, without a device model
    attached.

    Generic control motor groups
        group1 - [mot0, mot1, mot2]

        group2 - [mot3, mot4, mot5]

        group3 - [mot6]

        group4 - [mot7]

    The mask parameter addresses all 8 motors bitwise. If a single bit within
    a motor group's is enabled, all motors in that motor's group's
    electromagnetic brakes will be activated.

    :param mask:
        Bitwise mask of which motor groups should have their electromagnetic
        brakes be set on.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``mask`` is not implicitly convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns: 0 on success, -1 otherwise
    """

    return _runtime._libdhd.dhdSetBrk(mask, ID)


_runtime._libdhd.dhdGetDeltaJointAngles.argtypes = [
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_byte
]
_runtime._libdhd.dhdGetDeltaJointAngles.restype = c_int


def getDeltaJointAngles(out: MutableArray[int, float], ID: int = -1) -> int:
    """
    Retrieve the joint angles (in [rad]) for the DELTA structure.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param MutableArray[int, float] out:
        An output buffer to store the joint angles.

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.deltaEncodersToJointAngles()`
    | :func:`forcedimension_core.dhd.expert.deltaJointAnglesToEncoders()`
    | :func:`forcedimension_core.dhd.expert.deltaJointAnglesToJacobian()`
    """

    j0 = c_double()
    j1 = c_double()
    j2 = c_double()

    err = _runtime._libdhd.dhdGetDeltaJointAngles(
        j0,
        j1,
        j2,
        ID
    )

    out[0] = j0.value
    out[1] = j1.value
    out[2] = j2.value

    return err


_runtime._libdhd.dhdGetDeltaJacobian.argtypes = [c_double_ptr, c_byte]
_runtime._libdhd.dhdGetDeltaJacobian.restype = c_int


def getDeltaJacobian(
    out: Array[int, MutableArray[int, float]],
    ID: int = -1
) -> int:
    """
    Retrieve the 3x3 jacobian matrix for the DELTA structure based on the
    current end-effector position. Please refer to your device user manual for
    more information on your device coordinate system.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param MutableFloatMatrixLike out:
        An output buffer to store the Jacobian.

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If any dimension of ``out`` is less than 3.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.deltaJointAnglesToJacobian()`
    """

    J = ((c_double * 3) * 3)()
    err = _runtime._libdhd.dhdGetDeltaJacobian(ct.cast(J, c_double_ptr), ID)

    for i in range(3):
        for j in range(3):
            out[i][j] = J[i][j]

    return err


_runtime._libdhd.dhdDeltaJointAnglesToJacobian.argtypes = [
    c_double,
    c_double,
    c_double,
    c_double_ptr,
    c_byte
]
_runtime._libdhd.dhdDeltaJointAnglesToJacobian.restype = c_int


def deltaJointAnglesToJacobian(
    joint_angles: Array[int, float],
    out: MutableArray[int, MutableArray[int, float]],
    ID: int = -1,
) -> int:
    """
    Retrieve the 3x3 jacobian matrix for the DELTA structure
    based on a given joint configuration. Please refer to your device user
    manual for more information on your device coordinate system.

    :param Array[int, float] joint_angles:
        Sequence of (j0, j1, j2) where ``j0``, ``j1``, and ``j2`` refer to the
        joint angles for axis 0, 1, and 2, respectively.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param MutableFloatMatrixLike out:
        An output buffer to store the return.

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises ctypes.ArgumentError:
        If any element of ``joint_angles`` is not implicitly convertible to C
        double.

    :raises IndexError:
        If ``len(joint_angles) < 3``.

    :raises TypeError:
        If ``joint_angles`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.getJointAngles()`
    | :func:`forcedimension_core.dhd.expert.getDeltaJointAngles()`
    | :func:`forcedimension_core.dhd.expert.getDeltaJacobian()`
    """

    J = ((c_double * 3) * 3)()

    err = _runtime._libdhd.dhdDeltaJointAnglesToJacobian(
        joint_angles[0],
        joint_angles[1],
        joint_angles[2],
        ct.cast(J, c_double_ptr),
        ID
    )

    for i in range(3):
        for j in range(3):
            out[i][j] = J[i][j]

    return err


_runtime._libdhd.dhdDeltaJointTorquesExtrema.argtypes = [
    c_double,
    c_double,
    c_double,
    c_double_ptr,
    c_double_ptr,
    c_byte
]
_runtime._libdhd.dhdDeltaJointTorquesExtrema.restype = c_int


def deltaJointTorquesExtrema(
    joint_angles: Array[int, float],
    minq_out: MutableArray[int, float],
    maxq_out: MutableArray[int, float],
    ID: int = -1
) -> int:
    """
    Compute the range of applicable DELTA joint torques for a given DELTA joint
    angle configuration. Please refer to your device user manual for more
    information on your device coordinate system.

    :param Array[int, float] joint_angles:
        Sequence of ``(j0, j1, j2)`` where ``j0``, ``j1``, ``j2`` refer to the
        joint angles for axis 0, 1, and 2, respectively.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param MutableArray[int, float] minq_out:
        An output buffer to store the return.

    :param MutableArray[int, float] maxq_out:
        An output buffer to store the return.

    :raises TypeError:
        If ``minq_out`` does not support item assignment
        either because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(encMin_out) < MAX_DOF``

    :raises TypeError:
        If ``maxq_out`` does not support item assignment
        either because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < MAX_DOF``

    :raises ctypes.ArgumentError:
        If any element of ``joint_angles`` is not implicitly convertible to
        a C double.

    :raises IndexError:
        If ``len(joint_angles) < 3``.

    :raises TypeError:
        If ``joint_angles`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.wristJointTorquesExtrema()`
    | :func:`forcedimension_core.dhd.expert.getDeltaJointAngles()`
    | :func:`forcedimension_core.dhd.expert.getJointAngles()`
    """

    minq = (c_double * 3)()
    maxq = (c_double * 3)()

    err = _runtime._libdhd.dhdDeltaJointTorquesExtrema(
        joint_angles[0],
        joint_angles[1],
        joint_angles[2],
        ct.cast(minq, c_double_ptr),
        ct.cast(maxq, c_double_ptr),
        ID
    )

    minq_out[0] = minq[0]
    minq_out[1] = minq[1]
    minq_out[2] = minq[2]

    maxq_out[0] = maxq[0]
    maxq_out[1] = maxq[1]
    maxq_out[2] = maxq[2]

    return err


_runtime._libdhd.dhdSetDeltaJointTorques.argtypes = [
    c_double,
    c_double,
    c_double,
    c_byte
]
_runtime._libdhd.dhdSetDeltaJointTorques.restype = c_int


def setDeltaJointTorques(
    t: Array[int, float],
    ID: int = -1
) -> int:
    """
    Set all joint torques of the DELTA structure.

    :param Array[int, float] t:
        Sequence of ``(t0, t1, t2)`` where ``t0``, ``t1``, and ``t2`` are the
        DELTA axis torque commands for axes 0, 1, and 2, respectively
        (in [Nm]).

    :raises ctypes.ArgumentError:
        If any element of ``t`` is not implicitly convertible to a C char

    :raises IndexError:
        If ``len(t) < 3``.

    :raises TypeError:
        If ``t`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns: 0 on success, -1 otherwise

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.deltaJointTorquesExtrema()`
    | :func:`forcedimension_core.dhd.expert.setWristJointTorques()`
    | :func:`forcedimension_core.dhd.expert.setForceAndWristJointTorques()`
    | :func:`forcedimension_core.dhd.expert.setForceAndWristJointTorquesAndGripperForce()`
    """
    return _runtime._libdhd.dhdSetDeltaJointTorques(t[0], t[1], t[2], ID)


_runtime._libdhd.dhdDeltaEncodersToJointAngles.argtypes = [
    c_int,
    c_int,
    c_int,
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_byte
]
_runtime._libdhd.dhdDeltaEncodersToJointAngles.restype = c_int


def deltaEncodersToJointAngles(
    enc: Array[int, int],
    out: MutableArray[int, float],
    ID: int = -1
) -> int:
    """
    Compute and return the DELTA joint angles for a given set of
    encoder values.

    :param Array[int, int] enc:
        Sequence of ``(enc0, enc1, enc2)`` where ``enc0``, ``enc1``, and
        ``enc2`` refer to encoder values on axis 0, 1, and 2, respectively.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param MutableArray[int, float] out:
        An output buffer to store the return.

    :raises TypeError:
        If ``out`` does not support item
        assignment either because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises ctypes.ArgumentError:
        If any element of ``enc`` is not implicitly convertible to a C int.

    :raises IndexError:
        If ``len(enc) < 3``.

    :raises TypeError:
        If ``enc`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.deltaJointAnglesToJacobian()`
    | :func:`forcedimension_core.dhd.expert.deltaJointAnglesToEncoders()`
    """

    j0 = c_double()
    j1 = c_double()
    j2 = c_double()

    err = _runtime._libdhd.dhdDeltaEncodersToJointAngles(
        enc[0],
        enc[1],
        enc[2],
        j0,
        j1,
        j2,
        ID
    )

    out[0] = j0.value
    out[1] = j1.value
    out[2] = j2.value

    return err


_runtime._libdhd.dhdDeltaJointAnglesToEncoders.argtypes = [
    c_double,
    c_double,
    c_double,
    c_int_ptr,
    c_int_ptr,
    c_int_ptr,
    c_byte
]
_runtime._libdhd.dhdDeltaJointAnglesToEncoders.restype = c_int


def deltaJointAnglesToEncoders(
    joint_angles: Array[int, float],
    out: MutableArray[int, int],
    ID: int = -1,
) -> int:
    """
    Compute and return the DELTA encoder values for a given
    set of joint angles.

    :param Array[int, float] enc:
        Sequence of ``(j0, j1, j1)`` where ``j0``, ``j1``, and ``j2`` refer to
        DELTA joint angles for axes 0, 1, and 2, respectively, (in [rad]).

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param MutableArray[int, float] out:
        An output buffer to store the return.

    :raises TypeError:
        If ``out`` does not support item
        assignment either because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises ctypes.ArgumentError:
        If any element of ``joint_angles`` is not implicitly convertible to
        a C double.

    :raises IndexError:
        If ``len(joint_angles) < 3``.

    :raises TypeError:
        If ``joint_angles`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.deltaJointAnglesToJacobian()`
    | :func:`forcedimension_core.dhd.expert.deltaEncodersToJointAngles()`
    """

    enc0 = c_int()
    enc1 = c_int()
    enc2 = c_int()

    err = _runtime._libdhd.dhdDeltaJointAnglesToEncoders(
        joint_angles[0],
        joint_angles[1],
        joint_angles[2],
        enc0,
        enc1,
        enc2,
        ID
    )

    out[0] = enc0.value
    out[1] = enc1.value
    out[2] = enc2.value

    return err


_runtime._libdhd.dhdGetWristJointAngles.argtypes = [
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_byte
]
_runtime._libdhd.dhdGetWristJointAngles.restype = c_int


def getWristJointAngles(out: MutableArray[int, float], ID: int = -1) -> int:
    """
    Retrieve the joint angles (in [rad]) for the wrist structure.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param MutableArray[int, float] out:
        An output buffer to store the wrist joint angles.

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.dhdWristJointAnglesToJacobian()`
    | :func:`forcedimension_core.dhd.expert.dhdWristJointTorquesExtrema()`
    | :func:`forcedimension_core.dhd.expert.wristJointAnglesToEncoders()`
    | :func:`forcedimension_core.dhd.expert.wristEncodersToJointAngles()`
    """

    j0 = c_double()
    j1 = c_double()
    j2 = c_double()
    err = _runtime._libdhd.dhdGetWristJointAngles(
        j0,
        j1,
        j2,
        ID
    )

    out[0] = j0.value
    out[1] = j1.value
    out[2] = j2.value

    return err


_runtime._libdhd.dhdGetWristJacobian.argtypes = [c_double_ptr, c_byte]
_runtime._libdhd.dhdGetWristJacobian.restype = c_int


def getWristJacobian(
    out: MutableArray[int, MutableArray[int, float]],
    ID: int = -1
) -> int:
    """
    Retrieve the 3x3 jacobian matrix for the wrist structure based on the
    current end-effector position. Please refer to your device user manual for
    more information on your device coordinate system.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param MutableArray[int, float] out:
        An output buffer to store the Jacobian.

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If any dimension of out is less than 3.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD` on success,
        and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.wristJointAnglesToJacobian()`
    """

    J = ((c_double * 3) * 3)()

    err = _runtime._libdhd.dhdGetWristJacobian(ct.cast(J, c_double_ptr), ID)

    for i in range(3):
        for j in range(3):
            out[i][j] = J[i][j]

    return err


_runtime._libdhd.dhdWristJointAnglesToJacobian.argtypes = [
    c_double,
    c_double,
    c_double,
    c_double_ptr,
    c_byte
]
_runtime._libdhd.dhdWristJointAnglesToJacobian.restype = c_int


def wristJointAnglesToJacobian(
    joint_angles: Array[int, float],
    out: MutableArray[int, MutableArray[int, float]],
    ID: int = -1,
) -> int:
    """
    Retrieve the 3x3 jacobian matrix for the wrist structure
    based on a given joint configuration. Please refer to your device user
    manual for more information on your device coordinate system.

    :param Array[int, float] joint_angles:
        Sequence of ``(j0, j1, j2)`` where ``j0``, ``j1``, and ``j2`` refer to
        the joint angles for wrist axis 0, 1, and 2, respectively.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param MutableFloatMatrixLike out:
        An output buffer to store the Jacobian.

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises ctypes.ArgumentError:
        If any element of ``joint_angles`` is not implicitly convertible to
        a C double.

    :raises IndexError:
        If ``len(joint_angles) < 3``.

    :raises TypeError:
        If ``joint_angles`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.wristEncodersToJointAngles()`
    | :func:`forcedimension_core.dhd.getWristJointAngles()`
    """

    J = ((c_double * 3) * 3)()

    err = _runtime._libdhd.dhdWristJointAnglesToJacobian(
        joint_angles[0],
        joint_angles[1],
        joint_angles[2],
        ct.cast(J, c_double_ptr),
        ID
    )

    for i in range(3):
        for j in range(3):
            out[i][j] = J[i][j]

    return err


_runtime._libdhd.dhdWristJointTorquesExtrema.argtypes = [
    c_double,
    c_double,
    c_double,
    c_double_ptr,
    c_double_ptr,
    c_byte
]
_runtime._libdhd.dhdWristJointTorquesExtrema.restype = c_int


def wristJointTorquesExtrema(
    joint_angles: Array[int, float],
    minq_out: MutableArray[int, float],
    maxq_out: MutableArray[int, float],
    ID: int = -1
) -> int:
    """
    Compute the range of applicable wrist joint torques for a given wrist joint
    angle configuration. Please refer to your device user manual for more
    information on your device coordinate system.

    :param Array[int, float] joint_angles:
        Sequence of ``(j0, j1, j2)`` where ``j0``, ``j1``, ``j2`` refer to the
        joint angles for wrist axes 0, 1, and 2, respectively.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param MutableArray[int, float] minq_out:
        An output buffer to store the return.

    :param MutableArray[int, float] maxq_out:
        An output buffer to store the return.

    :raises TypeError:
        If ``minq_out`` does not support item assignment
        either because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(minq_out) < MAX_DOF``

    :raises TypeError:
        If ``maxq_out`` does not support item assignment
        either because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(maxq_out) < MAX_DOF``

    :raises ctypes.ArgumentError:
        If any element of ``joint_angles`` is not implicitly convertible to C
        double.

    :raises IndexError:
        If ``len(joint_angles) < 3``.

    :raises TypeError:
        If ``joint_angles`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.getJointAngles()`
    | :func:`forcedimension_core.dhd.expert.getWristJointAngles()`
    | :func:`forcedimension_core.dhd.expert.wristEncodersToJointAngles()`
    | :func:`forcedimension_core.dhd.expert.wristJointAnglesToJacobian()`
    | :func:`forcedimension_core.dhd.expert.wristJointAnglesToEncoders()`
    """

    minq = (c_double * 3)()
    maxq = (c_double * 3)()

    err = _runtime._libdhd.dhdWristJointTorquesExtrema(
        joint_angles[0],
        joint_angles[1],
        joint_angles[2],
        ct.cast(minq, c_double_ptr),
        ct.cast(maxq, c_double_ptr),
        ID
    )

    minq_out[0] = minq[0]
    minq_out[1] = minq[1]
    minq_out[2] = minq[2]

    maxq_out[0] = maxq[0]
    maxq_out[1] = maxq[1]
    maxq_out[2] = maxq[2]

    return err


_runtime._libdhd.dhdSetWristJointTorques.argtypes = [
    c_double,
    c_double,
    c_double,
    c_byte
]
_runtime._libdhd.dhdSetWristJointTorques.restype = c_int


def setWristJointTorques(
    t: Array[int, float],
    ID: int = -1
) -> int:
    """
    Set all joint torques of the wrist structure.

    :param Array[int, float] t:
        Sequence of (t0, t1, t2) where t0, t1, t2 are the wrist axis torque
        commands for axes 0, 1, and 2, respectively (in [Nm]).

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If any element of ``t`` is not implicitly convertible to a C double.

    :raises IndexError:
        If ``len(t) < 3``.

    :raises TypeError:
        If ``t`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns: 0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.setForceAndWristJointTorques()`
    | :func:`forcedimension_core.dhd.expert.setForceAndWristJointTorquesAndGripperForce()`
    """
    return _runtime._libdhd.dhdSetWristJointTorques(t[0], t[1], t[2], ID)


_runtime._libdhd.dhdSetForceAndWristJointTorques.argtypes = [
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    c_byte
]
_runtime._libdhd.dhdSetForceAndWristJointTorques.restype = c_int


def setForceAndWristJointTorques(
    f: Array[int, float],
    t: Array[int, float],
    ID: int = -1
) -> int:
    """
    Set force (in [N]) and wrist joint torques (in [Nm]) about the
    X, Y, and Z axes.

    :param Array[int, float] f:
        Sequence of ``(fx, fy, fz)`` where ``fx``, ``fy``, and ``fz`` are the
        translation forces (in [N]) to be applied to the DELTA end-effector on
        the X, Y, and Z axes respectively.

    :param Array[int, float] t:
        Sequence of (t0, t1, t2) where ``t0``, ``t1``, ``t2`` are the wrist
        joint torques (in [Nm]) to be applied to the wrist end-effector
        for axes 0, 1, and 2, respectively.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If any element of ``f`` is not implicitly convertible to a C double.

    :raises IndexError:
        If ``len(f) < 3``.

    :raises TypeError:
        If ``f`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If any element of ``t`` is not implicitly convertible to a C double.

    :raises IndexError:
        If ``len(t) < 3``.

    :raises TypeError:
        If ``t`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns: 0 on success, -1 otherwise

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.setWristJointTorques()`
    | :func:`forcedimension_core.dhd.expert.setForceAndWristJointTorquesAndGripperForce()`
    """
    return _runtime._libdhd.dhdSetForceAndWristJointTorques(
        f[0], f[1], f[2], t[0], t[1], t[2], ID
    )


_runtime._libdhd.dhdSetForceAndWristJointTorquesAndGripperForce.argtypes = [
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    c_byte
]
_runtime._libdhd.dhdSetForceAndWristJointTorquesAndGripperForce.restype = c_int


def setForceAndWristJointTorquesAndGripperForce(
        f: Array[int, float],
        t: Array[int, float],
        fg: float,
        ID: int = -1) -> int:
    """
    Set force (in [N]) and wrist joint torques (in [Nm]) about the X, Y, and Z
    axes as well as the and gripper force

    :param Array[int, float] f:
        Sequence of ``(fx, fy, fz)`` where ``fx``, ``fy``, and ``fz`` are the
        translation forces (in [N]) to be applied to the DELTA end-effector on
        the X, Y, and Z axes respectively.

    :param Array[int, float] t:
        Sequence of (t0, t1, t2) where ``t0``, ``t1``, ``t2`` are the wrist
        joint torques (in [Nm]) to be applied to the wrist end-effector
        for axes 0, 1, and 2, respectively.

    :param float fg:
        Gripper force (in [N]).

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If any element of ``f`` is not implicitly convertible to a C double.

    :raises IndexError:
        If ``len(f) < 3``.

    :raises TypeError:
        If ``f`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If any element of ``t`` is not implicitly convertible to a C double.

    :raises IndexError:
        If ``len(t) < 3``.

    :raises TypeError:
        If ``t`` is not subscriptable.

   :raises ctypes.ArgumentError:
        If ``gripper_force`` is not implicitly convertible to a C double.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns: 0 on success, -1 otherwise

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.setWristJointTorques()`
    | :func:`forcedimension_core.dhd.expert.setForceAndWristJointTorques()`
    """
    return _runtime._libdhd.dhdSetForceAndWristJointTorquesAndGripperForce(
        f[0], f[1], f[2], t[0], t[1], t[2], fg, ID
    )


_runtime._libdhd.dhdWristEncodersToJointAngles.argtypes = [
    c_int,
    c_int,
    c_int,
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_byte
]
_runtime._libdhd.dhdWristEncodersToJointAngles.restype = c_int


def wristEncodersToJointAngles(
    enc: Array[int, int],
    out: MutableArray[int, float],
    ID: int = -1
) -> int:
    """
    Compute and return the wrist joint angles (in [rad])
    for a given set of encoder values.

    :param Array[int, int] enc:
        Sequence of (enc0, enc1, enc2) where ``enc0``, ``enc1``, and ``enc2``
        refer to encoder values on wrist axes 0, 1, and 2, respectively.

    :param MutableArray[int, float] out:
        An output buffer to store the joint angles (in [rad]).

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If any element of ``enc`` is not implicitly convertible to a C int.

    :raises IndexError:
        If ``len(enc) < 3``.

    :raises TypeError:
        If ``enc`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.wristJointAnglesToJacobian()`
    | :func:`forcedimension_core.dhd.expert.wristJointTorquesExtrema()`
    | :func:`forcedimension_core.dhd.expert.wristJointAnglesToEncoders()`
    """

    j0 = c_double()
    j1 = c_double()
    j2 = c_double()

    err = _runtime._libdhd.dhdWristEncodersToJointAngles(
        enc[0], enc[1], enc[2], j0, j1, j2, ID
    )

    out[0] = j0.value
    out[1] = j1.value
    out[2] = j2.value

    return err


_runtime._libdhd.dhdWristJointAnglesToEncoders.argtypes = [
    c_double,
    c_double,
    c_double,
    c_int_ptr,
    c_int_ptr,
    c_int_ptr,
    c_byte
]
_runtime._libdhd.dhdWristJointAnglesToEncoders.restype = c_int


def wristJointAnglesToEncoders(
    joint_angles: Array[int, float],
    out: MutableArray[int, int],
    ID: int = -1
) -> int:
    """
    Compute and return the wrist encoder values for a given
    set of wrist joint angles (in [rad]).

    :param Array[int, float] enc:
        Sequence of ``(j0, j1, j1)`` where ``j0``, ``j1``, and ``j2`` refer to
        wrist joint angles for axes 0, 1, and 2, respectively, (in [rad]).

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param Array[int, int] out:
        An output buffer to store the raw encoder values.

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises ctypes.ArgumentError:
        If any element of ``joint_angles`` is not implicitly convertible to
        a C double.

    :raises IndexError:
        If ``len(joint_angles) < 3``.

    :raises TypeError:
        If ``joint_angles`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.wristJointAnglesToJacobian()`
    | :func:`forcedimension_core.dhd.expert.wristEncodersToJointAngles()`
    """

    enc0 = c_int()
    enc1 = c_int()
    enc2 = c_int()

    err = _runtime._libdhd.dhdWristJointAnglesToEncoders(
        joint_angles[0],
        joint_angles[1],
        joint_angles[2],
        enc0,
        enc1,
        enc2,
        ID
    )

    out[0] = enc0.value
    out[1] = enc1.value
    out[2] = enc2.value

    return err


_runtime._libdhd.dhdGetJointAngles.argtypes = [c_double_ptr, c_byte]
_runtime._libdhd.dhdGetJointAngles.restype = c_int


def getJointAngles(out: MutableArray[int, float], ID: int = -1) -> int:
    """
    Retrieve the joint angles (in [rad]) for all sensed degrees-of-freedom of
    the current device.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param MutableArray[int, float] out:
        An output buffer to store the joint angles (in [rad]).

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < MAX_DOF``

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.

    See Also
    ---------
    | :func:`forcedimension_core.dhd.expert.getDeltaJointAngles()`
    | :func:`forcedimension_core.dhd.expert.getWristJointAngles()`
    | :func:`forcedimension_core.dhd.expert.deltaJointAnglesToEncoders()`
    | :func:`forcedimension_core.dhd.expert.wristJointAnglesToEncoders()`
    | :func:`forcedimension_core.dhd.expert.deltaJointTorquesExtrema()`
    | :func:`forcedimension_core.dhd.expert.wristJointTorquesExtrema()`
    | :func:`forcedimension_core.dhd.expert.deltaJointAnglesToJacobian()`
    | :func:`forcedimension_core.dhd.expert.wristJointAnglesToJacobian()`
    | :func:`forcedimension_core.dhd.expert.jointAnglesToIntertiaMatrix()`
    | :func:`forcedimension_core.dhd.expert.jointAnglesToGravityJointTorques()`
    | :func:`forcedimension_core.dhd.expert.getJointVelocities()`
    """

    joint_angles = (c_double * MAX_DOF)()

    err = _runtime._libdhd.dhdGetJointAngles(ct.cast(joint_angles, c_double_ptr), ID)

    for i in range(MAX_DOF):
        out[i] = joint_angles[i]

    return err


_runtime._libdhd.dhdGetJointVelocities.argtypes = [c_double_ptr, c_byte]
_runtime._libdhd.dhdGetJointVelocities.restype = c_int


def getJointVelocities(out: MutableArray[int, float], ID: int = -1) -> int:
    """
    Retrieve the joint angle velocities (in [rad/s]) for all sensed
    degrees-of-freedom of the current device.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param MutableArray[int, float] out:
        An output buffer to store the joint velocities (in [rad/s]).

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < MAX_DOF``

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.getJointAngles()`
    | :func:`forcedimension_core.dhd.expert.getDeltaJacobian()`
    | :func:`forcedimension_core.dhd.expert.getWristJacobian()`
    """

    w = (c_double * MAX_DOF)()

    err = _runtime._libdhd.dhdGetJointVelocities(ct.cast(w, c_double_ptr), ID)

    for i in range(MAX_DOF):
        out[i] = w[i]

    return err


_runtime._libdhd.dhdGetEncVelocities.argtypes = [c_double_ptr, c_byte]
_runtime._libdhd.dhdGetEncVelocities.restype = c_int


def getEncVelocities(out: MutableArray[int, float], ID: int = -1) -> int:
    """
    Retrieve the encoder angle velocities (in [inc/s]) for all sensed
    degrees-of-freedom of the current device

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param MutableArray[int, float] out:
        An output buffer to store the encoder velocities (in [inc/s]).

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < MAX_DOF``

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
       0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD` on success,
       -1 otherwise.

    See Also
    --------
    | :data:`forcedimension_core.dhd.expert.getEnc()`
    """

    v = (c_double * MAX_DOF)()

    err = _runtime._libdhd.dhdGetEncVelocities(ct.cast(v, c_double_ptr), ID)

    for i in range(MAX_DOF):
        out[i] = v[i]

    return err


_runtime._libdhd.dhdJointAnglesToInertiaMatrix.argtypes = [
    c_double_ptr,
    c_double_ptr,
    c_byte
]
_runtime._libdhd.dhdJointAnglesToInertiaMatrix.restype = c_int


def jointAnglesToIntertiaMatrix(
    joint_angles: Array[int, float],
    out: MutableArray[int, MutableArray[int, float]],
    ID: int = -1,
) -> int:
    """
    Retrieve the inertia matrix based on a given joint
    configuration. Please refer to your device user manual for more information
    on your device coordinate system.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param MutableFloatMatrixLike out:
        Output buffer for the inertia matrix.

    :raises ctypes.ArgumentError:
        If ``joint_angles`` is not implicitly convertible to a C char

    :raises IndexError:
        If ``len(joint_angles) < 3``.

    :raises TypeError:
        If ``joint_angles`` is not subscriptable.

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If of the any dimension of ``out`` is less than 6.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.getJointAngles()`
    """

    inertia = ((c_double * 6) * 6)()
    joint_angles_arr = (c_double * MAX_DOF)(
            joint_angles[0],
            joint_angles[1],
            joint_angles[2],
            joint_angles[3],
            joint_angles[4],
            joint_angles[5],
            joint_angles[6],
            joint_angles[7]
        )

    err = _runtime._libdhd.dhdJointAnglesToInertiaMatrix(
        ct.cast(joint_angles_arr, c_double_ptr),
        ct.cast(inertia, c_double_ptr),
        ID
    )

    for i in range(6):
        for j in range(6):
            out[i][j] = inertia[i][j]

    return err


_runtime._libdhd.dhdJointAnglesToGravityJointTorques.argtypes = [
    c_double_ptr,
    c_double_ptr,
    c_ubyte,
    c_byte
]
_runtime._libdhd.dhdJointAnglesToGravityJointTorques.restype = c_int


def jointAnglesToGravityJointTorques(
    joint_angles: Array[int, float],
    out: MutableArray[int, float],
    mask: int = 0xff,
    ID: int = -1,
) -> int:
    """
    This function computes the joint torques (in [Nm]) required to provide
    gravity compensation on all actuated degrees-of-freedom of the current
    device for a given joint angles configuration (in [rad])

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param int mask:
        Bitwise mask of which joint torques should be computed.

    :param MutableFloatMatrixLike out:
        Output buffer for the joint torques required to provide gravity
        compensation (in [Nm]).

    :raises ctypes.ArgumentError:
        If ``joint_angles`` is not implicitly convertible to a C char

    :raises IndexError:
        If ``len(joint_angles) < forcedimension_core.dhd.constants.MAX_DOF``.

    :raises TypeError:
        If ``joint_angles`` is not subscriptable.

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out)`` is less than
        :data:`forcedimension_core.dhd.constants.MAX_DOF`.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``mask`` is not implicitly convertible to a C uchar.

    :returns:
        0 on success, -1 otherwise.

    See Also
    --------
    |  :func:`forcedimension_core.dhd.expert.getJointAngles()`
    """

    q = (c_double * MAX_DOF)()
    joint_angles_arr = (c_double * MAX_DOF)(
            joint_angles[0],
            joint_angles[1],
            joint_angles[2],
            joint_angles[3],
            joint_angles[4],
            joint_angles[5],
            joint_angles[6],
            joint_angles[7]
        )

    err = _runtime._libdhd.dhdJointAnglesToInertiaMatrix(
        ct.cast(joint_angles_arr, c_double_ptr),
        ct.cast(q, c_double_ptr),
        mask,
        ID
    )

    for i in range(MAX_DOF):
        out[i] = q[i]

    return err


_runtime._libdhd.dhdSetComMode.argtypes = [c_int, c_byte]
_runtime._libdhd.dhdSetComMode.restype = c_int


def setComMode(mode: ComMode, ID: int = -1) -> int:
    """
    Set the COM operation mode on compatible devices.

    :param ComMode mode:
        desired COM operation mode.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``mode`` is not implicitly convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns: 0 on success, -1 otherwise.
    """

    return _runtime._libdhd.dhdSetComMode(mode, ID)


_runtime._libdhd.dhdSetWatchdog.argtypes = [c_ubyte, c_byte]
_runtime._libdhd.dhdSetWatchdog.restype = c_int


def setWatchdog(duration: int, ID: int = -1) -> int:
    """
    Set the watchdog duration in multiples of 125 microseconds on compatible
    devices. If the watchdog duration is exceeded before the device recieves a
    new force command, the device firmware will disable forces.

    :param int duration:
        watchdog duration in multiples of 125 us.
        A value of 0 disables the watchdog feature.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``duration`` is not implicitly convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns: 0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.getWatchdog()`
    """

    return _runtime._libdhd.dhdSetWatchdog(duration, ID)


_runtime._libdhd.dhdGetWatchdog.argtypes = [c_ubyte_ptr, c_byte]
_runtime._libdhd.dhdGetWatchdog.restype = c_int


def getWatchdog(ID: int = -1) -> int:
    """
    Get the watchdog duration in multiples of 125 us on compatible
    devices.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        The (non-negative) watchdog duration on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.expert.setWatchdog()`
    """

    duration = c_int()

    if _runtime._libdhd.dhdSetWatchdog(duration, ID):
        return -1

    return duration.value


_runtime._libdhd.dhdGetEncRange.argtypes = [c_int_ptr, c_int_ptr, c_byte]
_runtime._libdhd.dhdGetEncRange.restype = c_int


def getEncRange(ID: int = -1) -> Tuple[IntDOFTuple, IntDOFTuple, int]:
    """
    Get the expected min and max encoder values for all axes present on the
    current device. Axis indices that do not exist on the device will return
    a range of 0.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.
    """

    encMin = (c_int * MAX_DOF)()
    encMax = (c_int * MAX_DOF)()

    err = _runtime._libdhd.dhdGetEncRange(encMin, encMax, ID)

    return (tuple(encMin), tuple(encMax), err)


_runtime._libdhd.dhdGetJointAngleRange.argtypes = [c_double_ptr, c_double_ptr, c_byte]
_runtime._libdhd.dhdGetJointAngleRange.restype = c_int


def getJointAngleRange(ID: int = -1) -> Tuple[
    FloatDOFTuple, FloatDOFTuple, int
]:
    """
    This function retrieves the expected min and max joint angles (in [rad])
    for all sensed degrees-of-freedom on the current device. Axis indices that
    do not exist on the device will return a range of 0.0.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        A tuple of (jmin, jmax, err). jmin and jmax are tuples of
        floats representing the min and max joint angles for each
        degree-of-freedom (in [rad]). err is 0 on success and -1 otherwise.
    """

    jmin = (c_double * MAX_DOF)()
    jmax = (c_double * MAX_DOF)()

    err = _runtime._libdhd.dhdGetEncRange(
        ct.cast(jmin, c_double_ptr), ct.cast(jmax, c_double_ptr), ID
    )

    return (tuple(jmin), tuple(jmax), err)


_runtime._libdhd.dhdControllerSetDevice.argtypes = [c_int, c_byte]
_runtime._libdhd.dhdControllerSetDevice.restype = c_int


def controllerSetDevice(devtype: DeviceType, ID: int = -1) -> int:
    """
    If the connected device is a controller lets the programmer define the
    Force Dimension mechanical structure attached to it. Upon selecting a
    device model, the routine will attempt to read that particular
    device configuration from the controller. If this fails, a default
    configuration will be selected and stored in the controller.

    Note
    ----
    This feature only applies to the following types of devices:

    :data:`forcedimension_core.constants.DeviceType.CONTROLLER`
    :data:`forcedimension_core.constants.DeviceType.CONTROLLER_HR`


    :param DeviceType devtype:
        The device type to use.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.
    """

    return _runtime._libdhd.dhdControllerSetDevice(devtype, ID)


_runtime._libdhd.dhdReadConfigFromFile.argtypes = [c_char_p, c_byte]
_runtime._libdhd.dhdReadConfigFromFile.restype = c_int


def readConfigFromFile(filename: str, ID: int = -1):
    """
    This function loads a specific device calibration/configuration data from
    a file. Particularly useful when using the generic controller connected to
    a Force Dimension device without using the
    :func:`forcedimension_core.dhd.controllerSetDevice()` call.

    :param bytes filename:
        Configuration file containing device calibration/configuration data.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.
    """

    return _runtime._libdhd.dhdReadConfigFromFile(filename.encode('utf-8'), ID)


_runtime._libdhd.dhdDeltaGravityJointTorques.argtypes = [
    c_double,
    c_double,
    c_double,
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_byte
]
_runtime._libdhd.dhdDeltaGravityJointTorques.restype = c_int


@typing_extensions.deprecated(
    "This function is deprecated, please use "
    "forcedimension_core.dhd.jointAnglesToGravityJointTorques() instead."
)
def deltaGravityJointTorques(
    joint_angles: Array[int, float],
    out: MutableArray[int, float],
    ID: int = -1
) -> int:
    """
    Compute the DELTA joint torques required to compensate for gravity in a
    given DELTA joint angle configuration. Please refer to your device user
    manual for more information on your device coordinate system.

    .. deprecated:: 1.0.0
       Force Dimension SDK v3.16.0+ recommends that you use
       :func:`forcedimension_core.dhd.expert.jointAnglesToGravityJointTorques()`
       instead.


    :param Array[int, float] joint_angles:
        Sequence of ``(j0, j1, j2)`` where ``j0``, ``j1``, ``j2`` refer to the
        joint angles for axis 0, 1, and 2, respectively.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param MutableArray[int, float] out:
        An output buffer to store the return.

    :raises TypeError:
        If ``out`` does not support item.
        assignment either because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises ctypes.ArgumentError:
        If any element of ``joint_angles`` is not implicitly convertible to
        a C double.

    :raises IndexError:
        If ``len(joint_angles) < 3``.

    :raises TypeError:
        If ``joint_angles`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.
    """

    q0 = c_double()
    q1 = c_double()
    q2 = c_double()

    err = _runtime._libdhd.dhdDeltaGravityJointTorques(
        joint_angles[0],
        joint_angles[1],
        joint_angles[2],
        q0,
        q1,
        q2,
        ID
    )

    out[0] = q0.value
    out[1] = q1.value
    out[2] = q2.value

    return err


_runtime._libdhd.dhdWristGravityJointTorques.argtypes = [
    c_double,
    c_double,
    c_double,
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_byte
]
_runtime._libdhd.dhdWristGravityJointTorques.restype = c_int


@typing_extensions.deprecated(
    "This function is deprecated, please use "
    "forcedimension_core.dhd.jointAnglesToGravityJointTorques() instead.",
)
def wristGravityJointTorques(
    joint_angles: Array[int, float],
    out: MutableArray[int, float],
    ID: int = -1
) -> int:
    """
    Compute the wrist joint torques required to compensate for gravity in a
    given wrist joint angle configuration. Please refer to your device user
    manual for more information on your device coordinate system.

    .. deprecated:: 1.0.0
       Force Dimension SDK v3.16.0+ recommends that you use
       :func:`forcedimension_core.dhd.jointAnglesToGravityJointTorques()`
       instead.


    :param Array[int, float] joint_angles:
        Sequence of ``(j0, j1, j2)`` where ``j0``, ``j1``, and ``j2`` refer to
        the joint angles for wrist axes 0, 1, and 2, respectively.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param MutableArray[int, float] out:
        An output buffer to store the joint torques.

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises ctypes.ArgumentError:
        If any element of ``joint_angles`` is not implicitly convertible to
        a C double.

    :raises IndexError:
        If ``len(joint_angles) < 3``.

    :raises TypeError:
        If ``joint_angles`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise
    """

    q0 = c_double()
    q1 = c_double()
    q2 = c_double()

    err = _runtime._libdhd.dhdWristGravityJointTorques(
        joint_angles[0],
        joint_angles[1],
        joint_angles[2],
        q0,
        q1,
        q2,
        ID
    )

    out[0] = q0.value
    out[1] = q1.value
    out[2] = q2.value

    return err
