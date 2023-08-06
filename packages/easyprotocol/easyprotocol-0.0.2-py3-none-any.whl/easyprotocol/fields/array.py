"""Classes for parsing fields made up of an array of uniform sub-fields."""
from __future__ import annotations

from collections import OrderedDict
from typing import Any, Generic, Sequence, TypeVar, cast

from bitarray import bitarray

from easyprotocol.base.parse_field_dict import parseGenericT
from easyprotocol.base.parse_field_list import ParseFieldListGeneric
from easyprotocol.base.parse_generic import ParseBase
from easyprotocol.base.parse_generic_dict import K
from easyprotocol.base.parse_generic_value import ParseGenericValue
from easyprotocol.base.parse_value_list import ParseValueListGeneric
from easyprotocol.base.utils import dataT, input_to_bytes
from easyprotocol.fields.unsigned_int import UIntFieldGeneric

T = TypeVar("T")


class ParseArrayFieldGeneric(
    ParseFieldListGeneric[T, K],
    Generic[T, K],
):
    """Generic base class for parsing an array of uniform sub-fields."""

    def __init__(
        self,
        name: str,
        count: UIntFieldGeneric[int] | int,
        array_item_class: type[ParseGenericValue[T]],
        array_item_default: T,
        default: Sequence[T] | Sequence[ParseGenericValue[T]] | None = None,
        data: dataT | None = None,
        string_format: str = "{}",
    ) -> None:
        """Create generic base class for parsing an array of uniform sub-fields.

        Args:
            name: name of parsed object
            count: number of sub-fields
            array_item_class: class to use for sub-fields
            array_item_default: default value of sub-fields
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
        """
        self._count = count
        self._array_item_class = array_item_class
        self._array_item_default = array_item_default
        super().__init__(
            name=name,
            data=None,
            string_format=string_format,
        )
        if data is not None:
            self.parse(data=data)
        elif default is not None:
            self.create_default(default=default)

    def parse(self, data: dataT) -> bitarray:
        """Parse the bits of this field into meaningful data.

        Args:
            data: bytes to be parsed

        Returns:
            any leftover bits after parsing the ones belonging to this field
        """
        bit_data = input_to_bytes(data=data)
        if isinstance(self._count, UIntFieldGeneric):
            count = self._count.value
        else:
            count = self._count
        if count is not None:
            for i in range(count):
                f = self._array_item_class(
                    name=f"#{i}",
                    default=self._array_item_default,
                )
                bit_data = f.parse(data=bit_data)
                self._children[f.name] = f
        return bit_data

    def create_default(self, default: Sequence[T] | Sequence[ParseGenericValue[T]]) -> None:
        """Create an array of default valued sub-fields for this array field.

        Args:
            default: default values for the sub-fields
        """
        for i, item in enumerate(default):
            if isinstance(item, ParseGenericValue):
                f = self._array_item_class(
                    name=f"#{i}",
                    default=cast(ParseGenericValue[T], item).value,
                )
            else:
                f = self._array_item_class(
                    name=f"#{i}",
                    default=cast(T, item),
                )
            self._children[f.name] = f

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
        if value is not None:
            if isinstance(value, (Sequence)):
                for index in range(len(value)):
                    item = value[index]
                    if isinstance(item, ParseBase):
                        if index < len(self.children):
                            self[index] = item
                            item._set_parent_generic(self)
                        else:
                            item = self._array_item_class(
                                name=f"#{index}",
                                default=item,
                            )
                            item._set_parent_generic(self)
                            self._children[item.name] = item
                    else:
                        self[index].value = item
            else:
                keys = list(value.keys())
                for index in range(len(keys)):
                    key = keys[index]
                    item = value[key]
                    if isinstance(item, ParseBase):
                        if index < len(self.children):
                            self[index] = item
                            item._set_parent_generic(self)
                        else:
                            item = self._array_item_class(
                                name=f"#{index}",
                                default=item,
                            )
                            item._set_parent_generic(self)
                            self._children[item.name] = item
                    else:
                        self[index].value = item


class ParseArrayField(
    ParseArrayFieldGeneric[T, str],
    Generic[T],
):
    """Base class for parsing an array of uniform sub-fields."""

    def __init__(
        self,
        name: str,
        count: UIntFieldGeneric[int] | int,
        array_item_class: type[ParseGenericValue[T]],
        array_item_default: T,
        default: Sequence[ParseGenericValue[T]] | Sequence[T] | None = None,
        string_format: str = "{}",
        data: dataT | None = None,
    ) -> None:
        """Create base class for parsing an array of uniform sub-fields.

        Args:
            name: name of parsed object
            count: number of sub-fields
            array_item_class: class to use for sub-fields
            array_item_default: default value of sub-fields
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
        """
        super().__init__(
            name=name,
            count=count,
            array_item_class=array_item_class,
            array_item_default=array_item_default,
            string_format=string_format,
            default=default,
            data=data,
        )


class ParseValueArrayFieldGeneric(
    ParseValueListGeneric[K, T],
    Generic[T, K],
):
    """Generic base class for parsing an array of uniform value-type sub-fields.

    This class is specialized to appear as an array of value-types instead of field-types.
    This is meant to be used where there is an array of integers or similar rather than an array
    of fields with sub-fields.
    """

    def __init__(
        self,
        name: str,
        count: UIntFieldGeneric[int] | int,
        array_item_class: type[ParseGenericValue[T]],
        array_item_default: T,
        default: Sequence[T] | Sequence[ParseGenericValue[T]] | None = None,
        data: dataT | None = None,
        string_format: str = "{}",
    ) -> None:
        """Create generic base class for parsing an array of uniform value-type sub-fields.

        This class is specialized to appear as an array of value-types instead of field-types.
        This is meant to be used where there is an array of integers or similar rather than an array
        of fields with sub-fields.

        Args:
            name: name of parsed object
            count: number of sub-fields
            array_item_class: class to use for sub-fields
            array_item_default: default value of sub-fields
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
        """
        self._count = count
        self._array_item_class = array_item_class
        self._array_item_default = array_item_default
        super().__init__(
            name=name,
            data=None,
            string_format=string_format,
        )
        if data is not None:
            self.parse(data=data)
        elif default is not None:
            self.create_default(default=default)

    def parse(self, data: dataT) -> bitarray:
        """Parse the bits of this field into meaningful data.

        Args:
            data: bytes to be parsed

        Returns:
            any leftover bits after parsing the ones belonging to this field
        """
        bit_data = input_to_bytes(data=data)
        if isinstance(self._count, UIntFieldGeneric):
            count = self._count.value
        else:
            count = self._count
        if count is not None:
            for i in range(count):
                f = self._array_item_class(
                    name=f"#{i}",
                    default=self._array_item_default,
                )
                bit_data = f.parse(data=bit_data)
                self._children[f.name] = f
        return bit_data

    def create_default(self, default: Sequence[T] | Sequence[ParseGenericValue[T]]) -> None:
        """Create an array of default valued sub-fields for this array field.

        Args:
            default: default values for the sub-fields
        """
        for i, item in enumerate(default):
            if isinstance(item, ParseGenericValue):
                f = self._array_item_class(
                    name=f"#{i}",
                    default=cast(ParseGenericValue[T], item).value,
                )
            else:
                f = self._array_item_class(
                    name=f"#{i}",
                    default=cast(T, item),
                )
            self._children[f.name] = f

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
        if value is not None:
            if isinstance(value, (Sequence)):
                for index in range(len(value)):
                    item = value[index]
                    if isinstance(item, ParseGenericValue):
                        if index < len(self.children):
                            self[index] = cast("ParseGenericValue[T]", item)
                            item._set_parent_generic(self)
                        else:
                            item = self._array_item_class(
                                name=f"#{index}",
                                default=item,
                            )
                            item._set_parent_generic(self)
                            self._children[item.name] = item
                    else:
                        self[index] = cast("ParseGenericValue[T]", item)
            else:
                keys = list(value.keys())
                for index in range(len(keys)):
                    key = keys[index]
                    item = value[key]
                    if isinstance(item, ParseGenericValue):
                        if index < len(self.children):
                            self[index] = cast("ParseGenericValue[T]", item)
                            item._set_parent_generic(self)
                        else:
                            item = self._array_item_class(
                                name=f"#{index}",
                                default=item,
                            )
                            item._set_parent_generic(self)
                            self._children[item.name] = item
                    else:
                        self[index] = cast("ParseGenericValue[T]", item)

    def append(self, value: ParseGenericValue[T]) -> None:
        """Append a new field to this list.

        Args:
            value: the new field to be appended
        """
        self.children[value.name] = value


class ParseValueArrayField(
    ParseValueArrayFieldGeneric[T, str],
):
    """Base class for parsing an array of uniform value-type sub-fields.

    This class is specialized to appear as an array of value-types instead of field-types.
    This is meant to be used where there is an array of integers or similar rather than an array
    of fields with sub-fields.
    """

    def __init__(
        self,
        name: str,
        count: UIntFieldGeneric[int] | int,
        array_item_class: type[ParseGenericValue[T]],
        array_item_default: T,
        default: Sequence[T] | Sequence[ParseGenericValue[T]] | None = None,
        data: dataT | None = None,
        string_format: str = "{}",
    ) -> None:
        """Create base class for parsing an array of uniform value-type sub-fields.

        This class is specialized to appear as an array of value-types instead of field-types.
        This is meant to be used where there is an array of integers or similar rather than an array
        of fields with sub-fields.

        Args:
            name: _description_
            count: _description_
            array_item_class: _description_
            array_item_default: _description_
            default: _description_. Defaults to list().
            data: _description_. Defaults to None.
            string_format: _description_. Defaults to "{}".
        """
        super().__init__(
            name,
            count,
            array_item_class,
            array_item_default,
            default,
            data,
            string_format,
        )
