from __future__ import annotations

import re
import sys
import types
from logging import getLogger

from pybind11_stubgen.parser.errors import (
    InvalidExpressionError,
    InvalidIdentifierError,
    NameResolutionError,
    ParserError,
)
from pybind11_stubgen.parser.interface import IParser
from pybind11_stubgen.structs import Class, Function, Method, Module, QualifiedName


class LocalErrors:
    def __init__(self, path: QualifiedName, errors: set[str], stack: list[LocalErrors]):
        self.path: QualifiedName = path
        self.errors: set[str] = errors
        self._stack: list[LocalErrors] = stack

    def __enter__(self) -> LocalErrors:
        self._stack.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        top = self._stack.pop()
        assert top == self


class LoggerData(IParser):
    def __init__(self):
        super().__init__()
        self.stack: list[LocalErrors] = []

    def __new_layer(self, path: QualifiedName) -> LocalErrors:
        return LocalErrors(path, errors=set(), stack=self.stack)

    def handle_module(
        self, path: QualifiedName, module: types.ModuleType
    ) -> Module | None:
        with self.__new_layer(path):
            return super().handle_module(path, module)

    def handle_class(self, path: QualifiedName, class_: type) -> Class | None:
        with self.__new_layer(path):
            return super().handle_class(path, class_)

    def handle_function(self, path: QualifiedName, class_: type) -> list[Function]:
        with self.__new_layer(path):
            return super().handle_function(path, class_)

    def handle_method(self, path: QualifiedName, class_: type) -> list[Method]:
        with self.__new_layer(path):
            return super().handle_method(path, class_)

    @property
    def current_path(self) -> QualifiedName:
        assert len(self.stack) != 0
        return self.stack[-1].path

    @property
    def reported_errors(self) -> set[str]:
        assert len(self.stack) != 0
        return self.stack[-1].errors


logger = getLogger("pybind11_stubgen")


class LogErrors(IParser):
    def report_error(self: LoggerData, error: ParserError) -> None:
        error_str = f"In {self.current_path} : {error}"
        if error_str not in self.reported_errors:
            logger.error(error_str)
            self.reported_errors.add(error_str)
        super().report_error(error)


class IgnoreUnresolvedNameErrors(IParser):
    def __init__(self):
        super().__init__()
        self.__regex: re.Pattern | None = None

    def set_ignored_unresolved_names(self, regex: re.Pattern):
        self.__regex = regex

    def report_error(self, error: ParserError):
        if self.__regex is not None:
            if isinstance(error, NameResolutionError):
                if self.__regex.match(str(error.name)):
                    return
        super().report_error(error)


class IgnoreInvalidExpressionErrors(IParser):
    def __init__(self):
        super().__init__()
        self.__regex: re.Pattern | None = None

    def set_ignored_invalid_expressions(self, regex: re.Pattern):
        self.__regex = regex

    def report_error(self, error: ParserError):
        if self.__regex is not None:
            if isinstance(error, InvalidExpressionError):
                if self.__regex.match(error.expression):
                    return
        super().report_error(error)


class IgnoreInvalidIdentifierErrors(IParser):
    def __init__(self):
        super().__init__()
        self.__regex: re.Pattern | None = None

    def set_ignored_invalid_identifiers(self, regex: re.Pattern):
        self.__regex = regex

    def report_error(self, error: ParserError):
        if self.__regex is not None:
            if isinstance(error, InvalidIdentifierError):
                if self.__regex.match(str(error.name)):
                    return
        super().report_error(error)


class IgnoreAllErrors(IParser):
    def report_error(self, error: ParserError):
        return None


class SuggestCxxSignatureFix(IParser):
    def __init__(self):
        super().__init__()
        self.suggest_cxx_fix = False

    def report_error(self, error: ParserError):
        if isinstance(error, InvalidExpressionError):
            expression = error.expression
            if "::" in expression or expression.endswith(">"):
                self.suggest_cxx_fix = True

        super().report_error(error)

    def finalize(self):
        if self.suggest_cxx_fix:
            logger.warning(
                "Raw C++ types/values were found in signatures extracted "
                "from docstrings.\n"
                "Please check the corresponding sections of pybind11 documentation "
                "to avoid common mistakes in binding code:\n"
                " - https://pybind11.readthedocs.io/en/latest/advanced/misc.html"
                "#avoiding-cpp-types-in-docstrings\n"
                " - https://pybind11.readthedocs.io/en/latest/advanced/functions.html"
                "#default-arguments-revisited"
            )
        super().finalize()


class TerminateOnFatalErrors(IParser):
    def __init__(self):
        super().__init__()
        self.__found_fatal_errors = False

    def report_error(self, error: ParserError):
        self.__found_fatal_errors = True
        super().report_error(error)

    def finalize(self):
        super().finalize()
        if self.__found_fatal_errors:
            logger.info("Terminating due to previous errors")
            sys.exit(1)
