from setuptools import setup

setup(
    name='pybind11-stubgen',
    maintainer="Sergei Izmailov",
    maintainer_email="sergei.a.izmailov@gmail.com",
    description="PEP 561 type stubs generator for pybind11 modules",
    url="https://github.com/sizmailov/pybind11_stubgen",
    version="0.0.3",
    license="BSD",
    entry_points={'console_scripts': 'pybind11-stubgen = pybind11_stubgen.__init__:main'},
    packages=['pybind11_stubgen']
)
