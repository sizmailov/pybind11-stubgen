from __future__ import annotations

import sys as sys
import typing as typing

__all__ = [
    "accept_frozenset",
    "builtin_function_as_default_arg",
    "function_as_default_arg",
    "lambda_as_default_arg",
    "search",
    "static_method_as_default_arg",
    "sys",
    "typing",
]

class _Dummy:
    @staticmethod
    def foo(): ...

def accept_frozenset(arg: frozenset[int | float]) -> int | None: ...
def builtin_function_as_default_arg(func: type(len) = len): ...
def function_as_default_arg(func: type(search) = search): ...
def lambda_as_default_arg(callback=...): ...
def search(a: int, b: list[int]) -> int: ...
def static_method_as_default_arg(callback=_Dummy.foo): ...
