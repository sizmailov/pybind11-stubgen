from __future__ import annotations

from demo._bindings import (
    aliases,
    classes,
    eigen,
    enum,
    flawed_bindings,
    functions,
    issues,
    methods,
    numpy,
    properties,
    stl,
    stl_bind,
    typing,
    values,
)

from . import _bindings, core

__all__ = [
    "aliases",
    "classes",
    "core",
    "eigen",
    "enum",
    "flawed_bindings",
    "functions",
    "issues",
    "methods",
    "numpy",
    "properties",
    "stl",
    "stl_bind",
    "typing",
    "values",
    "version",
]
version: str = "0.0.0"
