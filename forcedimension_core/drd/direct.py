from ctypes import c_byte, c_double, c_int

import forcedimension_core.runtime as _runtime
from forcedimension_core.typing import (
    SupportsPtr, SupportsPtrs3, c_int_ptr
)


def getPositionAndOrientation(
    p_out: SupportsPtrs3[c_double],
    o_out: SupportsPtrs3[c_double],
    pg_out: c_double,
    matrix_out: SupportsPtr[c_double],
    ID: int = -1,
) -> int:
    """
    Retrieve the position (in [m]) about the X, Y, and Z axes, the
    angle of each joint (in [rad]), (if applicable) the gripper position
    (in [m]), and orientation frame matrix of the end-effector. Please refer
    to your device user manual for more information on your device coordinate
    system.

    Note
    ----
    Unlike :func:`forcedimension_core.dhd.getPositionAndOrientation()`, this
    function returns immediately. It loads from an internal buffer that is
    refreshed by the robotic control loop. For more
    information about regulation see :ref:`regulation`.


    :param SupportsPtrs3[c_double] p_out:
        Output buffer to store the end-effector position (in [m]).

    :param SupportsPtrs3[c_double] o_out:
        Output buffer to store the angle of each joint (in [rad]).

    :param c_double pg_out:
        Output buffer to store the gripper opening gap (in [m]).

    :param MutableFloatMatrixLike matrix_out:
        Output buffer to store the orientation matrix.

    :param int ID:
        Device ID (see multiple devices section for details), defaults to -1.

    :raises AttributeError:
        If ``p_out.ptrs`` is not a valid attribute of ``p_out``

    :raises AttributeError:
        If ``o_out.ptrs`` is not a valid attribute of ``o_out``

    :raises AttributeError:
        If ``matrix_out.ptrs`` is not a valid attribute of ``matrix_out``

    :raises TypeError:
        If ``p_out.ptrs`` is not iterable.

    :raises TypeError:
        If ``o_out.ptrs`` is not iterable.

    :raises ArgumentError:
        If ``p_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ArgumentError:
        If ``o_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ArgumentError:
        If ``matrix_out.ptr`` is not a Pointer[c_double] type

    :raises ArgumentError:
        If ``pg_out`` is not a c_double type.

    :raises ArgumentError:
        If ``ID`` is not implicitly convertible to a C int.

    :returns:
        0 or :data:`forcedimension.dhd.libdhd.TIMEGUARD` on success,
        -1 otherwise.
    """

    return _runtime._libdrd.drdGetPositionAndOrientation(
        *p_out.ptrs, *o_out.ptrs, pg_out, matrix_out.ptr, ID
    )


def getVelocity(
    v_out: SupportsPtrs3[c_double],
    w_out: SupportsPtrs3[c_double],
    vg_out: c_double,
    ID: int = -1
) -> int:
    """
    Retrieve the linear velocity of the end-effector (in [m/s]k)
    as well as the angular velocity (in [rad/s]) about the X, Y, and Z
    axes. Please refer to your device user manual for more information on
    your device coordinate system.

    Note
    ----
    Unlike :func:`forcedimension_core.dhd.getLinearVelocity()`,
    :func:`forcedimension_core.dhd.getAngularVelocityRad()`, and
    :func:`forcedimension_core.dhd.getAngularVelocityDeg()` this
    function returns immediately. It loads from an internal buffer that is
    refreshed by the robotic control loop. For more
    information about regulation see :ref:`regulation`.


    :param int ID:
        Device ID (see multiple devices section for details), defaults to -1.

    :param SupportsPtrs3[c_double] v_out:
        Output buffer for the linear velocity (in [m/s]).

    :param SupportsPtrs3[c_double] w_out:
        Output buffer for the angular velocity (in [rad/s]).

    :param SupportsPtrs3[c_double] vg_out:
        Output buffer for the gripper linear velocity (in [m/s]).

    :raises AttributeError:
        If ``v_out.ptrs`` is not a valid attribute of ``v_out``

    :raises AttributeError:
        If ``w_out.ptrs`` is not a valid attribute of ``w_out``

    :raises TypeError:
        If ``p_out.ptrs`` is not iterable.

    :raises TypeError:
        If ``o_out.ptrs`` is not iterable.

    :raises ArgumentError:
        If ``p_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ArgumentError:
        If ``o_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ArgumentError:
        If ``pg_out`` is not a c_double type.

    :raises ArgumentError:
        If ``ID`` is not implicitly convertible to a C int.

    :returns:
        0 on success and -1 otherwise.
    """
    return _runtime._libdrd.drdGetVelocity(*v_out.ptrs, *w_out.ptrs, vg_out, ID)


def moveTo(pos: SupportsPtr[c_double], block: bool, ID: int = -1):
    """
    Send the robot end-effector to a desired Cartesian 7-DOF configuration.
    The motion uses smooth acceleration/deceleration. The acceleration and
    velocity profiles can be controlled by adjusting the trajectory generation
    parameters.

    Note
    ----
    The paths generated by this function are not guarunteed to be continuous if
    a command is interrupted by another call to this function while still in
    the process of being executed. If you want to guaruntee continuity use
    :func:`forcedimension_core.dhd.track()`. For more information see
    :ref:`regulation`.


    See Also
    --------
    :func:`forcedimension_core.drd.moveToAllEnc()`


    :param SupportsPtr[c_double] pos:
        Buffer of target positions/orientations for each DOF.
        DOFs 0-2 correspond to position about the X, Y, and Z axes (in [m]).
        DOFs 3-6 correspond to the target orientation about the first, second
        and third joints (in [rad]). DOF 7 corresponds to the gripper gap
        (in [m]).

    :param bool block:
        If ``True``, the call blocks until the destination is reached. If
        ``False``, the call returns immediately.

    :param int ID:
        Device ID (see multiple devices section for details), defaults to -1.

    :raises AttributeError:
        If ``pos.ptr`` is not a valid attribute of ``pos``

    :raises ArgumentError:
        If ``pos.ptr`` is not a ``Pointer[c_double]`` type.

    :raises ArgumentError:
        If ``ID`` is not convertible to a C char.'

    :returns:
        0 on success, and -1 otherwise.
    """

    return _runtime._libdrd.drdMoveTo(pos.ptr, block, ID)


def moveToAllEnc(enc: SupportsPtr[c_int], block: bool, ID: int = -1):
    """
    Send the robot end-effector to a desired encoder position. The motion
    follows a straight line in the encoder space, with smooth
    acceleration/deceleration. The acceleration and velocity profiles can be
    controlled by adjusting the trajectory generation parameters.

    Note
    ----
    The paths generated by this function are not guarunteed to be continuous if
    a command is interrupted by another call to this function while still in
    the process of being executed. If you want to guaruntee continuity use
    :func:`forcedimension_core.dhd.trackAllEnc()`.
    For more information see :ref:`regulation`.


    See Also
    --------
    :func:`forcedimension_core.drd.direct.moveTo()`


    :param SupportsPtr[c_int] enc:
        Target encoder positions.

    :param int ID:
        Device ID (see multiple devices section for details), defaults to -1.

    :param bool block:
        If ``True``, the call blocks until the destination is reached.
        If ``False``, the call returns immediately.

    :raises AttributeError:
        If ``enc.ptr`` is not a valid attribute of ``enc``

    :raises ValueError:
        If ``enc.ptr`` is not a ``Pointer[c_int]`` type.

    :raises ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 on success, and -1 otherwise.
    """
    return _runtime._libdrd.drdMoveToAllEnc(enc.ptr, block, ID)


def track(pos: SupportsPtr[c_double], ID: int = -1):
    """
    Send the robot end-effector to a desired Cartesian 7-DOF configuration.
    If motion filters are enabled, the motion follows a smooth
    acceleration/deceleration. The acceleration and velocity profiles can be
    controlled by adjusting the trajectory generation parameters.


    Note
    ----
    For more information see :ref:`regulation`.


    See Also
    --------
    :func:`forcedimension_core.drd.direct.trackAllEnc()`


    :param SupportsPtr[c_double] pos:
        Buffer of target positions/orientations for each DOF.
        DOFs 0-2 correspond to position about the X, Y, and Z axes (in [m]).
        DOFs 3-6 correspond to the target orientation about the first, second
        and third joints (in [rad]). DOF 7 corresponds to the gripper gap
        (in [m]).

    :param int ID:
        Device ID (see multiple devices section for details), defaults to -1.

    :raises AttributeError:
        If ``pos.ptr`` is not a valid attribute of ``pos``

    :raises ArgumentError:
        If ``pos.ptr`` is not a ``Pointer[c_double]`` type.

    :raises ArgumentError:
        If ``ID`` is not convertible to a C char.'

    :returns:
        0 on success, and -1 otherwise.
    """

    return _runtime._libdrd.drdTrack(pos.ptr, ID)


_runtime._libdrd.drdTrackAllEnc.argtypes = [c_int_ptr, c_byte]
_runtime._libdrd.drdTrackAllEnc.restype = c_int


def trackAllEnc(enc: SupportsPtr[c_int], ID: int = -1):
    """
    Send the robot end-effector to a desired encoder position. If motion
    filters are enabled, th emotion follows a smooth acceleration/deceleration
    constraint on each encoder axis. The acceleration and velocity profiles can
    be controlled by adjusting the trajectory generation parameters.

    Note
    ----
    For more information see :ref:`regulation`.


    See Also
    --------
    :func:`forcedimension_core.drd.direct.track()`


    :param SupportsPtr[c_int] enc:
        Target encoder positions.

    :param int ID:
        Device ID (see multiple devices section for details), defaults to -1.

    :raises AttributeError:
        If ``enc.ptr`` is not a valid attribute of ``enc``

    :raises ArgumentError:
        If ``enc.ptr`` is not a ``Pointer[c_int]`` type.

    :raises ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 on success, and -1 otherwise.
    """
    return _runtime._libdrd.drdTrackAllEnc(enc.ptr, ID)
