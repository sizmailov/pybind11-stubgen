from __future__ import annotations

import importlib
import logging
import re
from argparse import ArgumentParser
from pathlib import Path

from pybind11_stubgen.parser.interface import IParser
from pybind11_stubgen.parser.mixins.error_handlers import (
    IgnoreAllErrors,
    IgnoreInvalidExpressionErrors,
    IgnoreInvalidIdentifierErrors,
    IgnoreUnresolvedNameErrors,
    LogErrors,
    SuggestCxxSignatureFix,
    TerminateOnFatalErrors,
)
from pybind11_stubgen.parser.mixins.filter import (
    FilterClassMembers,
    FilterInvalidIdentifiers,
    FilterPybindInternals,
)
from pybind11_stubgen.parser.mixins.fix import (
    FixBuiltinTypes,
    FixCurrentModulePrefixInTypeNames,
    FixMissing__all__Attribute,
    FixMissing__future__AnnotationsImport,
    FixMissingEnumMembersAnnotation,
    FixMissingFixedSizeImport,
    FixMissingImports,
    FixMissingNoneHashFieldAnnotation,
    FixNumpyArrayDimAnnotation,
    FixNumpyArrayFlags,
    FixNumpyArrayRemoveParameters,
    FixPEP585CollectionNames,
    FixPybind11EnumStrDoc,
    FixRedundantBuiltinsAnnotation,
    FixRedundantMethodsFromBuiltinObject,
    FixTypingExtTypeNames,
    FixTypingTypeNames,
    FixValueReprRandomAddress,
    RemoveSelfAnnotation,
    ReplaceReadWritePropertyWithField,
)
from pybind11_stubgen.parser.mixins.parse import (
    BaseParser,
    ExtractSignaturesFromPybind11Docstrings,
    ParserDispatchMixin,
)
from pybind11_stubgen.printer import Printer
from pybind11_stubgen.structs import QualifiedName
from pybind11_stubgen.writer import Writer


def arg_parser() -> ArgumentParser:
    def regex(pattern_str: str) -> re.Pattern:
        try:
            return re.compile(pattern_str)
        except re.error as e:
            raise ValueError(f"Invalid REGEX pattern: {e}")

    parser = ArgumentParser(
        prog="pybind11-stubgen", description="Generates stubs for specified modules"
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        help="The root directory for output stubs",
        default="./stubs",
    )
    parser.add_argument(
        "--root-suffix",
        type=str,
        default=None,
        dest="root_suffix",
        help="Top-level module directory suffix",
    )

    parser.add_argument(
        "--ignore-invalid-expressions",
        metavar="REGEX",
        default=None,
        type=regex,
        help="Ignore invalid expressions matching REGEX",
    )
    parser.add_argument(
        "--ignore-invalid-identifiers",
        metavar="REGEX",
        default=None,
        type=regex,
        help="Ignore invalid identifiers matching REGEX",
    )

    parser.add_argument(
        "--ignore-unresolved-names",
        metavar="REGEX",
        default=None,
        type=regex,
        help="Ignore unresolved names matching REGEX",
    )

    parser.add_argument(
        "--ignore-all-errors",
        default=False,
        action="store_true",
        help="Ignore all errors during module parsing",
    )

    numpy_array_fix = parser.add_mutually_exclusive_group()
    numpy_array_fix.add_argument(
        "--numpy-array-wrap-with-annotated",
        default=False,
        action="store_true",
        help="Replace numpy/scipy arrays of "
        "'ARRAY_T[<TYPE>, [*DIMS], *FLAGS]' format with "
        "'Annotated[ARRAY_T, TYPE, FixedSize|DynamicSize(*DIMS), *FLAGS]'",
    )

    numpy_array_fix.add_argument(
        "--numpy-array-remove-parameters",
        default=False,
        action="store_true",
        help="Replace 'numpy.ndarray[...]' with 'numpy.ndarray'",
    )

    parser.add_argument(
        "--print-invalid-expressions-as-is",
        default=False,
        action="store_true",
        help="Suppress invalid expression replacement with '...'",
    )

    parser.add_argument(
        "--exit-code",
        action="store_true",
        dest="exit_code",
        help="On error exits with 1 and skips stub generation",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="Don't write stubs. Parses module and report errors",
    )

    parser.add_argument(
        "module_name",
        metavar="MODULE_NAME",
        type=str,
        help="module name",
    )

    return parser


def stub_parser_from_args(args) -> IParser:
    error_handlers_top: list[type] = [
        *([IgnoreAllErrors] if args.ignore_all_errors else []),
        *([IgnoreInvalidIdentifierErrors] if args.ignore_invalid_identifiers else []),
        *([IgnoreInvalidExpressionErrors] if args.ignore_invalid_expressions else []),
        *([IgnoreUnresolvedNameErrors] if args.ignore_unresolved_names else []),
    ]
    error_handlers_bottom: list[type] = [
        LogErrors,
        SuggestCxxSignatureFix,
        *([TerminateOnFatalErrors] if args.exit_code else []),
    ]

    numpy_fixes: list[type] = [
        *([FixNumpyArrayDimAnnotation] if args.numpy_array_wrap_with_annotated else []),
        *(
            [FixNumpyArrayRemoveParameters]
            if args.numpy_array_remove_parameters
            else []
        ),
    ]

    class Parser(
        *error_handlers_top,  # type: ignore[misc]
        FixMissing__future__AnnotationsImport,
        FixMissing__all__Attribute,
        FixMissingNoneHashFieldAnnotation,
        FixMissingImports,
        FixPEP585CollectionNames,
        FixTypingTypeNames,
        FixTypingExtTypeNames,
        FixMissingFixedSizeImport,
        FixMissingEnumMembersAnnotation,
        *numpy_fixes,  # type: ignore[misc]
        FixNumpyArrayFlags,
        FixCurrentModulePrefixInTypeNames,
        FixBuiltinTypes,
        FilterClassMembers,
        ReplaceReadWritePropertyWithField,
        FilterInvalidIdentifiers,
        FixValueReprRandomAddress,
        FixRedundantBuiltinsAnnotation,
        FilterPybindInternals,
        FixRedundantMethodsFromBuiltinObject,
        RemoveSelfAnnotation,
        FixPybind11EnumStrDoc,
        ExtractSignaturesFromPybind11Docstrings,
        ParserDispatchMixin,
        BaseParser,
        *error_handlers_bottom,  # type: ignore[misc]
    ):
        pass

    parser = Parser()

    if args.ignore_invalid_identifiers is not None:
        parser.set_ignored_invalid_identifiers(args.ignore_invalid_identifiers)
    if args.ignore_invalid_expressions is not None:
        parser.set_ignored_invalid_expressions(args.ignore_invalid_expressions)
    if args.ignore_unresolved_names is not None:
        parser.set_ignored_unresolved_names(args.ignore_unresolved_names)
    return parser


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(name)s - [%(levelname)7s] %(message)s",
    )
    args = arg_parser().parse_args()

    parser = stub_parser_from_args(args)
    printer = Printer(invalid_expr_as_ellipses=not args.print_invalid_expressions_as_is)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(exist_ok=True)

    if args.root_suffix is None:
        sub_dir = None
    else:
        sub_dir = Path(f"{args.module_name}{args.root_suffix}")
    run(
        parser,
        printer,
        args.module_name,
        out_dir,
        sub_dir=sub_dir,
        dry_run=args.dry_run,
    )


def run(
    parser: IParser,
    printer: Printer,
    module_name: str,
    out_dir: Path,
    sub_dir: Path | None,
    dry_run: bool,
):
    module = parser.handle_module(
        QualifiedName.from_str(module_name), importlib.import_module(module_name)
    )
    parser.finalize()

    if module is None:
        raise RuntimeError(f"Can't parse {module_name}")

    if dry_run:
        return

    writer = Writer()

    out_dir.mkdir(exist_ok=True)
    writer.write_module(module, printer, to=out_dir, sub_dir=sub_dir)


if __name__ == "__main__":
    main()
