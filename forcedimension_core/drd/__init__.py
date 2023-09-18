import ctypes as ct
from ctypes import c_bool, c_byte, c_double, c_int, c_ubyte
from typing import Tuple

import forcedimension_core.runtime as _runtime

from forcedimension_core.dhd.constants import MAX_DOF
from forcedimension_core.drd.adaptors import (
    DEFAULT_ENC_MOVE_PARAMS,
    DEFAULT_ENC_TRACK_PARAMS,
    DEFAULT_POS_MOVE_PARAMS,
    DEFAULT_POS_TRACK_PARAMS,
    DEFAULT_ROT_MOVE_PARAMS,
    DEFAULT_ROT_TRACK_PARAMS,
    DEFAULT_GRIP_MOVE_PARAMS,
    DEFAULT_GRIP_TRACK_PARAMS,
    TrajectoryGenParams
)

from forcedimension_core.typing import Array, MutableArray

from forcedimension_core.typing import c_int_ptr, c_double_ptr
from . import direct

import forcedimension_core.runtime as runtime


_runtime._libdrd.drdOpen.argtypes = []
_runtime._libdrd.drdOpen.restype = c_int


def open() -> int:
    """
    Open a connection to the first available device connected to the
    system. The order in which devices are opened persists until devices
    are added or removed.

    If this call is successful, the default device ID is set to the newly
    opened device. See the multiple device section for more information on
    using multiple devices on the same computer.

    :returns: The device ID on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.dhd.openID()`
    | :func:`forcedimension_core.drd.close()`
    """

    return _runtime._libdrd.drdOpen()


_runtime._libdrd.drdOpenID.argtypes = [c_int]
_runtime._libdrd.drdOpenID.restype = c_int


def openID(ID: int) -> int:
    """
    Open a connection to one particular device connected to the system. The
    order in which devices are opened persists until devices are added or
    removed. If the device at the specified index is already opened, its device
    ID is returned.

    If this call is successful, the default device ID is set to the newly
    opened device. See the multiple device section for more information on
    using multiple devices on the same computer.

    :param int ID:
        The device enumeration index, as assigned by the underlying operating
        system (must be between 0 and the number of devices connected to the
        system)

    :raises ctypes.ArgumentError:
        index is not convertible to a C int.

    :returns: The device ID on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.drd.open()`
    | :func:`forcedimension_core.drd.close()`
    """

    return _runtime._libdrd.drdOpenID(ID)


_runtime._libdrd.drdSetDevice.argtypes = [c_byte]
_runtime._libdrd.drdSetDevice.restype = c_int


def setDevice(ID: int) -> int:
    """
    Select the default device that will receive the API commands. The API
    supports multiple devices. This routine allows the programmer to decide
    which device the API dhd_single_device_call single-device calls will
    address. Any subsequent API call that does not specifically mention the
    device ID in its parameter list will be sent to that device.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C int.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.drd.getDeviceID()`
    """

    return _runtime._libdrd.drdSetDevice(ID)


_runtime._libdrd.drdGetDeviceID.argtypes = []
_runtime._libdrd.drdGetDeviceID.restype = c_int


def getDeviceID() -> int:
    """
    Return the ID of the current default device.

    :returns:
        The device ID on success, -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.drd.setDevice()`
    """

    return _runtime._libdrd.drdGetDeviceID()


_runtime._libdrd.drdClose.argtypes = [c_byte]
_runtime._libdrd.drdClose.restype = c_int


def close(ID: int = -1) -> int:
    """
    Close the connection to a particular device.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C int.

    :returns:
        0 on success, and -1 otherwise.
    """
    return _runtime._libdrd.drdClose(ID)


_runtime._libdrd.drdIsSupported.argtypes = [c_byte]
_runtime._libdrd.drdIsSupported.restype = c_bool


def isSupported(ID: int) -> bool:
    """
    Determine if the device is supported out-of-the-box by the DRD. The
    regulation gains of supported devices are configured internally so that
    such devices are ready to use.

    Note
    ----
    Unsupported devices can still be operated
    with the DRD, but their regulation gains must first be configured using the
    :func:`forcedimension_core.drd.setEncPGain()`,
    :func:`forcedimension_core.drd.setEncIGain()`, and
    :func:`forcedimension_core.drd.setEncDGain()` functions.


    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C int.

    :returns: ``True`` if the device is supported, ``False`` otherwise.

    """
    return _runtime._libdrd.drdIsSupported(ID)


_runtime._libdrd.drdIsRunning.argtypes = [c_byte]
_runtime._libdrd.drdIsRunning.restype = c_bool


def isRunning(ID: int = -1) -> bool:
    """
    Checks the state of the robotic control thread for a particular device.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns: ``True`` if the control thread is running, ``False`` otherwise.
    """

    return _runtime._libdrd.drdIsRunning(ID)


_runtime._libdrd.drdIsMoving.argtypes = [c_byte]
_runtime._libdrd.drdIsMoving.restype = c_int


def isFiltering(ID: int = -1) -> bool:
    """
    Checks whether the particular robot control thread is applying a motion
    filter while tracking a target using
    :func:`forcedimension_core.drd.trackPos()` or
    :func:`forcedimension_core.drd.trackEnc()`.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns: ``True`` if the motion filter is enabled, ``False`` otherwise.

    See Also
    --------
    | :func:`forcedimension_core.drd.isMoving()`
    """

    return _runtime._libdrd.drdIsMoving(ID)


_runtime._libdrd.drdIsInitialized.argtypes = [c_byte]
_runtime._libdrd.drdIsInitialized.restype = c_bool


def isInitialized(ID: int = -1) -> bool:
    """
    Checks the initialization status of a particular robot. The initialization
    status reflects the status of the controller RESET LED.
    The robot can be (re)initialized by calling
    :func:`forcedimension_core.drd.autoInit()`.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns: ``True`` if the robot is initialized, ``False`` otherwise

    See Also
    --------
    | :func:`forcedimension_core.drd.checkInit()`.
    """

    return _runtime._libdrd.drdIsInitialized(ID)


_runtime._libdrd.drdIsMoving.argtypes = [c_byte]
_runtime._libdrd.drdIsMoving.restype = c_int


def isMoving(ID: int = -1) -> bool:
    """
    Checks whether the particular robot is moving (following a call to
    :func:`forcedimension_core.drd.moveToPos()`,
    :func:`forcedimension_core.drd.moveToEnc()`,
    :func:`forcedimension_core.drd.trackPos()` or
    :func:`forcedimension_core.drd.trackEnc()`),
    as opposed to holding the target position after successfully reaching it.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns: ``True`` if the robot is moving, ``False`` otherwise

    See Also
    --------
    | :func:`forcedimension_core.drd.isFiltering()`
    """

    return _runtime._libdrd.drdIsMoving(ID)


_runtime._libdrd.drdAutoInit.argtypes = [c_byte]
_runtime._libdrd.drdAutoInit.restype = c_int


def autoInit(ID: int = -1) -> int:
    """
    Performs automatic initialization of that particular robot by robotically
    moving to a known position and reseting encoder counters to their correct
    values.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.drd.precisionInit()`
    | :func:`forcedimension_core.drd.checkInit()`
    | :func:`forcedimension_core.drd.isInitialized()`
    """

    return _runtime._libdrd.drdAutoInit(ID)


_runtime._libdrd.drdCheckInit.argtypes = [c_byte]
_runtime._libdrd.drdCheckInit.restype = c_int


def checkInit(ID: int = -1) -> int:
    """
    Check the validity of that particular robot initialization by robotically
    sweeping all endstops and comparing their joint space position to expected
    values (stored in each device internal memory). If the robot is not yet
    initialized, this function will first perform the same initialization
    routine as :func:`forcedimension_core.drd.autoInit()` before running the endstop
    check.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.drd.autoInit()`.
    | :func:`forcedimension_core.drd.precisionInit()`
    | :func:`forcedimension_core.drd.isInitialized()`
    """

    return _runtime._libdrd.drdCheckInit(ID)


_runtime._libdrd.drdPrecisionInit.argtypes = [c_byte]
_runtime._libdrd.drdPrecisionInit.restype = c_int


def precisionInit(ID: int = -1) -> int:
    """
    This function performs automatic initialization of supported devices by
    robotically moving each axis to a known position and reseting its encoder
    counter to its correct values. This initialization is carried out for each
    device axis in turn, and validates the initialization by asserting the
    position of a validation reference for each axis.

    Note
    ----
    The execution of this implementation takes longer than
    :func:`forcedimension_core.drd.autoInit()`, but
    includes the same validation as
    :func:`forcedimension_core.drd.checkInit()`. As a result, calling
    :func:`forcedimension_core.drd.checkInit()` is not necessary if this
    function succeeds.

    :returns:
        0 on success, -1 otherwise

    See Also
    --------
    | :func:`forcedimension_core.drd.autoInit()`.
    | :func:`forcedimension_core.drd.precisionInit()`
    | :func:`forcedimension_core.drd.isInitialized()`
    """

    return _runtime._libdrd.drdPrecisionInit(ID)


_runtime._libdrd.drdGetVelocity.argtypes = [
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_byte
]
_runtime._libdrd.drdGetVelocity.restype = c_int


_runtime._libdrd.drdGetCtrlFreq.argtypes = [c_byte]
_runtime._libdrd.drdGetCtrlFreq.restype = c_double


def getCtrlFreq(ID: int = -1) -> float:
    """
    This function returns the average refresh rate of the control loop
    (in [kHz]) since the function was last called.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        The control frequency on success, and -1.0 otherwise.
    """

    return _runtime._libdrd.drdGetCtrlFreq(ID)


_runtime._libdrd.drdStart.argtypes = [c_byte]
_runtime._libdrd.drdStart.restype = c_int


def start(ID: int = -1) -> int:
    """
    Start the robotic control loop for the given robot.

    Note
    ----
    The robot must be initialized before this function can be called
    successfully.


    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.drd.autoInit()`
    | :func:`forcedimension_core.drd.precisionInit()`
    | :func:`forcedimension_core.drd.checkInit()`
    | :func:`forcedimension_core.drd.stop()`
    """

    return _runtime._libdrd.drdStart(ID)


_runtime._libdrd.drdRegulatePos.argtypes = [c_bool, c_byte]
_runtime._libdrd.drdRegulatePos.restype = c_int


def regulatePos(enable: bool, ID: int = -1) -> int:
    """
    Enable/disable robotic regulation of the device delta base, which provides
    translations. If regulation is disabled, the base can move freely and
    will display any force set using
    :func:`forcedimension_core.drd.setForceAndTorqueAndGripperForce()`.
    If it is enabled, base position is locked and can be controlled by calling
    all robotic functions (e.g. :func:`forcedimension_core.drd.moveToPos()`).

    Note
    ----
    By default, delta base regulation is enabled.


    :param bool enable:
        ``True`` to enable base regulation, ``False`` to disable it.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``val`` is not implicitly convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C int.

    :returns:
        0 on success, and -1 otherwise.
    """

    return _runtime._libdrd.drdRegulatePos(enable, ID)


_runtime._libdrd.drdRegulateRot.argtypes = [c_bool, c_byte]
_runtime._libdrd.drdRegulateRot.restype = c_int


def regulateRot(enable: bool, ID: int = -1) -> int:
    """
    Enable/disable robotic regulation of the device wrist. If regulation is
    disabled, the wrist can move freely and will display any torque set using
    :func:`forcedimension_core.drd.setForceAndTorqueAndGripperForce()`. If it
    is enabled, wrist orientation is locked and can be controlled by calling
    all robotic functions (e.g. :func:`forcedimension_core.drd.moveTo()`).

    Note
    ----
    By default, wrist regulation is enabled.


    :param bool enable:
        ``True`` to enable wrist regulation, ``False`` to disable it.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``val`` is not implicitly convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C int.

    :returns:
        0 on success, and -1 otherwise.
    """

    return _runtime._libdrd.drdRegulateRot(enable, ID)


_runtime._libdrd.drdRegulateGrip.argtypes = [c_bool, c_byte]
_runtime._libdrd.drdRegulateGrip.restype = c_int


def regulateGrip(enable: bool, ID: int = -1) -> int:
    """
    Enable/disable robotic regulation of the device gripper. If regulation is
    disabled, the gripper can move freely and will display any force set using
    :func:`forcedimension_core.drd.setForceAndTorqueAndGripperForce()`. If it is
    enabled, gripper orientation is locked and can be controlled by calling all
    robotic functions (e.g. :func:`forcedimension_core.drd.moveTo()`).

    Note
    ----
    By default, gripper regulation is enabled.


    :param bool enable:
        ``True`` to enable gripper regulation, ``False`` to disable it.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``val`` is not implicitly convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C int.

    :returns:
        0 on success, and -1 otherwise.
    """

    return _runtime._libdrd.drdRegulateGrip(enable, ID)


_runtime._libdrd.drdSetForceAndTorqueAndGripperForce.argtypes = [
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    c_byte
]
_runtime._libdrd.drdSetForceAndTorqueAndGripperForce.restype = c_int


def setForceAndTorqueAndGripperForce(
    f: Array[int, float],
    t: Array[int, float],
    fg: float,
    ID: int = -1
) -> int:
    """
    Set the desired force and torque vectors to be applied to the device
    end-effector and gripper.

    Note
    ----
    Unlike
    :func:`forcedimension_core.dhd.expert.setForceAndWristJointTorquesAndGripperForce()`
    this function returns immediately. The function sets an internal buffer
    for the robotic control loop to send out to the device. For more
    information about regulation see the :ref:`regulation` section.


    :param VectorLike f:
        Translational force vector ``(fx, fy, fz)`` where ``fx``, ``fy``, and
        ``fz`` are the translation force (in [N]) on the end-effector about the
        X, Y, and Z axes, respectively.

    :param VectorLike t:
        Torque vector ``(tx, ty, tz)`` where ``tx``, ``ty``, and ``tz``
        are the torque (in [Nm]) on the end-effector about the X, Y, and Z
        axes, respectively.

    :param float fg:
        Grasping force of the gripper (in [N]).

    :param int ID:
         Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to C char.

    :raises ctypes.ArgumentError:
        If any elements of ``f`` is not implicitly convertible to a C double.

    :raises IndexError:
        If ``len(f) < 3``.

    :raises TypeError:
        If ``f`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If any elements of ``t`` is not implicitly convertible to a C double.

    :raises IndexError:
        If ``len(t) < 3``.

    :raises TypeError:
        If ``t`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If ``gripper_force`` is not implicitly convertible to a C double.

    :raises IndexError:
        If ``len(f) < 3``.

    :raises IndexError:
        If ``len(t) < 3``.

    :returns:
        0 or
        :data:`forcedimension_core.dhd.constants.MOTOR_SATURATED` on success, and
        -1 otherwise.

    """

    return _runtime._libdrd.drdSetForceAndTorqueAndGripperForce(
        f[0],
        f[1],
        f[2],
        t[0],
        t[1],
        t[2],
        fg,
        ID
    )


_runtime._libdrd.drdSetForceAndWristJointTorquesAndGripperForce.argtypes = [
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    c_double,
    c_byte
]
_runtime._libdrd.drdSetForceAndWristJointTorquesAndGripperForce.restype = c_int


def setForceAndWristJointTorquesAndGripperForce(
        f: Array[int, float],
        t: Array[int, float],
        fg: float,
        ID: int = -1) -> int:
    """
    Set Cartesian force, wrist joint torques, and gripper force

    Note
    ----
    Unlike :func:`forcedimension_core.dhd.setForceAndTorqueAndGripperForce()`
    this function returns immediately. The function sets an internal buffer
    for the robotic control loop to send out to the device. For more
    information about regulation see the :ref:`regulation` section.


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
    """
    return _runtime._libdrd.drdSetForceAndWristJointTorquesAndGripperForce(
        f[0],
        f[1],
        f[2],
        t[0],
        t[1],
        t[2],
        fg,
        ID
    )


_runtime._libdrd.drdGetPositionAndOrientation.argtypes = [
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_byte
]
_runtime._libdrd.drdGetPositionAndOrientation.restype = c_int


def getPositionAndOrientation(
    p_out: MutableArray[int, float],
    o_out: MutableArray[int, float],
    matrix_out: MutableArray[int, MutableArray[int, float]],
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
    information about regulation see the :ref:`regulation` section.


    :param VectorLike p_out:
        Output buffer to store the end-effector position (in [m]).

    :param VectorLike o_out:
        Output buffer to store the angle of each joint (in [rad]).

    :param MutableFloatMatrixLike matrix_out:
        Output buffer to store the orientation matrix.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises TypeError:
        If ``p_out`` does not support item assignment either
        because its immutable or not subscriptable.

    :raises IndexError:
        If ``len(p_out) < 3``.

    :raises TypeError:
        If ``o_out`` does not support item assignment either
        because its immutable or not subscriptable.

    :raises IndexError:
        If ``len(o_out) < 3``.

    :raises TypeError:
        If ``matrix_out`` does not support item assignment,
        either because it is not subscriptable or because it is not mutable.

    :raises IndexError:
        If any dimension of ``matrix_out`` is less than length 3.

    :raises ValueError:
        If ``ID`` is not implicitly convertible to a C int.

    :returns:
        0 or :data:`forcedimension_core.dhd.libdhd.TIMEGUARD` on success,
        -1 otherwise.
    """

    px = c_double()
    py = c_double()
    pz = c_double()

    oa = c_double()
    ob = c_double()
    og = c_double()

    pg = c_double()

    matrix = ((c_double * 3) * 3)()

    err: int = _runtime._libdrd.drdGetPositionAndOrientation(
        px, py, pz,
        oa, ob, og,
        pg,
        ct.cast(matrix, c_double_ptr),
        ID
    )

    p_out[0] = px.value
    p_out[1] = py.value
    p_out[2] = pz.value

    o_out[0] = oa.value
    o_out[1] = ob.value
    o_out[2] = og.value

    for i in range(3):
        for j in range(3):
            matrix_out[i][j] = matrix[i][j]

    return err


_runtime._libdrd.drdGetVelocity.argtypes = [
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_double_ptr,
    c_byte
]
_runtime._libdrd.drdGetVelocity.restype = c_int


def getVelocity(
    v_out: MutableArray[int, float],
    w_out: MutableArray[int, float],
    vg_out: c_double,
    ID: int = -1
) -> int:
    """
    Retrieve the linear velocity of the end-effector (in [m/s])
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
    information about regulation see the :ref:`regulation` section.


    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param VectorLike v_out:
        Output buffer for the linear velocity (in [m/s]).

    :param VectorLike w_out:
        Output buffer for the angular velocity (in [rad/s]).

    :param VectorLike vg_out:
        Output buffer for the gripper linear velocity (in [m/s]).

    :raises TypeError:
        if ``v_out`` does not support item assignment either
        because its immutable or not support item assignment

    :raises IndexError: If ``len(v_out) < 3``.

    :raises TypeError:
        If w_out does not support item assignment either
        because its immutable or does not support item assignment

    :raises IndexError: If ``len(w_out) < 3``.

    :raises ValueError:
        If ``ID`` is not implicitly convertible to a C int.

    :returns:
        0 on success and -1 otherwise.
    """

    vx = c_double()
    vy = c_double()
    vz = c_double()

    wx = c_double()
    wy = c_double()
    wz = c_double()

    err = _runtime._libdrd.drdGetVelocity(vx, vy, vz, wx, wy, wz, vg_out, ID)

    v_out[0] = vx.value
    v_out[1] = vy.value
    v_out[2] = vz.value

    w_out[0] = wx.value
    w_out[1] = wy.value
    w_out[2] = wz.value

    return err

_runtime._libdrd.drdEnableFilter.argtypes = [c_bool, c_byte]
_runtime._libdrd.drdEnableFilter.restype = c_int


def enableFilter(enabled: bool, ID: int = -1) -> int:
    """
    Enable or disable motion filtering for subsequent calls to
    :func:`forcedimension_core.drd.trackPos()` and
    :func:`forcedimension_core.drd.trackEnc()`

    :param bool enabled:
        ``True`` to enable motion filtering, ``False`` to disable it.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``enabled`` is not implicitly convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``ID`` is not implicitly convertible to a C int.

    :returns:
        0 on success, and -1 otherwise.
    """
    return _runtime._libdrd.drdEnableFilter(enabled, ID)


_runtime._libdrd.drdMoveToPos.argtypes = [c_double, c_double, c_double, c_bool, c_byte]
_runtime._libdrd.drdMoveToPos.restype = c_int


def moveToPos(pos: Array[int, float], block: bool, ID: int = -1):
    """
    Send the robot end-effector to a desired Cartesian position. The motion
    follows a straight line, with smooth acceleration/deceleration. The
    acceleration and velocity profiles can be controlled by adjusting the
    trajectory generation parameters.

    Note
    ----
    the paths generated by this function are not guarunteed to be continuous if
    a command is interrupted by another call to this function while still in
    the process of being executed. if you want to guaruntee continuity use
    :func:`forcedimension_core.dhd.trackPos()`. For more information see
    :ref:`regulation`.


    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param bool block:
        If ``True``, the call blocks until the destination is reached. If
        ``False``, the call returns immediately.

    :param Array[int, float] pos:
        A vector of ``[px, py, pz]`` where ``px``, ``py``, and ``pz``` are the
        position (in [m]) about the X, Y, and Z axes, respectively.

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.


    See Also
    --------
    | :func:`forcedimension_core.drd.moveTo()`
    """

    return _runtime._libdrd.drdMoveToPos(pos[0], pos[1], pos[2], block, ID)


_runtime._libdrd.drdMoveToRot.argtypes = [c_double, c_double, c_double, c_bool, c_byte]
_runtime._libdrd.drdMoveToRot.restype = c_int


def moveToRot(orientation: Array[int, float], block: bool, ID: int = -1):
    """
    Send the robot end-effector to a desired Cartesian rotation. The motion
    follows a straight curve, with smooth acceleration/deceleration. The
    acceleration and velocity profiles can be controlled by adjusting the
    trajectory generation parameters.

    Note
    ----
    the paths generated by this function are not guarunteed to be continuous if
    a command is interrupted by another call to this function while still in
    the process of being executed. if you want to guaruntee continuity use
    :func:`forcedimension_core.dhd.trackRot()`


    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param bool block:
        If ``True``, the call blocks until the destination is reached. If
        ``False``, the call returns immediately.

    :param Array[int, float] orientation:
        A vector of ``[oa, ob, og]`` where ``oa``, ``ob``, and ``og`` are the
        device orientation (in [rad])  around the first, second, and third
        joints, respectively.

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.


    See Also
    --------
    | :func:`forcedimension_core.drd.moveTo()`
    """

    return _runtime._libdrd.drdMoveToRot(
        orientation[0], orientation[1], orientation[2], block, ID
    )


_runtime._libdrd.drdMoveToGrip.argtypes = [c_double, c_bool, c_byte]
_runtime._libdrd.drdMoveToGrip.restype = c_int


def moveToGrip(pg: float, block: bool, ID: int = -1):
    """
    Send the robot gripper to a desired opening distance. The motion is
    executed with smooth acceleration/deceleration. The acceleration and
    velocity profiles can be controlled by adjusting the trajectory
    generation parameters.

    Note
    ----
    the paths generated by this function are not guarunteed to be continuous if
    a command is interrupted by another call to this function while still in
    the process of being executed. if you want to guaruntee continuity use
    :func:`forcedimension_core.dhd.trackGrip()`. For more information see
    :ref:`regulation`.


    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param bool block:
        If ``True``, the call blocks until the destination is reached. If
        ``False``, the call returns immediately.

    :param float pg:
        Target gripper opening distance (in [m]).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.drd.moveTo()`
    """

    return _runtime._libdrd.drdMoveToGrip(pg, block, ID)


_runtime._libdrd.drdMoveTo.argtypes = [c_double_ptr, c_bool, c_byte]
_runtime._libdrd.drdMoveTo.restype = c_int


def moveTo(pos: Array[int, float], block: bool, ID: int = -1):
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


    :param float pos:
        Buffer of target positions/orientations for each DOF.
        DOFs 0-2 correspond to position about the X, Y, and Z axes (in [m]).
        DOFs 3-6 correspond to the target orientation about the first, second
        and third joints (in [rad]). DOF 7 corresponds to the gripper gap
        (in [m]).

    :param bool block:
        If ``True``, the call blocks until the destination is reached. If
        ``False``, the call returns immediately.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ValueError:
        If any member of ``p`` is not convertible to a C double.

    :raises IndexError:
        If ``len(p) < MAX_DOF``.

    :raises TypeError:
        If ``p`` is not subscriptable.

    :raises ValueError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.drd.moveToAllEnc()`
    """

    pos_arr = (c_double * 8)(
            pos[0],
            pos[1],
            pos[2],
            pos[3],
            pos[4],
            pos[5],
            pos[6],
            pos[7],
        )

    return _runtime._libdrd.drdMoveTo(
        ct.cast(pos_arr, c_double_ptr),
        block,
        ID
    )


_runtime._libdrd.drdMoveToEnc.argtypes = [c_int, c_int, c_int, c_bool, c_byte]
_runtime._libdrd.drdMoveToEnc.restype = c_int


def moveToEnc(enc: Array[int, int], block: bool, ID: int = -1) -> int:
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
    :func:`forcedimension_core.dhd.trackEnc()`. For more information see
    :ref:`regulation`.


    :param int enc:
        A vector of ``(enc0, enc1, enc2)`` where ``enc0``, ``enc1``, and
        ``enc2`` are the target encoder position on axis 0, 1, and 2.

    :param bool block:
        If ``True``, the call blocks until the destination is reached. If
        ``False``, the call returns immediately.

    :raises ctypes.ArgumentError:
        If any member of ``enc`` is not convertible to a C int.

    :raises IndexError:
        If ``len(enc) < 3``.

    :raises TypeError:
        If ``enc`` is not subscriptable.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If any of elements of enc are not implicitly convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.


    See Also
    --------
    | :func:`forcedimension_core.drd.moveToAllEnc()`
    | :func:`forcedimension_core.drd.moveTo()`
    """

    return _runtime._libdrd.drdMoveToEnc(enc[0], enc[1], enc[2], block, ID)


_runtime._libdrd.drdMoveToAllEnc.argtypes = [c_int_ptr, c_bool, c_byte]
_runtime._libdrd.drdMoveToAllEnc.restype = c_int


def moveToAllEnc(enc: Array[int, int], block: bool, ID: int = -1):
    """
    Send the robot end-effector to a desired encoder position. The motion
    follows a straight line in the encoder space, with smooth
    acceleration/deceleration. The acceleration and velocity profiles can be
    controlled by adjusting the trajectory generation parameters.

    :param int enc:
        Target encoder positions.

    :raises ValueError:
        If any member of ``enc`` is not convertible to a C int.

    :raises IndexError:
        If ``len(enc) < MAX_DOF``.

    :raises TypeError:
        If ``enc`` is not subscriptable.

    :param bool block:
        If ``True``, the call blocks until the destination is reached.
        If ``False``, the call returns immediately.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ValueError:
        If any of elements of enc are not implicitly convertible to a C int.

    :raises ValueError:
        If ID is not convertible to a C int.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.drd.moveToEnc()`
    | :func:`forcedimension_core.drd.moveTo()`
    """

    enc_arr = (c_int * MAX_DOF)(
            enc[0],
            enc[1],
            enc[2],
            enc[3],
            enc[4],
            enc[5],
            enc[6],
            enc[7]
        )

    return _runtime._libdrd.drdMoveToAllEnc(
        ct.cast(enc_arr, c_int_ptr),
        block,
        ID
    )

_runtime._libdrd.drdHold.argtypes = [c_byte]
_runtime._libdrd.drdHold.restype = c_int


def hold(ID: int = -1) -> int:
    """
    Immediately make the robot hold its current position. All motion commands
    are abandoned.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.drd.lock()`
    """

    return _runtime._libdrd.drdHold(ID)


_runtime._libdrd.drdLock.argtypes = [c_ubyte, c_bool, c_byte]
_runtime._libdrd.drdLock.restype = c_int


def lock(mask: int, init: bool, ID: int = -1) -> int:
    """
    Depending on the value of the mask parameter, either:

    - Move the device to its park position and engage the locks, or
    - Removes the locks

    Upon success, the robotic regulation is running when the function returns.

    Note
    ----
    If the device has just been parked, it is recommended to call
    :func:`forcedimension_core.drd.stop()` to disable regulation.


    This function only applies to devices equipped with mechanical locks, and
    will return an error when called on other devices.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``mask`` is not convertible to a C unsigned char.

    :raises ctypes.ArgumentError:
        If ``init`` is not convertible to a C unsigned char.

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.


    See Also
    --------
    | :func:`forcedimension_core.drd.hold()`
    """

    return _runtime._libdrd.drdLock(mask, init, ID)


_runtime._libdrd.drdStop.argtypes = [c_byte]
_runtime._libdrd.drdStop.restype = c_int


def stop(ID: int = -1) -> int:
    """
    Stop the robotic control loop for the given robot.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.drd.start()`
    """

    return _runtime._libdrd.drdStop(ID)


_runtime._libdrd.drdGetPriorities.argtypes = [c_byte]
_runtime._libdrd.drdGetPriorities.restype = c_int


def getPriorities(ID: int = -1) -> Tuple[int, int, int]:
    """
    This function makes it possible to retrieve the priority of the control
    thread and the calling thread. Thread priority is system dependent, as
    described in thread priorities.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.drd.setPriorities()`
    """

    prio = c_int()
    ctrlprio = c_int()

    err: int = _runtime._libdrd.drdGetPriorities(prio, ctrlprio, ID)

    return (prio.value, ctrlprio.value, err)


_runtime._libdrd.drdSetPriorities.argtypes = [c_int, c_int, c_byte]
_runtime._libdrd.drdSetPriorities.restype = c_int


def setPriorities(prio: int, ctrlprio: int, ID: int = -1) -> int:
    """
    This function makes it possible to adjust the priority of the control
    thread and the calling thread. Thread priority is system dependent, as
    described in thread priorities.

    Note
    ----
    Administrator/superuser access is required on many
    platforms in order to increase thread priority. The first argument,
    ``prio`` is always applied to the calling thread, even when the call
    returns an error.

    :param int prio:
        Calling thread priority level (value is system dependent)

    :param int ctrlprio: Control thread priority level
        (value is system dependent)

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``prio`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``ctrlprio`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.


    See Also
    --------
    | :func:`forcedimension_core.drd.setPriorities()`
    """

    return _runtime._libdrd.drdSetPriorities(prio, ctrlprio, ID)


_runtime._libdrd.drdSetEncPGain.argtypes = [c_double, c_byte]
_runtime._libdrd.drdSetEncPGain.restype = c_int


def getEncPGain(gain: float, ID: int = -1) -> int:
    """
    Set the P term of the PID controller that regulates the base joint
    positions. In practice, this affects the stiffness of the regulation.

    :param float gain: P parameter of the PID regulator
    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``gain`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.setEncPGain()`
    """

    return _runtime._libdrd.drdSetEncPGain(gain, ID)


_runtime._libdrd.drdGetEncPGain.argtypes = [c_byte]
_runtime._libdrd.drdGetEncPGain.restype = c_double


def setEncPGain(ID: int = -1) -> int:
    """
    Retrieve the P term of the PID controller that regulates the base joint
    positions.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        The P term of the PID controller that regulates the base joint
        positions.

    See Also
    --------
    | :func:`forcedimension_core.getEncPGain()`
    """

    return _runtime._libdrd.drdGetEncPGain(ID)


_runtime._libdrd.drdSetEncIGain.argtypes = [c_double, c_byte]
_runtime._libdrd.drdSetEncIGain.restype = c_int


def setEncIGain(gain: float, ID: int = -1) -> int:
    """
    Set the I term of the PID controller that regulates the base joint
    positions. In practice, this affects the precision of the regulation.

    :param float gain:
        I parameter of the PID regulator.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``gain`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.getEncIGain()`
    """

    return _runtime._libdrd.drdSetEncIGain(gain, ID)


_runtime._libdrd.drdGetEncIGain.argtypes = [c_byte]
_runtime._libdrd.drdGetEncIGain.restype = c_double


def getEncIGain(ID: int = -1) -> int:
    """
    Retrieve the P term of the PID controller that regulates the base joint
    positions.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        The I term of the PID controller that regulates the base joint
        positions.

    See Also
    --------
    | :func:`forcedimension_core.setEncIGain()`
    """

    return _runtime._libdrd.drdGetEncIGain(ID)


_runtime._libdrd.drdSetEncDGain.argtypes = [c_double, c_byte]
_runtime._libdrd.drdSetEncDGain.restype = c_int


def setEncDGain(gain: float, ID: int = -1) -> int:
    """
    Set the D term of the PID controller that regulates the base joint
    positions. In practice, this affects the velocity of the regulation.

    :param float gain:
        D parameter of the PID regulator.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``gain`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.getEncDGain()`
    """

    return _runtime._libdrd.drdSetEncDGain(gain, ID)


_runtime._libdrd.drdGetEncDGain.argtypes = [c_int]
_runtime._libdrd.drdGetEncDGain.restype = c_double


def getEncDGain(ID: int = -1) -> int:
    """
    Retrieve the D term of the PID controller that regulates the base joint
    positions.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        The D term of the PID controller that regulates the base joint
        positions.

    See Also
    --------
    | :func:`forcedimension_core.setEncDGain()`
    """

    return _runtime._libdrd.drdGetEncDGain(ID)

_runtime._libdrd.drdTrackPos.argtypes = [c_double, c_double, c_double, c_byte]
_runtime._libdrd.drdTrackPos.restype = c_int


def trackPos(pos: Array[int, float], ID: int = -1):
    """
    Send the robot end-effector to a desired Cartesian position. If
    motion filters are enabled, the motion follows a smooth
    acceleration/deceleration constraint on each Cartesian axis.
    The acceleration and velocity profiles can be controlled by adjusting the
    trajectory generation parameters.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param Array[int, float] pos:
        A vector of ``[px, py, pz]`` where ``px``, ``py``, and ``pz``` are the
        position (in [m]) about the X, Y, and Z axes, respectively.

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.
    """
    return _runtime._libdrd.drdTrackPos(pos[0], pos[1], pos[2], ID)


_runtime._libdrd.drdTrackRot.argtypes = [c_double, c_double, c_double, c_byte]
_runtime._libdrd.drdTrackRot.restype = c_int


def trackRot(orientation: Array[int, float], ID: int = -1):
    """
    Send the robot end-effector to a desired Cartesian rotation. If motion
    filters are enabled, the motion follows a smooth acceleration/deceleration
    curve along each Cartesian axis. The acceleration and velocity profiles
    can be controlled by adjusting the trajectory generation parameters.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param Array[int, float] orientation:
        A vector of ``[oa, ob, og]`` where ``oa``, ``ob``, and ``og`` are the
        device orientation (in [rad])  around the first, second, and third
        joints, respectively.

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.

    """
    return _runtime._libdrd.drdTrackRot(
        orientation[0], orientation[1], orientation[2], ID
    )


_runtime._libdrd.drdTrackGrip.argtypes = [c_double, c_byte]
_runtime._libdrd.drdTrackGrip.restype = c_int


def trackGrip(pg: float, ID: int = -1):
    """
    Send the robot gripper to a desired opening distance. If motion filters
    are enabled, the motion follows a smooth acceleration/deceleration. The
    acceleration and velocity profiles can be controlled by adjusting the
    trajectory generation parameters.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :param float pg:
        Target gripper opening distance (in [m]).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.

    """
    return _runtime._libdrd.drdTrackGrip(pg, ID)


_runtime._libdrd.drdTrack.argtypes = [c_double_ptr, c_byte]
_runtime._libdrd.drdTrack.restype = c_int


def track(pos: Array[int, float], ID: int = -1):
    """
    Send the robot end-effector to a desired Cartesian 7-DOF configuration.
    If motion filters are enabled, the motion follows a smooth
    acceleration/deceleration. The acceleration and velocity profiles can be
    controlled by adjusting the trajectory generation parameters.

    Note
    ----
    For more information see the :ref:`regulation` section.


    :param float pos:
        Buffer of target positions/orientations for each DOF.
        DOFs 0-2 correspond to position about the X, Y, and Z axes (in [m]).
        DOFs 3-6 correspond to the target orientation about the first, second
        and third joints (in [rad]). DOF 7 corresponds to the gripper gap
        (in [m]).

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ValueError:
        If any member of ``p`` is not convertible to a C double.

    :raises IndexError:
        If ``len(p) < MAX_DOF``.

    :raises TypeError:
        If ``p`` is not subscriptable.

    :raises ValueError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.drd.trackAllEnc()`
    """

    pos_arr = (c_double * 8)(
            pos[0],
            pos[1],
            pos[2],
            pos[3],
            pos[4],
            pos[5],
            pos[6],
            pos[7],
        )

    return _runtime._libdrd.drdTrack(ct.cast(pos_arr, c_double_ptr), ID)


_runtime._libdrd.drdTrackEnc.argtypes = [c_int, c_int, c_int, c_byte]
_runtime._libdrd.drdTrackEnc.restype = c_int


def trackEnc(enc: Array[int, int], ID: int = -1) -> int:
    """
    Send the robot end-effector to a desired encoder position. If motion
    filters are enabled, the motion follows a smooth acceleration/deceleration
    constraint on each encoder axis. The acceleration and velocity profiles can
    be controlled by adjusting the trajectory generation parameters.

    Note
    ----
    For more information see the :ref:`regulation` section.


    :param int enc:
        A vector of ``(enc0, enc1, enc2)`` where ``enc0``, ``enc1``, and
        ``enc2`` are the target encoder position on axis 0, 1, and 2.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If any member of ``enc`` is not convertible to a C int.

    :raises IndexError:
        If ``len(enc) < 3``.

    :raises TypeError:
        If ``enc`` is not subscriptable.

    :raises ctypes.ArgumentError:
        If any of elements of enc are not implicitly convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.drd.trackAllEnc()`
    | :func:`forcedimension_core.drd.track()`
    """

    return _runtime._libdrd.drdTrackEnc(enc[0], enc[1], enc[2], ID)


_runtime._libdrd.drdTrackAllEnc.argtypes = [c_int_ptr, c_byte]
_runtime._libdrd.drdTrackAllEnc.restype = c_int


def trackAllEnc(enc: Array[int, int], ID: int = -1):
    """
    Send the robot end-effector to a desired encoder position. If motion
    filters are enabled, th emotion follows a smooth acceleration/deceleration
    constraint on each encoder axis. The acceleration and velocity profiles can
    be controlled by adjusting the trajectory generation parameters.

    Note
    ----
    For more information see the :ref:`regulation` section.


    :param int enc:
        Target encoder positions.

    :raises ValueError:
        If any member of ``enc`` is not convertible to a C int.

    :raises IndexError:
        If ``len(enc) < MAX_DOF``.

    :raises TypeError:
        If ``enc`` is not subscriptable.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ValueError:
        If any of elements of enc are not implicitly convertible to a C int.

    :raises ValueError:
        If ID is not convertible to a C int.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.drd.trackAllEnc()`
    | :func:`forcedimension_core.drd.track()`
    """

    enc_arr = (c_int * MAX_DOF)(
            enc[0],
            enc[1],
            enc[2],
            enc[3],
            enc[4],
            enc[5],
            enc[6],
            enc[7]
        )

    return _runtime._libdrd.drdTrackAllEnc(ct.cast(enc_arr, c_int_ptr), ID)

_runtime._libdrd.drdSetMotRatioMax.argtypes = [c_double, c_byte]
_runtime._libdrd.drdSetMotRatioMax.restype = c_int


def setMotRatioMax(scale: float, ID: int = -1) -> int:
    """
    Set the maximum joint torque applied to all regulated joints expressed as
    a fraction of the maximum torque available for each joint.

    In practice, this limits the maximum regulation torque (in joint space),
    making it potentially safer to operate in environments where humans or
    delicate obstacles are present.

    :param float scale:
        The joint torque scaling factor (must be between ``0.0`` and ``1.0``).

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``scale`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.getMotRatioMax()`
    """

    return _runtime._libdrd.drdSetMotRatioMax(scale, ID)


_runtime._libdrd.drdGetMotRatioMax.argtypes = [c_byte]
_runtime._libdrd.drdGetMotRatioMax.restype = c_double


def getMotRatioMax(ID: int = -1) -> float:
    """
    Retrieve the maximum joint torque applied to all regulated joints expressed
    as a fraction of the maximum torque available for each joint.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        The maximum joint torque ratio (between ``0.0`` and ``1.0``)

    See Also
    --------
    | :func:`forcedimension_core.setMotRatioMax()`
    """

    return _runtime._libdrd.drdGetMotRatioMax(ID)


_runtime._libdrd.drdSetEncMoveParam.argtypes = [
    c_double, c_double, c_double, c_byte
]
_runtime._libdrd.drdSetEncMoveParam.restype = c_int


def setEncMoveParam(
    vmax: float, amax: float, jerk: float, ID: int = -1
) -> int:
    """
    Sets the encoder positioning trajectory generation parameters.

    :param float vmax:
        max velocity (in [m/s])

    :param float amax:
        max acceleration (in [m/s^2])

    :param float jerk:
        jerk (in [m/s^3])

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``vmax`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``amax`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``jerk`` is not convertible to a C int.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.getEncTrackParam()`
    | :func:`forcedimension_core.getEncMoveParam()`
    | :func:`forcedimension_core.setEncTrackParam()`
    """

    return _runtime._libdrd.drdSetEncMoveParam(amax, vmax, jerk, ID)


_runtime._libdrd.drdSetEncTrackParam.argtypes = [
    c_double, c_double, c_double, c_byte
]
_runtime._libdrd.drdSetEncTrackParam.restype = c_int


def setEncTrackParam(
    vmax: float, amax: float, jerk: float, ID: int = -1
) -> int:
    """
    Sets the encoder tracking trajectory generation parameters.

    :param float vmax:
        max velocity (in [m/s])

    :param float amax:
        max acceleration (in [m/s^2])

    :param float jerk:
        jerk (in [m/s^3])

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``vmax`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``amax`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``jerk`` is not convertible to a C int.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.getEncTrackParam()`
    | :func:`forcedimension_core.getEncMoveParam()`
    | :func:`forcedimension_core.setEncMoveParam()`
    """

    return _runtime._libdrd.drdSetEncTrackParam(amax, vmax, jerk, ID)


_runtime._libdrd.drdSetPosMoveParam.argtypes = [c_double, c_double, c_double, c_byte]
_runtime._libdrd.drdSetPosMoveParam.restype = c_int


def setPosMoveParam(
    vmax: float, amax: float, jerk: float, ID: int = -1
) -> int:
    """
    Sets the cartesian positioning trajectory generation parameters.

    :param float vmax:
        max velocity (in [m/s])

    :param float amax:
        max acceleration (in [m/s^2])

    :param float jerk:
        jerk (in [m/s^3])

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``vmax`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``amax`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``jerk`` is not convertible to a C int.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.getPosTrackParam()`
    | :func:`forcedimension_core.getPosMoveParam()`
    | :func:`forcedimension_core.setPosTrackParam()`
    """


    return _runtime._libdrd.drdSetPosMoveParam(amax, vmax, jerk, ID)


_runtime._libdrd.drdSetPosTrackParam.argtypes = [c_double, c_double, c_double, c_byte]
_runtime._libdrd.drdSetPosTrackParam.restype = c_int


def setPosTrackParam(
    vmax: float, amax: float, jerk: float, ID: int = -1
) -> int:
    """
    Sets the cartesian tracking trajectory generation parameters.

    :param float vmax:
        max velocity (in [m/s])

    :param float amax:
        max acceleration (in [m/s^2])

    :param float jerk:
        jerk (in [m/s^3])

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``vmax`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``amax`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``jerk`` is not convertible to a C int.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.getPosTrackParam()`
    | :func:`forcedimension_core.getPosMoveParam()`
    | :func:`forcedimension_core.setPosMoveParam()`
    """

    return _runtime._libdrd.drdSetPosTrackParam(amax, vmax, jerk, ID)


_runtime._libdrd.drdSetRotMoveParam.argtypes = [c_double, c_double, c_double, c_byte]
_runtime._libdrd.drdSetRotMoveParam.restype = c_int


def setRotMoveParam(
    vmax: float, amax: float, jerk: float, ID: int = -1
) -> int:
    """
    Sets the cartesian rotation trajectory generation parameters.

    :param float vmax:
        max velocity (in [m/s])

    :param float amax:
        max acceleration (in [m/s^2])

    :param float jerk:
        jerk (in [m/s^3])

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``vmax`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``amax`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``jerk`` is not convertible to a C int.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.getRotTrackParam()`
    | :func:`forcedimension_core.getRotMoveParam()`
    | :func:`forcedimension_core.setRotTrackParam()`
    """

    return _runtime._libdrd.drdSetRotMoveParam(amax, vmax, jerk, ID)


_runtime._libdrd.drdSetRotTrackParam.argtypes = [c_double, c_double, c_double, c_byte]
_runtime._libdrd.drdSetRotTrackParam.restype = c_int


def setRotTrackParam(
    vmax: float, amax: float, jerk: float, ID: int = -1
) -> int:
    """
    Sets the cartesian rotation tracking trajectory generation parameters.

    :param float vmax:
        max velocity (in [m/s])

    :param float amax:
        max acceleration (in [m/s^2])

    :param float jerk:
        jerk (in [m/s^3])

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``vmax`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``amax`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``jerk`` is not convertible to a C int.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.getRotTrackParam()`
    | :func:`forcedimension_core.getRotMoveParam()`
    | :func:`forcedimension_core.setRotMoveParam()`
    """

    return _runtime._libdrd.drdSetRotTrackParam(amax, vmax, jerk, ID)


_runtime._libdrd.drdSetGripMoveParam.argtypes = [c_double, c_double, c_double, c_byte]
_runtime._libdrd.drdSetGripMoveParam.restype = c_int


def setGripMoveParam(
    vmax: float, amax: float, jerk: float, ID: int = -1
) -> int:
    """
    Sets the gripper trajectory generation parameters.

    :param float vmax:
        max velocity (in [m/s])

    :param float amax:
        max acceleration (in [m/s^2])

    :param float jerk:
        jerk (in [m/s^3])

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``vmax`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``amax`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``jerk`` is not convertible to a C int.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.getGripTrackParam()`
    | :func:`forcedimension_core.getGripMoveParam()`
    | :func:`forcedimension_core.setGripTrackParam()`
    """

    return _runtime._libdrd.drdSetGripMoveParam(amax, vmax, jerk, ID)


_runtime._libdrd.drdSetGripTrackParam.argtypes = [c_double, c_double, c_double, c_byte]
_runtime._libdrd.drdSetGripTrackParam.restype = c_int


def setGripTrackParam(
    vmax: float, amax: float, jerk: float, ID: int = -1
) -> int:
    """
    Sets the gripper trajectory generation parameters.

    :param float vmax:
        max velocity (in [m/s])

    :param float amax:
        max acceleration (in [m/s^2])

    :param float jerk:
        jerk (in [m/s^3])

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :raises ctypes.ArgumentError:
        If ``vmax`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``amax`` is not convertible to a C int.

    :raises ctypes.ArgumentError:
        If ``jerk`` is not convertible to a C int.

    :returns:
        0 on success, and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.getGripTrackParam()`
    | :func:`forcedimension_core.getGripMoveParam()`
    | :func:`forcedimension_core.setGripMoveParam()`
    """

    return _runtime._libdrd.drdSetGripTrackParam(amax, vmax, jerk, ID)


_runtime._libdrd.drdGetEncMoveParam.argtypes = [
    c_double_ptr, c_double_ptr, c_double_ptr, c_byte
]
_runtime._libdrd.drdGetEncMoveParam.restype = c_int


def getEncMoveParam(ID: int = -1) -> Tuple[Tuple[float, float, float], int]:
    """
    Retrieve encoder positioning trajectory generation parameters.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        tuple of `((v_max, a_max, jerk_max), err)` where v_max (in [m/s]),
        a_max (in [m/s^2]), and jerk (in [m/s^3]) are the max velocity
        acceeleration. err is 0 on success and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.setEncMoveParam()`
    | :func:`forcedimension_core.setEncTrackParam()`
    | :func:`forcedimension_core.getEncTrackParam()`
    """
    a_max = c_double()
    v_max = c_double()
    jerk_max = c_double()

    err = _runtime._libdrd.drdGetEncMoveParam(a_max, v_max, jerk_max, ID)

    return (v_max.value, a_max.value, jerk_max.value), err


_runtime._libdrd.drdGetEncTrackParam.argtypes = [
    c_double_ptr, c_double_ptr, c_double_ptr, c_byte
]
_runtime._libdrd.drdGetEncTrackParam.restype = c_int


def getEncTrackParam(ID: int = -1) -> Tuple[Tuple[float, float, float], int]:
    """
    Retrieve encoder tracking trajectory generation parameters.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        tuple of `((v_max, a_max, jerk_max), err)` where v_max (in [m/s]),
        a_max (in [m/s^2]), and jerk (in [m/s^3]) are the max velocity
        acceeleration. err is 0 on success and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.setEncMoveParam()`
    | :func:`forcedimension_core.setEncTrackParam()`
    | :func:`forcedimension_core.getEncMoveParam()`
    """

    amax = c_double()
    vmax = c_double()
    jerk = c_double()

    err = _runtime._libdrd.drdGetEncTrackParam(amax, vmax, jerk, ID)

    return (vmax.value, amax.value, jerk.value), err


_runtime._libdrd.drdGetPosMoveParam.argtypes = [
    c_double_ptr, c_double_ptr, c_double_ptr, c_byte
]
_runtime._libdrd.drdGetPosMoveParam.restype = c_int


def getPosMoveParam(ID: int = -1) -> Tuple[Tuple[float, float, float], int]:
    """
    Retrieve cartesian positioning trajectory generation parameters.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        tuple of `((v_max, a_max, jerk_max), err)` where v_max (in [m/s]),
        a_max (in [m/s^2]), and jerk (in [m/s^3]) are the max velocity
        acceeleration. err is 0 on success and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.setPosMoveParam()`
    | :func:`forcedimension_core.setPosTrackParam()`
    | :func:`forcedimension_core.getPosTrackParam()`
    """

    amax = c_double()
    vmax = c_double()
    jerk = c_double()

    err = _runtime._libdrd.drdGetPosMoveParam(amax, vmax, jerk, ID)

    return (vmax.value, amax.value, jerk.value), err


_runtime._libdrd.drdGetPosTrackParam.argtypes = [
    c_double_ptr, c_double_ptr, c_double_ptr, c_byte
]
_runtime._libdrd.drdGetPosTrackParam.restype = c_int


def getPosTrackParam(ID: int = -1) -> Tuple[Tuple[float, float, float], int]:
    """
    Retrieve cartesian tracking trajectory generation parameters.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        tuple of `((v_max, a_max, jerk_max), err)` where v_max (in [m/s]),
        a_max (in [m/s^2]), and jerk (in [m/s^3]) are the max velocity
        acceeleration. err is 0 on success and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.setPosMoveParam()`
    | :func:`forcedimension_core.setPosTrackParam()`
    | :func:`forcedimension_core.getPosMoveParam()`
    """

    amax = c_double()
    vmax = c_double()
    jerk = c_double()

    err = _runtime._libdrd.drdGetPosTrackParam(amax, vmax, jerk, ID)

    return (vmax.value, amax.value, jerk.value), err


_runtime._libdrd.drdGetRotMoveParam.argtypes = [
    c_double_ptr, c_double_ptr, c_double_ptr, c_byte
]
_runtime._libdrd.drdGetRotMoveParam.restype = c_int


def getRotMoveParam(ID: int = -1) -> Tuple[Tuple[float, float, float], int]:
    """
    Retrieve cartesian positioning trajectory generation parameters.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        tuple of `((v_max, a_max, jerk_max), err)` where v_max (in [m/s]),
        a_max (in [m/s^2]), and jerk (in [m/s^3]) are the max velocity
        acceeleration. err is 0 on success and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.setRotMoveParam()`
    | :func:`forcedimension_core.setRotTrackParam()`
    | :func:`forcedimension_core.getRotTrackParam()`
    """

    amax = c_double()
    vmax = c_double()
    jerk = c_double()

    err = _runtime._libdrd.drdGetRotMoveParam(amax, vmax, jerk, ID)

    return (vmax.value, amax.value, jerk.value), err


_runtime._libdrd.drdGetRotTrackParam.argtypes = [
    c_double_ptr, c_double_ptr, c_double_ptr, c_byte
]
_runtime._libdrd.drdGetRotTrackParam.restype = c_int


def getRotTrackParam(ID: int = -1) -> Tuple[Tuple[float, float, float], int]:
    """
    Retrieve cartesian tracking trajectory generation parameters.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        tuple of `((v_max, a_max, jerk_max), err)` where v_max (in [m/s]),
        a_max (in [m/s^2]), and jerk (in [m/s^3]) are the max velocity
        acceeleration. err is 0 on success and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.setRotMoveParam()`
    | :func:`forcedimension_core.setRotTrackParam()`
    | :func:`forcedimension_core.getRotMoveParam()`
    """

    amax = c_double()
    vmax = c_double()
    jerk = c_double()

    err = _runtime._libdrd.drdGetRotTrackParam(amax, vmax, jerk, ID)

    return (vmax.value, amax.value, jerk.value), err


_runtime._libdrd.drdGetGripMoveParam.argtypes = [
    c_double_ptr, c_double_ptr, c_double_ptr, c_byte
]
_runtime._libdrd.drdGetGripMoveParam.restype = c_int


def getGripMoveParam(ID: int = -1) -> Tuple[Tuple[float, float, float], int]:
    """
    Retrieve cartesian positioning trajectory generation parameters.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        tuple of `((v_max, a_max, jerk_max), err)` where v_max (in [m/s]),
        a_max (in [m/s^2]), and jerk (in [m/s^3]) are the max velocity
        acceeleration. err is 0 on success and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.setGripMoveParam()`
    | :func:`forcedimension_core.setGripTrackParam()`
    | :func:`forcedimension_core.getGripTrackParam()`
    """

    amax = c_double()
    vmax = c_double()
    jerk = c_double()

    err = _runtime._libdrd.drdGetGripMoveParam(amax, vmax, jerk, ID)

    return (vmax.value, amax.value, jerk.value), err


_runtime._libdrd.drdGetGripTrackParam.argtypes = [
    c_double_ptr, c_double_ptr, c_double_ptr, c_byte
]
_runtime._libdrd.drdGetGripTrackParam.restype = c_int


def getGripTrackParam(ID: int = -1) -> Tuple[Tuple[float, float, float], int]:
    """
    Retrieve cartesian tracking trajectory generation parameters.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.

    :returns:
        tuple of `((v_max, a_max, jerk_max), err)` where v_max (in [m/s]),
        a_max (in [m/s^2]), and jerk (in [m/s^3]) are the max velocity
        acceeleration. err is 0 on success and -1 otherwise.

    See Also
    --------
    | :func:`forcedimension_core.setGripMoveParam()`
    | :func:`forcedimension_core.setGripTrackParam()`
    | :func:`forcedimension_core.getGripMoveParam()`
    """

    amax = c_double()
    vmax = c_double()
    jerk = c_double()

    err = _runtime._libdrd.drdGetGripTrackParam(amax, vmax, jerk, ID)

    return (vmax.value, amax.value, jerk.value), err


_runtime._libdrd.drdWaitForTick.argtypes = [c_byte]
_runtime._libdrd.drdWaitForTick.restype = None

def waitForTick(ID: int = -1):
    """
    Puts the current thread to sleep until the next iteration of the robotic
    control loop begins.

    :param int ID:
        Device ID (see :ref:`multiple_devices` section for details).

    :raises ctypes.ArgumentError:
        If ``ID`` is not convertible to a C char.
    """
    _runtime._libdrd.drdWaitForTick(ID)
