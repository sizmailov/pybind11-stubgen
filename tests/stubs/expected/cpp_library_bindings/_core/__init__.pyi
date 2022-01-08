from __future__ import annotations
import cpp_library_bindings._core
import typing
import numpy.linalg

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


class Base():
    class Inner():
        pass
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @name.setter
    def name(self, arg0: str) -> None:
        pass
    pass
class CppException(Exception, BaseException):
    pass
class Derived(Base):
    @property
    def count(self) -> int:
        """
        :type: int
        """
    @count.setter
    def count(self, arg0: int) -> None:
        pass
    pass
class Foo():
    class FooChild():
        def __init__(self) -> None: ...
        def g(self) -> None: ...
        pass
    def __init__(self) -> None: ...
    def f(self) -> None: ...
    pass
class Outer():
    class Inner():
        class NestedEnum():
            """
            Members:

              ONE

              TWO
            """
            def __eq__(self, other: object) -> bool: ...
            def __getstate__(self) -> int: ...
            def __hash__(self) -> int: ...
            def __index__(self) -> int: ...
            def __init__(self, value: int) -> None: ...
            def __int__(self) -> int: ...
            def __ne__(self, other: object) -> bool: ...
            def __repr__(self) -> str: ...
            def __setstate__(self, state: int) -> None: ...
            @property
            def name(self) -> str:
                """
                :type: str
                """
            @property
            def value(self) -> int:
                """
                :type: int
                """
            ONE: cpp_library_bindings._core.Outer.Inner.NestedEnum # value = <NestedEnum.ONE: 1>
            TWO: cpp_library_bindings._core.Outer.Inner.NestedEnum # value = <NestedEnum.TWO: 2>
            __members__: dict # value = {'ONE': <NestedEnum.ONE: 1>, 'TWO': <NestedEnum.TWO: 2>}
            pass
        @property
        def value(self) -> Outer.Inner.NestedEnum:
            """
            :type: Outer.Inner.NestedEnum
            """
        @value.setter
        def value(self, arg0: Outer.Inner.NestedEnum) -> None:
            pass
        pass
    @property
    def inner(self) -> Outer.Inner:
        """
        :type: Outer.Inner
        """
    @inner.setter
    def inner(self, arg0: Outer.Inner) -> None:
        pass
    linalg = numpy.linalg
    pass
foolist: list # value = [<cpp_library_bindings._core.Foo object>, <cpp_library_bindings._core.Foo object>]
foovar: cpp_library_bindings._core.Foo
list_with_none = [None, 2, {}]
none = None
