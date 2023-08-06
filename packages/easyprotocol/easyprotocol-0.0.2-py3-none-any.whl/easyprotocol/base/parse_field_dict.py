"""The base parsing object for handling parsing in a convenient package."""
from __future__ import annotations

from enum import Enum
from typing import Any, Generic, Iterator, Mapping, OrderedDict, Sequence, Union, cast

from bitarray import bitarray

from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS, ParseBase, endianT
from easyprotocol.base.parse_generic_dict import K, ParseGenericDict
from easyprotocol.base.parse_generic_list import ParseGenericList
from easyprotocol.base.parse_generic_value import ParseGenericValue, T
from easyprotocol.base.utils import dataT, input_to_bytes

parseGenericT = Union[ParseGenericValue[T], ParseGenericDict[K, T], ParseGenericList[T]]


class ParseFieldDictGeneric(
    ParseBase,
    Mapping[K, parseGenericT[K, T]],
    Generic[T, K],
):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        default: Sequence[ParseBase]
        | Sequence[ParseBase]
        | Sequence[parseGenericT[K, T]]
        | OrderedDict[str, ParseBase]
        | OrderedDict[str, parseGenericT[K, T]] = (),
        data: dataT = None,
        bit_count: int = -1,
        string_format: str | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        """Create the base parsing object for handling parsing in a convenient package.

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
        if default is not None:
            if isinstance(default, list):
                self.set_children(children=default)
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

    def popitem(self, last: bool = False) -> tuple[K, parseGenericT[K, T]]:
        """Remove item from list.

        Args:
            last: delete the last added item instead of the first

        Returns:
            the popped item
        """
        return cast(
            tuple[K, parseGenericT[K, T]],
            self._children.popitem(last=last),
        )

    def pop(self, name: str, default: parseGenericT[K, T] | None = None) -> parseGenericT[K, T] | None:
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
            p = self._children.pop(str(name), default)
        if p is not None:
            p._set_parent_generic(None)
        return cast(parseGenericT[K, T], p)

    def get_value(
        self,
    ) -> OrderedDict[str, parseGenericT[K, T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return cast(
            OrderedDict[str, parseGenericT[K, T]],
            OrderedDict(self._children),
        )

    def set_value(
        self,
        value: OrderedDict[K, parseGenericT[K, T]] | Sequence[parseGenericT[K, T]],
    ) -> None:
        """Set the fields that are part of this field.

        Args:
            value: the new list of fields or dictionary of fields to assign to this field
        """
        if isinstance(value, dict):
            for key, item in value.items():
                self.__setitem__(key, item)
                item._set_parent_generic(self)
        else:
            for item in value:
                key = item.name
                self.__setitem__(cast(K, key), item)
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

    def get_children(self) -> OrderedDict[str, parseGenericT[str, Any]]:
        """Get the children of this field as an ordered dictionary.

        Returns:
            the children of this field
        """
        return self._children  # pyright:ignore[reportGeneralTypeIssues]

    def set_children(
        self,
        children: Sequence[ParseBase]
        | OrderedDict[str, ParseBase]
        | OrderedDict[str, parseGenericT[K, T]]
        | Sequence[parseGenericT[K, T]],
    ) -> None:
        """Set the children of this field using an ordered dictionary.

        Args:
            children: the new children for this field
        """
        self._children.clear()
        if isinstance(children, (dict, OrderedDict)):
            keys = list(children.keys())
            for key in keys:
                value = children[key]
                self._children[str(key)] = value
                value._set_parent_generic(self)
        elif isinstance(children, list):
            for value in children:
                self._children[value._name] = value
                value._set_parent_generic(self)

    def get_parent(self) -> parseGenericT[str, Any] | None:
        """Get the field (if any) that is this field's parent.

        Returns:
            this field's parent (or None)
        """
        return cast(parseGenericT[str, Any], self._parent)

    def set_parent(self, parent: parseGenericT[str, Any] | None) -> None:
        """Set this field's parent.

        Args:
            parent: this field's new parent (or None)
        """
        self._parent = parent

    def get_string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return f'{{{", ".join([str(value) for value in self._children.values()])}}}'

    @property
    def value(self) -> OrderedDict[str, parseGenericT[K, T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(
        self,
        value: Sequence[parseGenericT[K, T]],
    ) -> None:
        self.set_value(value)

    @property
    def parent(self) -> parseGenericT[str, Any] | None:
        """Get the field (if any) that is this field's parent.

        Returns:
            this field's parent (or None)
        """
        return self.get_parent()

    @parent.setter
    def parent(self, value: parseGenericT[str, Any] | None) -> None:
        self.set_parent(value)

    @property
    def children(self) -> OrderedDict[str, parseGenericT[str, Any]]:
        """Get the parse objects that are contained by this one.

        Returns:
            the parse objects that are contained by this one
        """
        return self.get_children()

    @children.setter
    def children(
        self,
        children: OrderedDict[str, ParseBase] | OrderedDict[str, parseGenericT[K, T]],
    ) -> None:
        self.set_children(children=children)

    def __setitem__(self, name: K, value: parseGenericT[K, T]) -> None:
        """Set an item in this list to a new value.

        Args:
            name: name of item to replace
            value: new field value
        """
        value._set_parent_generic(self)
        self._children.__setitem__(str(name), value)

    def __getitem__(self, name: K) -> parseGenericT[K, T]:
        """Get a field from this class by name.

        Args:
            name: name of the sub-field to retrieve

        Returns:
            the field
        """
        return cast(parseGenericT[K, T], self._children.__getitem__(str(name)))

    def __delitem__(self, name: K) -> None:
        """Delete item from this list by name.

        Args:
            name: name of item to delete
        """
        self._children.__delitem__(str(name))

    def __len__(self) -> int:
        """Get the count of this field's sub-fields.

        Returns:
            the length of this field dictionary
        """
        return len(self._children)

    def __iter__(self) -> Iterator[K]:
        """Iterate over the fields in this list.

        Returns:
            field iterator
        """
        return self._children.__iter__()  # pyright:ignore[reportGeneralTypeIssues]


class ParseFieldDict(ParseFieldDictGeneric[str, Any]):
    """The base field dictionary."""

    ...
