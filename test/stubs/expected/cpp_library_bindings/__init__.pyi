import cpp_library_bindings
from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64
_Shape = Tuple[int, ...]
__all__  = [
"CppException",
"Foo",
"Outer",
"sublibA"
]
class CppException(Exception, BaseException):
    __cause__: getset_descriptor # value = <attribute '__cause__' of 'BaseException' objects>
    __context__: getset_descriptor # value = <attribute '__context__' of 'BaseException' objects>
    __dict__: mappingproxy # value = mappingproxy({'__module__': 'cpp_library_bindings', '__weakref__': <attribute '__weakref__' of 'CppException' objects>, '__doc__': None})
    __suppress_context__: member_descriptor # value = <member '__suppress_context__' of 'BaseException' objects>
    __traceback__: getset_descriptor # value = <attribute '__traceback__' of 'BaseException' objects>
    __weakref__: getset_descriptor # value = <attribute '__weakref__' of 'CppException' objects>
    args: getset_descriptor # value = <attribute 'args' of 'BaseException' objects>
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
            ONE: cpp_library_bindings.Outer.Inner.NestedEnum # value = NestedEnum.ONE
            TWO: cpp_library_bindings.Outer.Inner.NestedEnum # value = NestedEnum.TWO
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
