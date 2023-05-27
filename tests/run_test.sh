#!/bin/bash

set -e

(cd pybind11-project-example; git submodule update --init --recursive)
(cd pybind11-project-example; python3 -m pip install -U . )

rm -rf "./stubs/generated"

(python ../pybind11_stubgen/__init__.py cpp_library_bindings \
           --output-dir="./stubs/generated" \
           --root-module-suffix="" \
           --ignore-invalid=all \
           --no-setup-py || exit 0)

# isort works slightly different when started from project root or ./tests/ directory
# cd to project root to match CI setup
(cd .. ; black ./tests/stubs/generated)
(cd .. ; isort --profile=black ./tests/stubs/generated)

python3 compare_walker.py
