from __future__ import annotations

import typing

import pybind11_stubgen.typing_ext

import demo._bindings.classes

__all__ = ["Bar1"]

class Bar1:
    foo: typing.ClassVar[
        demo._bindings.classes.Foo
    ] = pybind11_stubgen.typing_ext.ValueExpr("<demo._bindings.classes.Foo object>")
