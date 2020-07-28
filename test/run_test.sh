#!/bin/bash

set -e

(cd pybind11-project-example; git submodule update --init --recursive)
(cd pybind11-project-example; python setup.py install)

rm -rf "./stubs/generated"

coverage run -m pybind11_stubgen cpp_library_bindings \
           --output-dir="./stubs/generated" \
           --root_module_suffix="" \
           --no-setup-py \
           --log-level=ERROR

python compare_walker.py
