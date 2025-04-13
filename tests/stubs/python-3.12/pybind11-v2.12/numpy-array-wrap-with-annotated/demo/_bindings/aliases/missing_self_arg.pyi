from __future__ import annotations

import demo._bindings.classes

__all__ = ["Bar4"]

class Bar4:
    def set_foo(self: demo._bindings.classes.Foo) -> int: ...
