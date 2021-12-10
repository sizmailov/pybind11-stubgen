from __future__ import annotations
import cpp_library_bindings._core.numeric
import typing
import numpy
_Shape = typing.Tuple[int, ...]

__all__ = [
    "accept_ndarray_float64",
    "accept_ndarray_int",
    "get_ndarray_float64",
    "get_ndarray_int"
]


def accept_ndarray_float64(arg0: numpy.ndarray[numpy.float64]) -> None:
    pass
def accept_ndarray_int(arg0: numpy.ndarray[numpy.int32]) -> None:
    pass
def get_ndarray_float64() -> numpy.ndarray[numpy.float64]:
    pass
def get_ndarray_int() -> numpy.ndarray[numpy.int32]:
    pass
