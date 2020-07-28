import cpp_library_bindings
from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64
_Shape = Tuple[int, ...]
__all__  = [
"CppException",
"Foo",
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
