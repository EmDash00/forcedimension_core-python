from ctypes import c_double

import forcedimension_core.runtime as _runtime
from forcedimension_core.typing import (
    SupportsPtr, SupportsPtrs3
)


def getPosition(out: SupportsPtrs3[c_double], ID: int = -1) -> int:
    """
    Retrieve the position of the end-effector about the X, Y, and
    Z axes. Please refer to your device user manual for more
    information on your device coordinate system.

    :param SupportsPtrs3[ctypes.c_double] out:
        An output buffer to store the position of the end-effector
        (in [m]).

    :param int ID:
         Device ID (see :ref:`multiple_devices` section for
         details).

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
        0 or :data:`forcedimension_core.dhd.TIMEGUARD` on
        success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.direct.getPositionAndOrientationRad()`
    | :func:`forcedimension_core.dhd.direct.getPositionAndOrientationDeg()`
    | :func:`forcedimension_core.dhd.direct.getPositionAndOrientationFrame()`
    """

    return _runtime._libdhd.dhdGetPosition(*out.ptrs, ID)


def getForce(out: SupportsPtrs3[c_double], ID: int = -1) -> int:
    """
    Retrieve the force vector applied to the end-effector (in [N])
    about the X, Y, and Z axes Please refer to your device user
    manual for more information on your device coordinate system.

    :param SupportsPtrs3[ctypes.c_double] out:
        An output buffer to store the applied forces on the
        end-effector (in [N]).

    :param int ID:
         Device ID (see :ref:`multiple_devices` section for
         details).

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

    See Also
    --------
    | :func:`forcedimension_core.dhd.direct.setForce()`
    | :func:`forcedimension_core.dhd.direct.setForceAndTorque()`
    | :func:`forcedimension_core.dhd.direct.setForceAndTorqueAndGripperForce()`
    | :func:`forcedimension_core.dhd.direct.getForceAndTorque()`
    | :func:`forcedimension_core.dhd.direct.getForceAndTorqueAndGripperForce()`
    """

    return _runtime._libdhd.dhdGetForce(*out.ptrs, ID)


def getOrientationRad(
    out: SupportsPtrs3[c_double], ID: int = -1
) -> int:
    """
    For devices with a wrist structure, retrieve individual angle
    (in [rad]) of each joint, starting with the one located
    nearest to the wrist base plate.

    Note
    ----
    This feature only applies to devices with a wrist. See the
    :ref:`device_types` section for more details.


    Note
    ----
    :data:`forcedimension_core.constants.DeviceType.OMEGA6_RIGHT`
    and
    :data:`forcedimension_core.constants.DeviceType.OMEGA6_LEFT`
    have angles that are instead computed with respect to their
    internal reference frame, which is rotated π/4 radians around
    the Y axis. Please refer to your device user manual for more
    information on your device coordinate system.


    :param SupportsPtrs3[ctypes.c_double] out:
        An output buffer to store the joint angles (in [rad]).

    :param int ID:
         Device ID (see :ref:`multiple_devices` section for
         details).

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
        0 or :data:`forcedimension_core.constants.TIMEGUARD`
        on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.direct.getOrientationDeg()`
    | :func:`forcedimension_core.dhd.direct.getPositionAndOrientationRad()`
    | :func:`forcedimension_core.dhd.direct.getPositionAndOrientationDeg()`
    """

    return _runtime._libdhd.dhdGetOrientationRad(*out.ptrs, ID)


def getOrientationDeg(
    out: SupportsPtrs3[c_double], ID: int = -1
) -> int:
    """
    For devices with a wrist structure, retrieve individual angle
    (in [deg]) of each joint, starting with the one located
    nearest to the wrist base plate.

    Note
    ----
    This feature only applies to devices with a wrist. See
    the :ref:`device_types` section for more details.


    Note
    ----
    :data:`forcedimension_core.constants.DeviceType.OMEGA6_RIGHT`
    and
    :data:`forcedimension_core.constants.DeviceType.OMEGA6_LEFT`
    have angles that are instead computed with respect to their
    internal reference frame, which is rotated π/4 radians around
    the Y axis. Please refer to your device user manual for more
    information on your device coordinate system.


    :param SupportsPtrs3[ctypes.c_double] out:
        An output buffer to store the joint angles (in [deg]).

    :param int ID:
         Device ID (see :ref:`multiple_devices` section for
         details).

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
        0 or :data:`forcedimension_core.constants.TIMEGUARD`
        on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.direct.getOrientationRad()`
    | :func:`forcedimension_core.dhd.direct.getPositionAndOrientationRad()`
    | :func:`forcedimension_core.dhd.direct.getPositionAndOrientationDeg()`
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
    of each joint (in [rad]), starting with the one located nearest
    to the wrist base plate.

    Note
    ----
    This feature only applies to devices with a wrist. See
    the :ref:`device_types` section for more details.


    Note
    ----
    :data:`forcedimension_core.constants.DeviceType.OMEGA6_RIGHT`
    and
    :data:`forcedimension_core.constants.DeviceType.OMEGA6_LEFT`
    have angles that are instead computed with respect to their
    internal reference frame, which is rotated π/4 radians around
    the Y axis. Please refer to your device user manual for more
    information on your device coordinate system.


    :param int ID:
         Device ID (see :ref:`multiple_devices` section for
         details).

    :param SupportsPtrs3[ctypes.c_double] p_out:
        An output buffer to store the position (in [m]).

    :param SupportsPtrs3[ctypes.c_double] o_out:
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
        0 or :data:`forcedimension_core.constants.TIMEGUARD`
        on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.direct.getOrientationRad()`
    | :func:`forcedimension_core.dhd.direct.getOrientationDeeg()`
    | :func:`forcedimension_core.dhd.direct.getPositionAndOrientationDeg()`
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
    of each joint (in [deg]), starting with the one located nearest
    to the wrist base plate.


    Note
    ----
    This feature only applies to devices with a wrist. See
    the :ref:`device_types` section for more details.


    Note
    ----
    :data:`forcedimension_core.constants.DeviceType.OMEGA6_RIGHT`
    and
    :data:`forcedimension_core.constants.DeviceType.OMEGA6_LEFT`
    have angles that are instead computed with respect to their
    internal reference frame, which is rotated π/4 radians around
    the Y axis. Please refer to your device user manual for more
    information on your device coordinate system.


    :param int ID:
         Device ID (see :ref:`multiple_devices` section for
         details).

    :param SupportsPtrs3[ctypes.c_double] p_out:
        An output buffer to store the position (in [m]).

    :param SupportsPtrs3[ctypes.c_double] o_out:
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
        0 or :data:`forcedimension_core.constants.TIMEGUARD`
        on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.direct.getOrientationRad()`
    | :func:`forcedimension_core.dhd.direct.getOrientationDeg()`
    | :func:`forcedimension_core.dhd.direct.getPositionAndOrientationRad()`
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
    Retrieve the position (in [m]) and orientation matrix of the
    end-effector about the X, Y, and Z axes. Please refer to your
    device user manual for more information on your device
    coordinate system.

    Note
    ----
    This feature only applies to devices with a wrist. See the
    :ref:`device_types` section for more details.


    Note
    ----
    :data:`forcedimension_core.constants.DeviceType.OMEGA6_RIGHT`
    and
    :data:`forcedimension_core.constants.DeviceType.OMEGA6_LEFT`
    have angles that are instead computed with respect to their
    internal reference frame, which is rotated π/4 radians around
    the Y axis. Please refer to your device user manual for more
    information on your device coordinate system.


    :param int ID:
         Device ID (see :ref:`multiple_devices` section for
         details).

    :raises AttributeError:
        If ``p_out.ptrs`` is not a valid attribute of ``p_out``

    :raises TypeError:
        If ``p_out.ptrs`` is not iterable.

    :raises ctypes.ArgumentError:
        If ``p_out.ptrs`` does not expand into a tuple of 3
        ``Pointer[c_double]`` types.

    :raises AttributeError:
        If ``matrix_out.ptr`` is not a valid attribute of
        ``matrix_out``.

    :raises ctypes.ArgumentError:
        If ``p_out.ptr`` is not a ``Pointer[c_double]`` type.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :returns:
        0 or :data:`forcedimension_core.constants.TIMEGUARD`
        on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.direct.getOrientationRad()`
    | :func:`forcedimension_core.dhd.direct.getOrientationDeg()`
    | :func:`forcedimension_core.dhd.direct.getPositionAndOrientationRad()`
    | :func:`forcedimension_core.dhd.direct.getPositionAndOrientationDeg()`
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
    Retrieve the forces (in [N]) and torques (in [Nm]) applied to
    the device end-effector about the X, Y, and Z axes. Please
    refer to your device user manual for more information on your
    device coordinate system.

    :param int ID:
         Device ID (see :ref:`multiple_devices` section for
         details).

    :param SupportsPtrs3[ctypes.c_double] f_out:
        An output buffer to store the applied forces on the
        end-effector (in [N]).

    :param SupportsPtrs3[ctypes.c_double] t_out:
        An output buffer to store the applied torques on the
        end-effector (in [Nm]).

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

    See Also
    --------
    | :func:`forcedimension_core.dhd.direct.setForce()`
    | :func:`forcedimension_core.dhd.direct.setForceAndTorque()`
    | :func:`forcedimension_core.dhd.direct.setForceAndTorqueAndGripperForce()`
    | :func:`forcedimension_core.dhd.direct.getForce()`
    | :func:`forcedimension_core.dhd.direct.getForceAndTorque()`
    | :func:`forcedimension_core.dhd.direct.getForceAndTorqueAndGripperForce()`
    """

    return _runtime._libdhd.dhdGetForceAndTorque(*f_out.ptrs, *t_out.ptrs, ID)


def getOrientationFrame(out: SupportsPtr[c_double], ID: int = -1) -> int:
    """
    Retrieve the rotation matrix of the wrist structure. The
    identity matrix is returned for devices that do not support
    orientations.

    :param int ID:
         Device ID (see :ref:`multiple_devices` section for
         details).

    :param SupportsPtr[ctypes.c_double] out:
        An output buffer to store the orientation frame.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :raises AttributeError:
        If ``out.ptr`` is not a valid attribute of ``p_out``

    :raises ctypes.ArgumentError:
        If ``out.ptr`` is not a ``Pointer[c_double]`` type.

    :returns:
        0 or :data:`forcedimension_core.constants.TIMEGUARD`
        on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.direct.getPositionAndOrientationFrame()`
    """

    return _runtime._libdhd.dhdGetOrientationFrame(out.ptr, ID)


def getGripperThumbPos(
    out: SupportsPtrs3[c_double], ID: int = -1
) -> int:
    """
    Read the position (in [m]) of thumb rest location about the
    X, Y, and Z axes of the force gripper structure if present.

    Note
    ----
    This feature only applies to devices with a gripper. See
    the :ref:`device_types` section for more details.


    :param int ID:
         Device ID (see :ref:`multiple_devices` section for
         details).

    :param SupportsPtrs3[ctypes.c_double] out:
        An output buffer to store the grippper thumb position
        (in [m]).

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
        0 or :data:`forcedimension_core.constants.TIMEGUARD`
        on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.direct.getGripperFingerPos()`
    """

    return _runtime._libdhd.dhdGetGripperThumbPos(*out.ptrs, ID)


def getGripperFingerPos(
    out: SupportsPtrs3[c_double], ID: int = -1
) -> int:
    """
    Read the position (in [m]) of forefinger rest location about
    the X, Y, and Z axes of the force gripper structure if present.

    Note
    ----
    This feature only applies to devices with a gripper. See
    the :ref:`device_types` section for more details.


    :param int ID:
         Device ID (see :ref:`multiple_devices` section for
         details).

    :param SupportsPtrs3[ctypes.c_double] out:
        An output buffer to store the gripper finger position
        (in [m]).

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
        0 or :data:`forcedimension_core.constants.TIMEGUARD`
        on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.direct.getGripperFingerPos()`
    """

    return _runtime._libdhd.dhdGetGripperFingerPos(*out.ptrs, ID)


def getForceAndTorqueAndGripperForce(
    f_out: SupportsPtrs3[c_double],
    t_out: SupportsPtrs3[c_double],
    fg_out: c_double,
    ID: int = -1
) -> int:
    """
    Retrieve the forces (in [N]) and torques (in [Nm]) applied
    to the device end-effector as well as the gripper force (in
    [N]). Forces and torques are about the X, Y, and Z axes.

    :param int ID:
         Device ID (see :ref:`multiple_devices` section for
         details).

    :param SupportsPtrs3[ctypes.c_double] f_out:
        An output buffer to store the applied forces on the
        end-effector (in [N]).

    :param SupportsPtrs3[ctypes.c_double] t_out:
        An output buffer to store the applied torques on the
        end-effector (in [Nm]).

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

    See Also
    --------
    | :func:`forcedimension_core.dhd.direct.getForce()`
    | :func:`forcedimension_core.dhd.direct.getForceAndTorque()`
    """

    err = _runtime._libdhd.dhdGetForceAndTorqueAndGripperForce(
        *f_out.ptrs, *t_out.ptrs, fg_out, ID
    )
    return err


def getLinearVelocity(out: SupportsPtrs3[c_double], ID: int = -1) -> int:
    """
    Retrieve the estimated instanteous linear velocity (in [m/s]).

    Note
    ----
    The velocity estimator requires at least 2 position
    updates during the time interval defined in
    :func:`forcedimension_core.dhd.configLinearVelocity()` in
    order to be able to compute the estimate. Otherwise, if there
    are no calls to :func:`forcedimension_core.dhd.getPosition()`
    or :func:`forcedimension_core.dhd.getLinearVelocity()`, this
    function will error with
    :data:`forcedimension_core.constants.ErrorNum.TIMEOUT`.
    For more information refer to :ref:`velocity_estimator`.


    :param int ID:
         Device ID (see :ref:`multiple_devices` section for
         details).

    :param SupportsPtr[ctypes.c_double] out:
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

    See Also
    --------
    | :func:`forcedimension_core.dhd.direct.configLinearVelocity()`
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
    :func:`forcedimension_core.dhd.configAngularVelocity()` in
    order to be able to compute the estimate. Otherwise, if there
    are no
    calls to:func:`forcedimension_core.dhd.getPosition()` or
    :func:`forcedimension_core.dhd.getAngularVelocityRad()`,
    this function will return error with
    :data:`forcedimension_core.constants.ErrorNum.TIMEOUT`.
    For more information refer to :ref:`velocity_estimator`.


    :param int ID:
         Device ID (see :ref:`multiple_devices` section for
         details).

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

    See Also
    --------
    | :func:`forcedimension_core.dhd.direct.configAngularVelocity()`
    | :func:`forcedimension_core.dhd.direct.getAngularVelocityDeg()`
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
    :func:`forcedimension_core.dhd.configAngularVelocity()` in
    order to be able to compute the estimate. Otherwise, if there
    are no calls to:func:`forcedimension_core.dhd.getPosition()`
    or :func:`forcedimension_core.dhd.getAngularVelocityDeg()`,
    this function will error with
    :data:`forcedimension_core.constants.ErrorNum.TIMEOUT`.
    For more information refer to :ref:`velocity_estimator`.


    :param int ID:
         Device ID (see :ref:`multiple_devices` section for
         details).

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

    See Also
    --------
    | :func:`forcedimension_core.dhd.direct.configAngularVelocity()`
    | :func:`forcedimension_core.dhd.direct.getAngularVelocityRad()`
    """

    return _runtime._libdhd.dhdGetAngularVelocityDeg(*out.ptrs, ID)
