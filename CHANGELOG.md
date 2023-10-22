Changelog
=========

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
