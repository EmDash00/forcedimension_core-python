DRD Reference
=============

.. warning::
  Force Dimension nor any contributors to the Force Dimension Python bindings
  accept NO responsibility for any damage that result from using this software,
  including damage to any hardware involved.

  The performance and safety of the robotic regulation provided by DRD depends on the operating system,
  execution context and physical hardware used. A background in control theory and real-time programming
  is strongly recommended prior to writing applications using DRD.

Introduction
------------

The :doc:`forcedimension_core.drd` is the robotics software library.
DRD has been designed specifically to enable robotic control of Force Dimension haptic devices,
as well as to make it possible to write applications that combine interactive (haptic) and automatic (robotic) capabilities.
As a consequence, the DRD is built alongside the DHD haptic library and shares some fundamental resources with it.
It is therefore possible to use functions in :mod:`forcedimension_core.dhd`) and
mod:`forcedimension_core.drd` in the same application. For this reason, this page will ocassionally reference
:doc:`forcedimension_core.dhd-doc`.


Conceptually, the library manages axis regulation in its own high-priority thread, while all DRD function calls
asynchronously control the regulation loop parameters. The DRD library is targeted at real-time platforms to
guarantee the performance and safety of the regulation (as well as the users and hardware involved).
However, DRD has been implemented so that it can run with reasonable performance and acceptable safety on
non-real time platforms, thanks in part to a control instability detection algorithm.


.. _regulation:

Regulation
----------
At the heart of the library is the regulation thread, which constraints the position of each joint.
The thread can be started with :func:`forcedimension_core.drd.start()`
(after the device has been initialized), and stopped with :func:`forcedimension_core.drd.stop()`.
The refresh rate of the control thread can be retrieved by calling :func:`forcedimension_core.drd.getCtrlFreq()`.
Once the the thread is running (which can be assessed with :func:`forcedimension_core.drd.isRunning()`),
the device can only be moved by changing the regulation target of each joint.
This can be achieved by calling either :func:`forcedimension_core.drd.move()` and friends or
:func:`forcedimension_core.drd.track()` and friends.
The drdMove* functions are designed to send the device end-effector on a direct, smooth trajectory to any
point in the workspace, while the drdTrack* calls should be used to smoothly constrain the device motion on
a continuous trajectory along a set of points sent asynchronously to the control thread
(see :func:`forcedimension_core.drd.trackPos()` for more details).

The key difference between the two sets of functions is that calls to
:func:`forcedimension_core.drd.moveTo()` and friends do not guarantee continuity if
a new call is made before an earlier call finishes. On the other hand,
calls to :func:`forcedimension_core.drd.track()` and friends do guarantee
continuity regardless of when they are invoked. However, track functions trajectory generation is performed on
each axis individually, while move functions generate trajectories in 3D space. Outside of these different
behaviors, both move functions and track functions use a trajectory generation algorithm that guarantees continuous
acceleration changes. For more details on the trajectory generation, see :ref:`trajectory_generation_parameters`.


.. _trajectory_generation_parameters:

Trajectory Generation Parameters
--------------------------------

The trajectory generation algorithm implemented in DRD uses triangular acceleration constraints to guarantee
smooth movements in both joint and cartesian spaces. The following parameters can be used to change the
behavior of the generated trajectories:

- Amax  the maximal allowed acceleration [m/s^2]
- Vmax - the maximal allowed velocity [m/s]
- Jerk - the variation of acceleration over time [m/s^3]

Non Real-Time Considerations
----------------------------
On non real-time platforms, the periodicity of the regulation thread cannot be guaranteed. Moreover,
the Python bindings may also have periodic undeterministic pauses of unknown length due to the Python
garbage collector (though, this can be mitigated by preallocating memory to avoid allocations inside loops as well
as using :func:`gc.disable()`).
These considerations have direct consequences on control stability and performance.

In order to limit the performance degradation, DRD
implements a regulator that does not assume periodicity and can tolerate some jitter in the control loop.
In order to optimize the performance of the control thread, :func:`forcedimension_core.drd.setPriorities()`
can be used to change the priority of  both the calling and the regulation thread. It must however be
emphasized that, by definition, no performance guarantee can be offered on non real-time operating systems,
and unpredictable behaviors (including disastrous instability) may occur. In order to prevent hardware
damage, the regulation thread uses an internal measure of its
own stability. See :ref:`control_instability_detection` for more details.

.. _control_instability_detection:

Control Instability Detection
-----------------------------
During its execution, the regulation thread measures the jitter and delays of each iteration. Short of the thread being fully suspended by the system, these metrics allow the library to detect instability and exit gracefully, while applying the electro-magnetic brakes on the controlled device, in case of dangerous control performance degradation.
