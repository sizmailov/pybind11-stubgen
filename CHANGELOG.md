Changelog
=========

Version 1.0-dev (Aug 29, 2023)
--------------------------
⚠️ Project was rewritten from scratch for `1.x`. This allowed me to address some long-standing issues, but I might accidentally brake behaviour you relied on.

Changes:
 - Updated CLI interface, some options were removed, please see `pybind11-stubgen --help` for details
 - Replaced regex-based signature parsing with more robust procedure which enables to produce partially degraded signatures
 - Added type parsing/replacing, including deeply annotated types
 - Support implicit imports required for static analysis
 - Add introspection of pure python functions
 - Support python 3.10+ only (temporarily)
 - Improved structure of test binary pybind module
