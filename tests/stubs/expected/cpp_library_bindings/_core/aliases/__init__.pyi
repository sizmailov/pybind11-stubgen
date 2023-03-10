from __future__ import annotations

import typing

import cpp_library_bindings._core.aliases

__all__ = ["Color", "Colour"]

class Color:
    @property
    def value(self) -> int:
        """
        :type: int
        """
    @value.setter
    def value(self, arg0: int) -> None:
        pass
    pass

Colour = cpp_library_bindings._core.aliases.Color
