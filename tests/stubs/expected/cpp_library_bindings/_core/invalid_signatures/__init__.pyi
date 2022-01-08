from __future__ import annotations
import cpp_library_bindings._core.invalid_signatures
import typing

__all__ = [
    "Enum",
    "Unbound",
    "accept_unbound_enum",
    "accept_unbound_enum_defaulted",
    "accept_unbound_type",
    "accept_unbound_type_defaulted",
    "get_unbound_type"
]


class Enum():
    pass
class Unbound():
    pass
def accept_unbound_enum(*args, **kwargs) -> typing.Any:
    pass
def accept_unbound_enum_defaulted(x: Enum = ...) -> int:
    pass
def accept_unbound_type(arg0: typing.Tuple[forgotten::Unbound, int]) -> int:
    pass
def accept_unbound_type_defaulted(x: Unbound = ...) -> int:
    pass
def get_unbound_type(*args, **kwargs) -> typing.Any:
    pass
