.. image:: https://img.shields.io/travis/com/sizmailov/pybind11-stubgen/master.svg?logo=travis
    :alt: master status
    :target: https://travis-ci.com/sizmailov/pybind11-stubgen

.. image:: https://img.shields.io/pypi/v/pybind11-stubgen.svg?logo=PyPI&logoColor=white
    :alt: pypi package
    :target: https://pypi.org/project/pybind11-stubgen/

.. image:: https://codecov.io/gh/sizmailov/pybind11-stubgen/branch/master/graph/badge.svg
  :alt: coverage
  :target: https://codecov.io/gh/sizmailov/pybind11-stubgen


About
=====

Generates stubs for python modules

There are several tweaks to target specifically modules compiled using `pybind11 <https://github.com/pybind/pybind11>`_

Package targets python3 only. (In fact, it's compatible with python2 but it's not officially supported)

Issues/PR are welcome

Install
=======

**From PYPI:**

.. code-block:: bash

   python -m pip install pybind11-stubgen

**From github:**

.. code-block:: bash

   python -m pip install git+https://github.com/sizmailov/pybind11-stubgen.git



Usage
=====


.. code-block:: bash

   pybind11-stubgen [-h] [-o OUTPUT_DIR] \
                    [--root-module-suffix ROOT_MODULE_SUFFIX] \
                    [--no-setup-py] \
                    [--ignore-invalid {signature,defaultarg,all} [{signature,defaultarg,all} ...]] \
                    [--skip-signature-downgrade] \
                    [--bare-numpy-ndarray] \
                    [--log-level LOG_LEVEL] \
                    MODULE_NAME [MODULE_NAME ...]
