"""Utility functions for parsers."""
from __future__ import annotations

from typing import Literal, SupportsBytes, Union

from bitarray import bitarray

dataT = Union[bitarray, bytearray, bytes, None]
endianT = Literal["little", "big"]
DEFAULT_ENDIANNESS: endianT = "big"


def input_to_bytes(
    data: dataT | SupportsBytes,
    bit_count: int | None = None,
) -> bitarray:
    """Convert bits or bytes into valid bits.

    Args:
        data: data that needs to be little-endian bits
        bit_count: the number of desired output bits

    Returns:
        the bit data

    Raises:
        TypeError: if the passed type is not supported
    """
    if isinstance(data, (bytes, bytearray)):
        bits = bitarray(endian="little")
        bits.frombytes(data)
        if len(bits) < (8 * len(data)):
            bits = bits + bitarray("0" * ((8 * len(data)) - len(bits)), endian="little")
    elif isinstance(data, bitarray):
        bit_length = len(data)
        bits = bitarray(endian="little")
        bits.frombytes(data.tobytes())
        bits = bits[:bit_length]
    elif isinstance(data, SupportsBytes):
        bits = bitarray(endian="little")
        bits.frombytes(bytes(data))
    else:
        raise TypeError()
    if bit_count is not None:
        if len(bits) < bit_count and isinstance(data, bytes):
            bits = bits + bitarray("0" * (bit_count - len(bits)), endian="little")
    return bits


def hex(bts: bytes | SupportsBytes, lsB: bool = True) -> str:  # noqa
    """Convert bytes to hexadecimal, but nicely.

    Args:
        bts: object or bytes to be turned into a hex string
        lsB: if set false, then the bytes will be reversed before turning into hex

    Returns:
        space-delimited hexadecimal bytes
    """
    if not isinstance(bts, bytes):
        bts = bytes(bts)
    if lsB is False:
        bts = bytearray(bts)
        bts.reverse()
        bts = bytes(bts)
    return bytes.hex(bts, sep=" ").upper()
