Changelog
=========

Version 2.5.4 (May 14, 2025)
--------------------------
Changes:
- ✨ Add `argv` to `main()` to simplify use as a library (#252) by @gentlegiantJGC
- 🐛 Improve package detection (#253) by @gentlegiantJGC

Version 2.5.3 (Feb 24, 2025)
--------------------------
Changes:
- ✨ Ignore technical dunder Python 3.13 fields (`__static_attributes__` and `__firstlineno__`): (#243) by @nim65s
- 🔧 CI: Drop Python 3.7, add Python 3.13 (#243) by @nim65s


Version 2.5.2 (Feb 24, 2025)
--------------------------
Yanked to CI failure, released as 2.5.3


Version 2.5.1 (Mar 26, 2024)
--------------------------
Changes:
- 🐛 Fixed: Missed numpy unsigned int types (#219) by @Yc7521


Version 2.5 (Mar 3, 2024)
--------------------------
Changes:
- 🐛 Fixed: Don't render pybind11 `KeysView`, `ValuesView`, `ItemsView` class definitions (#211)
- 🐛 Fixed: Escape backslashes in stub output (#208)


Version 2.4.2 (Nov 27, 2023)
--------------------------
Changes:
- 🔁 Revert #196 due to poor review


Version 2.4.1 (Nov 25, 2023)
--------------------------
Changes:
- ✨ Automatically replace invalid enum expressions with corresponding valid expression & import (#196)  contributed by @ringohoffman
- 🐛 Fixed: do not remove `self` parameter annotation when types do not match (#195) contributed by @ringohoffman


Version 2.4 (Nov 21, 2023)
--------------------------
Changes:
- ✨ Added `--numpy-array-use-type-var` flag which reformats the pybind11-generated `numpy.ndarray[numpy.float32[m, 1]]`
annotation as `numpy.ndarray[tuple[M, Literal[1]], numpy.dtype[numpy.float32]]` contributed by @ringohoffman (#188)


Version 2.3.7 (Nov 18, 2023)
--------------------------
Changes:
- 🐛 fix: Handle top-level list-like annotations as types (#183)


Version 2.3.6 (Oct 24, 2023)
--------------------------
Changes:
- 🐛 fix: Missing `py::dtype` translation (#179)


Version 2.3.5 (Oct 23, 2023)
--------------------------
Changes:
- 🐛 fix: Wrong import for lowercase `buffer` (#175), issue (#173)


Version 2.3.4 (Oct 23, 2023)
--------------------------
Changes:
- 🐛 fix: Misleading warning that referred to ignored errors (#171)


Version 2.3.3 (Oct 22, 2023)
--------------------------
Changes:
- 🐛 fix: The `typing.Annotated` does not exist in python < 3.9, use `typing_extensions` (#168)


Version 2.3.2 (Oct 21, 2023)
--------------------------
Changes:
- 🐛 fix: Missing function name in error message (#165)


Version 2.3.1 (Oct 21, 2023)
--------------------------
Changes:
- 🐛 fix: Crash on `None`-valued docstring of property getter (#161)


Version 2.3 (Sep 27, 2023)
--------------------------
Changes:
- 🐛 fix: Inconsistent `--enum-class-locations` behaviour (#158)


Version 2.2.2 (Sep 26, 2023)
--------------------------
Changes:
- 🐛 fix: Missing `-?` in eum representation regex


Version 2.2.1 (Sep 23, 2023)
--------------------------
Changes:
- 📝 Update `--print-invalid-expressions-as-is` description


Version 2.2 (Sep 20, 2023)
--------------------------
Changes:

- 🐛 Fix: Python literals as default arg rendered as `...` (#147)
- ✨ Add `--print-safe-value-reprs=REGEX` CLI option to override the print-safe flag
     of Value (for custom default value representations provided via `pybind11::arg_v()`)  (#147)
- ✨ Add `--enum-class-locations=REGEX:LOC` CLI option to rewrite enum values as valid
     Python expressions with correct imports. (#147)

⚠️ This release detects more invalid expressions in bindings code.
  Previously Enum-like representations (e.g. `<MyEnum.Zero: 0>`) were always treated
  as non-printable values and were rendered as `...`.
  The invalid expressions should be acknowledged by `--enum-class-locations` or `--ignore-invalid-expressions`.


Version 2.1 (Sep 6, 2023)
--------------------------
Changes:

- ✨ Add `--stub-extension` CLI option (#142)


Version 2.0.2 (Sep 4, 2023)
--------------------------
Changes:

- 🐛 Fix: missing `isinstance` check (#138)

Version 2.0.1 (Sep 2, 2023)
--------------------------
Changes:

- 🐛 Fix: missing subdirectories for top-level submodules (#136)


Version 2.0 (Sep 1, 2023)
--------------------------
Changes:

- 🐛 Explicitly set encoding of stubs to utf-8 (#133)
- 🐛 Fix value representation for collections with print-unsafe elements (#132)


Version 2.0.dev1 (Sep 1, 2023)
--------------------------
Changes:

- 🐛 Fix missing remap of `numpy.ndarray.flags` (#128)
- ✨ Process `scipy.sparse.*` types the same as `numpy.ndarray` with `--numpy-array-wrap-with-annotated` (#128)
- ✨ Support dynamic array size with `--numpy-array-wrap-with-annotated` (#128)
- ❗️ Renamed CLI argument `--numpy-array-wrap-with-annotated-fixed-size` to `--numpy-array-wrap-with-annotated` (#128)


Version 1.2 (Aug 31, 2023)
--------------------------
Changes:

- 🐛 Fix compatibility with Python 3.7..3.9 (#124)
- 🐛 Fix incorrect list of base classes (#123)
- ✨ Replace `typing` collections with builtin types (e.g. `typing.List` -> `list`) according
  to [PEP 585](https://peps.python.org/pep-0585/)  (#122)
- ✨ Add missing translations of pybind types: `function` -> `Callable`, `object`/`handle` -> `typing.Any` (#121)
- ✨ Support function-valued default arguments (#119)
- 🐛 Fix missing properties docstrings (#118)


Version 1.1 (Aug 30, 2023)
--------------------------
Changes:

- Added `--dry-run` CLI option to skip writing stubs stage (#114 )


Version 1.0-dev (Aug 29, 2023)
------------------------------
⚠️ Project was rewritten from scratch for `1.x`. This allowed me to address some long-standing issues, but I might
accidentally brake behaviour you relied on.

Changes:

- Updated CLI interface, some options were removed, please see `pybind11-stubgen --help` for details
- Replaced regex-based signature parsing with more robust procedure which enables to produce partially degraded
  signatures
- Added type parsing/replacing, including deeply annotated types
- Support implicit imports required for static analysis
- Add introspection of pure python functions
- Support python 3.10+ only (temporarily)
- Improved structure of test binary pybind module
