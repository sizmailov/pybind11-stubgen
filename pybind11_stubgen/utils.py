from __future__ import annotations

from typing import Type, TypeVar

Class_ = TypeVar("Class_", bound=Type)


def implements(protocol: Type):
    def check(class_: Class_) -> Class_:
        assert issubclass(class_, protocol), (
            f"`{class_.__name__}` does not correctly "
            f"implement `{protocol.__name__}` protocol"
        )
        return class_

    return check
