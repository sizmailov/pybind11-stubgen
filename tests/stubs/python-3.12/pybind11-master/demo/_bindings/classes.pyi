from __future__ import annotations

import typing

__all__ = ["Base", "CppException", "Derived", "Foo", "Outer"]

class Base:
    class Inner:
        pass
    name: str

class CppException(Exception):
    pass

class Derived(Base):
    count: int

class Foo:
    class FooChild:
        def __init__(self) -> None: ...
        def g(self) -> None: ...

    def __init__(self) -> None: ...
    def f(self) -> None: ...

class Outer:
    class Inner:
        class NestedEnum:
            """
            Members:

              ONE

              TWO
            """

            ONE: typing.ClassVar[Outer.Inner.NestedEnum]  # value = <NestedEnum.ONE: 1>
            TWO: typing.ClassVar[Outer.Inner.NestedEnum]  # value = <NestedEnum.TWO: 2>
            __members__: typing.ClassVar[
                dict[str, Outer.Inner.NestedEnum]
            ]  # value = {'ONE': <NestedEnum.ONE: 1>, 'TWO': <NestedEnum.TWO: 2>}
            def __eq__(self, other: typing.Any) -> bool: ...
            def __getstate__(self) -> int: ...
            def __hash__(self) -> int: ...
            def __index__(self) -> int: ...
            def __init__(self, value: int) -> None: ...
            def __int__(self) -> int: ...
            def __ne__(self, other: typing.Any) -> bool: ...
            def __repr__(self) -> str: ...
            def __setstate__(self, state: int) -> None: ...
            def __str__(self) -> str: ...
            @property
            def name(self) -> str: ...
            @property
            def value(self) -> int: ...
        value: Outer.Inner.NestedEnum
    inner: Outer.Inner
