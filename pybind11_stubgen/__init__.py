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
    LoggerData,
    SuggestCxxSignatureFix,
    TerminateOnFatalErrors,
)
from pybind11_stubgen.parser.mixins.filter import (
    FilterClassMembers,
    FilterInvalidIdentifiers,
    FilterPybindInternals,
    FilterTypingModuleAttributes,
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
    OverridePrintSafeValues,
    RemoveSelfAnnotation,
    ReplaceReadWritePropertyWithField,
    RewritePybind11EnumValueRepr,
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

    def regex_colon_path(regex_path: str) -> tuple[re.Pattern, str]:
        pattern_str, path = regex_path.rsplit(":", maxsplit=1)
        if any(not part.isidentifier() for part in path.split(".")):
            raise ValueError(f"Invalid PATH: {path}")
        return regex(pattern_str), path

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

    parser.add_argument(
        "--enum-class-locations",
        dest="enum_class_locations",
        metavar="REGEX:LOC",
        action="append",
        default=[],
        type=regex_colon_path,
        help="Locations of enum classes in "
        "<enum-class-name-regex>:<path-to-class> format. "
        "Example: `MyEnum:foo.bar.Baz`",
    )

    numpy_array_fix = parser.add_mutually_exclusive_group()
    numpy_array_fix.add_argument(
        "--numpy-array-wrap-with-annotated",
        default=False,
        action="store_true",
        help="Replace numpy/scipy arrays of "
        "'ARRAY_T[TYPE, [*DIMS], *FLAGS]' format with "
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
        help="Suppress the replacement with '...' of invalid expressions"
        "found in annotations",
    )

    parser.add_argument(
        "--print-safe-value-reprs",
        metavar="REGEX",
        default=None,
        type=regex,
        help="Override the print-safe check for values matching REGEX",
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
        "--stub-extension",
        type=str,
        default="pyi",
        metavar="EXT",
        choices=["pyi", "py"],
        help="The file extension of the generated stubs. "
        "Must be 'pyi' (default) or 'py'",
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
        LoggerData,
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
        FilterTypingModuleAttributes,
        FixPEP585CollectionNames,
        FixTypingTypeNames,
        FixTypingExtTypeNames,
        FixMissingFixedSizeImport,
        FixMissingEnumMembersAnnotation,
        OverridePrintSafeValues,
        *numpy_fixes,  # type: ignore[misc]
        FixNumpyArrayFlags,
        FixCurrentModulePrefixInTypeNames,
        FixBuiltinTypes,
        RewritePybind11EnumValueRepr,
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

    if args.enum_class_locations:
        parser.set_pybind11_enum_locations(dict(args.enum_class_locations))
    if args.ignore_invalid_identifiers is not None:
        parser.set_ignored_invalid_identifiers(args.ignore_invalid_identifiers)
    if args.ignore_invalid_expressions is not None:
        parser.set_ignored_invalid_expressions(args.ignore_invalid_expressions)
    if args.ignore_unresolved_names is not None:
        parser.set_ignored_unresolved_names(args.ignore_unresolved_names)
    if args.print_safe_value_reprs is not None:
        parser.set_print_safe_value_pattern(args.print_safe_value_reprs)
    return parser


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(name)s - [%(levelname)7s] %(message)s",
    )
    args = arg_parser().parse_args()

    parser = stub_parser_from_args(args)
    printer = Printer(invalid_expr_as_ellipses=not args.print_invalid_expressions_as_is)

    out_dir, sub_dir = to_output_and_subdir(
        output_dir=args.output_dir,
        module_name=args.module_name,
        root_suffix=args.root_suffix,
    )

    run(
        parser,
        printer,
        args.module_name,
        out_dir,
        sub_dir=sub_dir,
        dry_run=args.dry_run,
        writer=Writer(stub_ext=args.stub_extension),
    )


def to_output_and_subdir(
    output_dir: Path, module_name: str, root_suffix: str | None
) -> tuple[Path, Path | None]:
    out_dir = Path(output_dir)

    module_path = module_name.split(".")

    if root_suffix is None:
        return out_dir.joinpath(*module_path[:-1]), None
    else:
        module_path = [f"{module_path[0]}{root_suffix}", *module_path[1:]]
        if len(module_path) == 1:
            sub_dir = Path(module_path[-1])
        else:
            sub_dir = None
        return out_dir.joinpath(*module_path[:-1]), sub_dir


def run(
    parser: IParser,
    printer: Printer,
    module_name: str,
    out_dir: Path,
    sub_dir: Path | None,
    dry_run: bool,
    writer: Writer,
):
    module = parser.handle_module(
        QualifiedName.from_str(module_name), importlib.import_module(module_name)
    )
    parser.finalize()

    if module is None:
        raise RuntimeError(f"Can't parse {module_name}")

    if dry_run:
        return

    out_dir.mkdir(exist_ok=True, parents=True)
    writer.write_module(module, printer, to=out_dir, sub_dir=sub_dir)


if __name__ == "__main__":
    main()
