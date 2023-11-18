from __future__ import annotations

import typing

__all__ = [
    "Foo",
    "accept_callable",
    "accept_py_handle",
    "accept_py_object",
    "accept_set",
    "add",
    "default_custom_arg",
    "default_int_arg",
    "default_list_arg",
    "default_optional_arg",
    "func_w_anon_args",
    "func_w_named_pos_args",
    "generic",
    "mul",
    "pass_callback",
    "pos_kw_only_mix",
    "pos_kw_only_variadic_mix",
]

class Foo:
    def __init__(self, arg0: int) -> None: ...

def accept_callable(arg0: typing.Callable) -> typing.Any: ...
def accept_py_handle(arg0: typing.Any) -> str: ...
def accept_py_object(arg0: typing.Any) -> str: ...
def accept_set(arg0: set) -> None: ...
def add(arg0: int, arg1: int) -> int: ...
def default_custom_arg(foo: Foo = Foo(5)) -> None: ...
def default_int_arg(n: int = 5) -> None: ...
def default_list_arg(l: list = [1, 2, 6, 18]) -> None: ...
def default_optional_arg(n: int | None = None) -> None: ...
def func_w_anon_args(arg0: int, arg1: int, arg2: int) -> None: ...
def func_w_named_pos_args(x: int, y: int, z: int) -> None: ...
def generic(*args, **kwargs) -> None: ...
@typing.overload
def mul(x: int, y: int) -> int:
    """
    Multiply x and y (int)
    """

@typing.overload
def mul(p: float, q: float) -> float:
    """
    Multiply p and q (double)
    """

def pass_callback(arg0: typing.Callable[[Foo], Foo]) -> Foo: ...
def pos_kw_only_mix(i: int, /, j: int, *, k: int) -> tuple: ...
def pos_kw_only_variadic_mix(i: int, /, j: int, *args, k: int, **kwargs) -> tuple: ...
