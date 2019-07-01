
.. image:: https://badge.fury.io/py/pybind11-stubgen.svg
    :target: https://pypi.org/project/pybind11-stubgen/


About
=====

Generates stubs for python modules

There are several tweaks to target specifically modules compiled using `pybind11 <https://github.com/pybind/pybind11>`_

Currently supports only python3

Issues/PR are welcome

Install
=======

**From github:**

.. code-block:: bash

   python -m pip install git+https://github.com/sizmailov/pybind11-stubgen.git



Usage
=====


.. code-block:: bash

   pybind11-stubgen [-h] [-o OUTPUT_DIR] \
                    [--root_module_suffix ROOT_MODULE_SUFFIX] \
                    [--no-setup-py] \
                    [--log-level LOG_LEVEL] \
                    MODULE_NAME [MODULE_NAME ...] \

