from __future__ import annotations

import numpy
from numpy import random

from demo._bindings.aliases.foreign_method_arg import Bar2 as foreign_type_alias
from demo._bindings.aliases.foreign_return import get_foo as foreign_class_alias

from . import (
    foreign_arg,
    foreign_attr,
    foreign_class_member,
    foreign_method_arg,
    foreign_method_return,
    foreign_return,
)

__all__ = [
    "Color",
    "Dummy",
    "foreign_arg",
    "foreign_attr",
    "foreign_class_alias",
    "foreign_class_member",
    "foreign_method_arg",
    "foreign_method_return",
    "foreign_return",
    "foreign_type_alias",
    "func",
    "local_func_alias",
    "local_type_alias",
    "random",
]

class Color:
    pass

class Dummy:
    linalg = numpy.linalg

def func(arg0: int) -> int: ...

local_func_alias = func
local_type_alias = Color
