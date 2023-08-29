from __future__ import annotations

import types
from typing import Any, Protocol, runtime_checkable

from pybind11_stubgen.parser.errors import ParserError
from pybind11_stubgen.structs import (
    Alias,
    Argument,
    Attribute,
    Class,
    Docstring,
    Field,
    Function,
    Import,
    InvalidExpression,
    Method,
    Module,
    Property,
    QualifiedName,
    ResolvedType,
    Value,
)


@runtime_checkable
class IParser(Protocol):
    def is_print_safe(self, value: Value) -> bool:
        ...

    def handle_alias(self, path: QualifiedName, origin: Any) -> Alias | None:
        ...

    def handle_attribute(self, path: QualifiedName, attr: Any) -> Attribute | None:
        ...

    def handle_bases(
        self, path: QualifiedName, bases: tuple[type, ...]
    ) -> list[QualifiedName]:
        ...

    def handle_class(self, path: QualifiedName, class_: type) -> Class | None:
        ...

    def handle_class_member(
        self, path: QualifiedName, class_: type, obj: Any
    ) -> Docstring | Alias | Class | list[Method] | Field | Property | None:
        ...

    def handle_docstring(self, path: QualifiedName, doc: Any) -> Docstring | None:
        ...

    def handle_field(self, path: QualifiedName, field: Any) -> Field | None:
        ...

    def handle_function(self, path: QualifiedName, func: Any) -> list[Function]:
        ...

    def handle_import(self, path: QualifiedName, origin: Any) -> Import | None:
        ...

    def handle_method(self, path: QualifiedName, method: Any) -> list[Method]:
        ...

    def handle_module(
        self, path: QualifiedName, module: types.ModuleType
    ) -> Module | None:
        ...

    def handle_module_member(
        self, path: QualifiedName, module: types.ModuleType, obj: Any
    ) -> (
        Docstring | Import | Alias | Class | list[Function] | Attribute | Module | None
    ):
        ...

    def handle_property(self, path: QualifiedName, prop: Any) -> Property | None:
        ...

    def handle_type(self, type_: type) -> QualifiedName:
        ...

    def handle_value(self, value: Any) -> Value:
        ...

    def parse_args_str(self, args_str: str) -> list[Argument]:
        ...

    def parse_annotation_str(
        self, annotation_str: str
    ) -> ResolvedType | InvalidExpression | Value:
        ...

    def parse_value_str(self, value: str) -> Value:
        ...

    def value_to_repr(self, value: Any) -> str:
        ...

    def report_error(self, error: ParserError) -> None:
        ...

    def finalize(self):
        ...
