from setuptools import find_packages, setup

setup(
    name="pybind11-stubgen",
    maintainer="Sergei Izmailov",
    maintainer_email="sergei.a.izmailov@gmail.com",
    description="PEP 561 type stubs generator for pybind11 modules",
    url="https://github.com/sizmailov/pybind11-stubgen",
    version="2.3.7",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="BSD",
    entry_points={
        "console_scripts": "pybind11-stubgen = pybind11_stubgen.__init__:main"
    },
    packages=find_packages(),
    package_data={"pybind11_stubgen": ["py.typed"]},
    python_requires="~=3.7",
)
