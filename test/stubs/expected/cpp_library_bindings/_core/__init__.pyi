import cpp_library_bindings._core
from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64
_Shape = Tuple[int, ...]
__all__  = [
"Base",
"CppException",
"Derived",
"Foo",
"Outer",
"sublibA",
"foolist",
"foovar"
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
            def __init__(self, arg0: int) -> None: ...
            def __int__(self) -> int: ...
            @property
            def name(self) -> str:
                """
                (self: handle) -> str

                :type: str
                """
            ONE: cpp_library_bindings._core.Outer.Inner.NestedEnum # value = NestedEnum.ONE
            TWO: cpp_library_bindings._core.Outer.Inner.NestedEnum # value = NestedEnum.TWO
            __entries: dict # value = {'ONE': (NestedEnum.ONE, None), 'TWO': (NestedEnum.TWO, None)}
            __members__: dict # value = {'ONE': NestedEnum.ONE, 'TWO': NestedEnum.TWO}
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
    pass
foolist: list # value = [<cpp_library_bindings._core.Foo object>, <cpp_library_bindings._core.Foo object>]
foovar: cpp_library_bindings._core.Foo
