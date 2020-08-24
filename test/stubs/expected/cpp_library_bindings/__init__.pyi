import cpp_library_bindings
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
import cpp_library_bindings._core.numeric
import cpp_library_bindings._core.opaque_types
import cpp_library_bindings._core.sublibA
__all__  = [
"Base",
"CppException",
"Derived",
"Foo",
"Outer",
"_core",
"core",
"foolist",
"foovar",
"version"
]
foolist: list # value = [<cpp_library_bindings._core.Foo object>, <cpp_library_bindings._core.Foo object>]
foovar: cpp_library_bindings._core.Foo
version = '0.0.0'
