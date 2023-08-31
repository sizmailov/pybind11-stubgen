from __future__ import annotations

import typing


class _Dummy:
    @staticmethod
    def foo():
        return 42


def search(a: int, b: list[int]) -> int:
    ...


def builtin_function_as_default_arg(func: type(len) = len):
    ...


def function_as_default_arg(func: type(search) = search):
    ...


def lambda_as_default_arg(callback=lambda val: 0):
    ...


def static_method_as_default_arg(callback=_Dummy.foo):
    ...


def arg_mix(
    a: int,
    b: float = 0.5,
    /,
    c: str = "",
    *args: int,
    x: int = 1,
    y=search,
    **kwargs: dict[int, str],
):
    """Mix of positional, kw and variadic args

    Note:
        The `inspect.getfullargspec` does not reflect presence
        of pos-only args separator (/)
    """
    ...


def accept_frozenset(arg: typing.FrozenSet[int | float]) -> int | None:
    pass
