"""The base parsing object for handling parsing in a convenient (to modify) package."""
from __future__ import annotations

from collections import OrderedDict
from typing import Literal, Sequence, SupportsBytes, TypeVar

from bitarray import bitarray

from easyprotocol.base.utils import DEFAULT_ENDIANNESS, dataT, endianT, hex

UNDEFINED = "?UNDEFINED?"

T = TypeVar("T")


class ParseBase(SupportsBytes):
    """The base parsing object for handling parsing in a convenient (to modify) package."""

    def __init__(
        self,
        name: str,
        data: dataT = None,
        bit_count: int = -1,
        string_format: str | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        """Create the base parsing object for handling parsing in a convenient package.

        Args:
            name: name of parsed object
            data: bytes to be parsed
            bit_count: number of bits assigned to this field
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        self._name: str = ""
        self._endian: endianT = endian
        self._bits: bitarray = bitarray(endian="little")
        self._bit_count: int = bit_count
        self._name = name
        self._initialized = False
        self._parent: ParseBase | None = None
        self._children: OrderedDict[str, ParseBase] = OrderedDict()
        if string_format is None:
            self._string_format = "{}"
        else:
            self._string_format = string_format
        if data is not None:
            self.parse(data=data)

    def parse(self, data: dataT) -> bitarray:
        """Parse the passed bits or bytes into meaningful data.

        Args:
            data: bits or bytes to be parsed

        Raises:
            NotImplementedError: if not implemented for this field
        """
        raise NotImplementedError()

    def get_name(self) -> str:
        """Get the name of this field.

        Returns:
            the name
        """
        return self._name

    def set_name(self, value: str) -> None:
        """Set the name of this field.

        Args:
            value: the new name of this field
        """
        self._name = value

    def get_bits_lsb(self) -> bitarray:
        """Get the bits of this field in least-significant-bit first format.

        Returns:
            lsb bits
        """
        return self._bits

    def get_bits_msb(self) -> bitarray:
        """Get the bits of this field in most-significant-bit first format.

        Returns:
            msb bits
        """
        b = self.get_bits_lsb().tobytes()
        bits = bitarray(endian="big")
        bits.frombytes(b)
        if self._bit_count != -1:
            return bits[-self._bit_count :]
        else:
            return bits

    def set_bits_lsb(self, bits: bitarray) -> None:
        """Set the bits of this field in least-significant-bit first format.

        Args:
            bits: lsb bits

        Raises:
            NotImplementedError: until you override it in a sub-class
        """
        raise NotImplementedError()

    def _get_parent_generic(self) -> ParseBase | None:
        return self._parent

    def _set_parent_generic(self, parent: ParseBase | None) -> None:
        self._parent = parent

    def _get_children_generic(self) -> OrderedDict[str, ParseBase]:
        return self._children

    def _set_children_generic(
        self,
        children: OrderedDict[str, ParseBase] | Sequence[ParseBase],
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

    def get_string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return UNDEFINED

    def get_bytes_value(self) -> bytes:
        """Get the bytes that make up this field.

        If there are not enough bits, the last byte is padded with zeros.

        Returns:
            field bytes
        """
        return self.__bytes__()

    def get_hex_value(self) -> str:
        """Get the hexadecimal value of this field.

        Returns:
            the hexadecimal value of this field
        """
        return hex(self.get_bytes_value())

    @property
    def name(self) -> str:
        """Get the name of the field.

        Returns:
            the name of the field
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def bits_lsb(self) -> bitarray:
        """Get the bit value of the field.

        Returns:
            the bit value of the field
        """
        return self.get_bits_lsb()

    @bits_lsb.setter
    def bits_lsb(self, bits: bitarray) -> None:
        self.set_bits_lsb(bits)

    @property
    def bits(self) -> bitarray:
        """Get the bits of this field in most-significant-bit first format.

        Returns:
            msb bits
        """
        return self.get_bits_msb()

    @property
    def bits_str(self) -> str:
        """Get the bit string of this field in most-significant-bit first format.

        Returns:
            msb bit string
        """
        return f"{self.bits.to01()}:<b"

    @property
    def bits_str_lsb(self) -> str:
        """Get the bit string of this field in least-significant-bit first format.

        Returns:
            lsb bit string
        """
        return f"b>:{self.bits_lsb.to01()}"

    @property
    def string_format(self) -> str:
        """Get the format string of the field.

        Returns:
            the format string of the field
        """
        return self._string_format

    @string_format.setter
    def string_format(self, fmt: str) -> None:
        self._string_format = fmt

    @property
    def endian(self) -> Literal["little", "big"]:
        """Get the byte endianness value of this object.

        Returns:
            the byte endianness value of this object
        """
        return self._endian

    @property
    def byte_value(self) -> bytes:
        """Get the byte value of this object.

        Returns:
            the byte value of this object
        """
        return self.__bytes__()

    @property
    def string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        return self.get_string_value()

    @property
    def hex_value(self) -> str:
        """Get the hexadecimal value of this field.

        Returns:
            the hexadecimal value of this field
        """
        return self.get_hex_value()

    def __bytes__(self) -> bytes:
        """Get the bytes that make up this field.

        Returns:
            the bytes of this field
        """
        return self.get_bits_lsb().tobytes()

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
