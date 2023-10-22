from __future__ import annotations

import numpy
import typing_extensions

__all__ = [
    "accept_ndarray_float64",
    "accept_ndarray_int",
    "get_ndarray_float64",
    "get_ndarray_int",
]

def accept_ndarray_float64(
    arg0: typing_extensions.Annotated[numpy.ndarray, numpy.float64]
) -> None: ...
def accept_ndarray_int(
    arg0: typing_extensions.Annotated[numpy.ndarray, numpy.int32]
) -> None: ...
def get_ndarray_float64() -> typing_extensions.Annotated[
    numpy.ndarray, numpy.float64
]: ...
def get_ndarray_int() -> typing_extensions.Annotated[numpy.ndarray, numpy.int32]: ...
