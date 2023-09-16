import ctypes as ct
from ctypes import c_double, c_int, c_ubyte, c_uint, c_ushort
from typing import (
    TYPE_CHECKING, Container, Generic, List, Literal, Protocol, Sized, Tuple,
    TypeVar, Union
)


_KT_contra = TypeVar("_KT_contra", contravariant=True)
_VT = TypeVar("_VT")
_VT_co = TypeVar("_VT_co", covariant=True)


class Array(Sized, Container[_VT_co], Protocol[_KT_contra, _VT_co]):
    def __getitem__(self, __k: _KT_contra) -> _VT_co: ...


class MutableArray(
    Array[_KT_contra, _VT], Protocol[_KT_contra, _VT]
):
    def __setitem__(self, __k: _KT_contra, __v: _VT) -> None: ...


if not TYPE_CHECKING:
    class Pointer:
        @classmethod
        def __class_getitem__(cls, item):

            # Don't try to resolve generic types at runtime.
            # They only matter for typing anyways.
            if isinstance(item, TypeVar):
                return None

            return ct.POINTER(item)

    CType = TypeVar('CType')
else:
    #: Generic type representing a C pointer
    Pointer = ct._Pointer

    #: Generic type representing a C data type (e.g. int, float, etc.)
    CType = TypeVar('CType', bound=ct._CData)

c_double_ptr = Pointer[c_double]
c_ubyte_ptr = Pointer[c_ubyte]
c_ushort_ptr = Pointer[c_ushort]
c_int_ptr = Pointer[c_int]
c_uint_ptr = Pointer[c_uint]


class SupportsPtr(Protocol, Generic[CType]):
    """
    A type which supports direct memory addressing of the front of a contiguous
    array.
    """

    @property
    def ptr(self) -> Pointer[CType]:
        ...


class SupportsPtrs3(Protocol, Generic[CType]):
    """
    A type which supports direct memory addressing of its stored values.
    """

    @property
    def ptrs(self) -> Tuple[
        Pointer[CType], Pointer[CType], Pointer[CType]
    ]:
        ...

#: Represents the type of a homogenous array of floats
#: specifically, it implements ``__getitem__`` and ``__len__``
CFloatArrayLike = Array[int, float]

#: Represents the type of a homogenous array of ints
#: specifically, it implements ``__getitem__`` and ``__len__``
CIntArrayLike = Array[int, int]

#: Represents the type of a mutable homogenous array of floats
#: specifically, it implements ``__setitem__``, ``__getitem__``, and
#: ``__len__``
MutableCFloatArrayLike = MutableArray[int, float]

#: Represents the type of a mutable homogenous array of ints
#: specifically, it implements ``__setitem__``, ``__getitem__``, and
#: ``__len__``
MutableCIntArrayLike = MutableArray[int, int]


#: Represents a 2D array of floats
MutableCFloatArray2DLike = MutableArray[int, MutableCFloatArrayLike]


#: Represents a tuple of integers, one for each DOF.
IntDOFTuple = Tuple[int, int, int, int, int, int, int, int]

#: Represents a tuple of floats, one for each DOF.
FloatDOFTuple = Tuple[float, float, float, float, float, float, float, float]
