"""The base field dictionary."""
from __future__ import annotations

from collections import OrderedDict
from typing import (
    Any,
    Generic,
    Iterable,
    Iterator,
    Mapping,
    Sequence,
    SupportsIndex,
    Union,
    cast,
    overload,
)

from bitarray import bitarray

from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS, ParseBase, T, endianT
from easyprotocol.base.parse_generic_dict import K, ParseGenericDict
from easyprotocol.base.parse_generic_list import ParseGenericList
from easyprotocol.base.parse_generic_value import ParseGenericValue
from easyprotocol.base.utils import dataT, input_to_bytes

parseGenericT = Union[ParseGenericValue[T], ParseGenericDict[K, T], ParseGenericList[T]]
valueGenericT = Union[T, Mapping[K, T], Sequence[T]]


class ParseFieldListGeneric(
    ParseBase,
    Sequence[parseGenericT[K, T]],
    Generic[T, K],
):
    """The base generic field dictionary."""

    def __init__(
        self,
        name: str,
        default: Sequence[ParseBase]
        | Sequence[parseGenericT[K, T]]
        | OrderedDict[str, ParseBase]
        | OrderedDict[str, parseGenericT[K, T]] = (),
        data: dataT = None,
        bit_count: int = -1,
        string_format: str = "{}",
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        """Create a generic field dictionary.

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

        self.set_children(default)
        if data is not None:
            self.parse(data)
        elif default is not None:
            self.set_value(default)

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

    def insert(self, index: SupportsIndex, value: parseGenericT[K, T]) -> None:
        """Insert a new field into this list.

        Args:
            index: the index at which the new field will be inserted
            value: the new field to be inserted
        """
        c: OrderedDict[str, ParseBase] = OrderedDict()
        existing_values = list(self._children.values())
        existing_values.insert(index, value)
        for v in existing_values:
            c[v.name] = v
        self.children = cast(OrderedDict[str, parseGenericT[K, T]], c)

    def append(self, value: parseGenericT[K, T] | Any) -> None:
        """Append a new field to this list.

        Args:
            value: the new field to be appended
        """
        self.children[value.name] = value

    def get_value(self) -> Sequence[parseGenericT[K, T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return [item for item in self.children.values()]

    def set_value(
        self,
        value: Sequence[parseGenericT[K, T] | Any]
        | OrderedDict[
            str,
            parseGenericT[K, T] | Any,
        ],
    ) -> None:
        """Set the fields that are part of this field.

        Args:
            value: the new list of fields or dictionary of fields to assign to this field
        """
        if isinstance(value, (dict, OrderedDict)):
            values = list(value.values())
            for index, (key, item) in enumerate(value.items()):
                item = values[index]
                if index < len(self._children):
                    if isinstance(item, (ParseFieldList, ParseGenericDict, ParseGenericValue)):
                        self[index] = item
                    else:
                        self[index].value = item
                    self[index]._set_parent_generic(self)
                else:
                    if isinstance(item, (ParseFieldList, ParseGenericDict, ParseGenericValue)):
                        self.children[item.name] = item
                    else:
                        self.children[key].value = item
                    self._children[item.name]._set_parent_generic(self)
        else:
            for index in range(len(value)):
                item = value[index]
                if index < len(self._children):
                    self[index] = item
                    self[index]._set_parent_generic(self)
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

    def get_children(self) -> OrderedDict[str, parseGenericT[K, T]]:
        """Get the children of this field as an ordered dictionary.

        Returns:
            the children of this field
        """
        return cast(OrderedDict[str, parseGenericT[K, T]], self._children)

    def set_children(
        self,
        children: OrderedDict[str, parseGenericT[K, T]]
        | Sequence[parseGenericT[K, T]]
        | OrderedDict[str, ParseBase]
        | Sequence[ParseBase],
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
                self._children[key] = value
                value._set_parent_generic(self)
        elif isinstance(children, list):
            for value in children:
                self._children[value._name] = value
                value._set_parent_generic(self)

    def get_parent(self) -> parseGenericT[K, T] | None:
        """Get the field (if any) that is this field's parent.

        Returns:
            this field's parent (or None)
        """
        return cast(parseGenericT[K, T], self._parent)

    def set_parent(self, parent: parseGenericT[K, T] | None) -> None:
        """Set this field's parent.

        Args:
            parent: this field's new parent (or None)
        """
        self._parent = parent

    @property
    def parent(self) -> parseGenericT[K, T] | None:
        """Get the field (if any) that is this field's parent.

        Returns:
            this field's parent (or None)
        """
        return self.get_parent()

    @parent.setter
    def parent(self, value: parseGenericT[K, T] | None) -> None:
        self.set_parent(value)

    @property
    def children(self) -> OrderedDict[str, parseGenericT[K, T]]:
        """Get the parse objects that are contained by this one.

        Returns:
            the parse objects that are contained by this one
        """
        return self.get_children()

    @children.setter
    def children(
        self,
        children: OrderedDict[str, parseGenericT[K, T]],
    ) -> None:
        self.set_children(children=children)

    def get_string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return f'[{", ".join([str(value) for value in self._children .values()])}]'

    @property
    def value(self) -> Sequence[parseGenericT[K, T]]:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(self, value: Sequence[parseGenericT[K, T]] | Sequence[Any] | Any) -> None:
        self.set_value(value=value)

    @overload
    def __getitem__(self, index: SupportsIndex) -> parseGenericT[K, T]:
        """Get a field from this class by index.

        Args:
            index: index of the sub-field to retrieve
        """
        ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[parseGenericT[K, T]]:
        """Get fields from this class by index.

        Args:
            index: indices of the sub-fields to retrieve
        """
        ...

    def __getitem__(self, index: SupportsIndex | slice) -> parseGenericT[K, T] | Sequence[parseGenericT[K, T]]:
        """Get a field or fields from this class by index.

        Args:
            index: index or indices of the sub-field(s) to retrieve

        Returns:
            the field or fields
        """
        vs = list(self.children.values())[index]
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
    def __setitem__(self, index: SupportsIndex, value: parseGenericT[K, T] | Any) -> None:
        """Set an item in this list to a new value.

        Args:
            index: index to replace
            value: new field value
        """
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[parseGenericT[K, T]] | Iterable[Any]) -> None:
        """Set items in this list to new values.

        Args:
            index: indices to replace
            value: new field values
        """
        ...

    def __setitem__(
        self, index: SupportsIndex | slice, value: parseGenericT[K, T] | Iterable[parseGenericT[K, T]] | Iterable[Any]
    ) -> None:
        """Set one or more items in this list to new values.

        Args:
            index: one ore more indices
            value: one or more values
        """
        indexed_keys = list(self._children.keys())[index]
        c: OrderedDict[str, ParseBase] = OrderedDict()
        for existing_key in self.children:
            if isinstance(indexed_keys, str):
                if isinstance(value, ParseBase):
                    if existing_key != indexed_keys:
                        c[existing_key] = self.children[existing_key]
                    else:
                        c[indexed_keys] = value
                else:
                    if existing_key != indexed_keys:
                        c[existing_key] = self.children[existing_key]
                    else:
                        c[indexed_keys] = self.children[existing_key]
                        c[indexed_keys].value = value  # pyright:ignore[reportGeneralTypeIssues]
            else:
                if isinstance(value, list):
                    for i, sub_key in enumerate(indexed_keys):
                        if isinstance(value[i], ParseBase):
                            sub_value = value[i]
                            if existing_key != sub_key:
                                c[existing_key] = self.children[existing_key]
                            else:
                                c[sub_value._name] = sub_value
                                sub_value._set_parent_generic(self)
                        else:
                            sub_value = value[i]
                            if existing_key != sub_key:
                                c[existing_key] = self.children[existing_key]
                            else:
                                c[sub_value._name].value = sub_value  # pyright:ignore[reportGeneralTypeIssues]
                                sub_value._set_parent_generic(self)
        self.children = cast("OrderedDict[str,parseGenericT[K,T]]", c)

    def __len__(self) -> int:
        """Get the count of this field's sub-fields.

        Returns:
            the length of this field list
        """
        return len(self._children)

    def __iter__(self) -> Iterator[parseGenericT[K, T]]:
        """Iterate over the fields in this list.

        Returns:
            field iterator
        """
        return self.children.values().__iter__()


class ParseFieldList(ParseFieldListGeneric[str, Any]):
    """The base field list."""

    ...
