from __future__ import annotations

import typing

__all__ = [
    "WithGetterSetterDoc",
    "WithPropAndGetterSetterDoc",
    "WithPropDoc",
    "WithoutDoc",
]

class WithGetterSetterDoc:
    """
    User docstring provided via pybind11::cpp_function(..., doc) to getters/setters, but NOT to `def_*(..., doc)` calls
    """

    def_property_readonly_static: typing.ClassVar[int] = 0
    def_property_static: typing.ClassVar[int] = 0
    @property
    def def_property(self) -> int:
        """
        getter doc token
        """
    @def_property.setter
    def def_property(self, arg1: int) -> None:
        """
        setter doc token
        """
    @property
    def def_property_readonly(self) -> int:
        """
        getter doc token
        """

class WithPropAndGetterSetterDoc:
    """
    User docstring provided via pybind11::cpp_function(..., doc) to getters/setters and to `def_*(, doc)` calls
    """

    def_property_readonly_static: typing.ClassVar[int] = 0
    def_property_static: typing.ClassVar[int] = 0
    @property
    def def_property(self) -> int:
        """
        prop doc token
        """
    @def_property.setter
    def def_property(self, arg1: int) -> None: ...
    @property
    def def_property_readonly(self) -> int:
        """
        prop doc token
        """

class WithPropDoc:
    """
    User docstring provided only to `def_` calls
    """

    def_property_readonly_static: typing.ClassVar[int] = 0
    def_property_static: typing.ClassVar[int] = 0
    @property
    def def_property(self) -> int:
        """
        prop doc token
        """
    @def_property.setter
    def def_property(self, arg1: int) -> None: ...
    @property
    def def_property_readonly(self) -> int:
        """
        prop doc token
        """
    @property
    def def_readonly(self) -> int:
        """
        prop doc token
        """
    @property
    def def_readwrite(self) -> int:
        """
        prop doc token
        """
    @def_readwrite.setter
    def def_readwrite(self, arg0: int) -> None: ...

class WithoutDoc:
    """
    No user docstring provided
    """

    def_property_readonly_static: typing.ClassVar[int] = 0
    def_property_static: typing.ClassVar[int] = 0
    def_property: int
    def_readwrite: int
    @property
    def def_property_readonly(self) -> int: ...
    @property
    def def_readonly(self) -> int: ...
