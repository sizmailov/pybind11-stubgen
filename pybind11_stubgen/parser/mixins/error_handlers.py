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
from pybind11_stubgen.structs import Module, QualifiedName

logger = getLogger("pybind11_stubgen")


class LogErrors(IParser):
    def __init__(self):
        super().__init__()
        self._seen_errors: set[str] = set()
        self._module: str | None = None

    def handle_module(
        self, path: QualifiedName, module: types.ModuleType
    ) -> Module | None:
        old_errors = self._seen_errors
        old_module = self._module
        self._seen_errors = set()
        self._module = str(path)
        result = super().handle_module(path, module)
        self._seen_errors = old_errors
        self._module = old_module
        return result

    def report_error(self, error: ParserError) -> None:
        error_str = f"In {self._module} : {error}"
        if error_str not in self._seen_errors:
            logger.error(error_str)
            self._seen_errors.add(error_str)
        super().report_error(error)


class IgnoreFixedErrors(IParser):
    def report_error(self, error: ParserError):
        if isinstance(error, NameResolutionError):
            if error.name[0] in ["pybind11_builtins", "PyCapsule", "module"]:
                return
        elif isinstance(error, InvalidExpressionError):
            if error.expression.startswith("FixedSize"):
                # https://github.com/pybind/pybind11/pull/4679
                return
        elif isinstance(error, InvalidIdentifierError):
            name = error.name
            if (
                name.startswith("ItemsView[")
                and name.endswith("]")
                or name.startswith("KeysView[")
                and name.endswith("]")
                or name.startswith("ValuesView[")
                and name.endswith("]")
            ):
                return

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
        super().report_error(error)
        self.__found_fatal_errors = True

    def finalize(self):
        super().finalize()
        if self.__found_fatal_errors:
            logger.info("Terminating due to previous errors")
            sys.exit(1)
