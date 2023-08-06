"""This class is the basic parsing class for value types."""
from __future__ import annotations

from typing import Any, Generic, TypeVar

from easyprotocol.base.parse_generic import ParseBase, dataT, endianT

T = TypeVar("T", covariant=True)


class ParseGenericValue(
    ParseBase,
    Generic[T],
):
    """This class is the basic parsing class for value types."""

    def __init__(
        self,
        name: str,
        default: T = None,
        data: dataT = None,
        bit_count: int = -1,
        string_format: str | None = None,
        endian: endianT = ...,
    ) -> None:
        """Create the basic parsing class for value types.

        Args:
            name: name of parsed object
            default: the default value for this class
            data: bytes to be parsed
            bit_count: number of bits assigned to this field
            string_format: python format string (e.g. "{}")
            endian: the byte endian-ness of this object
        """
        super().__init__(
            name,
            data,
            bit_count,
            string_format,
            endian,
        )
        if data is None and default is not None:
            self.value = default

    def get_value(self) -> Any:
        """Get the parsed value of this class.

        Raises:
            NotImplementedError: until overridden in a subclass
        """
        raise NotImplementedError()

    def set_value(self, value: Any) -> None:
        """Set the parsed value of this class.

        Args:
            value: the new value of this field

        Raises:
            NotImplementedError: until overridden in a subclass
        """
        raise NotImplementedError()

    @property
    def value(self) -> T:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self.get_value()

    @value.setter
    def value(self, value: Any) -> None:
        self.set_value(value)

    @property
    def parent(self) -> ParseBase | None:
        """Get the parsed value of the field.

        Returns:
            the value of the field
        """
        return self._get_parent_generic()

    @parent.setter
    def parent(self, value: ParseBase) -> None:
        self._set_parent_generic(value)
