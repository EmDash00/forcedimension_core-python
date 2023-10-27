from ctypes import c_byte, c_double, c_int, c_ushort
from typing import Tuple

import forcedimension_core.runtime as _runtime
from forcedimension_core.typing import (
    Array, SupportsPtr, SupportsPtrs3, c_double_ptr
)


def getDeltaEncoders(out: SupportsPtrs3[c_int], ID: int = -1) -> int:
    """
    Read all encoders values of the DELTA structure.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param SupportsPtrs3[ctypes.c_int] out:
        An output buffer to store the delta encoder values.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD`
        on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.dco_expert.deltaEncodersToJointAngles()`
    | :func:`forcedimension_core.dhd.dco_expert.deltaEncoderToPosition()`
    """

    return _runtime._libdhd.dhdGetDeltaEncoders(*out.ptrs, ID)


def getWristEncoders(out: SupportsPtrs3[c_int], ID: int = -1) -> int:
    """
    Read all encoders values of the wrist structure.


    Note
    ----
    This feature only applies to devices with a wrist. See
    the :ref:`device_types` section for more details.


    :param SupportsPtrs3[ctypes.c_int] out:
        An output buffer to store the wrist encoder values.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

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

    return _runtime._libdhd.dhdGetWristEncoders(*out.ptrs, ID)


def deltaEncoderToPosition(
    enc: Array[int, int],
    out: SupportsPtrs3[c_double],
    ID: int = -1
) -> int:
    """
    This routine computes and returns the position of the end-effector about
    the X, Y, and Z axes (in [m]) for a given set of encoder values.

    :param Array[int, int] enc:
        Sequence of ``(enc0, enc1, enc2)`` where ``enc0``, ``enc1``, and
        ``enc2`` refer to raw encoder values on axis 0, 1, and 2,
        respectively.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param SupportsPtrs3[ctypes.c_double] out:
        An output buffer to store the position about the X, Y, and Z axes
        (in [m]).

    :raises ctypes.ArgumentError:
        If any element of ``enc`` is not implicitly convertible to a C int.

    :raises IndexError:
        If ``len(enc) < 3``.

    :raises TypeError:
        If ``enc`` is not subscriptable.

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.dco_expert.getDeltaEncoders()`
    | :func:`forcedimension_core.dhd.dco_expert.deltaPositionToEncoder()`
    | :func:`forcedimension_core.dhd.dco_expert.deltaEncodersToJointAngles()`
    """

    return _runtime._libdhd.dhdDeltaEncoderToPosition(
        enc[0], enc[1], enc[2], *out.ptrs, ID
    )


def deltaPositionToEncoder(
    pos: Array[int, float],
    out: SupportsPtrs3[c_int],
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

    :param SupportsPtrs3[ctypes.c_int] out:
        An output buffer to store the delta encoder values.

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

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
    | :func:`forcedimension_core.dhd.dco_expert.getDeltaEncoders()`
    | :func:`forcedimension_core.dhd.dco_expert.deltaEncoderToPosition()`
    | :func:`forcedimension_core.dhd.dco_expert.deltaEncodersToJointAngles()`
    """

    return _runtime._libdhd.dhdDeltaPositionToEncoder(
        pos[0], pos[1], pos[2], *out.ptrs, ID
    )


def deltaMotorToForce(
    mot: Array[int, int],
    enc: Array[int, int],
    out: SupportsPtrs3[c_double],
    ID: int = -1
) -> int:
    """
    This routine computes and returns the force applied to the end-effector
    about the X, Y, and Z axes (in [N]) for a given set of motor commands at a
    given position (defined by encoder readings)

    :param Array[int, int] mot:
        Sequence of ``(mot0, mot1, mot2)`` where ``mot0``, ``mot1``,
        and ``mot2`` are the axis 0, 1, and 2 DELTA motor commands,
        respectively.

    :param Array[int, int] enc:
        Sequence of ``(enc0, enc1, enc2)`` where ``enc0``, ``enc1``, and
        ``enc2`` refer to encoder values on axis 0, 1, and 2,
        respectively.

    :param SupportsPtrs3[ctypes.c_double] out:
        An output buffer to store the force applied to the end effector about
        the X, Y, and Z axes (in [N])

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises TypeError:
        If ``out`` does not support item assignment either
        because it's immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

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
    | :func:`forcedimension_core.dhd.dco_expert.deltaForceToMotor()`
    """

    return _runtime._libdhd.dhdDeltaMotorToForce(
        mot[0], mot[1], mot[2],
        enc[0], enc[1], enc[2],
        *out.ptrs,
        ID
    )


def deltaForceToMotor(
    f: Array[int, float],
    enc: Array[int, int],
    out: SupportsPtrs3[c_ushort],
    ID=-1
) -> int:
    """
    This routine computes and returns the motor commands necessary to obtain a
    given force on the end-effector at a given position (defined by encoder
    readings).

    :param Array[int, float] f:
        Sequence of ``(fx, fy, fz)`` where ``fx``, ``fy``, and ``fz`` are the
        force on the DELTA end-effector on the X, Y, and Z axes, respectively
        (in [N]).

    :param Array[int, int] enc:
        Sequence of ``(enc0, enc1, enc2)`` where ``enc0``, ``enc1``, and
        ``enc2`` refer to encoder values on axis 0, 1, and 2, respectively.

    :param SupportsPtrs3[ctypes.c_ushort] out:
        An output buffer to store the motor commands on axes 0, 1, and 2.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If any element of ``f`` is not implicitly convertible to a C double.

    :raises IndexError:
        If ``len(f) < 3``.

    :raises TypeError:
        If ``f`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If any element of ``enc`` is not implicitly convertible to a C int.

    :raises IndexError:
        If ``len(enc) < 3``.

    :raises TypeError:
        If ``enc`` is not subscriptable.

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_ushort]`` types.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 or :data:`forcedimension_core.dhd.constants.MOTOR_SATURATED`
        on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.dco_expert.deltaMotorToForce()`
    """

    return _runtime._libdhd.dhdDeltaForceToMotor(
        f[0], f[1], f[2],
        enc[0], enc[1], enc[2],
        *out.ptrs,
        ID
    )


def wristEncoderToOrientation(
    enc: Array[int, int],
    out: SupportsPtrs3[c_double],
    ID: int = -1,
) -> int:
    """
    For devices with a wrist structure, compute the individual angle of each
    joint (in [rad]), starting with the one located nearest to the wrist base
    plate. For the :data:`forcedimension_core.dhd.constants.DeviceType.OMEGA6`
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

    :param SupportsPtrs3[ctypes.c_double] out:
        An output buffer to store the wrist end-effector orientation about the
        first, second, and third wrist joints (in [rad]).

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If any element of ``enc`` is not implicitly convertible
        to a C int.

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
    | :func:`forcedimension_core.dhd.dco_expert.wristEncodersToJointAngles()`
    | :func:`forcedimension_core.dhd.dco_expert.wristOrientationToEncoder()`
    | :func:`forcedimension_core.dhd.dco_expert.wristJointAnglesToEncoders()`
    """
    return _runtime._libdhd.dhdWristEncoderToOrientation(
        enc[0], enc[1], enc[2],
        *out.ptrs,
        ID
    )


def wristOrientationToEncoder(
    orientation: Array[int, float],
    out: SupportsPtrs3[c_int],
    ID: int = -1,
) -> int:
    """
    For devices with a wrist structure, compute the encoder values from the
    individual angle of each joint, starting with the one located nearest to
    the wrist plate base.

    Note
    ----
    For the :data:`forcedimension_core.dhd.constants.DeviceType.OMEGA6` and
    :data:`forcedimension_core.dhd.constants.DeviceType.OMEGA6_LEFT` devices,
    angles must be expressed with respect to their internal reference frame,
    which is rotated 45 degrees or π/4 radians about the Y axis. Please refer
    to your device user manual for more information on your device coordinate
    system.


    Note
    ----
    This feature only applies to devices with an wrist. See
    the :ref:`device_types` section for more details.


    :param Array[int, float] orientation:
        Sequence of ``(oa, ob, og)`` where ``oa``, ``ob``, and ``og`` refer to
        wrist end effector orientation (in [rad]) around the X, Y, and Z axes,
        respectively.

    :param SupportsPtrs3[ctypes.c_int] out:
        An output buffer to store the encoder values.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).


    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_int]`` types.

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
    | :func:`forcedimension_core.dhd.dco_expert.wristEncodersToJointAngles()`
    | :func:`forcedimension_core.dhd.dco_expert.wristEncodersToOrientation()`
    | :func:`forcedimension_core.dhd.dco_expert.wristJointAnglesToEncoders()`
    """

    return _runtime._libdhd.dhdWristOrientationToEncoder(
        orientation[0], orientation[1], orientation[2],
        *out.ptrs,
        ID
    )


def wristMotorToTorque(
    output: Array[int, int],
    enc: Array[int, int],
    out: SupportsPtrs3[c_double],
    ID: int = -1
) -> int:
    """
    This routine computes and returns the torque applied to the wrist
    end-effector about the, X, Y, and Z axes (in [Nm]) for a given set of motor
    commands at a given orientation (defined by encoder values)

    Note
    ----
    This feature only applies to devices with an active wrist. See
    the :ref:`device_types` section for more details.


    :param Array[int, int] cmd:
        Sequence of ``(cmd0, cmd1, cmd2)`` where ``cmd0``, ``cmd1``,
        and ``cmd2`` are the axis 0, 1, and 2 DELTA motor commands,
        respectively.

    :param Array[int, int] enc:
        Sequence of ``(enc0, enc1, enc2)`` where ``enc0``, ``enc1``, and
        ``enc2`` refer to encoder values on axis 0, 1, and 2, respectively.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param SupportsPtrs3[ctypes.c_double] out:
        An output buffer to store the torques applied to the wrist about the
        X, Y, and Z axes (in [Nm]).

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If any element of ``cmd`` is not implicitly convertible to a C ushort.

    :raises IndexError:
        If ``len(cmd) < 3``.

    :raises TypeError:
        If ``cmd`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If any element of ``enc`` is not implicitly convertible to a C int.

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
    | :func:`forcedimension_core.dhd.dco_expert.wristTorqueToMotor()`
    | :func:`forcedimension_core.dhd.dco_expert.wristJointTorquesExtrema()`
    """

    return _runtime._libdhd.dhdWristMotorToTorque(
        output[0], output[1], output[2],
        enc[0], enc[1], enc[2],
        *out.ptrs,
        ID
    )


def wristTorqueToMotor(
    t: Array[int, float],
    enc: Array[int, int],
    out: SupportsPtrs3[c_ushort],
    ID: int = -1
) -> int:
    """
    This routine computes and returns the wrist motor commands necessary to
    obtain a given torque on the wrist end-effector about the X, Y, and Z axes
    (in [Nm]) at a given orientation (defined by encoder values)

    Note
    ----
    This feature only applies to the following devices:

    :data:`forcedimension_core.dhd.constants.DeviceType.SIGMA7_RIGHT`
    :data:`forcedimension_core.dhd.constants.DeviceType.SIGMA7_LEFT`


    :param Array[int, float] t:
        Sequence of ``(t0, t1, t2)`` where ``t0``, ``t1``, and ``t2`` are the
        DELTA axis torque commands (in [Nm]) for axes 0, 1, and 2,
        respectively.

    :param Array[int, int] enc:
        Sequence of ``(enc0, enc1, enc2)`` where ``enc0``, ``enc1``, and
        ``enc2`` refer to encoder values on axis 0, 1, and 2, respectively.

    :param SupportsPtrs3[ctypes.c_ushort] out:
        An output buffer to store the wrist motor commands.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_ushort]`` types.

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
    | :func:`forcedimension_core.dhd.dco_expert.wristTorqueToMotor()`
    """

    return _runtime._libdhd.dhdWristTorqueToMotor(
        t[0], t[1], t[2],
        enc[0], enc[1], enc[2],
        *out.ptrs,
        ID
    )


def gripperMotorToForce(
    cmd: int,
    enc_wrist_grip: SupportsPtr[c_int],
    out: c_double,
    ID: int = -1
) -> int:
    """
    Computes the force applied to the end-effector (in [N]) for a given
    motor command.

    Note
    ----
    This feature only applies to devices with an active gripper. See
    the :ref:`device_types` section for more details.


    :param int output:
        Motor command on gripper axis.

    :param SupportsPtr[c_int] enc_wrist_grip:
        Buffer which contains the encoder values about wrist joints 0, 1, and
        2 as well as the encoder value of the gripper.

    :param c_ushort out:
        Output buffer to store the force applied to the end-effector (in [N]).

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``cmd`` is not implicitly convertible to a C ushort.

    :raises AttributeError:
        If ``enc_wrist_grip.ptr`` is not a valid attribute of
        ``enc_wrist_grip``

    :raises ctypes.ArgumentError:
        If ``enc_wrist_grip.ptr`` is not of type Pointer[c_int]

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.dco_expert.gripperForceToMotor()`
    """

    return _runtime._libdhd.dhdGripperMotorToForce(
        cmd, out, enc_wrist_grip.ptr, ID
    )


def gripperForceToMotor(
    f: float,
    enc_wrist_grip: SupportsPtr[c_int],
    out: c_ushort,
    ID: int = -1
) -> Tuple[int, int]:
    """
    Given a desired force to be displayed by the force gripper, this routine
    computes and returns the refering motor command.

    Note
    ----
    This feature only applies to devices with an active gripper. See
    the :ref:`device_types` section for more details.


    :param int f:
        Force on the gripper end-effector (in [N]).

    :param Array[int, int] enc_wrist:
        An output buffer to store the wrist encoding readings.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``f`` is not implicitly convertible to a C double.

    :raises AttributeError:
        If ``enc_wrist_grip.ptr`` is not a valid attribute of
        ``enc_wrist_grip``

    :raises ctypes.ArgumentError:
        If ``enc_wrist_grip.ptr`` is not of type Pointer[c_int]

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        A tuple in the form ``(cmd, err)``.  ``cmd`` is the motor command on
        the gripper axis. ``err`` is 0 or
        :data:`forcedimension_core.dhd.constants.MOTOR_SATURATED` on success,
        -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.dco_expert.gripperForceToMotor()`
    """

    return _runtime._libdhd.dhdGripperForceToMotor(f, out, enc_wrist_grip.ptr, ID)


def getEnc(out: SupportsPtr[c_int], mask: int = 0xff, ID: int = -1) -> int:
    """
    Get a selective list of encoder values. Particularly useful when using the
    generic controller directly, without a device model attached.

    :param SupportsPtr[c_int] out:
        An output buffer to store the encoder values.

    :param int mask:
        Bitwise mask of which motor should be set.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of
        :data:`forcedimension_core.dhd.constants.MAX_DOF` ``Pointer[c_int]``
        types.

    :raises ctypes.ArgumentError:
        If ``mask`` is not implicitly convertible to a C uchar.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD`
        on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.dco_expert.getEncVelocities()`
    """

    return _runtime._libdhd.dhdGetEnc(out.ptr, mask, ID)


def getDeltaJointAngles(out: SupportsPtrs3[c_double], ID: int = -1) -> int:
    """
    Retrieve the joint angles (in [rad]) for the DELTA structure.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param SupportsPtrs3[ctypes.c_double] out:
        An output buffer to store the joint angles (in [rad]) of the DELTA
        structure for axes 0, 1, and 2.

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.dco_expert.deltaEncodersToJointAngles()`
    | :func:`forcedimension_core.dhd.dco_expert.deltaJointAnglesToEncoders()`
    | :func:`forcedimension_core.dhd.dco_expert.deltaJointAnglesToJacobian()`
    """

    return _runtime._libdhd.dhdGetDeltaJointAngles(*out.ptrs, ID)


def getDeltaJacobian(out: SupportsPtr[c_double], ID: int = -1) -> int:
    """
    Retrieve the 3x3 jacobian matrix for the DELTA structure based on the
    current end-effector position. Please refer to your device user manual for
    more information on your device coordinate system.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param SupportsPtr[c_double] out:
        An output buffer to store the Jacobian.

    :raises AttributeError:
        If ``out.ptr`` is not a valid attribute of ``out``

    :raises ctypes.ArgumentError:
        If ``out.ptr`` is not of type Pointer[c_double]

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.dco_expert.deltaJointAnglesToJacobian()`
    """

    return _runtime._libdhd.dhdGetDeltaJacobian(out.ptr, ID)


def deltaJointAnglesToJacobian(
    joint_angles: Array[int, float],
    out: SupportsPtr[c_double],
    ID: int = -1,
) -> int:
    """
    Retrieve the 3x3 jacobian matrix for the DELTA structure
    based on a given joint configuration. Please refer to your device user
    manual for more information on your device coordinate system.

    :param Array[int, float] joint_angles:
        Sequence of (j0, j1, j2) where ``j0``, ``j1``, and ``j2`` refer to the
        joint angles (in [rad]) for axis 0, 1, and 2, respectively.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param SupportsPtr[c_double] out:
        An output buffer to store the Jacobian.

    :raises AttributeError:
        If ``out.ptr`` is not a valid attribute of ``out``

    :raises ctypes.ArgumentError:
        If ``out.ptr`` is not of type Pointer[c_double]

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
    | :func:`forcedimension_core.dhd.dco_expert.getJointAngles()`
    | :func:`forcedimension_core.dhd.dco_expert.getDeltaJointAngles()`
    | :func:`forcedimension_core.dhd.dco_expert.getDeltaJacobian()`
    """

    return _runtime._libdhd.dhdDeltaJointAnglesToJacobian(
        joint_angles[0], joint_angles[1], joint_angles[2],
        out.ptr,
        ID
    )


def deltaJointTorquesExtrema(
    joint_angles: Array[int, float],
    minq_out: SupportsPtr[c_double],
    maxq_out: SupportsPtr[c_double],
    ID: int = -1
) -> int:
    """
    Compute the range of applicable DELTA joint torques (in [Nm]) for a
    given DELTA joint angle configuration (in [rad]).
    Please refer to your device user manual for more information on your device
    coordinate system.

    :param Array[int, float] joint_angles:
        Sequence of (j0, j1, j2) where ``j0``, ``j1``, and ``j2`` refer to the
        joint angles (in [rad]) for axis 0, 1, and 2, respectively.

    :param SupportsPtrs3[ctypes.c_double] minq_out:
        An output buffer to store the minimum appliable DELTA joint torques
        about axes 0, 1, and 2 (in [Nm]).

    :param SupportsPtrs3[ctypes.c_double] maxq_out:
        An output buffer to store the maximum appliable DELTA joint torques
        about axes 0, 1, and 2 (in [Nm]).

    :raises AttributeError:
        If ``minq_out.ptrs`` is not a valid attribute of ``minq_out``

    :raises TypeError:
        If ``minq_out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``minq_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises AttributeError:
        If ``maxq_out.ptrs`` is not a valid attribute of ``maxq_out``

    :raises TypeError:
        If ``maxq_out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``maxq_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

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
    | :func:`forcedimension_core.dhd.dco_expert.wristJointTorquesExtrema()`
    | :func:`forcedimension_core.dhd.dco_expert.getDeltaJointAngles()`
    | :func:`forcedimension_core.dhd.dco_expert.getJointAngles()`
    """

    return _runtime._libdhd.dhdDeltaJointTorquesExtrema(
        joint_angles[0],
        joint_angles[1],
        joint_angles[2],
        minq_out.ptr,
        maxq_out.ptr,
        ID
    )


def deltaEncodersToJointAngles(
    enc: Array[int, int],
    out: SupportsPtrs3[c_double],
    ID: int = -1
) -> int:
    """
    This routine computes and returns the DELTA joint angles (in [rad]) for a
    given set of encoder values.

    :param Array[int, int] enc:
        Sequence of ``(enc0, enc1, enc2)`` where ``enc0``, ``enc1``, and
        ``enc2`` refer to encoder values on axis 0, 1, and 2, respectively.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param SupportsPtrs3[ctypes.c_double] out:
        An output buffer to store the DELTA joint angles (in [rad]) about axes
        0, 1, and 2.

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

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
    | :func:`forcedimension_core.dhd.dco_expert.deltaJointAnglesToJacobian()`
    | :func:`forcedimension_core.dhd.dco_expert.deltaJointAnglesToEncoders()`
    """

    return _runtime._libdhd.dhdDeltaEncodersToJointAngles(
        enc[0],
        enc[1],
        enc[2],
        *out.ptrs,
        ID
    )


def deltaJointAnglesToEncoders(
    joint_angles: Array[int, float],
    out: SupportsPtrs3[c_int],
    ID: int = -1,
) -> int:
    """
    This routine computes and returns the DELTA encoder values for a given
    set of joint angles (in [rad]).

    :param Array[int, float] enc:
        Sequence of ``(j0, j1, j1)`` where ``j0``, ``j1``, and ``j2`` refer to
        DELTA joint angles (in [rad]) for axes 0, 1, and 2, respectively.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param SupportsPtrs3[ctypes.c_double] out:
        An output buffer to store the DELTA encoder values.

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
    | :func:`forcedimension_core.dhd.dco_expert.deltaJointAnglesToJacobian()`
    | :func:`forcedimension_core.dhd.dco_expert.deltaEncodersToJointAngles()`
    """

    return _runtime._libdhd.dhdDeltaJointAnglesToEncoders(
        joint_angles[0],
        joint_angles[1],
        joint_angles[2],
        *out.ptrs,
        ID
    )


def getWristJointAngles(out: SupportsPtrs3[c_double], ID: int = -1) -> int:
    """
    Retrieve the joint angles (in [rad]) for the wrist structure.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param SupportsPtrs3[ctypes.c_double] out:
        An output buffer to store the wrist joint angles.

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.dco_expert.dhdWristJointAnglesToJacobian()`
    | :func:`forcedimension_core.dhd.dco_expert.dhdWristJointTorquesExtrema()`
    | :func:`forcedimension_core.dhd.dco_expert.wristJointAnglesToEncoders()`
    | :func:`forcedimension_core.dhd.dco_expert.wristEncodersToJointAngles()`
    """

    return _runtime._libdhd.dhdGetWristJointAngles(*out.ptrs, ID)


def getWristJacobian(out: SupportsPtr[c_double], ID: int = -1) -> int:
    """
    Retrieve the 3x3 jacobian matrix for the wrist structure based on the
    current end-effector position. Please refer to your device user manual for
    more information on your device coordinate system.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param SupportsPtr[c_double] out:
        An output buffer to store the Jacobian.

    :raises AttributeError:
        If ``out.ptr`` is not a valid attribute of ``out``

    :raises ctypes.ArgumentError:
        If ``out.ptr`` is not a ``Pointer[c_double]`` type.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD` on success,
        and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.dco_expert.wristJointAnglesToJacobian()`
    """

    return _runtime._libdhd.dhdGetWristJacobian(out.ptr, ID)


def wristJointAnglesToJacobian(
    joint_angles: Array[int, float],
    out: SupportsPtr[c_double],
    ID: int = -1,
) -> int:
    """
    Retrieve the 3x3 jacobian matrix for the wrist structure
    based on a given joint configuration. Please refer to your device user
    manual for more information on your device coordinate system.

    :param Array[int, float] joint_angles:
        Sequence of ``(j0, j1, j2)`` where ``j0``, ``j1``, and ``j2`` refer to
        the joint angles for wrist axis 0, 1, and 2, respectively.

    :param SupportsPtr[c_double] out:
        An output buffer to store the wrist jacobian.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises AttributeError:
        If ``out.ptr`` is not a valid attribute of ``out``

    :raises ctypes.ArgumentError:
        If ``out.ptr`` is not a ``Pointer[c_double]`` type.

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
    | :func:`forcedimension_core.dhd.dco_expert.wristEncodersToJointAngles()`
    | :func:`forcedimension_core.dhd.dco_expert.getWristJointAngles()`
    """

    return _runtime._libdhd.dhdWristJointAnglesToJacobian(
        joint_angles[0],
        joint_angles[1],
        joint_angles[2],
        out.ptr,
        ID
    )


def wristJointTorquesExtrema(
    joint_angles: Array[int, float],
    minq_out: SupportsPtr[c_double],
    maxq_out: SupportsPtr[c_double],
    ID: int = -1
) -> int:
    """
    Compute the range of applicable wrist joint torques for a given wrist joint
    angle configuration. Please refer to your device user manual for more
    information on your device coordinate system.

    :param Array[int, float] joint_angles:
        Sequence of ``(j0, j1, j2)`` where ``j0``, ``j1``, ``j2`` refer to the
        joint angles for wrist axes 0, 1, and 2, respectively.

    :param SupportsPtrs3[ctypes.c_double] minq_out:
        An output buffer to store the minimum appliable DELTA joint torques
        about axes 0, 1, and 2 (in [Nm]).

    :param SupportsPtrs3[ctypes.c_double] maxq_out:
        An output buffer to store the maximum appliable DELTA joint torques
        about axes 0, 1, and 2 (in [Nm]).

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If any element of ``joint_angles`` is not implicitly convertible to C
        double.

    :raises IndexError:
        If ``len(joint_angles) < 3``.

    :raises TypeError:
        If ``joint_angles`` is not subscriptable.

    :raises AttributeError:
        If ``minq_out.ptrs`` is not a valid attribute of ``minq_out``

    :raises TypeError:
        If ``minq_out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``minq_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises AttributeError:
        If ``maxq_out.ptrs`` is not a valid attribute of ``maxq_out``

    :raises TypeError:
        If ``maxq_out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``maxq_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.dco_expert.getJointAngles()`
    | :func:`forcedimension_core.dhd.dco_expert.getWristJointAngles()`
    | :func:`forcedimension_core.dhd.dco_expert.wristEncodersToJointAngles()`
    | :func:`forcedimension_core.dhd.dco_expert.wristJointAnglesToJacobian()`
    | :func:`forcedimension_core.dhd.dco_expert.wristJointAnglesToEncoders()`
    """

    return _runtime._libdhd.dhdWristJointTorquesExtrema(
        joint_angles[0],
        joint_angles[1],
        joint_angles[2],
        minq_out.ptr,
        maxq_out.ptr,
        ID
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
    out: SupportsPtrs3[c_double],
    ID: int = -1
) -> int:
    """
    This routine computes and returns the wrist joint angles (in [rad])
    for a given set of encoder values.

    :param Array[int, int] enc:
        Sequence of (enc0, enc1, enc2) where ``enc0``, ``enc1``, and ``enc2``
        refer to encoder values on wrist axes 0, 1, and 2, respectively.

    :param SupportsPtrs3[ctypes.c_double] out:
        An output buffer to store the joint angles (in [rad]) about wrist
        joint axes 0, 1, and 2.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

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
    | :func:`forcedimension_core.dhd.dco_expert.wristJointAnglesToJacobian()`
    | :func:`forcedimension_core.dhd.dco_expert.wristJointTorquesExtrema()`
    | :func:`forcedimension_core.dhd.dco_expert.wristJointAnglesToEncoders()`
    """

    return _runtime._libdhd.dhdWristEncodersToJointAngles(
        enc[0], enc[1], enc[2], *out.ptrs, ID
    )


def wristJointAnglesToEncoders(
    joint_angles: Array[int, float],
    out: SupportsPtrs3[c_int],
    ID: int = -1
) -> int:
    """
    This routine computes and returns the wrist encoder values for a given
    set of wrist joint angles (in [rad]).

    :param Array[int, float] enc:
        Sequence of ``(j0, j1, j1)`` where ``j0``, ``j1``, and ``j2`` refer to
        wrist joint angles (in [rad]) for axes 0, 1, and 2, respectively.

    :param Array[int, int] out:
        An output buffer to store the wrist encoder values.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_int]`` types.

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
    | :func:`forcedimension_core.dhd.dco_expert.wristJointAnglesToJacobian()`
    | :func:`forcedimension_core.dhd.dco_expert.wristEncodersToJointAngles()`
    """

    return _runtime._libdhd.dhdWristJointAnglesToEncoders(
        joint_angles[0],
        joint_angles[1],
        joint_angles[2],
        *out.ptrs,
        ID
    )


def getJointAngles(out: SupportsPtr[c_double], ID: int = -1) -> int:
    """
    Retrieve the joint angles (in [rad]) for all sensed degrees-of-freedom of
    the current device.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param SupportsPtr[c_double] out:
        An output buffer to store the joint angles (in [rad]) for all sensed
        degrees-of-freedom for the current device.

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of
        :data:`forcedimension_core.dhd.constants.MAX_DOF`
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.

    See Also
    ---------
    | :func:`forcedimension_core.dhd.dco_expert.getDeltaJointAngles()`
    | :func:`forcedimension_core.dhd.dco_expert.getWristJointAngles()`
    | :func:`forcedimension_core.dhd.dco_expert.deltaJointAnglesToEncoders()`
    | :func:`forcedimension_core.dhd.dco_expert.wristJointAnglesToEncoders()`
    | :func:`forcedimension_core.dhd.dco_expert.deltaJointTorquesExtrema()`
    | :func:`forcedimension_core.dhd.dco_expert.wristJointTorquesExtrema()`
    | :func:`forcedimension_core.dhd.dco_expert.deltaJointAnglesToJacobian()`
    | :func:`forcedimension_core.dhd.dco_expert.wristJointAnglesToJacobian()`
    | :func:`forcedimension_core.dhd.dco_expert.jointAnglesToIntertiaMatrix()`
    | :func:`forcedimension_core.dhd.dco_expert.jointAnglesToGravityJointTorques()`
    | :func:`forcedimension_core.dhd.dco_expert.getJointVelocities()`
    """

    return _runtime._libdhd.dhdGetJointAngles(out.ptr, ID)


def getJointVelocities(out: SupportsPtr[c_double], ID: int = -1) -> int:
    """
    Retrieve the joint angle velocities (in [rad/s]) for all sensed
    degrees-of-freedom of the current device.

    :param SupportsPtr[c_double] out:
        An output buffer to store the joint velocities (in [rad/s]) for all
        sensed degrees-of-freedom of the current device.

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of
        :data:`forcedimension_core.dhd.constants.MAX_DOF`
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.dco_expert.getJointAngles()`
    | :func:`forcedimension_core.dhd.dco_expert.getDeltaJacobian()`
    | :func:`forcedimension_core.dhd.dco_expert.getWristJacobian()`
    """

    return _runtime._libdhd.dhdGetJointVelocities(out.ptr, ID)


def getEncVelocities(out: SupportsPtr[c_double], ID: int = -1) -> int:
    """
    Retrieve the encoder angle velocities (in [inc/s]) for all sensed
    degrees-of-freedom of the current device.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param SupportsPtr[c_double] out:
        An output buffer to store the encoder velocities (in [inc/s]) for all
        sensed degrees-of-freedom of the current device.

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of
        :data:`forcedimension_core.dhd.constants.MAX_DOF`
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
       0 or :data:`forcedimension_core.dhd.constants.TIMEGUARD` on success,
       -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.dco_expert.getEnc()`
    """

    return _runtime._libdhd.dhdGetEncVelocities(out.ptr, ID)


def jointAnglesToIntertiaMatrix(
    joint_angles: SupportsPtr[c_double],
    out: SupportsPtr[c_double],
    ID: int = -1,
) -> int:
    """
    Retrieve the inertia matrix based on a given joint
    configuration. Please refer to your device user manual for more information
    on your device coordinate system.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param SupportsPtr[c_double] out:
        An array of joint angles (in [rad]) containing joint angles for all
        degrees of freedom.

    :param SupportsPtr[c_double] out:
        An output buffer for the 6x6 inertia matrix.

    :raises AttributeError:
        If ``joint_angles.ptrs`` is not a valid attribute of ``joint_angles``

    :raises TypeError:
        If ``joint_angles.ptrs`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``joint_angles.ptr`` is not of type ``Pointer[c_double]``.

    :raises AttributeError:
        If ``out.ptr`` is not a valid attribute of ``out``

    :raises ctypes.ArgumentError:
        If ``out.ptr`` is not a ``Pointer[c_double]`` type.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.dco_expert.getJointAngles()`
    """

    return _runtime._libdhd.dhdJointAnglesToInertiaMatrix(
        joint_angles.ptr, out.ptr, ID
    )


def jointAnglesToGravityJointTorques(
    joint_angles: SupportsPtr[c_double],
    out: SupportsPtr[c_double],
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

    :param SupportsPtr[c_double] out:
        Output buffer for the joint torques required to provide gravity
        compensation (in [Nm]).

    :raises AttributeError:
        If ``joint_angles.ptrs`` is not a valid attribute of ``joint_angles``

    :raises TypeError:
        If ``joint_angles.ptrs`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``joint_angles.ptr`` is not of type ``Pointer[c_double]``.

    :raises AttributeError:
        If ``out.ptr`` is not a valid attribute of ``out``

    :raises ctypes.ArgumentError:
        If ``out.ptr`` is not a ``Pointer[c_double]`` type.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C char.

    :returns:
        0 on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.dco_expert.getJointAngles()`
    """

    return _runtime._libdhd.dhdJointAnglesToGravityJointTorques(
        joint_angles.ptr,
        out.ptr,
        mask,
        ID
    )
