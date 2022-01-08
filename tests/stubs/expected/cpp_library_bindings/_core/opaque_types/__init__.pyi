from __future__ import annotations
import cpp_library_bindings._core.opaque_types
import typing

__all__ = [
    "MapStringComplex",
    "VectorPairStringDouble",
    "get_complex_map",
    "get_vector_of_pairs"
]


class MapStringComplex():
    def __bool__(self) -> bool: 
        """
        Check whether the map is nonempty
        """
    @typing.overload
    def __contains__(self, arg0: object) -> bool: ...
    @typing.overload
    def __contains__(self, arg0: str) -> bool: ...
    def __delitem__(self, arg0: str) -> None: ...
    def __getitem__(self, arg0: str) -> complex: ...
    def __init__(self) -> None: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    def __repr__(self) -> str: 
        """
        Return the canonical string representation of this map.
        """
    def __setitem__(self, arg0: str, arg1: complex) -> None: ...
    def items(self) -> typing.ItemsView[MapStringComplex]: ...
    def keys(self) -> typing.KeysView[MapStringComplex]: ...
    def values(self) -> typing.ValuesView[MapStringComplex]: ...
    pass
class VectorPairStringDouble():
    def __bool__(self) -> bool: 
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: typing.Tuple[str, float]) -> bool: 
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None: 
        """
        Delete the list elements at index ``i``

        Delete list elements using a slice object
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None: ...
    def __eq__(self, arg0: VectorPairStringDouble) -> bool: ...
    @typing.overload
    def __getitem__(self, arg0: int) -> typing.Tuple[str, float]: 
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, s: slice) -> VectorPairStringDouble: ...
    @typing.overload
    def __init__(self) -> None: 
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: VectorPairStringDouble) -> None: ...
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None: ...
    def __iter__(self) -> typing.Iterator: ...
    def __len__(self) -> int: ...
    def __ne__(self, arg0: VectorPairStringDouble) -> bool: ...
    @typing.overload
    def __setitem__(self, arg0: int, arg1: typing.Tuple[str, float]) -> None: 
        """
        Assign list elements using a slice object
        """
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: VectorPairStringDouble) -> None: ...
    def append(self, x: typing.Tuple[str, float]) -> None: 
        """
        Add an item to the end of the list
        """
    def clear(self) -> None: 
        """
        Clear the contents
        """
    def count(self, x: typing.Tuple[str, float]) -> int: 
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: VectorPairStringDouble) -> None: 
        """
        Extend the list by appending all the items in the given list

        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None: ...
    def insert(self, i: int, x: typing.Tuple[str, float]) -> None: 
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> typing.Tuple[str, float]: 
        """
        Remove and return the last item

        Remove and return the item at index ``i``
        """
    @typing.overload
    def pop(self, i: int) -> typing.Tuple[str, float]: ...
    def remove(self, x: typing.Tuple[str, float]) -> None: 
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """
    __hash__ = None
    pass
def get_complex_map() -> MapStringComplex:
    pass
def get_vector_of_pairs() -> VectorPairStringDouble:
    pass
