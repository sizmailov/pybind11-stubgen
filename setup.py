from setuptools import setup

setup(
    name='pybind11_stubgen',
    maintainer="Sergei Izmailov",
    maintainer_email="sergei.a.izmailov@gmail.com",
    description="PEP 561 type stubs generator for pybind11 modules",
    url="https://github.com/sizmailov/pybind11_stubgen",
    version="0.0.2",
    entry_points={'console_scripts' : 'py11_stubgen = pybind11_stubgen.__main__:main'},
    packages=['pybind11_stubgen']
)
