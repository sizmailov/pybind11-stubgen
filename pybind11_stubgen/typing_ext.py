from __future__ import annotations

from typing import Any


class FixedSize:
    def __init__(self, *dim: int):
        self.dim: tuple[int, ...] = dim

    def __repr__(self):
        return (
            f"{self.__module__}."
            f"{self.__class__.__qualname__}"
            f"({', '.join(str(d) for d in self.dim)})"
        )


class DynamicSize:
    def __init__(self, *dim: int | str):
        self.dim: tuple[int | str, ...] = dim

    def __repr__(self):
        return (
            f"{self.__module__}."
            f"{self.__class__.__qualname__}"
            f"({', '.join(repr(d) for d in self.dim)})"
        )


def InvalidExpr(expr: str) -> Any:
    raise RuntimeError(
        "The method exists only for annotation purposes in stub files. "
        "Should never not be used at runtime"
    )


def ValueExpr(expr: str) -> Any:
    raise RuntimeError(
        "The method exists only for annotation purposes in stub files. "
        "Should never not be used at runtime"
    )
