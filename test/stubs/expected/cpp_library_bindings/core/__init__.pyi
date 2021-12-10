from __future__ import annotations
import cpp_library_bindings.core
import typing
from cpp_library_bindings._core import Base
from cpp_library_bindings._core import CppException
from cpp_library_bindings._core import Derived
from cpp_library_bindings._core import Foo
from cpp_library_bindings._core import Outer
import cpp_library_bindings._core
import cpp_library_bindings._core.copy_types
import cpp_library_bindings._core.eigen
import cpp_library_bindings._core.invalid_signatures
import cpp_library_bindings._core.issues
import cpp_library_bindings._core.numeric
import cpp_library_bindings._core.opaque_types
import cpp_library_bindings._core.sublibA

__all__ = [
    "Base",
    "CppException",
    "Derived",
    "Foo",
    "Outer",
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
    "sublibA"
]


foolist: list # value = [<cpp_library_bindings._core.Foo object>, <cpp_library_bindings._core.Foo object>]
foovar: cpp_library_bindings._core.Foo
list_with_none = [None, 2, {}]
none = None
