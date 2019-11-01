import cpp_library_bindings.sublibA
from typing import *
from typing import Iterable as iterable
from typing import Iterator as iterator
from numpy import float64
_Shape = Tuple[int, ...]
__all__  = [
"ConsoleBackgroundColor",
"ConsoleForegroundColor",
"add",
"Blue",
"Green",
"Magenta",
"Yellow"
]
class ConsoleBackgroundColor():
    """Members:

  Green

  Yellow

  Blue

  Magenta"""
    def __init__(self, arg0: int) -> None: ...
    def __int__(self) -> int: ...
    @property
    def name(self) -> str:
        """(self: handle) -> str

:type: str"""
    Blue: cpp_library_bindings.sublibA.ConsoleBackgroundColor # value = ConsoleBackgroundColor.Blue
    Green: cpp_library_bindings.sublibA.ConsoleBackgroundColor # value = ConsoleBackgroundColor.Green
    Magenta: cpp_library_bindings.sublibA.ConsoleBackgroundColor # value = ConsoleBackgroundColor.Magenta
    Yellow: cpp_library_bindings.sublibA.ConsoleBackgroundColor # value = ConsoleBackgroundColor.Yellow
    __entries: dict # value = {'Green': (ConsoleBackgroundColor.Green, None), 'Yellow': (ConsoleBackgroundColor.Yellow, None), 'Blue': (ConsoleBackgroundColor.Blue, None), 'Magenta': (ConsoleBackgroundColor.Magenta, None)}
    __members__: dict # value = {'Green': ConsoleBackgroundColor.Green, 'Yellow': ConsoleBackgroundColor.Yellow, 'Blue': ConsoleBackgroundColor.Blue, 'Magenta': ConsoleBackgroundColor.Magenta}
    pass
class ConsoleForegroundColor():
    """Members:

  Green

  Yellow

  Blue

  Magenta"""
    def __init__(self, arg0: int) -> None: ...
    def __int__(self) -> int: ...
    @property
    def name(self) -> str:
        """(self: handle) -> str

:type: str"""
    Blue: cpp_library_bindings.sublibA.ConsoleForegroundColor # value = ConsoleForegroundColor.Blue
    Green: cpp_library_bindings.sublibA.ConsoleForegroundColor # value = ConsoleForegroundColor.Green
    Magenta: cpp_library_bindings.sublibA.ConsoleForegroundColor # value = ConsoleForegroundColor.Magenta
    Yellow: cpp_library_bindings.sublibA.ConsoleForegroundColor # value = ConsoleForegroundColor.Yellow
    __entries: dict # value = {'Green': (ConsoleForegroundColor.Green, None), 'Yellow': (ConsoleForegroundColor.Yellow, None), 'Blue': (ConsoleForegroundColor.Blue, None), 'Magenta': (ConsoleForegroundColor.Magenta, None)}
    __members__: dict # value = {'Green': ConsoleForegroundColor.Green, 'Yellow': ConsoleForegroundColor.Yellow, 'Blue': ConsoleForegroundColor.Blue, 'Magenta': ConsoleForegroundColor.Magenta}
    pass
def add(arg0: int, arg1: int) -> int:
    pass
Blue: cpp_library_bindings.sublibA.ConsoleBackgroundColor # value = ConsoleBackgroundColor.Blue
Green: cpp_library_bindings.sublibA.ConsoleBackgroundColor # value = ConsoleBackgroundColor.Green
Magenta: cpp_library_bindings.sublibA.ConsoleBackgroundColor # value = ConsoleBackgroundColor.Magenta
Yellow: cpp_library_bindings.sublibA.ConsoleBackgroundColor # value = ConsoleBackgroundColor.Yellow