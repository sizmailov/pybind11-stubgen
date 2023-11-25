from __future__ import annotations

import typing as typing

import pybind11_stubgen.typing_ext

__all__ = ["args_mix", "typing"]

def args_mix(
    a: int,
    b: float = 0.5,
    c: str = "",
    *args: int,
    x: int = 1,
    y=int,
    **kwargs: pybind11_stubgen.typing_ext.ValueExpr("typing.Dict[int, str]"),
): ...
