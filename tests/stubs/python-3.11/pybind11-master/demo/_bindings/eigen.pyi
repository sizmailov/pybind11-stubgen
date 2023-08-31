from __future__ import annotations

import typing

import numpy
import pybind11_stubgen.typing_ext

__all__ = [
    "accept_matrix_int",
    "accept_vector_float64",
    "get_matrix_int",
    "get_vector_float64",
]

def accept_matrix_int(
    arg0: typing.Annotated[
        numpy.ndarray, numpy.int32, pybind11_stubgen.typing_ext.FixedSize(3, 3)
    ]
) -> None: ...
def accept_vector_float64(
    arg0: typing.Annotated[
        numpy.ndarray, numpy.float64, pybind11_stubgen.typing_ext.FixedSize(3, 1)
    ]
) -> None: ...
def get_matrix_int() -> typing.Annotated[
    numpy.ndarray, numpy.int32, pybind11_stubgen.typing_ext.FixedSize(3, 3)
]: ...
def get_vector_float64() -> typing.Annotated[
    numpy.ndarray, numpy.float64, pybind11_stubgen.typing_ext.FixedSize(3, 1)
]: ...
