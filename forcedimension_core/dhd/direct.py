from ctypes import c_byte, c_double, c_int

import forcedimension_core.runtime as _runtime
from forcedimension_core.typing import (
    SupportsPtr, SupportsPtrs3, c_double_ptr
)


def getPosition(out: SupportsPtrs3[c_double], ID: int = -1) -> int:
    """
    Retrieve the position of the end-effector about the X, Y, and Z axes.
    Please refer to your device user manual for more information on your device
    coordinate system.

    See Also
    --------
    :func:`forcedimension_core.dhd.direct.getPositionAndOrientationRad()`
    :func:`forcedimension_core.dhd.direct.getPositionAndOrientationDeg()`
    :func:`forcedimension_core.dhd.direct.getPositionAndOrientationFrame()`


    :param SupportsPtrs3[c_double] out:
        An output buffer to store the position of the end-effector (in [m]).

    :param int ID:
         Device ID (see multiple devices section for details).

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 or :data:`forcedimension.dhd.TIMEGUARD` on success,
        -1 otherwise.
    """

    return _runtime._libdhd.dhdGetPosition(*out.ptrs, ID)


def getForce(out: SupportsPtrs3[c_double], ID: int = -1) -> int:
    """
    Retrieve the force vector applied to the end-effector (in [N])
    about the X, Y, and Z axes Please refer to your device user manual for more
    information on your device coordinate system.

    See Also
    --------
    :func:`forcedimension_core.dhd.direct.setForce()`
    :func:`forcedimension_core.dhd.direct.setForceAndTorque()`
    :func:`forcedimension_core.dhd.direct.setForceAndTorqueAndGripperForce()`
    :func:`forcedimension_core.dhd.direct.getForceAndTorque()`
    :func:`forcedimension_core.dhd.direct.getForceAndTorqueAndGripperForce()`


    :param SupportsPtrs3[c_double] out:
        An output buffer to store the applied forces on the end-effector
        (in [N]).

    :param int ID:
         Device ID (see multiple devices section for details).

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out`` does not support item assignment either
        because its immutable or not subscriptable.

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 on success, -1 otherwise.
    """

    return _runtime._libdhd.dhdGetForce(*out.ptrs, ID)


def getOrientationRad(
    out: SupportsPtrs3[c_double], ID: int = -1
) -> int:
    """
    For devices with a wrist structure, retrieve individual angle (in [rad])
    of each joint, starting with the one located nearest to the wrist base
    plate.

    Note
    ----
    This feature only applies to the following devices:

    :data:`forcedimension.dhd.constants.DeviceType.OMEGA6_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA6_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA7_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.SIGMA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.SIGMA7_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.LAMBDA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.LAMBDA7_LEFT`


    Note
    ----
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA6_RIGHT` and
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA6_LEFT`
    have angles that are instead computed with respect to their internal
    reference frame, which is rotated π/4 radians around the Y axis.
    Please refer to your device user manual for more information on your
    device coordinate system.


    See Also
    --------
    :func:`forcedimension_core.dhd.direct.getOrientationDeg()`
    :func:`forcedimension_core.dhd.direct.getPositionAndOrientationRad()`
    :func:`forcedimension_core.dhd.direct.getPositionAndOrientationDeg()`


    :param SupportsPtrs3[c_double] out:
        An output buffer to store the joint angles (in [rad]).

    :param int ID:
         Device ID (see multiple devices section for details).

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out`` does not support item assignment either
        because its immutable or not subscriptable.

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 or :data:`forcedimension.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.
    """

    return _runtime._libdhd.dhdGetOrientationRad(*out.ptrs, ID)


def getOrientationDeg(
    out: SupportsPtrs3[c_double], ID: int = -1
) -> int:
    """
    For devices with a wrist structure, retrieve individual angle (in [deg])
    of each joint, starting with the one located nearest to the wrist base
    plate.

    Note
    ----
    This feature only applies to the following devices:

    :data:`forcedimension.dhd.constants.DeviceType.OMEGA6_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA6_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA7_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.SIGMA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.SIGMA7_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.LAMBDA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.LAMBDA7_LEFT`


    Note
    ----
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA6_RIGHT` and
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA6_LEFT`
    have angles that are instead computed with respect to their internal
    reference frame, which is rotated π/4 radians around the Y axis.
    Please refer to your device user manual for more information on your
    device coordinate system.


    See Also
    --------
    :func:`forcedimension_core.dhd.direct.getOrientationRad()`
    :func:`forcedimension_core.dhd.direct.getPositionAndOrientationRad()`
    :func:`forcedimension_core.dhd.direct.getPositionAndOrientationDeg()`


    :param SupportsPtrs3[c_double] out:
        An output buffer to store the joint angles (in [deg]).

    :param int ID:
         Device ID (see multiple devices section for details).

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out`` does not support item assignment either
        because its immutable or not subscriptable.

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 or :data:`forcedimension.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.
    """

    return _runtime._libdhd.dhdGetOrientationDeg(*out.ptrs, ID)


def getPositionAndOrientationRad(
    p_out: SupportsPtrs3[c_double],
    o_out: SupportsPtrs3[c_double],
    ID: int = -1
) -> int:
    """
    Retrieve the position (in [m]) and
    for devices with a wrist structure, retrieve individual angle
    of each joint (in [rad]), starting with the one located nearest to the wrist
    base plate.

    Note
    ----
    This feature only applies to the following devices:

    :data:`forcedimension.dhd.constants.DeviceType.OMEGA6_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA6_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA7_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.SIGMA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.SIGMA7_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.LAMBDA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.LAMBDA7_LEFT`


    Note
    ----
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA6_RIGHT` and
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA6_LEFT`
    have angles that are instead computed with respect to their internal
    reference frame, which is rotated π/4 radians around the Y axis.
    Please refer to your device user manual for more information on your
    device coordinate system.


    See Also
    --------
    :func:`forcedimension_core.dhd.direct.getOrientationRad()`
    :func:`forcedimension_core.dhd.direct.getOrientationDeeg()`
    :func:`forcedimension_core.dhd.direct.getPositionAndOrientationDeg()`



    :param int ID:
         Device ID (see multiple devices section for details).

    :param SupportsPtrs3[c_double] p_out:
        An output buffer to store the position (in [m]).

    :param SupportsPtrs3[c_double] o_out:
        An output buffer to store the joint angles (in [rad]).

    :raises AttributeError:
        If ``p_out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``p_out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``p_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises AttributeError:
        If ``o_out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``o_out`` does not support item assignment either
        because its immutable or not subscriptable.

    :raises TypeError:
        If ``o_out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``o_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 or :data:`forcedimension.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.
    """

    return _runtime._libdhd.dhdGetPositionAndOrientationRad(
        *p_out.ptrs, *o_out.ptrs, ID
    )


def getPositionAndOrientationDeg(
    p_out: SupportsPtrs3[c_double],
    o_out: SupportsPtrs3[c_double],
    ID: int = -1
) -> int:
    """
    Retrieve the position (in [m]) and
    for devices with a wrist structure, retrieve individual angle
    of each joint (in [deg]), starting with the one located nearest to the wrist
    base plate.


    Note
    ----
    This feature only applies to the following devices:

    :data:`forcedimension.dhd.constants.DeviceType.OMEGA6_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA6_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA7_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.SIGMA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.SIGMA7_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.LAMBDA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.LAMBDA7_LEFT`


    Note
    ----
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA6_RIGHT` and
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA6_LEFT`
    have angles that are instead computed with respect to their internal
    reference frame, which is rotated π/4 radians around the Y axis.
    Please refer to your device user manual for more information on your
    device coordinate system.


    See Also
    --------
    :func:`forcedimension_core.dhd.direct.getOrientationRad()`
    :func:`forcedimension_core.dhd.direct.getOrientationDeg()`
    :func:`forcedimension_core.dhd.direct.getPositionAndOrientationRad()`


    :param int ID:
         Device ID (see multiple devices section for details).

    :param SupportsPtrs3[c_double] p_out:
        An output buffer to store the position (in [m]).

    :param SupportsPtrs3[c_double] o_out:
        An output buffer to store the joint angles (in [rad]).

    :raises AttributeError:
        If ``p_out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``p_out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``p_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises AttributeError:
        If ``o_out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``o_out`` does not support item assignment either
        because its immutable or not subscriptable.

    :raises TypeError:
        If ``o_out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``o_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 or :data:`forcedimension.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.
    """

    return _runtime._libdhd.dhdGetPositionAndOrientationDeg(
        *p_out.ptrs, *o_out.ptrs, ID
    )


def getPositionAndOrientationFrame(
    p_out: SupportsPtrs3[c_double],
    matrix_out: SupportsPtr[c_double],
    ID: int = -1
) -> int:
    """
    Retrieve the position (in [m]) and orientation matrix of the end-effector
    about the X, Y, and Z axes. Please refer to your device user manual for
    more information on your device coordinate system.

    Note
    ----
    This feature only applies to the following devices:

    :data:`forcedimension.dhd.constants.DeviceType.OMEGA6_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA6_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA7_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.SIGMA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.SIGMA7_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.LAMBDA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.LAMBDA7_LEFT`


    Note
    ----
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA6_RIGHT` and
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA6_LEFT`
    have angles that are instead computed with respect to their internal
    reference frame, which is rotated π/4 radians around the Y axis.
    Please refer to your device user manual for more information on your
    device coordinate system.


    See Also
    --------
    :func:`forcedimension_core.dhd.direct.getOrientationRad()`
    :func:`forcedimension_core.dhd.direct.getOrientationDeg()`
    :func:`forcedimension_core.dhd.direct.getPositionAndOrientationRad()`
    :func:`forcedimension_core.dhd.direct.getPositionAndOrientationDeg()`


    :param int ID:
         Device ID (see multiple devices section for details).

    :raises AttributeError:
        If ``p_out.ptrs`` is not a valid attribute of ``p_out``

    :raises TypeError:
        If ``p_out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``p_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises AttributeError:
        If ``matrix_out.ptr`` is not a valid attribute of ``matrix_out``

    :raises ctypes.ArgumentError:
        If ``p_out.ptr`` is not a ``Pointer[c_double]`` type.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 or :data:`forcedimension.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.
    """

    return _runtime._libdhd.dhdGetPositionAndOrientationFrame(
        *p_out.ptrs, matrix_out.ptr, ID
    )


def getForceAndTorque(
    f_out: SupportsPtrs3[c_double],
    t_out: SupportsPtrs3[c_double],
    ID: int = -1
) -> int:
    """
    Retrieve the forces (in [N]) and torques (in [Nm]) applied to the device
    end-effector about the X, Y, and Z axes. Please refer to your device user
    manual for more information on your device coordinate system.

    See Also
    --------
    :func:`forcedimension_core.dhd.direct.setForce()`
    :func:`forcedimension_core.dhd.direct.setForceAndTorque()`
    :func:`forcedimension_core.dhd.direct.setForceAndTorqueAndGripperForce()`
    :func:`forcedimension_core.dhd.direct.getForce()`
    :func:`forcedimension_core.dhd.direct.getForceAndTorque()`
    :func:`forcedimension_core.dhd.direct.getForceAndTorqueAndGripperForce()`


    :param int ID:
         Device ID (see multiple devices section for details).

    :param SupportsPtrs3[c_double] f_out:
        An output buffer to store the applied forces on the end-effector
        (in [N]).

    :param SupportsPtrs3[c_double] t_out:
        An output buffer to store the applied torques on the end-effector
        (in [Nm]).

    :raises AttributeError:
        If ``f_out.ptrs`` is not a valid attribute of ``f_out``

    :raises TypeError:
        If ``f_out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``f_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises AttributeError:
        If ``t_out.ptrs`` is not a valid attribute of ``t_out``

    :raises TypeError:
        If ``t_out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``t_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0, on success, -1 otherwise.
    """

    return _runtime._libdhd.dhdGetForceAndTorque(*f_out.ptrs, *t_out.ptrs, ID)


def getOrientationFrame(out: SupportsPtr[c_double], ID: int = -1) -> int:
    """
    Retrieve the rotation matrix of the wrist structure. The identity matrix
    is returned for devices that do not support orientations.

    See Also
    --------
    :func:`forcedimension_core.dhd.direct.getPositionAndOrientationFrame()`


    :param int ID:
         Device ID (see multiple devices section for details).

    :param SupportsPtr[c_double] out:
        An output buffer to store the orientation frame.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :raises AttributeError:
        If ``out.ptr`` is not a valid attribute of ``p_out``

    :raises ctypes.ArgumentError:
        If ``out.ptr`` is not a ``Pointer[c_double]`` type.

    :returns:
        0 or :data:`forcedimension.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.
    """

    return _runtime._libdhd.dhdGetOrientationFrame(out.ptr, ID)


def getGripperAngleDeg(out: c_double, ID: int = -1) -> int:
    """
    Get the gripper opening angle (in [deg]).

    Note
    ----
    This feature only applies to the following devices:

    :data:`forcedimension.dhd.constants.DeviceType.OMEGA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA7_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.SIGMA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.SIGMA7_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.LAMBDA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.LAMBDA7_LEFT`


    See Also
    --------
    :func:`forcedimension.dhd.direct.getGripperAngleRad()`
    :func:`forcedimension.dhd.direct.getGripperGap()`


    :param c_double out:
        Buffer to store the gripper opening angle (in [deg]).

    :param int ID:
         Device ID (see multiple devices section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 or :data:`forcedimension.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.
    """

    return _runtime._libdhd.dhdGetGripperAngleDeg(out, ID)


def getGripperAngleRad(out: c_double, ID: int = -1) -> int:
    """
    Get the gripper opening angle (in [rad]).

    Note
    ----
    This feature only applies to the following devices:

    :data:`forcedimension.dhd.constants.DeviceType.OMEGA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA7_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.SIGMA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.SIGMA7_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.LAMBDA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.LAMBDA7_LEFT`


    See Also
    --------
    :func:`forcedimension.dhd.direct.getGripperAngleRad()`
    :func:`forcedimension.dhd.direct.getGripperGap()`


    :param c_double out:
        Buffer to store the gripper opening angle (in [rad]).

    :param int ID:
         Device ID (see multiple devices section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 or :data:`forcedimension.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.
    """

    return _runtime._libdhd.dhdGetGripperAngleRad(out, ID)


def getGripperGap(out: c_double, ID: int = -1) -> int:
    """
    Get the gripper opening distance (in [m]).

    Note
    ----
    This feature only applies to the following devices:

    :data:`forcedimension.dhd.constants.DeviceType.OMEGA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA7_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.SIGMA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.SIGMA7_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.LAMBDA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.LAMBDA7_LEFT`


    See Also
    --------
    :func:`forcedimension.dhd.direct.getGripperAngleDeg()`
    :func:`forcedimension.dhd.direct.getGripperAngleRad()`


    :param c_double out:
        buffer to store the gripper opening distance (in [m]).

    :param int ID:
         Device ID (see multiple devices section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 or :data:`forcedimension.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.
    """

    return _runtime._libdhd.dhdGetGripperGap(out, ID)


def getGripperThumbPos(
    out: SupportsPtrs3[c_double], ID: int = -1
) -> int:
    """
    Read the position (in [m]) of thumb rest location about the X, Y, and Z
    axes of the force gripper structure if present.

    Note
    ----
    This feature only applies to the following devices:

    :data:`forcedimension.dhd.constants.DeviceType.OMEGA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA7_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.SIGMA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.SIGMA7_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.LAMBDA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.LAMBDA7_LEFT`


    See Also
    --------
    :func:`forcedimension_core.dhd.direct.getGripperFingerPos()`


    :param int ID:
         Device ID (see multiple devices section for details).

    :param SupportsPtrs3[c_double] out:
        An output buffer to store the grippper thumb position (in [m]).

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 or :data:`forcedimension.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.

    """

    return _runtime._libdhd.dhdGetGripperFingerPos(*out.ptrs, ID)


def getGripperFingerPos(
    out: SupportsPtrs3[c_double], ID: int = -1
) -> int:
    """
    Read the position (in [m]) of forefinger rest location about the X, Y, and
    Z axes of the force gripper structure if present.

    Note
    ----
    This feature only applies to the following devices:

    :data:`forcedimension.dhd.constants.DeviceType.OMEGA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.OMEGA7_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.SIGMA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.SIGMA7_LEFT`
    :data:`forcedimension.dhd.constants.DeviceType.LAMBDA7_RIGHT`
    :data:`forcedimension.dhd.constants.DeviceType.LAMBDA7_LEFT`


    See Also
    --------
    :func:`forcedimension_core.dhd.direct.getGripperFingerPos()`


    :param int ID:
         Device ID (see multiple devices section for details).

    :param SupportsPtrs3[c_double] out:
        An output buffer to store the gripper finger position (in [m]).

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 or :data:`forcedimension.dhd.constants.TIMEGUARD` on success,
        -1 otherwise.

    """

    return _runtime._libdhd.dhdGetGripperFingerPos(*out.ptrs, ID)


def getForceAndTorqueAndGripperForce(
    f_out: SupportsPtrs3[c_double],
    t_out: SupportsPtrs3[c_double],
    fg_out: c_double,
    ID: int = -1
) -> int:
    """
    Retrieve the forces (in [N]) and torques (in [Nm]) applied to the device
    end-effector as well as the gripper force (in [N]).
    Forces and torques are about the X, Y, and Z axes.

    See Also
    --------
    :func:`forcedimension_core.dhd.direct.getForce()`
    :func:`forcedimension_core.dhd.direct.getForceAndTorque()`


    :param int ID:
         Device ID (see multiple devices section for details).

    :param SupportsPtrs3[c_double] f_out:
        An output buffer to store the applied forces on the end-effector
        (in [N]).

    :param SupportsPtrs3[c_double] t_out:
        An output buffer to store the applied torques on the end-effector
        (in [Nm]).

    :raises AttributeError:
        If ``f_out.ptrs`` is not a valid attribute of ``f_out``

    :raises TypeError:
        If ``f_out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``f_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises AttributeError:
        If ``t_out.ptrs`` is not a valid attribute of ``t_out``

    :raises TypeError:
        If ``t_out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``t_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises AttributeError:
        If ``fg_out.ptr`` is not a valid attribute of ``fg_out``

    :raises ctypes.ArgumentError:
        If ``fg_out.ptr`` is not a ``Pointer[c_double]``.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
       0, on success, -1 otherwise.
    """

    err = _runtime._libdhd.dhdGetForceAndTorqueAndGripperForce(
        *f_out.ptrs, *t_out.ptrs, fg_out, ID
    )
    return err


def getLinearVelocity(out: SupportsPtrs3[c_double], ID: int = -1) -> int:
    """
    Retrieve the estimated instanteous linear velocity (in [m/s]).

    By default :data:`forcedimension.dhd.constants.VELOCITY_WINDOW` and
    :data:`forcedimension.dhd.constants.VELOCITY_WINDOWING`
    are used. See velocity estimator for details.

    Note
    ----
    The velocity estimator requires at least 2 position
    updates during the time interval defined in
    :func:`forcedimension_core.dhd.configLinearVelocity()` in order to be able to
    compute the estimate. Otherwise, if there are no calls to
    :func:`forcedimension_core.dhd.getPosition()
    or :func:`forcedimension_core.dhd.getLinearVelocity()`,
    this function will error with
    :data:`forcedimension_core.dhd.constants.ErrorNum.TIMEOUT`.
    For more information refer to :ref:`velocity_estimator`.


    See Also
    --------
    :func:`forcedimension_core.dhd.direct.configLinearVelocity()`


    :param int ID:
         Device ID (see multiple devices section for details).

    :param SupportsPtr[c_double] out:
        An output buffer to store the linear velocity (in [m/s]).

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

    :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.


   :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 on success, -1 otherwise.
    """

    return _runtime._libdhd.dhdGetLinearVelocity(*out.ptrs, ID)


def getAngularVelocityRad(
    out: SupportsPtrs3[c_double], ID: int = -1
) -> int:
    """
    Retrieve the estimated angular velocity (in [rad/s]).

    Note
    ----
    The velocity estimator requires at least 2 position
    updates during the time interval defined in
    :func:`forcedimension_core.dhd.configAngularVelocity()` in order to be able to
    compute the estimate. Otherwise, if there are no calls to
    :func:`forcedimension_core.dhd.getPosition() or
    :func:`forcedimension_core.dhd.getAngularVelocityRad()`, this function
    will return error with
    (:data:`forcedimension_core.dhd.constants.ErrorNum.TIMEOUT`).
    For more information refer to :ref:`velocity_estimator`.


    See Also
    --------
    :func:`forcedimension_core.dhd.direct.configAngularVelocity()`
    :func:`forcedimension_core.dhd.direct.getAngularVelocityDeg()`


    :param int ID:
         Device ID (see multiple devices section for details).

    :param out:
        An output buffer to store the angular velocity (in [rad/s]).

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

   :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.


    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 on success, -1 otherwise.
    """

    return _runtime._libdhd.dhdGetAngularVelocityRad(*out.ptrs, ID)


def getAngularVelocityDeg(
    out: SupportsPtrs3[c_double], ID: int = -1
) -> int:
    """
    Retrieve the estimated angular velocity (in [deg/s]).

    Note
    ----
    The velocity estimator requires at least 2 position
    updates during the time interval defined in
    :func:`forcedimension_core.dhd.configAngularVelocity()` in order to be able
    to compute the estimate. Otherwise, if there are no calls to
    :func:`forcedimension_core.dhd.getPosition()` or
    :func:`forcedimension_core.dhd.getAngularVelocityDeg()`,
    this function will error with
    :data:`forcedimension_core.dhd.constants.ErrorNum.TIMEOUT`.
    For more information refer to :ref:`velocity_estimator`.


    See Also
    --------
    :func:`forcedimension_core.dhd.direct.configAngularVelocity()`
    :func:`forcedimension_core.dhd.direct.getAngularVelocityRad()`



    :param int ID:
         Device ID (see multiple devices section for details).

    :param out:
        An output buffer to store the angular velocity (in [deg/s]).

    :raises AttributeError:
        If ``out.ptrs`` is not a valid attribute of ``out``

   :raises TypeError:
        If ``out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.


    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 on success, -1 otherwise.
    """

    return _runtime._libdhd.dhdGetAngularVelocityDeg(*out.ptrs, ID)


def getGripperLinearVelocity(out: c_double, ID: int = -1) -> int:
    """
    Retrieve the estimated linear velocity of the gripper (in [m/s]).

    Note
    ----
    The velocity estimator requires at least 2 position
    updates during the time interval defined in
    :func:`forcedimension_core.dhd.configGripperVelocity()` in order to be able
    to compute the estimate. Otherwise, if there are no calls to
    :func:`forcedimension_core.dhd.getGripperGap() or
    :func:`forcedimension_core.dhd.getGripperLinearVelocity()`, this function
    will error with data:`forcedimension_core.dhd.constants.ErrorNum.TIMEOUT`.
    For more information please refer to :ref:`velocity_estimator`

    See Also
    --------
    :data:`forcedimension_core.dhd.direct.configGripperVelocity()`


    :param c_double out:
        Output buffer to store the gripper linear velocity (in [m/s]).

    :param int ID:
         Device ID (see multiple devices section for details).

    :param SupportsPtr[c_double] out:
        An output buffer to store the gripper linear velocity (in [m/s]).

    :raises TypeError:
        If ``out`` does not support item assignment either
        because its immutable or not subscriptable.

    :raises IndexError:
        If ``len(out) < 3``.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 on success, -1 otherwise.
    """

    return _runtime._libdhd.dhdGetGripperLinearVelocity(out, ID)


def getGripperAngularVelocityRad(out: c_double, ID: int = -1) -> int:
    """
    Retrieve the estimated angular velocity of the gripper (in [rad/s]).

    Note
    ----
    The velocity estimator requires at least 2 position
    updates during the time interval defined in
    :func:`forcedimension_core.dhd.configGripperVelocity()` in order to be able
    to compute the estimate. Otherwise, e.g. if there are no calls to
    :func:`forcedimension_core.dhd.getGripperGap()` or
    :func:`forcedimension_core.dhd.getGripperAngularVelocityRad()`, this
    function will error with
    :data:`forcedimension_core.dhd.constants.ErrorNum.TIMEOUT`.
    For more information please refer to :ref:`velocity_estimator`


    See Also
    --------
    :func:`forcedimension_core.dhd.direct.configGripperVelocity()`
    :func:`forcedimension_core.dhd.direct.getGripperAngularVelocityDeg()`


    :param int ID:
         Device ID (see multiple devices section for details).

    :param c_double out:
        An output buffer to store the gripper angular velocity (in [rad/s])

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 on success, -1 otherwise.
    """

    return _runtime._libdhd.dhdGetGripperAngularVelocityRad(out, ID)


def getGripperAngularVelocityDeg(out: c_double, ID: int = -1) -> int:
    """
    Retrieve the estimated angular velocity of the gripper (in [rad/s]).
    Velocity computation can be figured by calling:

    Note
    ----
    The velocity estimator requires at least 2 position
    updates during the time interval defined in
    :func:`forcedimension_core.dhd.configGripperVelocity()` in order to be able
    to compute the estimate. Otherwise, e.g. if there are no calls to
    :func:`forcedimension_core.dhd.getGripperGap()` or
    :func:`forcedimension_core.dhd.getGripperAngularVelocityDeg()`, this
    funtion
    will error with :data:`forcedimension_core.dhd.constants.ErrorNum.TIMEOUT`.
    For more information refer to :ref:`velocity_estimator`


    See Also
    --------
    :func:`forcedimension_core.dhd.direct.configGripperVelocity()`
    :func:`forcedimension_core.dhd.direct.getGripperAngularVelocityDeg()`


    :param int ID:
         Device ID (see multiple devices section for details).

    :param c_double out:
        An output buffer to store the gripper angular velocity (in [deg/s]).

    :returns:
        0 on success, and -1 otherwise.
    """

    return _runtime._libdhd.dhdGetGripperAngularelocityDeg(out, ID)
