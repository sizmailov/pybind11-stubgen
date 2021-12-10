#!/bin/bash

set -e

(cd pybind11-project-example; git submodule update --init --recursive)
(cd pybind11-project-example; python3 -m pip install -U . )

rm -rf "./stubs/generated"

(coverage run -m pybind11_stubgen cpp_library_bindings \
           --output-dir="./stubs/generated" \
           --root-module-suffix="" \
           --ignore-invalid=all \
           --no-setup-py || exit 0)

python3 compare_walker.py
