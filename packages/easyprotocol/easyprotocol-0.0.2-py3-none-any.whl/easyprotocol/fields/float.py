"""Floating point-number field parsing."""
from __future__ import annotations

import math
import struct
from typing import Any, Generic, TypeVar, Union, cast

from bitarray import bitarray

from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS, endianT
from easyprotocol.base.parse_generic_value import ParseGenericValue
from easyprotocol.base.utils import dataT, input_to_bytes

F = TypeVar("F", bound=Union[float, Any])
FLOAT_STRING_FORMAT = "{:.3e}"


class FloatField(ParseGenericValue[F]):
    """The base floating-point number field parsing."""

    def __init__(
        self,
        name: str,
        bit_count: int,
        default: F = 0.0,
        data: dataT | None = None,
        string_format: str | None = FLOAT_STRING_FORMAT,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        """Create base floating-point number field parsing class.

        This class doesn't do much but provide a superclass for non-integer number fields.

        Args:
            name: name of parsed object
            default: the default value for this class
            data: bytes to be parsed
            bit_count: number of bits assigned to this field
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        self.bit_count = bit_count
        super().__init__(
            name=name,
            data=data,
            default=default,
            string_format=string_format,
            endian=endian,
        )


class Float32IEEFieldGeneric(
    FloatField[F],
    Generic[F],
):
    """Base thirty-two bit IEEE floating-point number field parsing.

    This class is generic in case there is some other class in the future that can inherit from it.
    """

    def __init__(
        self,
        name: str,
        default: F = 0.0,
        data: dataT | None = None,
        string_format: str | None = FLOAT_STRING_FORMAT,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        """Create base thirty-two bit IEEE floating-point number class.

        This class is generic in case there is some other class in the future that can inherit from it.

        Args:
            name: name of parsed object
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        super().__init__(
            name,
            bit_count=32,
            data=data,
            default=default,
            string_format=string_format,
            endian=endian,
        )

    def parse(self, data: dataT) -> bitarray:
        """Parse bytes that make up this field into meaningful data.

        Args:
            data: bytes to be parsed

        Returns:
            any leftover bits after parsing this field

        Raises:
            IndexError: if there is insufficient data to parse this field
        """
        bits = input_to_bytes(
            data=data,
            bit_count=self.bit_count,
        )
        _bit_mask = (2**self.bit_count) - 1
        bit_mask = bitarray(endian="little")
        bit_mask.frombytes(
            int.to_bytes(_bit_mask, length=math.ceil(self.bit_count / 8), byteorder="little", signed=False)
        )
        if len(bit_mask) < len(bits):
            bit_mask = bit_mask + bitarray("0" * (len(bits) - len(bit_mask)), endian="little")
        if len(bits) < len(bit_mask) or len(bits) < self._bit_count:
            raise IndexError("Too little data to parse field.")
        my_bits = (bits & bit_mask)[: self.bit_count]
        temp_bits = bitarray(my_bits)
        byte_count = math.ceil(self.bit_count / 8)
        if len(temp_bits) < byte_count * 8:
            temp_bits = temp_bits + bitarray("0" * ((byte_count * 8) - len(temp_bits)), endian="little")
        self._bits = my_bits[: self.bit_count]
        if len(bits) >= self.bit_count:
            return bits[self.bit_count :]
        else:
            return bitarray(endian="little")

    def get_value(self) -> F:
        """Get the parsed value of this class.

        Returns:
            the parsed value of this class
        """
        b = self.bits_lsb.tobytes()
        if self.endian == "little":
            return cast(F, struct.unpack("<f", b)[0])
        else:
            return cast(F, struct.unpack(">f", b)[0])

    def set_value(self, value: F) -> None:
        """Set the value of this field.

        Args:
            value: the new value to assign to this field
        """
        if self.endian == "little":
            bytes_val = bytearray(struct.pack("<f", value))
        else:
            bytes_val = bytearray(struct.pack(">f", value))
        bits = bitarray(endian="little")
        bits.frombytes(bytes_val)
        self._bits = bits

    def __bytes__(self) -> bytes:
        """Get the bytes that make up this field.

        Returns:
            the bytes of this field
        """
        return self._bits.tobytes()

    def set_bits_lsb(self, bits: bitarray) -> None:
        """Set the bits of this field in least-significant-bit first format.

        Args:
            bits: lsb bits
        """
        if bits.endian() != "little":
            v = bits.tobytes()
            _bits = bitarray(endian="little")
            _bits.frombytes(v)
        else:
            _bits = bits
        if len(_bits) < self.bit_count:
            _bits = _bits + bitarray("0" * (self.bit_count - len(_bits)), endian="little")
        self._bits = _bits[: self.bit_count]

    def get_string_value(self) -> str:
        """Get the string value of this field.

        Returns:
            the string value of this field
        """
        return self.string_format.format(self.value)


class Float32IEEField(Float32IEEFieldGeneric[float]):
    """Thirty-two bit IEEE floating-point number field parsing."""

    ...


class Float32Field(Float32IEEField):
    """Thirty-two bit IEEE floating-point number field parsing."""

    ...
