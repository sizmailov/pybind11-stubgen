from __future__ import annotations

import typing as typing

__all__ = ["args_mix", "typing"]

def args_mix(
    a: int,
    b: float = 0.5,
    c: str = "",
    *args: int,
    x: int = 1,
    y=int,
    **kwargs: dict[int, str],
): ...
