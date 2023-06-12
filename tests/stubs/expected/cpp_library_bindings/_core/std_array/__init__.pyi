from __future__ import annotations

import typing

import cpp_library_bindings._core.std_array

import pybind11_stubgen.typing_ext

__all__ = ["Transform", "transform"]

class Transform:
    @property
    def transform(
        self,
    ) -> typing.Annotated[typing.List[int], pybind11_stubgen.typing_ext.FixedSize(3)]:
        """
        :type: typing.Annotated[typing.List[int], pybind11_stubgen.typing_ext.FixedSize(3)]
        """
    @transform.setter
    def transform(
        self,
        arg0: typing.Annotated[
            typing.List[int], pybind11_stubgen.typing_ext.FixedSize(3)
        ],
    ) -> None:
        pass
    pass

def transform(
    arg0: typing.Annotated[typing.List[int], pybind11_stubgen.typing_ext.FixedSize(3)]
) -> typing.Annotated[typing.List[int], pybind11_stubgen.typing_ext.FixedSize(3)]:
    pass
