from __future__ import annotations

import math
from typing import Literal, cast

from bitarray import bitarray
from bitarray.util import int2ba
from crc import Calculator, Configuration

from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS, endianT
from easyprotocol.base.utils import dataT, input_to_bytes
from easyprotocol.fields.unsigned_int import UIntFieldGeneric


class ChecksumField(UIntFieldGeneric[int]):
    def __init__(
        self,
        name: str,
        bit_count: int,
        crc_configuration: Configuration,
        default: int = 0,
        data: dataT | None = None,
        string_format: str = "{:X}(hex)",
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        super().__init__(
            name=name,
            bit_count=bit_count,
            data=data,
            default=default,
            string_format=string_format,
            endian=endian,
        )
        self.crc_calculator = Calculator(
            configuration=crc_configuration,
        )

    def update_field(self, data: dataT | None = None) -> tuple[int, bytes, bitarray]:
        if data is None:
            if self.parent is not None:
                byte_data = bytes(self.parent)
            else:
                byte_data = b""
        else:
            byte_data = input_to_bytes(data=data, bit_count=self._bit_count).tobytes()
        crc_int = self.crc_calculator.checksum(byte_data)
        byte_length = math.ceil(self._bit_count / 8)
        crc_bytes = int.to_bytes(crc_int, length=byte_length, byteorder="little")
        crc_int = int.from_bytes(crc_bytes, byteorder=self._endian, signed=False)
        crc_bits = int2ba(crc_int, length=self._bit_count)
        self.value = crc_int
        return (crc_int, crc_bytes, crc_bits)
