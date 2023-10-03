import ctypes as ct
from array import array
from ctypes import c_double, c_int
from typing import Any, Iterable, NamedTuple, Tuple

import pydantic as pyd
import pydantic_core as pyd_core

from forcedimension_core.dhd.constants import MAX_DOF, MAX_STATUS
from forcedimension_core.typing import (
    Pointer, c_double_ptr, c_int_ptr, c_ushort_ptr
)


class VersionTuple(NamedTuple):
    """
    Adapts the four seperate number return into a single grouped
    :class:`typing.NamedTuple`.
    """

    major: int
    minor: int
    release: int
    revision: int

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.release}-{self.revision}"


class Status(ct.Structure):
    """
    Adapts the status array returned by
    :func:`forcedimension.bindings.dhd.getStatus()`
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ptr = ct.cast(ct.pointer(self), c_int_ptr)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: pyd.GetCoreSchemaHandler
    ) -> pyd_core.CoreSchema:
        return pyd_core.core_schema.no_info_after_validator_function(
            cls,
            handler(cls.__init__),
            serialization=pyd_core.core_schema.plain_serializer_function_ser_schema(
                lambda status: tuple(*status)
            )
        )

    @property
    def ptr(self) -> Pointer[c_int]:
        return self._ptr

    def __len__(self) -> int:
        return MAX_STATUS

    def __getitem__(self, i: int) -> int:
        return getattr(self, self._fields_[i][0])

    def __setitem__(self, i: int, val: int):
        setattr(self, self._fields_[i][0], val)

    def __iter__(self):
        for field_name, _ in self._fields_[:-1]:
            yield getattr(self, field_name)

    def __str__(self) -> str:
        return (
            f"Status(power={self.power}, connected={self.connected}, "
            f"started={self.started}, reset={self.reset}, idle={self.idle}, "
            f"force={self.force}, brake={self.brake}, torque={self.torque}, "
            f"wrist_detected={self.wrist_detected}, error={self.error}, "
            f"gravity={self.gravity}, timeguard={self.timeguard}, "
            f"redundancy={self.redundancy}, "
            f"forceoffcause={self.forceoffcause}, locks={self.locks}, "
            f"axis_checked={self.axis_checked})"
        )

    _fields_ = (
        ('power', c_int),
        ('connected', c_int),
        ('started', c_int),
        ('reset', c_int),
        ('idle', c_int),
        ('force', c_int),
        ('brake', c_int),
        ('torque', c_int),
        ('wrist_detected', c_int),
        ('error', c_int),
        ('gravity', c_int),
        ('timeguard', c_int),
        ('wrist_init', c_int),
        ('redundancy', c_int),
        ('forceoffcause', c_int),
        ('locks', c_int),
        ('axis_checked', c_int),

        # Prevents out of bounds access if they expand MAX_STATUS.
        ('__padding', c_int * (32 - MAX_STATUS)),
    )

    #: Indicates if the device is powered or not.
    power: int
    "Indicates if the device is powered or not."

    #: Indicates if the device is connected or not.
    connected: int
    "Indicates if the device is connected or not."

    #: Indicates if the device controller is running or not.
    started: int
    "Indicates if the device controller is running or not."

    #: Indicates if the device is in RESET mode or not.
    #: See device modes for details.
    reset: int
    "1 if the device controller is in RESET mode, 0 otherwise"

    #: Indicates if the device is in IDLE mode or not.
    #: see device modes for details.
    idle: int
    "1 if the device controller is in idle mode or not, 0 otherwise"

    #: Indicates if the device is in force mode or not.
    #: see device modes for details.
    force: int
    "1 if the device controller is in force mode or not, 0 otherwise"

    #: Indicates if the device is in brake mode or not.
    #: see device modes for details.
    brake: int
    "1 if device controller is in break mode or not, 0 otherwise"

    #: indicates if the torques are active or not when the device is
    #: in force mode. see device modes for details.
    torque: int
    "1 if torques are active when the device is in force mode, 0 otherwise"

    #: Indicates if the device has a wrist or not.
    #: see device types for details.
    wrist_detected: int
    "1 if the device has a wrist, 0 otherwise."

    #: Indicates if the an error happened on the device controller.
    error: int
    "1 if an error happend on the device controller, 0 otherwise"

    #: Indicates if the gravity compensation option is enabled or not.
    gravity: int
    "1 if the gravity compensation option is enabled, 0 otherwise"

    #: Indicates if the TimeGuard op is enabled or not.
    #: See TimeGuard op for details.
    timeguard: int
    "1 if the TimeGuard option is enabled, 0 otherwise"

    #: Indicates if the device wrist is initialized or not.
    #: See device types for details.
    wrist_init: int
    "1 if the device wrist is initialized, 0 otherwise."

    #: The status of the redundant encoder consistency check. For devices
    #: equipped with redundant encoders, a value of 1 indicates that the
    #: redundancy check is successful. A value of 0 is reported otherwise, or
    # if the device does not op redundant encoders.
    redundancy: int
    """
    1 if the redundant encoder check was successful. For devices that
    don't op redundant encoders, this value is 0.
    """

    #: The event that caused forces to be disabled on the device (the last time
    #: forces were turned off).
    forceoffcause: int
    """
    The event that caused forces to be disabled on the device (the last time
    forces were turned off).
    """

    #: The status of the locks on supported devices. The value can be either
    #: 1 if the locks are engaged, 0 if the locks are disengagned,
    #: or -1 if the status of the locks is unknown.
    locks: int
    """
    The status of the locks on supported devices. The value can be either
    1 if the locks are engaged, 0 if the locks are disengagned, or -1 if the
    status of the locks is unknown.
    """

    #: A bit vector that indicates the validation status of each axis. The
    #: validation status of all device axes can be assessed by calling the
    #: :func:`forcedimension.drd.checkInit()` function in the Force Dimension
    #: Robotic SDK (DRD). Each bit of the status value returned corresponds
    #: to the validation status of the corresponding axis.
    axis_checked: int
    """
    A bit vector that indicates the validation status of each axis. The
    validation status of all device axes can be assessed by calling the
    drd.checkInit() function in the Force Dimension Robotic SDK (DRD). Each bit
    of the status value returned corresponds to a the validation status of the
    corresponding axis:
    """


class Vector3(array):
    """
    Represents a vector with attributes x, y, and z corresponding to the 0th,
    1st, and 2nd indicies, respectively, as a Python ``array.array``.
    """

    def __new__(
        cls, initializer: Iterable[float] = (0., 0., 0.)
    ):
        if isinstance(initializer, array):
            return initializer

        arr = super(Vector3, cls).__new__(
            cls, 'd', initializer  # type: ignore
        )

        if len(arr) != 3:
            raise ValueError(
                "Vector 3 initializer must be only contain 3 "
                "elements"
            )

        return arr

    def __init__(self, *args, **kwargs):
        ptr = self.buffer_info()[0]
        self._ptrs = (
            ct.cast(ptr, c_double_ptr),
            ct.cast(ptr + self.itemsize, c_double_ptr),
            ct.cast(ptr + 2 * self.itemsize, c_double_ptr),
        )

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: pyd.GetCoreSchemaHandler
    ) -> pyd_core.CoreSchema:
        return pyd_core.core_schema.no_info_after_validator_function(
            cls,
            handler(cls.__init__),
            serialization=pyd_core.core_schema.plain_serializer_function_ser_schema(
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
        """
        Alias to 0th element
        """

        return self[0]

    @x.setter
    def x(self, value: float):
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


class Enc3(array):
    """
    Represents the type of a 3-axis encoder array (e.g. delta or wrist encoder
    arrays) as a Python ``array.array``.
    """

    def __new__(
        cls, initializer: Iterable[int] = (0, 0, 0)
    ):
        if isinstance(initializer, array):
            return initializer

        arr = super(Enc3, cls).__new__(
            cls, 'i', initializer  # type: ignore
        )

        if len(arr) != 3:
            raise ValueError(
                "Vector 3 initializer must be only contain 3 "
                "elements"
            )

        return arr

    def __init__(self, *args, **kwargs):
        ptr = self.buffer_info()[0]
        self._ptrs = (
            ct.cast(ptr, c_int_ptr),
            ct.cast(ptr + self.itemsize, c_int_ptr),
            ct.cast(ptr + 2 * self.itemsize, c_int_ptr),
        )

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: pyd.GetCoreSchemaHandler
    ) -> pyd_core.CoreSchema:
        return pyd_core.core_schema.no_info_after_validator_function(
            cls,
            handler(cls.__init__),
            serialization=pyd_core.core_schema.plain_serializer_function_ser_schema(
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

class Mot3(array):
    """
    Represents an array of motor commands as a Python ``array.array``.
    """

    def __new__(
        cls, initializer: Iterable[int] = tuple(0 for _ in range(3))
    ):
        arr = super(Mot3, cls).__new__(
            cls, 'H', initializer  # type: ignore
        )

        if len(arr) != 3:
            raise ValueError()

        return arr

    def __init__(self, *args, **kwargs):
        ptr = self.buffer_info()[0]
        self._ptrs = (
            ct.cast(ptr, c_ushort_ptr),
            ct.cast(ptr + self.itemsize, c_ushort_ptr),
            ct.cast(ptr + 2 * self.itemsize, c_ushort_ptr),
        )

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: pyd.GetCoreSchemaHandler
    ) -> pyd_core.CoreSchema:
        return pyd_core.core_schema.no_info_after_validator_function(
            cls,
            handler(cls.__init__),
            serialization=pyd_core.core_schema.plain_serializer_function_ser_schema(
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


class Enc4(array):
    """
    Represents an array of wrist encoders and a gripper encoder as a Python
    ``array.array``
    """

    def __new__(
        cls, initializer: Iterable[int] = (0, 0, 0, 0)
    ):
        if isinstance(initializer, array):
            return initializer

        arr = super(Enc4, cls).__new__(
            cls, 'i', initializer  # type: ignore
        )

        if len(arr) != 4:
            raise ValueError()

        return arr

    def __init__(self, *args, **kwargs):
        self._ptr = ct.cast(self.buffer_info()[0], c_int_ptr)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: pyd.GetCoreSchemaHandler
    ) -> pyd_core.CoreSchema:
        return pyd_core.core_schema.no_info_after_validator_function(
            cls,
            handler(cls.__init__),
            serialization=pyd_core.core_schema.plain_serializer_function_ser_schema(
                lambda arr: arr.tolist()
            )
        )

    @property
    def ptr(self) -> c_int_ptr:
        """
        A pointer to the front of the underlying contiguous data.
        """

        return self._ptr


class DOFInt(array):
    """
    Represents an array of encoders for each degree-of-freedom as a Python
    ``array.array``
    """

    def __new__(
        cls, initializer: Iterable[int] = tuple(0 for _ in range(MAX_DOF))
    ):
        arr = super(DOFInt, cls).__new__(
            cls, 'i', initializer  # type: ignore
        )

        if len(arr) != MAX_DOF:
            raise ValueError()

        return arr

    def __init__(self, *args, **kwargs):
        self._ptr = ct.cast(self.buffer_info()[0], c_int_ptr)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: pyd.GetCoreSchemaHandler
    ) -> pyd_core.CoreSchema:
        return pyd_core.core_schema.no_info_after_validator_function(
            cls,
            handler(cls.__init__),
            serialization=pyd_core.core_schema.plain_serializer_function_ser_schema(
                lambda arr: arr.tolist()
            )
        )

    @property
    def ptr(self) -> c_int_ptr:
        """
        A pointer to the front of the underlying contiguous data.
        """

        return self._ptr


class DOFMotorArray(array):
    """
    Represents an array of motor commands as a Python ``array.array``.
    """

    def __new__(
        cls, initializer: Iterable[int] = tuple(0 for _ in range(MAX_DOF))
    ):
        arr = super(DOFMotorArray, cls).__new__(
            cls, 'H', initializer  # type: ignore
        )

        if len(arr) != MAX_DOF:
            raise ValueError()

        return arr

    def __init__(self, *args, **kwargs):
        self._ptr = ct.cast(self.buffer_info()[0], c_ushort_ptr)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: pyd.GetCoreSchemaHandler
    ) -> pyd_core.CoreSchema:
        return pyd_core.core_schema.no_info_after_validator_function(
            cls,
            handler(cls.__init__),
            serialization=pyd_core.core_schema.plain_serializer_function_ser_schema(
                lambda arr: arr.tolist()
            )
        )

    @property
    def ptr(self) -> c_ushort_ptr:
        """
        A pointer to the front of the underlying contiguous data.
        """

        return self._ptr


class DOFFloat(array):
    """
    Represents an array of joint angles as a Python ``array.array``.
    """

    def __new__(
        cls, initializer: Iterable[float] = tuple(0 for _ in range(MAX_DOF))
    ):
        arr = super(DOFFloat, cls).__new__(
            cls, 'd', initializer  # type: ignore
        )

        if len(arr) != MAX_DOF:
            raise ValueError()

        return arr

    def __init__(self, *args, **kwargs):
        self._ptr = ct.cast(self.buffer_info()[0], c_double_ptr)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: pyd.GetCoreSchemaHandler
    ) -> pyd_core.CoreSchema:
        return pyd_core.core_schema.no_info_after_validator_function(
            cls,
            handler(cls.__init__),
            serialization=pyd_core.core_schema.plain_serializer_function_ser_schema(
                lambda arr: arr.tolist()
            )
        )

    @property
    def ptr(self) -> c_double_ptr:
        """
        A pointer to the front of the underlying contiguous data.
        """

        return self._ptr


class Mat3x3(array):
    """
    Represents the type of a coordinate frame matrix as a Python
    ``array.array``.
    """

    def __new__(
        cls, initializer: Iterable[float] = tuple(0. for _ in range(9))
    ):
        if isinstance(initializer, array):
            return initializer

        arr = super(Mat3x3, cls).__new__(
            cls, 'd', initializer  # type: ignore
        )

        if len(arr) != 9:
            raise ValueError(
                "Mat3x3 initializer must be only contain 9 "
                "elements"
            )

        return arr

    def __init__(self, *args, **kwargs):
        self._ptr = ct.cast(self.buffer_info()[0], c_double_ptr)

    def __getitem__(self, indicies: Tuple[int, int]) -> float:
        if not isinstance(indicies, Tuple):
            raise TypeError("Indicies must be a tuple of two ints")

        i, j = indicies

        if not isinstance(i, int):
            raise TypeError("First index is not an int.")

        if not isinstance(j, int):
            raise TypeError("Second index is not an int.")


        return super().__getitem__(3 * i + j)

    def __setitem__(self, indicies: Tuple[int, int], value: float):
        if not isinstance(indicies, Tuple):
            raise TypeError("Indicies must be a tuple of two ints")

        i, j = indicies

        if not isinstance(i, int):
            raise TypeError("First index is not an int.")

        if not isinstance(j, int):
            raise TypeError("Second index is not an int.")

        super().__setitem__(3 * i + j, value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: pyd.GetCoreSchemaHandler
    ) -> pyd_core.CoreSchema:
        return pyd_core.core_schema.no_info_after_validator_function(
            cls,
            handler(cls.__init__),
            serialization=pyd_core.core_schema.plain_serializer_function_ser_schema(
                lambda arr: arr.tolist()
            )
        )

    @property
    def ptr(self) -> c_double_ptr:
        """
        A pointer to the front of the underlying contiguous data.
        """

        return self._ptr


class Mat6x6(array):
    """
    Represents the type of an inertia matrix as a list of Python
    ``array.array``.
    """
    def __new__(
        cls, initializer: Iterable[float] = tuple(0. for _ in range(36))
    ):
        if isinstance(initializer, array):
            return initializer

        arr = super(Mat6x6, cls).__new__(
            cls, 'd', initializer  # type: ignore
        )

        if len(arr) != 36:
            raise ValueError(
                "Mat3x3 initializer must be only contain 36 "
                "elements"
            )

        return arr

    def __init__(self, *args, **kwargs):
        self._ptr = ct.cast(self.buffer_info()[0], c_double_ptr)

    def __getitem__(self, indicies: Tuple[int, int]) -> float:
        if not isinstance(indicies, Tuple):
            raise TypeError("Indicies must be a tuple of two ints")

        i, j = indicies

        if not isinstance(i, int):
            raise TypeError("First index is not an int.")

        if not isinstance(j, int):
            raise TypeError("Second index is not an int.")

        return super().__getitem__(6 * i + j)


    def __setitem__(self, indicies: Tuple[int, int], value: float):
        if not isinstance(indicies, Tuple):
            raise TypeError("Indicies must be a tuple of two ints")

        i, j = indicies

        if not isinstance(i, int):
            raise TypeError("First index is not an int.")

        if not isinstance(j, int):
            raise TypeError("Second index is not an int.")

        super().__setitem__(6 * i + j, value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: pyd.GetCoreSchemaHandler
    ) -> pyd_core.CoreSchema:
        return pyd_core.core_schema.no_info_after_validator_function(
            cls,
            handler(cls.__init__),
            serialization=pyd_core.core_schema.plain_serializer_function_ser_schema(
                lambda arr: arr.tolist()
            )
        )

    @property
    def ptr(self) -> c_double_ptr:
        """
        A pointer to the front of the underlying contiguous data.
        """

        return self._ptr
