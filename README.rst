.. image:: https://img.shields.io/pypi/v/pybind11-stubgen.svg?logo=PyPI&logoColor=white
    :alt: pypi package
    :target: https://pypi.org/project/pybind11-stubgen/

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



Customization
=============

If you need some docstring pre-processing, or you find the hard-coded ``pybind11-stubgen`` defaults to be off,
you can make the adjustments using a tiny wrapper, see examples below.


Customization examples
----------------------

Strip a license from docstring

.. code-block:: python

    import pybind11_stubgen
    import re

    license_pattern = re.compile(r"EXAMPLE CORP LICENCE")

    def strip_license(docstring: str):
        return license_pattern.sub("", docstring)


    if __name__ == '__main__':

        pybind11_stubgen.function_docstring_preprocessing_hooks.append(
            strip_license
        )

        pybind11_stubgen.main()



Replace ``List[int[3]]`` with ``Annotated[List[int], FixedSize(3)]``

.. code-block:: python

    import pybind11_stubgen
    import re

    std_array_pattern = re.compile(r"List\[(int|complex|float)[(\d+)]]")

    def std_array_fix(match: re.Match):
        return f"Annotated[List[{match.group(0)}], FixedSize({match.group(1)})]"


    def strip_dimension_from_std_array(docstring: str):
        return std_array_pattern.sub(std_array_fix, docstring)


    if __name__ == '__main__':

        pybind11_stubgen.function_docstring_preprocessing_hooks.append(
            strip_dimension_from_std_array
        )

        pybind11_stubgen.main()


Replace one type with another


.. code-block:: python

    import pybind11_stubgen
    import re


    def library_b_replacement(match: re.Match):
        type_name = match.group(0)
        return f"library_b.types.{type_name}"


    if __name__ == '__main__':
        pybind11_stubgen.StubsGenerator.GLOBAL_CLASSNAME_REPLACEMENTS[
            re.compile(r"library_a\.types\.(\w+)")
        ] = library_b_replacement

        pybind11_stubgen.main()

