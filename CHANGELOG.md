# Release 1.0.0rc1 (November 5, 2023)

Targets: Force Dimension SDK 3.16.0+

## Additions

The entire Force Dimension SDK v3.16.0 is now bound.

Newly implemented DHD Functions:
- `forcedimension_core.dhd.checkControllerMemory()`
- `forcedimension_core.dhd.getComponentVersionStr()`
- `forcedimension_core.dhd.getSystemRev()`

Newly implemented DRD Functions:
- `forcedimension_core.drd.getCtrlFreq()`
- `forcedimension_core.drd.getGripMoveParam()`
- `forcedimension_core.drd.getGripTrackParam()`
- `forcedimension_core.drd.getPriorities()`
- `forcedimension_core.drd.getRotMoveParam()`
- `forcedimension_core.drd.getRotTrackParam()`
- `forcedimension_core.drd.lock()`
- `forcedimension_core.drd.precisionInit()`
- `forcedimension_core.drd.setForceAndTorqueAndGripperForce()`
- `forcedimension_core.drd.setForceAndWristJointTorquesAndGripperForce()`
- `forcedimension_core.drd.setGripMoveParam()`
- `forcedimension_core.drd.setGripTrackParam()`
- `forcedimension_core.drd.setRotMoveParam()`
- `forcedimension_core.drd.setRotTrackParam()`
- `forcedimension_core.drd.track()`
- `forcedimension_core.drd.trackAllEnc()`
- `forcedimension_core.drd.trackEnc()`
- `forcedimension_core.drd.trackGrip()`
- `forcedimension_core.drd.trackPos()`
- `forcedimension_core.drd.trackRot()`
- `forcedimension_core.drd.waitForTick()`

Newly implemented utility functions:
- `forcedimension_core.forcedimension_core.util.com_mode_str()`
- `forcedimension_core.forcedimension_core.util.com_mode_from_str()`
- `forcedimension_core.forcedimension_core.util.num_dof()`
- `forcedimension_core.forcedimension_core.util.devtype_str()`
- `forcedimension_core.forcedimension_core.util.handedness()`
- `forcedimension_core.forcedimension_core.util.handedness_str()`
- `forcedimension_core.forcedimension_core.util.velocity_estimator_mode_str()`

### Containers

New container types are included. NumPy style continers are also defined and can be imported if
NumPy is installed (v1.20.0 required). Install the optional dependency using `python3 -m pip install forcedimension_core[numpy]`


## Typing

`forcedimension_core.typing` has been greatly simplified. The only 2 types used extensively by the library are now:
- `forcedimension_core.typing.Array`
- `forcedimension_core.typing.MutableArray`

Additional protocols were introduced for direct copy optimization:
- `forcedimension_core.typing.SupportsPtr`
- `forcedimension_core.typing.SupportsPtrs3`

Other additions:
- `forcedimension_core.typing.CBoolLike`
- `forcedimension_core.typing.ComModeStr`
- `forcedimension_core.typing.FloatDOFTuple`


### Direct copy optimization

Direct copy optimization was introduced for the following functions.

DHD functions:
- `forcedimension_core.dhd.direct.getAngularVelocityDeg()`
- `forcedimension_core.dhd.direct.getAngularVelocityRad()`
- `forcedimension_core.dhd.direct.getForce()`
- `forcedimension_core.dhd.direct.getForceAndTorque()`
- `forcedimension_core.dhd.direct.getForceAndTorqueAndGripperForce()`
- `forcedimension_core.dhd.direct.getGripperFingerPos()`
- `forcedimension_core.dhd.direct.getGripperThumbPos()`
- `forcedimension_core.dhd.direct.getLinearVelocity()`
- `forcedimension_core.dhd.direct.getOrientationDeg()`
- `forcedimension_core.dhd.direct.getOrientationFrame()`
- `forcedimension_core.dhd.direct.getOrientationRad()`
- `forcedimension_core.dhd.direct.getPosition()`
- `forcedimension_core.dhd.direct.getPositionAndOrientationDeg()`
- `forcedimension_core.dhd.direct.getPositionAndOrientationFrame()`
- `forcedimension_core.dhd.direct.getPositionAndOrientationRad()`

DHD Expert Mode functions:

- `forcedimension_core.dhd.expert.direct.deltaEncoderToPosition()`
- `forcedimension_core.dhd.expert.direct.deltaEncodersToJointAngles()`
- `forcedimension_core.dhd.expert.direct.deltaForceToMotor()`
- `forcedimension_core.dhd.expert.direct.deltaJointAnglesToEncoders()`
- `forcedimension_core.dhd.expert.direct.deltaJointAnglesToJacobian()`
- `forcedimension_core.dhd.expert.direct.deltaJointTorquesExtrema()`
- `forcedimension_core.dhd.expert.direct.deltaMotorToForce()`
- `forcedimension_core.dhd.expert.direct.deltaPositionToEncoder()`
- `forcedimension_core.dhd.expert.direct.getDeltaEncoders()`
- `forcedimension_core.dhd.expert.direct.getDeltaJacobian()`
- `forcedimension_core.dhd.expert.direct.getDeltaJointAngles()`
- `forcedimension_core.dhd.expert.direct.getEnc()`
- `forcedimension_core.dhd.expert.direct.getEncVelocities()`
- `forcedimension_core.dhd.expert.direct.getJointAngles()`
- `forcedimension_core.dhd.expert.direct.getJointVelocities()`
- `forcedimension_core.dhd.expert.direct.getWristEncoders()`
- `forcedimension_core.dhd.expert.direct.getWristJacobian()`
- `forcedimension_core.dhd.expert.direct.getWristJointAngles()`
- `forcedimension_core.dhd.expert.direct.gripperForceToMotor()`
- `forcedimension_core.dhd.expert.direct.gripperMotorToForce()`
- `forcedimension_core.dhd.expert.direct.jointAnglesToGravityJointTorques()`
- `forcedimension_core.dhd.expert.direct.jointAnglesToIntertiaMatrix()`
- `forcedimension_core.dhd.expert.direct.preloadMot()`
- `forcedimension_core.dhd.expert.direct.setJointTorques()`
- `forcedimension_core.dhd.expert.direct.setMot()`
- `forcedimension_core.dhd.expert.direct.wristEncoderToOrientation()`
- `forcedimension_core.dhd.expert.direct.wristEncodersToJointAngles()`
- `forcedimension_core.dhd.expert.direct.wristJointAnglesToEncoders()`
- `forcedimension_core.dhd.expert.direct.wristJointAnglesToJacobian()`
- `forcedimension_core.dhd.expert.direct.wristJointTorquesExtrema()`
- `forcedimension_core.dhd.expert.direct.wristMotorToTorque()`
- `forcedimension_core.dhd.expert.direct.wristOrientationToEncoder()`
- `forcedimension_core.dhd.expert.direct.wristTorqueToMotor()`

DRD functions:

- `forcedimension_core.drd.direct.getPositionAndOrientation()`
- `forcedimension_core.drd.direct.getVelocity()`
- `forcedimension_core.drd.direct.moveTo()`
- `forcedimension_core.drd.direct.moveToAllEnc()`
- `forcedimension_core.drd.direct.track()`
- `forcedimension_core.drd.direct.trackAllEnc()`


## Deprecations

`forcedimension_core.dhd.expert.jointAnglesToGravityJointTorques()` deprecates:
- `forcedimension_core.dhd.expert.deltaGravityJointTorques()`
- `forcedimension_core.dhd.expert.wristGravityJointTorques()`

Device type names have changed. Old style names have been moved to:
- `forcedimension_core.deprecated.constants.DeviceType`


## Breaking Changes

## Refactor forcedimension_core.dhd.adaptors and forcedimension_core.dhd.constants

- `forcedimension_core.dhd.constants` has been refactored into `forcedimension_core.constants`
- Functions in `forcedimension_core.dhd.adaptors` has been refactored into `forcedimension_core.util`
    - `forcedimension_core.dhd.adaptors.errno_to_exception()` -> `forcedimension_core.util.errno_to_exception()`

### SDK v3.16.0 Changes

- `forcedimension_core.constants.MAX_STATUS` is now 17
- `forcedimension_core.constants.MAX_BUTTONS` is now 32
- Four New Errors (and respective exception adadptors):
    - `forcedimension_core.constants.ErrorNum.CONFIGURATION`
    - `forcedimension_core.constants.ErrorNum.INVALID_INDEX`
    - `forcedimension_core.constants.ErrorNum.INVALID`
    - `forcedimension_core.constants.ErrorNum.NO_REGULATION`

### Renames and Removals
Renamed constants:
- `forcedimension_core.dhd.constants.VELOCITY_WINDOWING` has been renamed `forcedimension_core.constants.VelocityEstimatorMode.WINDOWING`
- `forcedimension_core.dhd.constants.VELOCITY_WINDOW` has been renamed `forcedimension_core.constants.DEFAULT_VELOCITY_WINDOW`

Removed types:
- `forcedimension_core.typing.IntVectorLike`
    - Use `forcedimension_core.typing.Array[int, int]` instead
- `forcedimension_core.typing.FloatVectorLike`
    - Use `forcedimension_core.typing.Array[int, float]` instead
- `forcedimension_core.typing.MutableFloatVectorLike`
    - Use `forcedimension_core.typing.MutableArray[int, float]` instead
- `forcedimension_core.typing.MutableFloatMatrixLike`
    - Use `forcedimension_core.typing.Array[int, forcedimension_core.typing.MutableArray[int, float]]` instead

Renamed types:
- `forcedimension_core.typing.DOFTuple` -> `forcedimension_core.typing.IntDOFTuple`

Renamed DRD Functions:
- `drd.getComFreq()` -> `drd.getCtrlFreq()`
- `drd.getLinearVelocity()` -> `drd.getVelocity()`

Removed DHD Functions:
- `forcedimension_core.dhd.os_independent.startThread()`

Removed DRD Functions:
- `forcedimension_core.drd.enableSimulator()`


### Tuple Returns
Tuple returns on many functions have been removed in favor of either
out parameters or negative returns for performance reasons. This has broken
many functions which are shown below. In addition some functions have
been renamed or removed due to accidental misnaming or inclusion.

DHD Breaking Changes:
- `forcedimension_core.dhd.getStatus()`
- `forcedimension_core.dhd.getSerialNumber()`
- `forcedimension_core.dhd.getDeviceAngleRad()`
- `forcedimension_core.dhd.getDeviceAngleDeg()`
- `forcedimension_core.dhd.getEffectorMass()`
- `forcedimension_core.dhd.getButton()`
- `forcedimension_core.dhd.getPosition()`
- `forcedimension_core.dhd.getForce()`
- `forcedimension_core.dhd.getOrientationRad()`
- `forcedimension_core.dhd.getOrientationDeg()`
- `forcedimension_core.dhd.getPositionAndOrientationRad()`
- `forcedimension_core.dhd.getPositionAndOrientationDeg()`
- `forcedimension_core.dhd.getPositionAndOrientationFrame()`
- `forcedimension_core.dhd.getForceAndTorque()`
- `forcedimension_core.dhd.getOrientationFrame()`
- `forcedimension_core.dhd.getGripperAngleRad()`
- `forcedimension_core.dhd.getGripperAngleDeg()`
- `forcedimension_core.dhd.getGripperAngleGap()`
- `forcedimension_core.dhd.getGripperAngleThumbPos()`
- `forcedimension_core.dhd.getGripperAngleFingerPos()`
- `forcedimension_core.dhd.getForceAndTorqueAndGripperForce()`
- `forcedimension_core.dhd.getLinearVelocity()`
- `forcedimension_core.dhd.getAngularVelocityRad()`
- `forcedimension_core.dhd.getAngularVelocityDeg()`
- `forcedimension_core.dhd.getGripperLinearVelocity()`
- `forcedimension_core.dhd.getGripperAngularVelocityRad()`
- `forcedimension_core.dhd.getGripperAngularVelocityDeg()`
- `forcedimension_core.dhd.getBaseAngleXRad()`
- `forcedimension_core.dhd.getBaseAngleXDeg()`
- `forcedimension_core.dhd.getBaseAngleZRad()`
- `forcedimension_core.dhd.getBaseAngleZDeg()`

DHD Expert Mode Breaking Changes:
- `forcedimension_core.dhd.expert.getVelocityThreshold()`
- `forcedimension_core.dhd.expert.getDeltaEncoders()`
- `forcedimension_core.dhd.expert.getWristEncoders()`
- `forcedimension_core.dhd.expert.getGripperEncoder()`
- `forcedimension_core.dhd.expert.deltaEncoderToPosition()`
- `forcedimension_core.dhd.expert.deltaMotorToForce()`
- `forcedimension_core.dhd.expert.deltaForceToMotor()`
- `forcedimension_core.dhd.expert.wristEncoderToOrientation()`
- `forcedimension_core.dhd.expert.wristOrientationToEncoder()`
- `forcedimension_core.dhd.expert.wristMotorToTorque()`
- `forcedimension_core.dhd.expert.wristTorqueToMotor()`
- `forcedimension_core.dhd.expert.gripperEncoderToAngleRad()`
- `forcedimension_core.dhd.expert.gripperEncoderToGap()`
- `forcedimension_core.dhd.expert.gripperAngleRadToEncoder()`
- `forcedimension_core.dhd.expert.gripperGapToEncoder()`
- `forcedimension_core.dhd.expert.gripperMotorToForce()`
- `forcedimension_core.dhd.expert.gripperForceToMotor()`
- `forcedimension_core.dhd.expert.getEnc()`
- `forcedimension_core.dhd.expert.getEncRange()`
- `forcedimension_core.dhd.expert.getDeltaJointAngles()`
- `forcedimension_core.dhd.expert.getDeltaJacobian()`
- `forcedimension_core.dhd.expert.deltaJointAnglesToJacobian()`
- `forcedimension_core.dhd.expert.deltaJointTorquesExtrema()`
- `forcedimension_core.dhd.expert.deltaGravityJointTorques()`
- `forcedimension_core.dhd.expert.deltaEncodersToJointAngles()`
- `forcedimension_core.dhd.expert.deltaJointAnglesToEncoders()`
- `forcedimension_core.dhd.expert.getWristJointAngles()`
- `forcedimension_core.dhd.expert.getWristJacobian()`
- `forcedimension_core.dhd.expert.wristJointAnglesToJacobian()`
- `forcedimension_core.dhd.expert.wristJointTorquesExtrema()`
- `forcedimension_core.dhd.expert.wristGravityJointTorques()`
- `forcedimension_core.dhd.expert.wristEncodersToJointAngles()`
- `forcedimension_core.dhd.expert.wristJointAnglesToEncoders()`
- `forcedimension_core.dhd.expert.getJointAngles()`
- `forcedimension_core.dhd.expert.getJointVelocities()`
- `forcedimension_core.dhd.expert.getEncVelocities()`
- `forcedimension_core.dhd.expert.jointAnglesToIntertiaMatrix()`
- `forcedimension_core.dhd.expert.getWatchdog()`

DRD Breaking Changes:
- `forcedimension_core.drd.getPositionAndOrientation()`
- `forcedimension_core.drd.getLinearVelocity()` -> `forcedimension_core.drd.getVelocity()`

## Bugfixes

The runtime loader now is truly cross platform and has been rigorously tested on all
operating systems. Additional fixes for ctypes bindings were also done.

- Call correct C function for `forcedimension_core.dhd.getVersion()`
- Fix ctypes and argtypes for `forcedimension_core.dhd.openID()`
- Call correct C function for `forcedimension_core.dhd.getGripperAngularVelocityDeg()`
- Call correct C function for `forcedimension_core.dhd.configGripperVelocity()`
- Call correct C function for `forcedimension_core.dhd.getGripperThumbPos()`
- Call correct C function for `forcedimension_core.dhd.setGravityCompensation()`
- Call correct C function for and fix ctypes argtypes and restype for `forcedimension_core.dhd.setDeviceAngleDeg()`
- Call correct C function for and fix ctypes argtypes and restype for `forcedimension_core.dhd.getGripperAngularVelocityDeg()`

- Fix optional timeout logic for for `forcedimension_core.dhd.waitForReset()`

- Call correct C function for and fix ctypes argtypes for `forcedimension_core.dhd.expert.deltaPositionToEncoder()`
- Call correct C function for `forcedimension_core.dhd.expert.wristEncoderToOrientation()`
- Call correct C function for `forcedimension_core.dhd.expert.wristOrientationToEncoder()`
- Call correct C function for`forcedimension_core.dhd.expert.wristMotorToTorque()`
- Call correct C function for `forcedimension_core.dhd.expert.gripperAngleRadToEncoder()`
- Call correct C function and fix ctypes restype for `forcedimension_core.dhd.expert.gripperGapToEncoder()`
- Call correct C function for `forcedimension_core.dhd.expert.gripperMotorToForce()`
- Call correct C function for and add missing ID parameter for `forcedimension_core.dhd.expert.deltaForceToMotor()`
- Call correct C function for and add missing ID parameter for `forcedimension_core.dhd.expert.deltaForceToMotor()`
- Call correct C function for and add missing ID parameter for `forcedimension_core.dhd.expert.wristMotorToTorque()`
- Fix buffer type on `forcedimension_core.dhd.expert.setJointTorques()`


- Call correct C function for `forcedimension_core.drd.isFiltering()`
- Call correct C function and use correct container for `forcedimension_core.dhd.expert.getWatchdog()`

- Fix ctypes argtypes for `forcedimension_core.dhd.direct.setWristMotor()`
- Fix ctypes restype for `forcedimension_core.dhd.direct.getGripperEncoder()`

- Fix ctypes argtypes for `forcedimension_core.drd.stop()`
- Fix ctypes argtypes for `forcedimension_core.drd.getPositionAndOrientation()`
- Fix ctypes argtypes for `forcedimension_core.drd.getPriorities()`
- Fix ctypes restype for `forcedimension_core.drd.isMoving()`
- Add default value for ID paremeter in `forcedimension_core.drd.isSupported()`


# Release 0.1.0 (November 1, 2023)

README.md is updated for clarity.

# Release 0.1.0rc3 (November 1, 2023)

Add proper links for the PyPI version, Python version, and LICENSE badge in the README.md.

# Release 0.1.0rc2 (November 1, 2023)

Fix README.md Python version badge incorrectly linking the wrong PyPI package.

# Release 0.1.0rc1 (November 1, 2023)

Refactor of Force Dimension SDK bindings from the `forcedimension` v0.1.6 package. All functionality is maintained from that release as well as some minor typo fixes.

Targets: Force Dimension SDK 3.14.0+

## Additions

Implemented DHD Functions:
- `forcedimension_core.dhd.close()`
- `forcedimension_core.dhd.configAngularVelocity()`
- `forcedimension_core.dhd.configGripperVelocity()`
- `forcedimension_core.dhd.configLinearVelocity()`
- `forcedimension_core.dhd.emulateButton()`
- `forcedimension_core.dhd.enableForce()`
- `forcedimension_core.dhd.enableGripperForce()`
- `forcedimension_core.dhd.enableSimulator()`
- `forcedimension_core.dhd.errorGetLast()`
- `forcedimension_core.dhd.errorGetLastStr()`
- `forcedimension_core.dhd.errorGetStr()`
- `forcedimension_core.dhd.getAngularVelocityDeg()`
- `forcedimension_core.dhd.getAngularVelocityRad()`
- `forcedimension_core.dhd.getAvailableCount()`
- `forcedimension_core.dhd.getBaseAngleXDeg()`
- `forcedimension_core.dhd.getBaseAngleXRad()`
- `forcedimension_core.dhd.getBaseAngleZDeg()`
- `forcedimension_core.dhd.getBaseAngleZRad()`
- `forcedimension_core.dhd.getButton()`
- `forcedimension_core.dhd.getButtonMask()`
- `forcedimension_core.dhd.getComFreq()`
- `forcedimension_core.dhd.getComMode()`
- `forcedimension_core.dhd.getDeviceAngleDeg()`
- `forcedimension_core.dhd.getDeviceAngleRad()`
- `forcedimension_core.dhd.getDeviceCount()`
- `forcedimension_core.dhd.getDeviceID()`
- `forcedimension_core.dhd.getEffectorMass()`
- `forcedimension_core.dhd.getForce()`
- `forcedimension_core.dhd.getForceAndTorque()`
- `forcedimension_core.dhd.getForceAndTorqueAndGripperForce()`
- `forcedimension_core.dhd.getGripperAngleDeg()`
- `forcedimension_core.dhd.getGripperAngleRad()`
- `forcedimension_core.dhd.getGripperAngularVelocityDeg()`
- `forcedimension_core.dhd.getGripperAngularVelocityRad()`
- `forcedimension_core.dhd.getGripperFingerPos()`
- `forcedimension_core.dhd.getGripperGap()`
- `forcedimension_core.dhd.getGripperLinearVelocity()`
- `forcedimension_core.dhd.getGripperThumbPos()`
- `forcedimension_core.dhd.getLinearVelocity()`
- `forcedimension_core.dhd.getMaxForce()`
- `forcedimension_core.dhd.getMaxGripperForce()`
- `forcedimension_core.dhd.getMaxTorque()`
- `forcedimension_core.dhd.getOrientationDeg()`
- `forcedimension_core.dhd.getOrientationFrame()`
- `forcedimension_core.dhd.getOrientationRad()`
- `forcedimension_core.dhd.getPosition()`
- `forcedimension_core.dhd.getPositionAndOrientationDeg()`
- `forcedimension_core.dhd.getPositionAndOrientationFrame()`
- `forcedimension_core.dhd.getPositionAndOrientationRad()`
- `forcedimension_core.dhd.getSDKVersion()`
- `forcedimension_core.dhd.getSerialNumber()`
- `forcedimension_core.dhd.getStatus()`
- `forcedimension_core.dhd.getSystemName()`
- `forcedimension_core.dhd.getSystemType()`
- `forcedimension_core.dhd.getVersion()`
- `forcedimension_core.dhd.hasActiveGripper()`
- `forcedimension_core.dhd.hasActiveWrist()`
- `forcedimension_core.dhd.hasBase()`
- `forcedimension_core.dhd.hasGripper()`
- `forcedimension_core.dhd.hasWrist()`
- `forcedimension_core.dhd.isLeftHanded()`
- `forcedimension_core.dhd.open()`
- `forcedimension_core.dhd.openID()`
- `forcedimension_core.dhd.openSerial()`
- `forcedimension_core.dhd.openType()`
- `forcedimension_core.dhd.reset()`
- `forcedimension_core.dhd.setBaseAngleXDeg()`
- `forcedimension_core.dhd.setBaseAngleXRad()`
- `forcedimension_core.dhd.setBaseAngleZDeg()`
- `forcedimension_core.dhd.setBaseAngleZRad()`
- `forcedimension_core.dhd.setBrakes()`
- `forcedimension_core.dhd.setDevice()`
- `forcedimension_core.dhd.setDeviceAngleDeg()`
- `forcedimension_core.dhd.setDeviceAngleRad()`
- `forcedimension_core.dhd.setEffectorMass()`
- `forcedimension_core.dhd.setForce()`
- `forcedimension_core.dhd.setForceAndGripperForce()`
- `forcedimension_core.dhd.setForceAndTorque()`
- `forcedimension_core.dhd.setForceAndTorqueAndGripperForce()`
- `forcedimension_core.dhd.setGravityCompensation()`
- `forcedimension_core.dhd.setMaxForce()`
- `forcedimension_core.dhd.setMaxGripperForce()`
- `forcedimension_core.dhd.setMaxTorque()`
- `forcedimension_core.dhd.setOutput()`
- `forcedimension_core.dhd.setStandardGravity()`
- `forcedimension_core.dhd.setVibration()`
- `forcedimension_core.dhd.stop()`
- `forcedimension_core.dhd.waitForReset()`

Implemented DHD Expert Mode Functions:
- `forcedimension_core.dhd.expert.deltaEncoderToPosition()`
- `forcedimension_core.dhd.expert.deltaEncodersToJointAngles()`
- `forcedimension_core.dhd.expert.deltaForceToMotor()`
- `forcedimension_core.dhd.expert.deltaGravityJointTorques()`
- `forcedimension_core.dhd.expert.deltaJointAnglesToEncoders()`
- `forcedimension_core.dhd.expert.deltaJointAnglesToJacobian()`
- `forcedimension_core.dhd.expert.deltaJointTorquesExtrema()`
- `forcedimension_core.dhd.expert.deltaMotorToForce()`
- `forcedimension_core.dhd.expert.deltaPositionToEncoder()`
- `forcedimension_core.dhd.expert.disableExpertMode()`
- `forcedimension_core.dhd.expert.enableExpertMode()`
- `forcedimension_core.dhd.expert.getDeltaEncoders()`
- `forcedimension_core.dhd.expert.getDeltaJacobian()`
- `forcedimension_core.dhd.expert.getDeltaJointAngles()`
- `forcedimension_core.dhd.expert.getEnc()`
- `forcedimension_core.dhd.expert.getEncRange()`
- `forcedimension_core.dhd.expert.getEncVelocities()`
- `forcedimension_core.dhd.expert.getEncoder()`
- `forcedimension_core.dhd.expert.getGripperEncoder()`
- `forcedimension_core.dhd.expert.getJointAngles()`
- `forcedimension_core.dhd.expert.getJointVelocities()`
- `forcedimension_core.dhd.expert.getVelocityThreshold()`
- `forcedimension_core.dhd.expert.getWatchdog()`
- `forcedimension_core.dhd.expert.getWristEncoders()`
- `forcedimension_core.dhd.expert.getWristJacobian()`
- `forcedimension_core.dhd.expert.getWristJointAngles()`
- `forcedimension_core.dhd.expert.gripperAngleRadToEncoder()`
- `forcedimension_core.dhd.expert.gripperEncoderToAngleRad()`
- `forcedimension_core.dhd.expert.gripperEncoderToGap()`
- `forcedimension_core.dhd.expert.gripperForceToMotor()`
- `forcedimension_core.dhd.expert.gripperGapToEncoder()`
- `forcedimension_core.dhd.expert.gripperMotorToForce()`
- `forcedimension_core.dhd.expert.jointAnglesToIntertiaMatrix()`
- `forcedimension_core.dhd.expert.preloadMot()`
- `forcedimension_core.dhd.expert.preset()`
- `forcedimension_core.dhd.expert.setBrk()`
- `forcedimension_core.dhd.expert.setComMode()`
- `forcedimension_core.dhd.expert.setDeltaJointTorques()`
- `forcedimension_core.dhd.expert.setDeltaMotor()`
- `forcedimension_core.dhd.expert.setForceAndWristJointTorques()`
- `forcedimension_core.dhd.expert.setForceAndWristJointTorquesAndGripperForce()`
- `forcedimension_core.dhd.expert.setGripperMotor()`
- `forcedimension_core.dhd.expert.setMot()`
- `forcedimension_core.dhd.expert.setMotor()`
- `forcedimension_core.dhd.expert.setTimeGuard()`
- `forcedimension_core.dhd.expert.setVelocityThreshold()`
- `forcedimension_core.dhd.expert.setWatchdog()`
- `forcedimension_core.dhd.expert.setWristJointTorques()`
- `forcedimension_core.dhd.expert.setWristMotor()`
- `forcedimension_core.dhd.expert.updateEncoders()`
- `forcedimension_core.dhd.expert.wristEncoderToOrientation()`
- `forcedimension_core.dhd.expert.wristEncodersToJointAngles()`
- `forcedimension_core.dhd.expert.wristGravityJointTorques()`
- `forcedimension_core.dhd.expert.wristJointAnglesToEncoders()`
- `forcedimension_core.dhd.expert.wristJointAnglesToJacobian()`
- `forcedimension_core.dhd.expert.wristJointTorquesExtrema()`
- `forcedimension_core.dhd.expert.wristMotorToTorque()`
- `forcedimension_core.dhd.expert.wristOrientationToEncoder()`
- `forcedimension_core.dhd.expert.wristTorqueToMotor()`

Implemented DHD OS Independent Functions:
- `forcedimension_core.dhd.os_independent.getTime()`
- `forcedimension_core.dhd.os_independent.kbGet()`
- `forcedimension_core.dhd.os_independent.kbHit()`
- `forcedimension_core.dhd.os_independent.sleep()`
- `forcedimension_core.dhd.os_independent.startThread()`

Implemented DRD Functions:
- `forcedimension_core.drd.autoInit()`
- `forcedimension_core.drd.checkInit()`
- `forcedimension_core.drd.close()`
- `forcedimension_core.drd.enableFilter()`
- `forcedimension_core.drd.enableSimulator()`
- `forcedimension_core.drd.getComFreq()`
- `forcedimension_core.drd.getDeviceID()`
- `forcedimension_core.drd.getEncDGain()`
- `forcedimension_core.drd.getEncIGain()`
- `forcedimension_core.drd.getEncMoveParam()`
- `forcedimension_core.drd.getEncPGain()`
- `forcedimension_core.drd.getEncTrackParam()`
- `forcedimension_core.drd.getLinearVelocity()`
- `forcedimension_core.drd.getMotRatioMax()`
- `forcedimension_core.drd.getPosMoveParam()`
- `forcedimension_core.drd.getPosTrackParam()`
- `forcedimension_core.drd.getPositionAndOrientation()`
- `forcedimension_core.drd.getPriorities()`
- `forcedimension_core.drd.hold()`
- `forcedimension_core.drd.isFiltering()`
- `forcedimension_core.drd.isInitialized()`
- `forcedimension_core.drd.isMoving()`
- `forcedimension_core.drd.isRunning()`
- `forcedimension_core.drd.isSupported()`
- `forcedimension_core.drd.moveTo()`
- `forcedimension_core.drd.moveToAllEnc()`
- `forcedimension_core.drd.moveToEnc()`
- `forcedimension_core.drd.moveToGrip()`
- `forcedimension_core.drd.moveToPos()`
- `forcedimension_core.drd.moveToRot()`
- `forcedimension_core.drd.open()`
- `forcedimension_core.drd.openID()`
- `forcedimension_core.drd.regulateGrip()`
- `forcedimension_core.drd.regulatePos()`
- `forcedimension_core.drd.regulateRot()`
- `forcedimension_core.drd.setDevice()`
- `forcedimension_core.drd.setEncDGain()`
- `forcedimension_core.drd.setEncIGain()`
- `forcedimension_core.drd.setEncMoveParam()`
- `forcedimension_core.drd.setEncPGain()`
- `forcedimension_core.drd.setEncTrackParam()`
- `forcedimension_core.drd.setMotRatioMax()`
- `forcedimension_core.drd.setPosMoveParam()`
- `forcedimension_core.drd.setPosTrackParam()`
- `forcedimension_core.drd.setPriorities()`
- `forcedimension_core.drd.start()`
- `forcedimension_core.drd.stop()`
