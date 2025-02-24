from __future__ import annotations

__all__ = ["Dummy"]

class Dummy:
    @staticmethod
    def static_method(arg0: int) -> int: ...
    def regular_method(self, arg0: int) -> int: ...
