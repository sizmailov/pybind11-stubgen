from __future__ import annotations

import typing

import cpp_library_bindings._core
import cpp_library_bindings._core.aliases
import cpp_library_bindings._core.copy_types
import cpp_library_bindings._core.eigen
import cpp_library_bindings._core.invalid_signatures
import cpp_library_bindings._core.issues
import cpp_library_bindings._core.numeric
import cpp_library_bindings._core.opaque_types
import cpp_library_bindings._core.protocols
import cpp_library_bindings._core.std_array
import cpp_library_bindings._core.sublibA
import cpp_library_bindings.core
from cpp_library_bindings._core import Base, CppException, Derived, Foo, Outer

__all__ = [
    "Base",
    "Colour",
    "CppException",
    "Derived",
    "Foo",
    "Outer",
    "aliases",
    "copy_types",
    "eigen",
    "foolist",
    "foovar",
    "invalid_signatures",
    "issues",
    "list_with_none",
    "none",
    "numeric",
    "opaque_types",
    "protocols",
    "std_array",
    "sublibA",
]

foolist: list  # value = [<cpp_library_bindings._core.Foo object>, <cpp_library_bindings._core.Foo object>]
foovar: cpp_library_bindings._core.Foo
list_with_none = [None, 2, {}]
none = None
Colour = cpp_library_bindings._core.aliases.Color
