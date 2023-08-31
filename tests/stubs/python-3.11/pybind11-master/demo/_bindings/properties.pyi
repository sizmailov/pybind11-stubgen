from __future__ import annotations

import typing

__all__ = ["Dummy"]

class Dummy:
    def_property_readonly_static: typing.ClassVar[int] = 0
    def_property_static: typing.ClassVar[int] = 0
    def_property: int
    def_readwrite: int
    @property
    def def_property_readonly(arg0: Dummy) -> int: ...
    @property
    def def_readonly(self) -> int: ...
