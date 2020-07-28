#!/bin/bash

set -e

if [ ! -d pybind11-project-example ]
then
    git clone https://github.com/sizmailov/pybind11-project-example.git
else
    (cd pybind11-project-example; git fetch origin)
fi

# update the commit below when the example code changes and you want to extend the tests
(cd pybind11-project-example; git checkout 2310344c932c404d8bcfa2c355f07dcfedcc4082)
(cd pybind11-project-example; git submodule update --init --recursive)
(cd pybind11-project-example; python setup.py install)


rm -rf "./stubs/generated"

coverage run -m pybind11_stubgen cpp_library_bindings \
           --output-dir="./stubs/generated" \
           --root_module_suffix="" \
           --no-setup-py \
           --log-level=ERROR

python compare_walker.py
