from __future__ import annotations

import demo._bindings.classes

__all__ = ["Bar3"]

class Bar3:
    @staticmethod
    def get_foo() -> demo._bindings.classes.Foo: ...
