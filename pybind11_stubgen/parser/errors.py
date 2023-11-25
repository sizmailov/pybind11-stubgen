from __future__ import annotations

from pybind11_stubgen.structs import Identifier, Import, QualifiedName, Value


class ParserError(Exception):
    pass


class InvalidIdentifierError(ParserError):
    def __init__(self, name: Identifier, found_at: QualifiedName):
        super().__init__()
        self.name = name
        self.at = found_at

    def __str__(self):
        return f"Invalid identifier '{self.name}' at '{self.at}'"


class InvalidExpressionError(ParserError):
    def __init__(self, expression: str):
        super().__init__()
        self.expression: str = expression

    def __str__(self):
        return f"Invalid expression '{self.expression}'"


class NameResolutionError(ParserError):
    def __init__(self, name: QualifiedName):
        super().__init__()
        self.name = name

    def __str__(self):
        return f"Can't find/import '{self.name}'"


class AmbiguousEnumError(InvalidExpressionError):
    def __init__(self, repr_: str, *values_and_imports: tuple[Value, Import]):
        super().__init__(repr_)
        self.values_and_imports = values_and_imports

        if len(self.values_and_imports) < 2:
            raise ValueError(
                "Expected at least 2 values_and_imports, got "
                f"{len(self.values_and_imports)}"
            )

    def __str__(self) -> str:
        origins = sorted(import_.origin for _, import_ in self.values_and_imports)
        return (
            f"Enum member '{self.expression}' could not be resolved; multiple "
            "matching definitions found in: "
            + ", ".join(f"'{origin}'" for origin in origins)
        )
