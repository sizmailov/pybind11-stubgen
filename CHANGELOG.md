Changelog
=========

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
