from __future__ import annotations

import pybind11_stubgen.typing_ext

import demo._bindings.classes

__all__ = ["value"]
value: demo._bindings.classes.Foo = pybind11_stubgen.typing_ext.ValueExpr(
    "<demo._bindings.classes.Foo object>"
)
