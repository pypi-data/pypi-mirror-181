from __future__ import annotations

import math
import struct
from collections import OrderedDict
from typing import Any, Sequence

import crc
from bitarray import bitarray
from bitarray.util import int2ba

from easyprotocol.base import dataT, input_to_bytes
from easyprotocol.base.parse_generic import ParseBase
from easyprotocol.fields import (
    BoolField,
    ChecksumField,
    ParseArrayField,
    ParseArrayFieldGeneric,
    UInt8EnumField,
    UInt8Field,
    UInt16Field,
    UIntField,
)
from easyprotocol.protocols.modbus.constants import (
    ModbusFieldNamesEnum,
    ModbusFunctionEnum,
)


class ModbusDeviceId(UInt8Field):
    def __init__(
        self,
        default: int = 1,
        data: dataT | None = None,
    ) -> None:
        super().__init__(
            name=ModbusFieldNamesEnum.DeviceID.value,
            data=data,
            default=default,
            endian="big",
        )


class ModbusFunction(UInt8EnumField[ModbusFunctionEnum]):
    def __init__(
        self,
        default: ModbusFunctionEnum = ModbusFunctionEnum.ReadCoils,
        data: dataT | None = None,
    ) -> None:
        super().__init__(
            name=ModbusFieldNamesEnum.FunctionCode.value,
            enum_type=ModbusFunctionEnum,
            default=default,
            data=data,
            endian="little",
        )


class ModbusAddress(UInt16Field):
    def __init__(
        self,
        default: int = 1,
        data: dataT | None = None,
    ) -> None:
        super().__init__(
            name=ModbusFieldNamesEnum.Address.value,
            default=default,
            data=data,
            endian="little",
        )


class ModbusCount(UInt16Field):
    def __init__(
        self,
        default: int = 1,
        data: dataT | None = None,
    ) -> None:
        super().__init__(
            name=ModbusFieldNamesEnum.Count.value,
            default=default,
            data=data,
            endian="little",
            string_format="{}",
        )


class ModbusByteCount(UInt8Field):
    def __init__(
        self,
        default: int = 0,
        data: dataT | None = None,
    ) -> None:
        super().__init__(
            name=ModbusFieldNamesEnum.ByteCount.value,
            default=default,
            data=data,
            endian="big",
            string_format="{}",
        )


class ModbusCRC(ChecksumField):
    def __init__(
        self,
        default: int = 0,
        data: dataT | None = None,
    ) -> None:
        super().__init__(
            name=ModbusFieldNamesEnum.CRC.value,
            bit_count=16,
            default=default,
            crc_configuration=crc.Configuration(
                width=16,
                polynomial=0x8005,
                init_value=0xFFFF,
                final_xor_value=0x0000,
                reverse_input=True,
                reverse_output=True,
            ),
            data=data,
            string_format="{:04X}(hex)",
            endian="little",
        )

    def update_field(self, data: dataT | None = None) -> tuple[int, bytes, bitarray]:
        if self.parent is not None:
            byte_data = bytes(self.parent)
        else:
            raise Exception("can't")
        crc_int = self.crc_calculator.checksum(byte_data[:-2])
        crc_bytes = int.to_bytes(crc_int, length=2, byteorder=self.endian)
        crc_bits = int2ba(crc_int, length=self._bit_count)
        self.value = crc_int
        return (crc_int, crc_bytes, crc_bits)


class ModbusCoilArray(ParseArrayField[bool]):
    def __init__(
        self, count: int | UIntField, data: dataT | None = None, default: Sequence[bool] | Sequence[int] = list()
    ) -> None:
        super().__init__(
            name=ModbusFieldNamesEnum.CoilArray.value,
            count=count,
            array_item_class=BoolField,
            array_item_default=False,
            data=data,
        )
        if default:
            self.set_value(default)

    def set_value(  # pyright:ignore[reportIncompatibleMethodOverride]
        self, value: Sequence[bool] | Sequence[int]
    ) -> None:
        if len(value) == 0:
            return
        if isinstance(value[0], bool):
            _value = value
        else:
            bit_array = bitarray(endian="little")
            for v in value:
                bit_array.frombytes(struct.pack("B", v))
            _value = [True if b else False for b in bit_array]
        keys = list(self._children.keys())
        for i, b in enumerate(_value):
            if i < len(self.children):
                self.children[keys[i]].value = b
            else:
                f = self._array_item_class(
                    name=f"+{i}",
                    default=self._array_item_default,
                )
                self.append(f)

    def parse(self, data: dataT) -> bitarray:
        """Parse bytes that make of this protocol field into meaningful data.

        Args:
            data: bytes to be parsed

        Raises:
            NotImplementedError: if not implemented for this field
        """
        bit_data = input_to_bytes(data=data)
        if isinstance(self._count, int):
            _count = self._count * 8
        else:
            if self._count.value is None:
                _count = 0
            else:
                _count = self._count.value * 8
        for i in range(_count):
            f = self._array_item_class(
                f"+{i}",
                self._array_item_default,
            )
            bit_data = f.parse(data=bit_data)
            self.append(f)
        return bit_data

    @property
    def string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        chunks: list[str] = []
        keys = list(self._children.keys())
        bits_per_chunk = 8
        for i in range(0, len(keys), bits_per_chunk):
            chunk_key = keys[i]
            vals = "".join(["1" if self.children[keys[j]].value else "0" for j in range(i, i + bits_per_chunk)])
            chunks.append(chunk_key + ":" + vals)
        return f"[{', '.join( chunks)}]"

    # @property
    # def value(self) -> list[bool]:
    #     """Get the parsed value of the field.

    #     Returns:
    #         the value of the field
    #     """
    #     return list([v.value for v in self.children.values()])

    # @value.setter
    # def value(self, value: Sequence[bool]) -> None:
    #     temp = UInt8Field(name="temp", endian="little")
    #     for index, item in enumerate(value):
    #         temp.value = item
    #         bits = temp.bits_lsb
    #         bits.reverse()
    #         for i in range(len(bits)):
    #             self[index * 8 + i] = True if bits[i] else False
