"""Classes for parsing enumerations from bit fields."""
from __future__ import annotations

from enum import IntEnum
from typing import TypeVar, Union

from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS, endianT
from easyprotocol.base.utils import dataT
from easyprotocol.fields.unsigned_int import UIntFieldGeneric

E = TypeVar("E", bound=Union[IntEnum, int])


class EnumField(UIntFieldGeneric[E]):
    """Base IntEnum parsing class."""

    def __init__(
        self,
        name: str,
        bit_count: int,
        enum_type: type[E],
        default: E,
        data: dataT | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
        string_format: str = "{}",
    ) -> None:
        """Create base IntEnum parsing class.

        Args:
            name: name of parsed object
            bit_count: number of bits assigned to this field
            enum_type: the Enum.IntEnum class that defines the flags in use
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        self._enum_type: type[E] = enum_type
        super().__init__(
            name=name,
            bit_count=bit_count,
            data=data,
            default=default,
            endian=endian,
            string_format=string_format,
        )

    def get_value(self) -> E:
        """Get the parsed value of this class.

        Returns the integer value if the Enum.IntEnum value is not defined.

        Returns:
            the parsed value of this class
        """
        v = super().get_value()
        try:
            return self._enum_type(v)
        except Exception:
            return v

    def set_value(self, value: E) -> None:
        """Set the value of this field.

        Args:
            value: the new value to assign to this field
        """
        if isinstance(value, IntEnum):
            _value = value.value
        else:
            _value = value
        super().set_value(_value)

    def get_string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        v = self.value
        if isinstance(v, IntEnum):
            s = v.name
        else:
            s = v
        return self.string_format.format(s)

    @property
    def value(self) -> E:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(self, value: E) -> None:
        self.set_value(value)


class UInt8EnumField(EnumField[E]):
    """Eight bit enum parsing class."""

    def __init__(
        self,
        name: str,
        enum_type: type[E],
        default: E,
        data: dataT | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
        string_format: str = "{}",
    ) -> None:
        """Create eight bit enum parsing class.

        Args:
            name: name of parsed object
            enum_type: the Enum.IntEnum class that defines the flags in use
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        super().__init__(
            name=name,
            bit_count=8,
            enum_type=enum_type,
            data=data,
            default=default,
            endian=endian,
            string_format=string_format,
        )


class Enum8Field(UInt8EnumField[E]):
    """Eight bit enum parsing class."""

    ...


class UInt16EnumField(EnumField[E]):
    """Sixteen bit enum parsing class."""

    def __init__(
        self,
        name: str,
        enum_type: type[E],
        default: E,
        data: dataT | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
        string_format: str = "{}",
    ) -> None:
        """Create sixteen bit enum parsing class.

        Args:
            name: name of parsed object
            enum_type: the Enum.IntEnum class that defines the flags in use
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        super().__init__(
            name=name,
            bit_count=16,
            enum_type=enum_type,
            data=data,
            default=default,
            endian=endian,
            string_format=string_format,
        )


class Enum16Field(UInt16EnumField[E]):
    """Sixteen bit enum parsing class."""

    ...


class UInt24EnumField(EnumField[E]):
    """Twenty-four bit enum parsing class."""

    def __init__(
        self,
        name: str,
        enum_type: type[E],
        default: E,
        data: dataT | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
        string_format: str = "{}",
    ) -> None:
        """Create twenty-four bit enum parsing class.

        Args:
            name: name of parsed object
            enum_type: the Enum.IntEnum class that defines the flags in use
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        super().__init__(
            name=name,
            bit_count=24,
            enum_type=enum_type,
            data=data,
            default=default,
            endian=endian,
            string_format=string_format,
        )


class Enum24Field(UInt24EnumField[E]):
    """Twenty-four bit enum parsing class."""

    ...


class UInt32EnumField(EnumField[E]):
    """Thirty-two bit enum parsing class."""

    def __init__(
        self,
        name: str,
        enum_type: type[E],
        default: E,
        data: dataT | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
        string_format: str = "{}",
    ) -> None:
        """Create thirty-two bit enum parsing class.

        Args:
            name: name of parsed object
            enum_type: the Enum.IntEnum class that defines the flags in use
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        super().__init__(
            name=name,
            bit_count=32,
            enum_type=enum_type,
            data=data,
            default=default,
            endian=endian,
            string_format=string_format,
        )


class Enum32Field(UInt32EnumField[E]):
    """Thirty-two bit enum parsing class."""

    ...
