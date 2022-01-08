from __future__ import annotations
import cpp_library_bindings._core.sublibA
import typing

__all__ = [
    "Blue",
    "ConsoleBackgroundColor",
    "ConsoleForegroundColor",
    "Green",
    "Magenta",
    "Yellow",
    "accept_defaulted_enum",
    "add"
]


class ConsoleBackgroundColor():
    """
    Members:

      Green

      Yellow

      Blue

      Magenta
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
    Blue: cpp_library_bindings._core.sublibA.ConsoleBackgroundColor # value = <ConsoleBackgroundColor.Blue: 44>
    Green: cpp_library_bindings._core.sublibA.ConsoleBackgroundColor # value = <ConsoleBackgroundColor.Green: 42>
    Magenta: cpp_library_bindings._core.sublibA.ConsoleBackgroundColor # value = <ConsoleBackgroundColor.Magenta: 45>
    Yellow: cpp_library_bindings._core.sublibA.ConsoleBackgroundColor # value = <ConsoleBackgroundColor.Yellow: 43>
    __members__: dict # value = {'Green': <ConsoleBackgroundColor.Green: 42>, 'Yellow': <ConsoleBackgroundColor.Yellow: 43>, 'Blue': <ConsoleBackgroundColor.Blue: 44>, 'Magenta': <ConsoleBackgroundColor.Magenta: 45>}
    pass
class ConsoleForegroundColor():
    """
    Members:

      Green

      Yellow

      Blue

      Magenta
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
    Blue: cpp_library_bindings._core.sublibA.ConsoleForegroundColor # value = <ConsoleForegroundColor.Blue: 34>
    Green: cpp_library_bindings._core.sublibA.ConsoleForegroundColor # value = <ConsoleForegroundColor.Green: 32>
    Magenta: cpp_library_bindings._core.sublibA.ConsoleForegroundColor # value = <ConsoleForegroundColor.Magenta: 35>
    Yellow: cpp_library_bindings._core.sublibA.ConsoleForegroundColor # value = <ConsoleForegroundColor.Yellow: 33>
    __members__: dict # value = {'Green': <ConsoleForegroundColor.Green: 32>, 'Yellow': <ConsoleForegroundColor.Yellow: 33>, 'Blue': <ConsoleForegroundColor.Blue: 34>, 'Magenta': <ConsoleForegroundColor.Magenta: 35>}
    pass
def accept_defaulted_enum(color: ConsoleForegroundColor = ConsoleForegroundColor.Blue) -> None:
    pass
def add(arg0: int, arg1: int) -> int:
    pass
Blue: cpp_library_bindings._core.sublibA.ConsoleBackgroundColor # value = <ConsoleBackgroundColor.Blue: 44>
Green: cpp_library_bindings._core.sublibA.ConsoleBackgroundColor # value = <ConsoleBackgroundColor.Green: 42>
Magenta: cpp_library_bindings._core.sublibA.ConsoleBackgroundColor # value = <ConsoleBackgroundColor.Magenta: 45>
Yellow: cpp_library_bindings._core.sublibA.ConsoleBackgroundColor # value = <ConsoleBackgroundColor.Yellow: 43>
