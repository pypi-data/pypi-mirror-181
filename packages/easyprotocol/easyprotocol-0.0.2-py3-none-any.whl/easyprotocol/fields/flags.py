"""Classes for parsing flags from bit fields."""
from __future__ import annotations

from enum import IntFlag
from typing import Sequence, TypeVar, Union, cast

from easyprotocol.base.parse_generic import DEFAULT_ENDIANNESS, endianT
from easyprotocol.base.utils import dataT
from easyprotocol.fields.unsigned_int import UIntFieldGeneric

F = TypeVar("F", bound=Union[IntFlag, int])


class FlagsField(UIntFieldGeneric[F]):
    """Base flags parsing class."""

    def __init__(
        self,
        name: str,
        bit_count: int,
        flags_type: type[F],
        default: F,
        data: dataT | None = None,
        string_format: str = "{}",
        endian: endianT = DEFAULT_ENDIANNESS,
    ) -> None:
        """Create base flags parsing class.

        Args:
            name: name of parsed object
            flags_type: the Enum.IntFlag class that defines the flags in use
            default: the default value for this class
            data: bytes to be parsed
            bit_count: number of bits assigned to this field
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        self._flags_type: type[IntFlag] = cast("type[IntFlag]", flags_type)
        super().__init__(
            name=name,
            bit_count=bit_count,
            data=data,
            default=default,
            endian=endian,
            string_format=string_format,
        )

    def get_value(self) -> F | int:  # pyright:ignore[reportIncompatibleMethodOverride]
        """Get the parsed value of this class.

        Returns the integer value if the Enum.IntFlag value is not defined.

        Returns:
            the parsed value of this class
        """
        v = super().get_value()
        try:
            return cast("F", self._flags_type(v))
        except Exception:
            return v

    def set_value(self, value: F) -> None:
        """Set the value of this field.

        Args:
            value: the new value to assign to this field
        """
        if isinstance(value, IntFlag):
            _value = value.value
        else:
            _value = value
        super().set_value(_value)

    def get_string_value(self) -> str:
        """Get a formatted value for the field (for any custom formatting).

        Returns:
            the value of the field with custom formatting
        """
        value = self.value
        flags_dict: dict[str, IntFlag] = dict(self._flags_type._member_map_)  # pyright:ignore[reportGeneralTypeIssues]
        flags: Sequence[IntFlag] = list(flags_dict.values())
        if isinstance(value, IntFlag):
            s = "|".join([v.name for v in flags if v in value and v.name])
        else:
            s = str(value)
        return self.string_format.format(s)

    @property
    def value(self) -> F | int:  # pyright:ignore[reportIncompatibleMethodOverride]
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(self, value: F) -> None:
        self.set_value(value)


class UInt8FlagsField(FlagsField[F]):
    """Eight bit flags parsing class."""

    def __init__(
        self,
        name: str,
        flags_type: type[F],
        default: F,
        data: dataT | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
        string_format: str = "{}",
    ) -> None:
        """Create eight bit flags parsing class.

        Args:
            name: name of parsed object
            flags_type: the Enum.IntFlag class that defines the flags in use
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        super().__init__(
            name=name,
            bit_count=8,
            flags_type=flags_type,
            data=data,
            default=default,
            endian=endian,
            string_format=string_format,
        )


class Flags8Field(UInt8FlagsField[F]):
    """Eight bit flags parsing class."""

    ...


class UInt16FlagsField(FlagsField[F]):
    """Sixteen bit flags parsing class."""

    def __init__(
        self,
        name: str,
        flags_type: type[F],
        default: F,
        data: dataT | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
        string_format: str = "{}",
    ) -> None:
        """Create sixteen bit flags parsing class.

        Args:
            name: name of parsed object
            flags_type: the Enum.IntFlag class that defines the flags in use
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        super().__init__(
            name=name,
            bit_count=16,
            flags_type=flags_type,
            data=data,
            default=default,
            endian=endian,
            string_format=string_format,
        )


class Flags16Field(UInt16FlagsField[F]):
    """Sixteen bit flags parsing class."""

    ...


class UInt24FlagsField(FlagsField[F]):
    """Twenty-four bit flags parsing class."""

    def __init__(
        self,
        name: str,
        flags_type: type[F],
        default: F,
        data: dataT | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
        string_format: str = "{}",
    ) -> None:
        """Create twenty-four bit flags parsing class.

        Args:
            name: name of parsed object
            flags_type: the Enum.IntFlag class that defines the flags in use
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        super().__init__(
            name=name,
            bit_count=24,
            flags_type=flags_type,
            data=data,
            default=default,
            endian=endian,
            string_format=string_format,
        )


class Flags24Field(UInt24FlagsField[F]):
    """Twenty-four bit flags parsing class."""

    ...


class UInt32FlagsField(FlagsField[F]):
    """Thirty-two bit flags parsing class."""

    def __init__(
        self,
        name: str,
        flags_type: type[F],
        default: F,
        data: dataT | None = None,
        endian: endianT = DEFAULT_ENDIANNESS,
        string_format: str = "{}",
    ) -> None:
        """Create thirty-two bit flags parsing class.

        Args:
            name: name of parsed object
            flags_type: the Enum.IntFlag class that defines the flags in use
            default: the default value for this class
            data: bytes to be parsed
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        super().__init__(
            name=name,
            bit_count=32,
            flags_type=flags_type,
            data=data,
            default=default,
            endian=endian,
            string_format=string_format,
        )


class Flags32Field(UInt32FlagsField[F]):
    """Thirty-two bit flags parsing class."""

    ...
