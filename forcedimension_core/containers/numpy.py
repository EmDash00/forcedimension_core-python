from __future__ import annotations

import ctypes
from ctypes import c_double, c_int, c_ushort
from typing import Any, Tuple

try:
    import numpy as np
    import numpy.typing as npt
except ModuleNotFoundError as ex:
    raise ImportError(
        "Optional dependency numpy as not found. NumPy containers not "
        "available. Use the basic containers instead."
    ) from ex

import pydantic as pyd
import pydantic_core as pyd_core
from pydantic_core import core_schema as _core_schema

from forcedimension_core.constants import MAX_DOF
from forcedimension_core.typing import (
    Array, c_double_ptr, c_int_ptr, c_ushort_ptr
)


class Vec3(np.ndarray):
    """
    Represents an array of three C floats as a view over a
    :class:`numpy.ndarray`. Typically used by functions which
    return a vector or take a vector. Can also be used by
    functions which convert a set of 3 float such as in the
    functions which get orientation.
    """

    def __new__(cls, data: npt.ArrayLike = (0., 0., 0.)):
        arr = np.ascontiguousarray(data, dtype=c_double).view(cls)

        if len(arr) != 3:
            raise ValueError

        return arr

    def __init__(self, *args, **kwargs):
        super().__init__()

        self._ptrs = (
            ctypes.cast(self.ctypes.data, c_double_ptr),
            ctypes.cast(self.ctypes.data + self.itemsize, c_double_ptr),
            ctypes.cast(self.ctypes.data + 2 * self.itemsize, c_double_ptr)
        )

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: pyd.GetCoreSchemaHandler
    ) -> pyd_core.CoreSchema:
        return _core_schema.no_info_plain_validator_function(
            cls,
            serialization=_core_schema.plain_serializer_function_ser_schema(
                lambda arr: arr.tolist()
            )
        )

    @property
    def ptr(self) -> c_double_ptr:
        """
        A pointer to the front of the array.
        """

        return self._ptrs[0]

    @property
    def ptrs(self) -> Tuple[c_double_ptr, c_double_ptr, c_double_ptr]:
        """
        A tuple of pointers to each element of the array in order.
        """

        return self._ptrs

    @property
    def x(self) -> float:
        return self[0]

    @x.setter
    def x(self, value: float):
        """
        Alias to 0th element
        """

        self[0] = value

    @property
    def y(self) -> float:
        """
        Alias to 1st element
        """

        return self[1]

    @y.setter
    def y(self, value: float):
        self[1] = value

    @property
    def z(self) -> float:
        """
        Alias to 2nd element
        """

        return self[2]

    @z.setter
    def z(self, value: float):
        self[2] = value


class Enc3(np.ndarray):
    """
    Represents an array of three C ints as a view over a
    :class:`numpy.ndarray`. Typically used by functions which
    return information about encoders from the WRIST or DELTA
    structure.
    """

    def __new__(cls, data: npt.ArrayLike = (0., 0., 0.)):
        arr = np.ascontiguousarray(data, dtype=c_int).view(cls)

        if len(arr) != 3:
            raise ValueError

        return arr

    def __init__(self, *args, **kwargs):
        super().__init__()

        self._ptrs = (
            ctypes.cast(self.ctypes.data, c_int_ptr),
            ctypes.cast(self.ctypes.data + self.itemsize, c_int_ptr),
            ctypes.cast(self.ctypes.data + 2 * self.itemsize, c_int_ptr)
        )

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: pyd.GetCoreSchemaHandler
    ) -> pyd_core.CoreSchema:
        return _core_schema.no_info_plain_validator_function(
            cls,
            serialization=_core_schema.plain_serializer_function_ser_schema(
                lambda arr: arr.tolist()
            )
        )

    @property
    def ptr(self) -> c_int_ptr:
        """
        A pointer to the front of the array.
        """

        return self._ptrs[0]

    @property
    def ptrs(self) -> Tuple[c_int_ptr, c_int_ptr, c_int_ptr]:
        """
        A tuple of pointers to each element of the array in order.
        """

        return self._ptrs


class Mot3(np.ndarray):
    """
    Represents an array of three C ushorts as a view over a
    :class:`numpy.ndarray`. Typically used functions which take
    motor commands or convert motor commands to forces (and vice
    versa). In those functions, represents an array of motor
    commands for each axis of the delta or wrist structure.
    """

    def __new__(cls, data: npt.ArrayLike = (0., 0., 0.)):
        arr = np.ascontiguousarray(data, dtype=c_ushort).view(cls)

        if len(arr) != 3:
            raise ValueError

        return arr

    def __init__(self, *args, **kwargs):
        super().__init__()

        self._ptrs = (
            ctypes.cast(self.ctypes.data, c_ushort_ptr),
            ctypes.cast(self.ctypes.data + self.itemsize, c_ushort_ptr),
            ctypes.cast(self.ctypes.data + 2 * self.itemsize, c_ushort_ptr)
        )

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: pyd.GetCoreSchemaHandler
    ) -> pyd_core.CoreSchema:
        return _core_schema.no_info_plain_validator_function(
            cls,
            serialization=_core_schema.plain_serializer_function_ser_schema(
                lambda arr: arr.tolist()
            )
        )

    @property
    def ptr(self) -> c_ushort_ptr:
        """
        A pointer to the front of the array.
        """

        return self._ptrs[0]

    @property
    def ptrs(self) -> Tuple[c_ushort_ptr, c_ushort_ptr, c_ushort_ptr]:
        """
        A tuple of pointers to each element of the array in order.
        """

        return self._ptrs


class Enc4(np.ndarray):
    """
    Represents an array of four C ints as a view over a
    :class:`numpy.ndarray`. Typically used functions which
    convert gripper motor commands to forces and vice versa.
    """

    def __new__(cls, data: npt.ArrayLike = (0., 0., 0., 0.)):
        arr = np.ascontiguousarray(data, dtype=c_int).view(cls)

        if len(arr) != 4:
            raise ValueError

        return arr

    def __init__(self, *args, **kwargs):
        super().__init__()

        self._ptr = ctypes.cast(self.ctypes.data, c_int_ptr)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: pyd.GetCoreSchemaHandler
    ) -> pyd_core.CoreSchema:
        return _core_schema.no_info_plain_validator_function(
            cls,
            serialization=_core_schema.plain_serializer_function_ser_schema(
                lambda arr: arr.tolist()
            )
        )

    @property
    def ptr(self) -> c_int_ptr:
        """
        A pointer to the front of the underlying contiguous data.
        """

        return self._ptr


class DOFInt(np.ndarray):
    """
    Represents an array of C ints, one for each
    degree-of-freedom as a view over a :class:`numpy.ndarray`.
    Typically used by functions that get encoder values for each
    degree-of-freedom
    """

    def __new__(cls, data: Array[int, int] = tuple(0 for _ in range(MAX_DOF))):
        arr = np.ascontiguousarray(data, dtype=c_int).view(cls)

        if len(arr) != MAX_DOF:
            raise ValueError()

        return arr

    def __init__(self, *args, **kwargs):
        super().__init__()

        self._ptr = ctypes.cast(self.ctypes.data, c_int_ptr)
        self._delta = Enc3(self[:3])
        self._wrist = Enc3(self[3:6])
        self._wrist_grip = Enc4(self[3:7])

        self._gripper = ctypes.cast(
            self.ctypes.data + 7 * self.itemsize, c_int_ptr
        ).contents

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: pyd.GetCoreSchemaHandler
    ) -> pyd_core.CoreSchema:
        return _core_schema.no_info_plain_validator_function(
            cls,
            serialization=_core_schema.plain_serializer_function_ser_schema(
                lambda arr: arr.tolist()
            )
        )

    @property
    def ptr(self) -> c_int_ptr:
        return self._ptr

    @property
    def delta(self) -> Enc3:
        """
        A view over the part of the buffer that corresponds to the
        degrees-of-freedom typically associated with the DELTA
        structure.
        """
        return self._delta

    @property
    def wrist(self) -> Enc3:
        """
        A view over the part of the buffer that corresponds to the
        degrees-of-freedom typically associated with the WRIST
        structure.
        """

        return self._wrist

    @property
    def wrist_grip(self) -> Enc4:
        """
        A view over the part of the buffer that corresponds to the
        degrees-of-freedom typically associated with the WRIST structure
        and the gripper.
        """

        return self._wrist_grip

    @property
    def gripper(self) -> c_int:
        """
        A view over the part of the buffer that corresponds to the
        degrees-of-freedom typically associated with the gripper.
        """

        return self._gripper


class DOFMotor(np.ndarray):
    """
    Represents an array of C unsigned shorts, one for each
    degree-of-freedom  as a view over a :class:`numpy.ndarray`.
    Typically used by functions that request motor commands for
    each degree-of-freedom.
    """

    def __new__(cls, data: Array[int, int] = tuple(0 for _ in range(MAX_DOF))):
        arr = np.ascontiguousarray(data, dtype=c_ushort).view(cls)

        if len(arr) != MAX_DOF:
            raise ValueError()

        return arr

    def __init__(self, *args, **kwargs):
        super().__init__()

        self._ptr = ctypes.cast(self.ctypes.data, c_ushort_ptr)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: pyd.GetCoreSchemaHandler
    ) -> pyd_core.CoreSchema:
        return _core_schema.no_info_plain_validator_function(
            cls,
            serialization=_core_schema.plain_serializer_function_ser_schema(
                lambda arr: arr.tolist()
            )
        )

    @property
    def ptr(self) -> c_ushort_ptr:
        return self._ptr


class DOFFloat(np.ndarray):
    """
    Represents an array of floats, one for each
    degree-of-freedom as a view over a :class:`numpy.array`.
    Typically used by functions that request joint angles or
    linear/angular velocities for each  degree-of-freedom.
    """

    def __new__(
        cls, data: npt.ArrayLike = tuple(0. for _ in range(MAX_DOF))
    ):
        arr = np.ascontiguousarray(data, dtype=c_double).view(cls)

        if len(arr) != MAX_DOF:
            raise ValueError()

        return arr

    def __init__(self, *args, **kwargs):
        super().__init__()

        self._ptr = ctypes.cast(self.ctypes.data, c_double_ptr)

        self._delta = Vec3(self[:3])
        self._wrist = Vec3(self[3:6])
        self._gripper = ctypes.cast(
            self.ctypes.data + 7 * self.itemsize, c_double_ptr
        ).contents

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: pyd.GetCoreSchemaHandler
    ) -> pyd_core.CoreSchema:
        return _core_schema.no_info_plain_validator_function(
            cls,
            serialization=_core_schema.plain_serializer_function_ser_schema(
                lambda arr: arr.tolist()
            )
        )

    @property
    def ptr(self) -> c_double_ptr:
        """
        A pointer to the front of the underlying contiguous data.
        """

        return self._ptr

    @property
    def delta(self) -> Vec3:
        """
        A view over the part of the buffer that corresponds to the
        degrees-of-freedom typically associated with the DELTA structure.
        """

        return self._delta

    @property
    def wrist(self) -> Vec3:
        """
        A view over the part of the buffer that corresponds to the
        degrees-of-freedom typically associated with the WRIST structure.
        """

        return self._wrist

    @property
    def gripper(self) -> c_double:
        """
        A view over the part of the buffer that corresponds to the
        degrees-of-freedom typically associated with the gripper.
        """

        return self._gripper


class Mat3x3(np.ndarray):
    """
    Represents the type of a 3x3 matrix of floats as a view
    over a :class:`numpy.ndarray``. Typically used to represent
    a 3x3 coordinate frame matrix.
    """

    def __new__(cls, data: npt.ArrayLike = tuple(0. for _ in range(9))):
        arr = np.ascontiguousarray(data, dtype=c_double)

        if arr.size != 9:
            raise ValueError()

        return arr.reshape((3, 3)).view(cls)

    def __init__(self, *args, **kwargs):
        super().__init__()

        self._ptr = ctypes.cast(self.ctypes.data, c_double_ptr)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: pyd.GetCoreSchemaHandler
    ) -> pyd_core.CoreSchema:
        return _core_schema.no_info_plain_validator_function(
            cls,
            serialization=_core_schema.plain_serializer_function_ser_schema(
                lambda arr: arr.tolist()
            )
        )

    @property
    def ptr(self) -> c_double_ptr:
        """
        A pointer to the front of the underlying contiguous data.
        """

        return self._ptr


class Mat6x6(np.ndarray):
    """
    Represents the type of a 6x6 matrix of floats as a view over
    a :class:`numpy.ndarray`. Typically used to represent a 6x6
    inertia matrix.
    """

    def __new__(cls, data: npt.ArrayLike = tuple(0. for _ in range(36))):
        arr = np.ascontiguousarray(data, dtype=c_double)

        if arr.size != 36:
            raise ValueError()

        return arr.reshape((6, 6)).view(cls)

    def __init__(self, *args, **kwargs):
        super().__init__()

        self._ptr = ctypes.cast(self.ctypes.data, c_double_ptr)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: pyd.GetCoreSchemaHandler
    ) -> pyd_core.CoreSchema:
        return _core_schema.no_info_plain_validator_function(
            cls,
            serialization=_core_schema.plain_serializer_function_ser_schema(
                lambda arr: arr.tolist()
            )
        )

    @property
    def ptr(self) -> c_double_ptr:
        """
        A pointer to the front of the underlying contiguous data.
        """

        return self._ptr
