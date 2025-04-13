from __future__ import annotations

import demo._bindings.classes

__all__ = ["get_foo"]

def get_foo() -> demo._bindings.classes.Foo: ...
