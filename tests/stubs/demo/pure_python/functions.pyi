from __future__ import annotations

import typing

__all__ = [
    "arg_mix",
    "builtin_function_as_default_arg",
    "function_as_default_arg",
    "lambda_as_default_arg",
    "search",
    "static_method_as_default_arg",
]

class _Dummy(object):
    @staticmethod
    def foo(): ...

def arg_mix(
    a: int,
    b: float = 0.5,
    c: str = "",
    *args: int,
    x: int = 1,
    y=search,
    **kwargs: dict[int, str],
):
    """
    Mix of positional, kw and variadic args

        Note:
            The `inspect.getfullargspec` does not reflect presence
            of pos-only args separator (/)

    """

def builtin_function_as_default_arg(func: typing.Callable = ...): ...
def function_as_default_arg(func: typing.Callable = search): ...
def lambda_as_default_arg(callback=...): ...
def search(a: int, b: list[int]) -> int: ...
def static_method_as_default_arg(callback=_Dummy.foo): ...
