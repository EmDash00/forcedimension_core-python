DHD Reference
=============

.. toctree::
   :maxdepth: 1
   :caption: Contents:


The :doc:`forcedimension_core.dhd`
is the Force Dimension haptic SDK. The following document describes its theory of operation,
conventions, and terms. This document was adapted from the C/C++ API official documentation for the
purpose of facilitating Python programmers; however, there may be errors and the users should always refer
to the official documentation. This version of the bindings targets SDK v3.14.0.


.. _device_types:

Device Types
------------

Devices in the library have a type which can be retrieved via :func:`forcedimension_core.dhd.getSystemType()`
and they are encoded with :class:`forcedimension_core.dhd.constants.DeviceType`.

The supported devices (and their encoded system types) for DHD v3.16.0 are:

+----------------------------+--------------------------------------------------------------------+
| Device Family              |  Device Types                                                      |
+============================+====================================================================+
| 2nd Gen DELTA.X            | :data:`forcedimension_core.dhd.constants.DeviceType.DELTA3`        |
+----------------------------+--------------------------------------------------------------------+
| 2nd Gen OMEGA.X            | :data:`forcedimension_core.dhd.constants.DeviceType.OMEGA3`        |
|                            |                                                                    |
|                            | :data:`forcedimension_core.dhd.constants.DeviceType.OMEGA6_RIGHT`  |
|                            |                                                                    |
|                            | :data:`forcedimension_core.dhd.constants.DeviceType.OMEGA6_LEFT`   |
|                            |                                                                    |
|                            | :data:`forcedimension_core.dhd.constants.DeviceType.OMEGA7_RIGHT`  |
|                            |                                                                    |
|                            | :data:`forcedimension_core.dhd.constants.DeviceType.OMEGA7_LEFT`   |
+----------------------------+--------------------------------------------------------------------+
| SIGMA.X                    | :data:`forcedimension_core.dhd.constants.DeviceType.SIGMA3`        |
|                            |                                                                    |
|                            | :data:`forcedimension_core.dhd.constants.DeviceType.SIGMA7_RIGHT`  |
|                            |                                                                    |
|                            | :data:`forcedimension_core.dhd.constants.DeviceType.SIGMA7_LEFT`   |
+----------------------------+--------------------------------------------------------------------+
| LAMBDA.X                   | :data:`forcedimension_core.dhd.constants.DeviceType.LAMBDA3`       |
|                            |                                                                    |
|                            | :data:`forcedimension_core.dhd.constants.DeviceType.LAMBDA7_RIGHT` |
|                            |                                                                    |
|                            | :data:`forcedimension_core.dhd.constants.DeviceType.LAMBDA7_LEFT`  |
+----------------------------+--------------------------------------------------------------------+
| Stand-alone USB Controller | :data:`forcedimension_core.dhd.constants.DeviceType.CONTROLLER`    |
|                            |                                                                    |
|                            | :data:`forcedimension_core.dhd.constants.DeviceType.CONTROLLER_HR` |
+----------------------------+--------------------------------------------------------------------+
| Novint Falcon              | :data:`forcedimension_core.dhd.constants.DeviceType.FALCON`        |
+----------------------------+--------------------------------------------------------------------+


Unknown devices that comply with the Force Dimension SDK protocol are referenced by
:data:`forcedimension_core.dhd.constants.DeviceType.CUSTOM`

The table below summarizes features supported by each device.


.. rst-class:: center-columns
.. table::
  :widths: auto

  ============== ====== ======== ======= ============== ========= ================ =============
   Device Type    Base   Handed   Wrist   Active Wrist   Gripper   Active Gripper   Output Bits
  ============== ====== ======== ======= ============== ========= ================ =============
  FALCON           ✓       ❌       ❌         ❌           ❌           ❌             ❌
  DELTA.3          ✓       ❌       ❌         ❌           ❌           ❌             ✓
  OMEGA.3          ✓       ❌       ❌         ❌           ❌           ❌             ❌
  SIGMA.3          ✓       ❌       ❌         ❌           ❌           ❌             ❌
  LAMBDA.3         ✓       ❌       ❌         ❌           ❌           ❌             ❌
  OMEGA.6          ✓       ✓        ✓          ❌           ❌           ❌             ❌
  OMEGA.7          ✓       ✓        ✓          ❌           ✓            ✓              ❌
  SIGMA.7          ✓       ✓        ✓          ✓            ✓            ✓              ✓
  LAMBDA.7         ✓       ✓        ✓          ✓            ✓            ✓              ❌
  ============== ====== ======== ======= ============== ========= ================ =============

Axis Convention
---------------

For data is passed in or out as a (mutable) sequence of floats
(at :data:`forcedimension_core.dhd.constants.MAX_DOF` length) it is encoded as follows:

``postion_dof = [pos_x, pos_y, pos_z, euler_angle_x, euler_angle_y, euler_angle_z, gripper_gap]``

``velocity_dof = [v_x, v_y, v_z, w_x, w_y, w_z, v_gripper]``

``force_torque_dof = [f_x, f_y, f_z, t_x, t_y, t_z, f_gripper]``


.. _device_modes:

Device Modes
------------

When the device is active (powered ON) it is in one of four states or 'modes'.

- RESET mode
  In this mode, the user is expected to put the end-effector at its rest position. This is out the device
  performs its calibration. A calibration can be explicitly requested by calling :func:`forcedimension_core.dhd.reset()`.

- IDLE mode
  In this mode, the position of the end-effector can be read, but no current is applied to the device motors. This
  is a safe way debug an application or to use the device as a pointer. The device can be forced into IDLE mode
  by disabling the brakes via :func:`forcedimension_core.dhd.setBrakes()`.

- FORCE mode
  In this mode, the device motors are enabled so that forces (and torques for 6+ DOF devices) can be applied. This
  includes forces on the gripper if the device has one.

- BRAKE mode
  In this mode, electromagnetic braking is applied on the motors. As a result, there is added viscosity that prevents
  the end-effector from moving rapidly. This mode is entered when forces are disabled or if a :ref:`safety_feature`
  triggers it.

Device Status
-------------

Force Dimension haptic devices statuses can be retrieved via the :func:`forcedimension_core.dhd.getStatus()` function.
The status returned is a :class:`forcedimension_core.dhd.adaptors.StatusTuple`. See the class for more details on the meaning
of individual statuses.

.. _multiple_devices:

Support for Multiple Devices
----------------------------

DHD supports as many haptic devices connected to the same computer as the underlying OS can accomodate. Once
a device is opened, it recieves and ID that uniquely identifies it within the SDK. The default device that recieves
commands from the SDK can be gotten via :func:`forcedimension_core.dhd.getDeviceID()` and set via
:func:`forcedimension_core.dhd.setDevice()`. Every device specific function of the SDK can take as an optional
last argument the device ID. If no device ID is given, or if that ID is -1, the default device is used.

.. _velocity_estimator:

Velocity Estimator
------------------

The SDK provides internal mechanisms that estimate the velocity of the device in the joint and cartesian
coordinate systems. THe default (and currently only) velocity estimator configuration should be suitable for
most use cases but can be reconfigured via:

- :func:`forcedimension_core.dhd.configLinearVelocity()`
- :func:`forcedimension_core.dhd.configAngularVelocity()`
- :func:`forcedimension_core.dhd.configGripperVelocity()`

The estimated velocity can be retrieved by calling:

- :func:`forcedimension_core.dhd.getLinearVelocity()`
- :func:`forcedimension_core.dhd.getAngularVelocityRad()`
- :func:`forcedimension_core.dhd.getAngularVelocityDeg()`
- :func:`forcedimension_core.dhd.getGripperLinearVelocity()`
- :func:`forcedimension_core.dhd.getGripperAngularVelocityRad()`
- :func:`forcedimension_core.dhd.getGripperAngularVelocityDeg()`

Currently, the only supported velocity estimator mode is :data:`forcedimension_core.dhd.constants.VELOCITY_WINDOWING`.
The default window size (in [ms]) for the velocity estimator is :data:`forcedimension_core.dhd.constants.VELOCITY_WINDOW`.

.. _time_guard:

TimeGuard
---------

DHD features a throttling mechanism to provide a controllable communication refresh rate whil preserving
resources on non real-time OSes. This mechanism prvents the OS from querying the device for its position at a
rate higher than an adjustable threshold. In order to do so, TimeGuard prevents the application from requesting new
data if recent data from an earlier communication event is still recent enough.

This mechanism can remove communication overhead without affecting performance if set properly, but can also
significantly affect performance if set to the wrong value. It is recommended to leave the TimeGuard feature to its
default setting unless a specific software architecture requires it. The SDK calls that trigger the TimeGuard feature
will return :data:`forcedimension_core.dhd.constants.TIMEGUARD` if communication with the device was deemed unnecessary
and 0 otherwise. See :ref:`error_management` for more information.

The value of the TimeGuard can be adjust via :func:`forcedimension_core.dhd.expert.setTimeGuard()`.
See its documentation for more details.

Threading
---------

Force Dimension is thread-safe. Programmers do not need to add additional synchronization mechanisms to control access
to the device or its geometric model.

Thus, multi-threading is fully supported by the SDK. The Python bindings do not bind the platform independent
threading functions offerred by the C/C++ API as Python already has its own threading library. You are recommended
to use that instead.


.. _error_management:

Error Management
----------------

DHD uses a thread-safe global accessible via :func:`forcedimension_core.dhd.errorGetLast()` to store the last
error that occurred in each running thread. These errors are encoded by :data:`forcedimension_core.dhd.constants.ErrorNum`.
You can get a message that describes the error with :func:`forcedimension_core.dhd.errorGetLastStr()` and
:func:`forcedimension_core.dhd.errorGetStr()`.

The Python bindings also add an additional function (automatically imported with DHD),
:func:`forcedimension_core.dhd.adaptors.errno_to_exception()`
that converts an error number to an excepion that you can raise. See
:mod:`forcedimension_core.dhd.adaptors` for more information on what kinds of exceptions may be raised.

.. _safety_feature:

Safety Feature
--------------

Since Force Dimension haptic devices can generate a significant amount of force, it could accelerate to a point that
might damage the system or surprise unaware users. To prevent such situations, the controller's factory settings offer
a safety feature that forces the device into BRAKE mode if the velocity (similar to if you had called
:func:`forcedimension_core.dhd.stop()`)
becomes greater than a given threshold. While it is possible to modify this value using more advanced features of the SDK
it is recommended that you keep this threshold as low as the application permits.

Expert Mode
-----------

The expert SDK offers more direct access to lower-level functionalities of the device (such as encoder readings
and direct motor commands). These functions are in :mod:`forcedimension_core.dhd.expert` and must be enabled
via :func:`forcedimension_core.dhd.enableExpertMode()`. They may be disabled via
:func:`forcedimension_core.dhd.disableExpertMode()`.

Please note that expert mode should only be used by experienced programmers who have a thorough understanding
of their haptic interface and control theory. Force Dimension and any contributors to the Force Dimension Python
Bindings are NOT responsible for any damage resulting from the use of expert mode.

Glossary
--------

Initialization
^^^^^^^^^^^^^^
Initialization is necessary to obtain accurate, reproducible localization of the end-effector within the workspace of the device. Force Dimension haptic devices are designed in such a way that there can be no drift of the calibration over time, so the procedure only needs to be performed once when the device is powered on. The calibration procedure consists in placing the calibration pole in the dedicated calibration pit. The device detects when the calibration position is reached and the status LED stops blinking.

.. _device_controller:

Device Controller
^^^^^^^^^^^^^^^^^
The electronic controller is responsible for the real-time behavior of the device. It connects to the host computer and provides the low-level safety features such as velocity thresholding and communication timeouts.

Default Device
^^^^^^^^^^^^^^
In a multiple devices utilization, the SDK keeps an internal ID of one of the devices. All the SDK calls that do not explicitly mention a device ID are directed to the default device. The default device can be determined by calling
:func:`forcedimension_core.dhd.getDeviceID()`. The default device can be changed by calling
:func:`forcedimension_core.dhd.setDevice()`. Calls to
:func:`forcedimension_core.dhd.open()` and friends change the default device ID to the last successfully opened device.

Electromagnetic Brakes
^^^^^^^^^^^^^^^^^^^^^^
In BRAKES mode, the device motor circuits are shortcut to produce electromagnetic viscosity. The viscosity is sufficient to prevent the device from falling too hard onto if forces are disabled abruptly, either by pressing the force button or by action of a safety feature.

Gravity Compensation
^^^^^^^^^^^^^^^^^^^^
To prevent user fatigue and to increase accuracy during manipulation, Force Dimension haptic devices features gravity compensation. When gravity compensation is enabled, the weights of the arms and of the end-effector are taken into account and a vertical force is dynamically applied to the end-effector on top of the user command. Please note that gravity compensation is computed on the host computer, and therefore only gets applied whenever a force command is sent to the device by the application. By default, gravity compensation is enabled and
:func:`forcedimension_core.dhd.setForce()` compensates for the device weight.
Gravity compensation can be disabled by calling :func:`forcedimension_core.dhd.setGravityCompensation()`.

Single Device Calls
^^^^^^^^^^^^^^^^^^^
When used with a single Force Dimension haptic device, programmers should use the single device version of the functions. Single device calls use the null default device ID, unlike the multiple devices SDK calls, which explicitly take the device ID as a last argument.

.. _velocity_threshold:

Velocity Threshold
^^^^^^^^^^^^^^^^^^
Every Force Dimension haptic device features a safety feature that prevents the device from accelerating without control. If the control unit detects that the velocity of the end-effector is higher than the programmed security limit, the forces are automatically disabled and the device brakes are engaged to prevent a possibly dangerous acceleration from the device. This velocity threshold can be adjusted or removed by calling
:func:`forcedimension_core.dhd.setVelocityThreshold()`.

Watchdog Threshold
^^^^^^^^^^^^^^^^^^
Force Dimension haptic devices with firmware version greater or equal to 3.0 features a safety feature that disables forces on the device if no communication is received by the controller for a given amount of time. If the control unit does not receive an expected input, the forces are automatically disabled and the device brakes are engaged to prevent potentially dangerous device behavior. This time duration of the watchdog feature can be adjusted or removed by calling
:func:`forcedimension_core.dhd.setWatchdog()`.

Wrist Calibration
^^^^^^^^^^^^^^^^^
For 6 DOF Force Dimension devices, the controller performs a calibration procedure at power-up. This procedure is fully automated and does not require any user intervention during the few seconds it lasts. The calibration can be repeated without power-cycling the device by calling
:func:`forcedimension_core.dhd.calibrateWrist()`.

COM operating Mode
^^^^^^^^^^^^^^^^^^
USB operations can be executed in two different modes:
:data:`forcedimension_core.dhd.constants.ComMode.SYNC` and  :data:`forcedimension_core.dhd.constants.ComMode.ASYNC`.
Other operation modes are reported for virtual devices
(:data:`forcedimension_core.dhd.constants.ComMode.VIRTUAL`) and devices that are connected over the network
(:data:`forcedimension_core.dhd.constants.ComMode.NETWORK`). Please check the documentation of each mode for more details.
