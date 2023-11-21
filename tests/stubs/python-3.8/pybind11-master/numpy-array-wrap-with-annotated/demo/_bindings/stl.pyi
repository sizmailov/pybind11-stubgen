from __future__ import annotations

import typing

import pybind11_stubgen.typing_ext
import typing_extensions

__all__ = ["std_array", "std_map", "std_optional", "std_variant", "std_vector"]

def std_array(
    arg0: typing_extensions.Annotated[
        list[int], pybind11_stubgen.typing_ext.FixedSize(3)
    ]
) -> typing_extensions.Annotated[
    list[int], pybind11_stubgen.typing_ext.FixedSize(3)
]: ...
def std_map() -> dict[int, complex]: ...
def std_optional(arg0: int | None) -> None: ...
def std_variant(arg0: int | float | tuple[int, int]) -> None: ...
def std_vector() -> list[tuple[int, float]]: ...
