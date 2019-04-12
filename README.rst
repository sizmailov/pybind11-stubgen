About
=====

Generates stubs for python modules

There are several tweaks to target specifically modules compiled using `pybind11 <https://github.com/pybind/pybind11>`_

Currently supports only python3

Issues/PR are welcome

Usage 
=====


.. code-block:: bash

    pybind11_stubgen/__init__.py [-h] \
            [-o OUTPUT_DIR] \
            [--root_module_suffix ROOT_MODULE_SUFFIX] \
            [--no-setup-py] \
            MODULE_NAME [MODULE_NAME ...]

