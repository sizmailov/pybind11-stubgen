from __future__ import annotations

import typing

import pybind11_stubgen.typing_ext

__all__ = ["ConsoleForegroundColor", "Magenta", "accepts_ambiguous_enum"]

class ConsoleForegroundColor:
    """
    Members:

      Magenta
    """

    Magenta: typing.ClassVar[
        ConsoleForegroundColor
    ] = pybind11_stubgen.typing_ext.ValueExpr("<ConsoleForegroundColor.Magenta: 35>")
    __members__: typing.ClassVar[
        dict[str, ConsoleForegroundColor]
    ] = pybind11_stubgen.typing_ext.ValueExpr(
        "{'Magenta': <ConsoleForegroundColor.Magenta: 35>}"
    )
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

def accepts_ambiguous_enum(
    color: ConsoleForegroundColor = pybind11_stubgen.typing_ext.InvalidExpr(
        "<ConsoleForegroundColor.Magenta: 35>"
    ),
) -> None: ...

Magenta: ConsoleForegroundColor = pybind11_stubgen.typing_ext.ValueExpr(
    "<ConsoleForegroundColor.Magenta: 35>"
)
