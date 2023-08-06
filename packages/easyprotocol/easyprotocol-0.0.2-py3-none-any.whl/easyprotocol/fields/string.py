"""String and bytes parsing fields."""
from __future__ import annotations

import math
import struct
from typing import cast

from bitarray import bitarray

from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS
from easyprotocol.base.utils import dataT
from easyprotocol.fields.array import ParseValueArrayField
from easyprotocol.fields.unsigned_int import UIntField, UIntFieldGeneric

DEFAULT_CHAR_FORMAT: str = '"{}"'
DEFAULT_STRING_FORMAT: str = '"{}"'
DEFAULT_BYTE_FORMAT: str = '"{}"(byte)'
DEFAULT_BYTES_FORMAT: str = '"{}"(bytes)'


class CharField(UIntFieldGeneric[str]):
    """Single ASCII character field."""

    def __init__(
        self,
        name: str,
        default: str = "\x00",
        data: dataT | None = None,
        string_format: str = '"{}"',
        string_encoding: str = "latin1",
    ) -> None:
        """Create eight-bit character field.

        Defaults to ASCII (latin1) decoding.

        Args:
            name: name of parsed object
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
            string_encoding: encoding for bytes to string conversion (e.g. 'latin1' or 'utf-8'),
        """
        self._string_encoding: str = string_encoding
        super().__init__(
            name=name,
            bit_count=8,
            data=data,
            default=default,
            endian=DEFAULT_ENDIANNESS,
            string_format=string_format,
        )

    def get_value(self) -> str:
        """Get the parsed value of this class.

        Returns:
            the parsed value of this class
        """
        b = bytes(self)
        s = b.decode(self._string_encoding)
        return s

    def set_value(self, value: str) -> None:
        """Set the value of this field.

        Args:
            value: the new value to assign to this field
        """
        _value = ord(value[0])
        byte_count = math.ceil(self._bit_count / 8)
        my_bytes = int.to_bytes(_value, length=byte_count, byteorder=self.endian, signed=False)
        bits = bitarray(endian="little")
        bits.frombytes(my_bytes)
        self._bits = bits[: self._bit_count]


class UInt8CharField(CharField):
    """Single ASCII character field."""

    ...


class StringField(ParseValueArrayField[str]):
    """String parsing field."""

    def __init__(
        self,
        name: str,
        count: UIntField | int = 0,
        data: dataT | None = None,
        string_format: str = '"{}"',
        string_encoding: str = "latin1",
        default: str = "",
        char_default: str = "\x00",
    ) -> None:
        """Create string parsing field.

        Args:
            name: name of parsed object
            default: the default value for this class
            char_default: default character for instantiating an instance of this class with count > 1
            count: the number of bytes in this field
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
            string_encoding: encoding for bytes to string conversion (e.g. 'latin1' or 'utf-8'),
        """
        self._string_encoding: str = string_encoding
        super().__init__(
            name=name,
            count=count,
            array_item_class=CharField,
            array_item_default=char_default,
            default=[s for s in default],
            data=data,
            string_format=string_format,
        )

    def get_value(self) -> str:
        """Get the parsed value of this class.

        Returns:
            the parsed value of this class
        """
        return "".join([v.value for v in self.children.values()])

    def set_value(self, value: str) -> None:  # pyright:ignore[reportIncompatibleMethodOverride]
        """Set the value of this field.

        Args:
            value: the new value to assign to this field
        """
        if value is None:
            return
        for index, item in enumerate(value):
            if index < len(self._children):
                kid = cast(CharField, self[index])
                kid.value = item
            else:
                f = self._array_item_class(f"#{index}", default=self._array_item_default)
                f.value = item
                self._children[f.name] = f

    @property
    def value(self) -> str:
        """Get the parsed value of this class.

        Returns:
            the parsed value of this class
        """
        return self.get_value()

    @value.setter
    def value(self, value: str) -> None:  # pyright:ignore[reportIncompatibleMethodOverride]
        self.set_value(value=value)

    def get_string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return self._string_format.format(self.value)


class ByteField(UIntFieldGeneric[bytes]):
    """Single byte field that returns bytes object instead of int."""

    def __init__(
        self,
        name: str,
        default: bytes = b"\x00",
        data: dataT | None = None,
        string_format: str = '"{}"(bytes)',
    ) -> None:
        """Single byte field that returns bytes object instead of int.

        Args:
            name: name of parsed object
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
        """
        super().__init__(
            name=name,
            bit_count=8,
            data=data,
            default=default,
            endian=DEFAULT_ENDIANNESS,
            string_format=string_format,
        )

    def get_value(self) -> bytes:
        """Get the parsed value of this class.

        Returns:
            the parsed value of this class
        """
        return self.byte_value

    @property
    def value(self) -> bytes:
        """Get the parsed value of this class.

        Returns:
            the parsed value of this class
        """
        return self.get_value()

    @value.setter
    def value(self, value: int | str | bytes) -> None:
        self.set_value(value)

    def set_value(self, value: int | str | bytes) -> None:
        """Set the value of this field.

        Args:
            value: the new value to assign to this field
        """
        if isinstance(value, bytes):
            _value = value[0]
        elif isinstance(value, str):
            _value = struct.pack("s", value[0])[0]
        else:
            _value = int(value)
        byte_count = math.ceil(self._bit_count / 8)
        my_bytes = int.to_bytes(_value, length=byte_count, byteorder=self.endian, signed=False)
        bits = bitarray(endian="little")
        bits.frombytes(my_bytes)
        self._bits = bits[: self._bit_count]

    def get_string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return self._string_format.format(self.hex_value)


class UInt8ByteField(ByteField):
    """Single byte field that returns bytes object instead of int."""

    ...


class BytesField(ParseValueArrayField[bytes]):
    """Variable length bytes field that returns bytes."""

    def __init__(
        self,
        name: str,
        count: UIntField | int,
        default: bytes = b"",
        byte_default: bytes = b"\x00",
        data: dataT | None = None,
        string_format: str = '"{}"(bytes)',
    ) -> None:
        """Create variable length bytes field that returns bytes.

        Args:
            name: name of parsed object
            default: the default value for this class
            byte_default: the default value of each byte when creating BytesField with count > 0
            count: the number of bytes in this field
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
        """
        super().__init__(
            name=name,
            count=count,
            array_item_class=ByteField,
            array_item_default=byte_default,
            default=[bytes([b]) for b in default],
            data=data,
            string_format=string_format,
        )

    @property
    def value(self) -> bytes:  # pyright:ignore[reportIncompatibleMethodOverride]
        """Get the parsed value of this class.

        Returns:
            the parsed value of this class
        """
        return self.get_value()

    @value.setter
    def value(self, value: bytes) -> None:  # pyright:ignore[reportIncompatibleMethodOverride]
        self.set_value(value=value)

    def get_value(self) -> bytes:  # pyright:ignore[reportIncompatibleMethodOverride]
        """Get the parsed value of this class.

        Returns:
            the parsed value of this class
        """
        return b"".join([v.value for v in self.children.values()])

    def set_value(self, value: bytes) -> None:  # pyright:ignore[reportIncompatibleMethodOverride]
        """Set the value of this field.

        Args:
            value: the new value to assign to this field
        """
        for index, item in enumerate(value):
            if index < len(self._children):
                kid = cast(ByteField, self[index])
                kid.value = item
            else:
                f = self._array_item_class(
                    name=f"#{index}",
                    default=self._array_item_default,
                )
                f.value = bytes([item])
                self._children[f.name] = f

    def get_string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return self.string_format.format(self.get_hex_value())
