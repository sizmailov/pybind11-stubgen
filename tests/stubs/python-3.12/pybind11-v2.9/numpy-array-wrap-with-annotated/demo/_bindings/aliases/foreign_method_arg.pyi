from __future__ import annotations

import demo._bindings.classes

__all__ = ["Bar2"]

class Bar2:
    def set_foo(self: demo._bindings.classes.Foo) -> int: ...
