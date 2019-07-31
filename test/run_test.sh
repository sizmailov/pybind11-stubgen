#!/bin/bash

if [ ! -d pybind11-project-example ]
then
    git clone git@github.com:sizmailov/pybind11-project-example.git
else
    (cd pybind11-project-example; git pull origin)
fi

(cd pybind11-project-example; git submodule update --init --recursive)
(cd pybind11-project-example; python setup.py install)


rm -rf "./stubs/generated"
pybind11-stubgen cpp_library_bindings \
           --output-dir="./stubs/generated" \
           --root_module_suffix="" \
           --no-setup-py \
           --log-level=ERROR

python compare_walker.py