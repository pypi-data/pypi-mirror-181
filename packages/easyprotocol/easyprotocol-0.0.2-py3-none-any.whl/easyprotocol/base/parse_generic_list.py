"""This class is the basic parsing class for list types."""
from __future__ import annotations

from collections import OrderedDict
from typing import (
    Any,
    Generic,
    Iterable,
    Iterator,
    MutableSequence,
    Sequence,
    SupportsIndex,
    overload,
)

from bitarray import bitarray

from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS, ParseBase, T, endianT
from easyprotocol.base.utils import dataT, input_to_bytes


class ParseGenericList(
    ParseBase,
    MutableSequence[ParseBase],
    Generic[T],
):
    """The base parsing object for handling parsing in a convenient package."""

    def __init__(
        self,
        name: str,
        default: Sequence[ParseBase] | OrderedDict[str, ParseBase] = (),
        data: dataT = None,
        bit_count: int = -1,
        string_format: str = "{}",
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

        if isinstance(default, dict):
            self._set_children_generic(default)
        else:
            self._set_children_generic(OrderedDict({val._name: val for val in default}))
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

    def insert(self, index: SupportsIndex, value: ParseBase) -> None:
        """Insert a new field into this list.

        Args:
            index: the index at which the new field will be inserted
            value: the new field to be inserted
        """
        c: OrderedDict[str, ParseBase] = OrderedDict()
        existing_values = list(self._children.values())
        existing_values.insert(index, value)
        for v in existing_values:
            c[v._name] = v
        self._children = c

    def append(self, value: ParseBase) -> None:
        """Append a new field to this list.

        Args:
            value: the new field to be appended
        """
        self._children[value.name] = value

    def get_value(self) -> Sequence[ParseBase]:
        """Get the parsed fields that are part of this field.

        Returns:
            the value(s) of this field
        """
        return [item for item in self._children.values()]

    def set_value(
        self,
        value: Sequence[ParseBase] | OrderedDict[str, ParseBase] | Any,
    ) -> None:
        """Set the fields that are part of this field.

        Args:
            value: the new list of fields to assign to this field
        """
        if isinstance(value, (dict, OrderedDict)):
            values = list(value.values())
            for index in range(len(value)):
                item = values[index]
                if index < len(self._children):
                    self[index] = item
                    item._set_parent_generic(self)
                else:
                    self._children[item.name] = item
                    item._set_parent_generic(self)
        if isinstance(value, (Sequence)):
            for index in range(len(value)):
                item = value[index]
                if index < len(self._children):
                    self[index] = item
                    item._set_parent_generic(self)
                else:
                    self._children[item.name] = item
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

    def get_string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return f'[{", ".join([str(value) for value in self._children .values()])}]'

    @property
    def value(self) -> Sequence[ParseBase]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(self, value: Sequence[ParseBase] | Iterable[Any] | Any) -> None:
        self.set_value(value=value)

    @overload
    def __getitem__(self, index: SupportsIndex) -> ParseBase:
        """Get a field from this class by index.

        Args:
            index: index of the sub-field to retrieve
        """
        ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[ParseBase]:
        """Get fields from this class by index.

        Args:
            index: indices of the sub-fields to retrieve
        """
        ...

    def __getitem__(self, index: SupportsIndex | slice) -> ParseBase | Sequence[ParseBase]:
        """Get a field or fields from this class by index.

        Args:
            index: index or indices of the sub-field(s) to retrieve

        Returns:
            the field or fields
        """
        vs = list(self._children.values())[index]
        if isinstance(vs, list):
            return [v for v in vs]
        else:
            return vs

    def __delitem__(self, index: SupportsIndex | slice) -> None:
        """Delete one or more items from this list by index.

        Args:
            index: index or slice to delete
        """
        item = list(self._children.values())[index]
        if isinstance(item, list):
            for x in item:
                x._set_parent_generic(None)
                self._children.pop(x._name)
        else:
            item._set_parent_generic(None)
            self._children = OrderedDict({k: v for k, v in self._children.items() if k != item.name})

    @overload
    def __setitem__(self, index: SupportsIndex, value: ParseBase) -> None:
        """Set an item in this list to a new value.

        Args:
            index: index to replace
            value: new field value
        """
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[ParseBase]) -> None:
        """Set items in this list to new values.

        Args:
            index: indices to replace
            value: new field values
        """
        ...

    def __setitem__(self, index: SupportsIndex | slice, value: ParseBase | Iterable[ParseBase]) -> None:
        """Set one or more items in this list to new values.

        Args:
            index: one ore more indices
            value: one or more values
        """
        indexed_keys = list(self._children.keys())[index]
        c: OrderedDict[str, ParseBase] = OrderedDict()
        for existing_key in self._children:
            if isinstance(indexed_keys, str) and isinstance(value, ParseBase):
                if existing_key != indexed_keys:
                    c[existing_key] = self._children[existing_key]
                else:
                    c[indexed_keys] = value
            else:
                if isinstance(value, list):
                    for i, sub_key in enumerate(indexed_keys):
                        sub_value = value[i]
                        if existing_key != sub_key:
                            c[existing_key] = self._children[existing_key]
                        else:
                            c[sub_value._name] = sub_value
                            sub_value._set_parent_generic(self)
        self._children = c

    def __len__(self) -> int:
        """Get the count of this field's sub-fields.

        Returns:
            the length of this field list
        """
        return len(self._children)

    def _get_children_generic(self) -> OrderedDict[str, ParseBase]:
        return self._children

    def _set_children_generic(
        self,
        children: OrderedDict[str, ParseBase] | Sequence[ParseBase] | None,
    ) -> None:
        self._children.clear()
        if isinstance(children, (dict, OrderedDict)):
            keys = list(children.keys())
            for key in keys:
                value = children[key]
                self._children[key] = value
                value._set_parent_generic(self)
        elif isinstance(children, list):
            for value in children:
                self._children[value._name] = value
                value._set_parent_generic(self)

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

    def __iter__(self) -> Iterator[ParseBase]:
        """Iterate over the fields in this list.

        Returns:
            field iterator
        """
        return self._children.values().__iter__()
