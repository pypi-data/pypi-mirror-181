"""This class is the basic parsing class for dictionary types."""
from __future__ import annotations

from enum import Enum
from typing import Any, Generic, Mapping, OrderedDict, Sequence, TypeVar, cast

from bitarray import bitarray

from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS, ParseBase, endianT
from easyprotocol.base.utils import dataT, input_to_bytes

T = TypeVar("T")
K = TypeVar("K")


class ParseGenericDict(
    ParseBase,
    Mapping[K, ParseBase],
    Generic[K, T],
):
    """This class is the basic parsing class for dictionary types."""

    def __init__(
        self,
        name: str,
        default: OrderedDict[str, ParseBase] | Sequence[ParseBase] | None = None,
        data: dataT = None,
        bit_count: int = -1,
        string_format: str | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        """Create the basic parsing class for dictionary types.

        Args:
            name: name of parsed object
            default: the default value for this class
            data: bytes to be parsed
            bit_count: number of bits assigned to this field
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        super().__init__(
            name=name,
            data=None,
            bit_count=bit_count,
            string_format=string_format,
            endian=endian,
        )
        self._set_children_generic(children=default)
        if data is not None:
            self.parse(data)

    def parse(self, data: dataT) -> bitarray:
        """Parse the bits of this field into meaningful data.

        Args:
            data: bytes to be parsed

        Returns:
            any leftover bits after parsing the ones belonging to this field
        """
        bit_data = input_to_bytes(data=data)
        for field in self._children.values():
            bit_data = field.parse(data=bit_data)
        return bit_data

    def popitem(self, last: bool = False) -> tuple[K, ParseBase]:
        """Remove item from list.

        Args:
            last: delete the last added item instead of the first

        Returns:
            the popped item
        """
        return cast(tuple[K, ParseBase], self._children.popitem(last=last))

    def pop(self, name: str, default: ParseBase | None = None) -> ParseBase | None:
        """Pop item from dictionary by name.

        Args:
            name: name of item to pop
            default: object to return if the name is not in the dictionary

        Returns:
            the item (or default item)
        """
        if isinstance(name, Enum):
            p = self._children.pop(name.name, default)
        else:
            p = self._children.pop(name, default)
        if p is not None:
            p._set_parent_generic(None)
        return p

    def get_value(
        self,
    ) -> OrderedDict[str, ParseBase]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return OrderedDict(self._children)

    def set_value(
        self,
        value: OrderedDict[str, ParseBase] | Sequence[ParseBase],
    ) -> None:
        """Set the parsed value of the field.

        Args:
            value: the value of the field
        """
        if isinstance(value, dict):
            for key, item in value.items():
                self.__setitem__(key, item)
                item._set_parent_generic(self)
        else:
            for item in value:
                key = item.name
                self.__setitem__(key, item)
                item._set_parent_generic(self)

    def get_bits_lsb(self) -> bitarray:
        """Get the bits of this field in least-significant-bit first format.

        Returns:
            lsb bits
        """
        data = bitarray(endian="little")
        values = list(self._children.values())
        for value in values:
            data += value.bits_lsb
        return data

    def _get_children_generic(self) -> OrderedDict[str, ParseBase]:
        return self._children

    def _set_children_generic(
        self,
        children: OrderedDict[str, ParseBase] | Sequence[ParseBase] | None,
    ) -> None:
        self._children.clear()
        if isinstance(children, (dict)):
            keys = list(children.keys())
            for key in keys:
                value = children[key]
                self._children[key] = value
                value._set_parent_generic(self)
        elif isinstance(children, list):
            for value in children:
                self._children[value._name] = value
                value._set_parent_generic(self)

    def get_string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return f'{{{", ".join([str(value) for value in self._children.values()])}}}'

    @property
    def value(self) -> OrderedDict[str, ParseBase]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(
        self,
        value: OrderedDict[str, ParseBase] | Sequence[ParseBase] | Any,
    ) -> None:
        self.set_value(value)

    @property
    def children(self) -> OrderedDict[str, ParseBase]:
        """Get the parse objects that are contained by this one.

        Returns:
            the parse objects that are contained by this one
        """
        return self._get_children_generic()

    @children.setter
    def children(
        self,
        children: OrderedDict[str, ParseBase] | Sequence[ParseBase] | None,
    ) -> None:
        self._set_children_generic(children=children)

    def __bytes__(self) -> bytes:
        """Get the bytes that make up this field.

        Returns:
            the bytes of this field
        """
        return self.bits_lsb.tobytes()

    def __str__(self) -> str:
        """Get a nicely formatted string describing this field.

        Returns:
            a nicely formatted string describing this field
        """
        return f"{self._name}: {self.string_value}"

    def __repr__(self) -> str:
        """Get a nicely formatted string describing this field.

        Returns:
            a nicely formatted string describing this field
        """
        return f"<{self.__class__.__name__}> {self.__str__()}"

    def __setitem__(self, name: object, value: ParseBase) -> None:
        """Set an item in this dictionary to a new value.

        Args:
            name: a field name
            value: a new field value

        Returns:
            None
        """
        value._set_parent_generic(self)
        return self._children.__setitem__(str(name), value)

    def __getitem__(self, name: object) -> ParseBase:
        """Get an item in this dictionary by name.

        Args:
            name: a field name

        Returns:
            the named field
        """
        return self._children.__getitem__(str(name))

    def __delitem__(self, name: object) -> None:
        """Delete an item in this dictionary by name.

        Args:
            name: a field name

        Returns:
            None
        """
        return self._children.__delitem__(str(name))

    def __len__(self) -> int:
        """Get the count of this field's sub-fields.

        Returns:
            the length of this field dictionary
        """
        return len(self._children)

    @property
    def parent(self) -> ParseBase | None:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self._get_parent_generic()

    @parent.setter
    def parent(self, value: ParseBase | None) -> None:
        self._set_parent_generic(value)
