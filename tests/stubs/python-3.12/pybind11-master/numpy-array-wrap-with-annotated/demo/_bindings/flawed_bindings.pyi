from __future__ import annotations

import typing

import pybind11_stubgen.typing_ext

__all__ = [
    "Enum",
    "Unbound",
    "accept_unbound_enum",
    "accept_unbound_enum_defaulted",
    "accept_unbound_type",
    "accept_unbound_type_defaulted",
    "get_unbound_type",
]

class Enum:
    pass

class Unbound:
    pass

def accept_unbound_enum(
    arg0: typing.Annotated[
        typing.Any,
        pybind11_stubgen.typing_ext.InvalidExpr("(anonymous namespace)::Enum"),
    ]
) -> int: ...
def accept_unbound_enum_defaulted(x: Enum = ...) -> int: ...
def accept_unbound_type(
    arg0: tuple[
        typing.Annotated[
            typing.Any,
            pybind11_stubgen.typing_ext.InvalidExpr("(anonymous namespace)::Unbound"),
        ],
        int,
    ]
) -> int: ...
def accept_unbound_type_defaulted(x: Unbound = ...) -> int: ...
def get_unbound_type() -> typing.Annotated[
    typing.Any,
    pybind11_stubgen.typing_ext.InvalidExpr("(anonymous namespace)::Unbound"),
]: ...
