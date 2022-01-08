from __future__ import annotations
import cpp_library_bindings._core.eigen
import typing
import numpy
_Shape = typing.Tuple[int, ...]

__all__ = [
    "accept_matrix_int",
    "accept_vector_float64",
    "get_matrix_int",
    "get_vector_float64"
]


def accept_matrix_int(arg0: numpy.ndarray[numpy.int32, _Shape[3, 3]]) -> None:
    pass
def accept_vector_float64(arg0: numpy.ndarray[numpy.float64, _Shape[3, 1]]) -> None:
    pass
def get_matrix_int() -> numpy.ndarray[numpy.int32, _Shape[3, 3]]:
    pass
def get_vector_float64() -> numpy.ndarray[numpy.float64, _Shape[3, 1]]:
    pass
