
An example of C++ project with pybind11 bindings

The primary purpose of this project is to test `pybind11-stubgen <https://github.com/sizmailov/pybind11-stubgen>`_ functionality.

It can be used as a C++ python module template.

Project layout
--------------


.. code-block:: sh

    ./include/cpp_library/     # includes (.h) of C++ project
    ./src/                     # sources (.cpp) of C++ project
    ./cpp_library_bindings/    # pybind11 bindings of C++ project
    ./external/                # root for 3rd party libraries sources (pybind11, gtests, etc.)

Build module shared library
---------------------------

Needed only for testing/debug

.. code-block:: sh

    mkdir build
    (cd build ; cmake .. )


Install python
--------------

The build step will be invoked automatically during install process

.. code-block:: sh

    python setup.py install  # regular python install is working
