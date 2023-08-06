"""Define common field types in an easy to modify manner."""
from easyprotocol.base.parse_generic import ParseBase as ParseBase  # noqa
from easyprotocol.base.utils import hex as hex  # noqa
from easyprotocol.base.utils import input_to_bytes as input_to_bytes  # noqa
from easyprotocol.fields.array import ParseArrayField as ParseArrayField  # noqa
from easyprotocol.fields.array import (  # noqa
    ParseArrayFieldGeneric as ParseArrayFieldGeneric,
)
from easyprotocol.fields.checksum import ChecksumField as ChecksumField  # noqa
from easyprotocol.fields.enum import Enum8Field as Enum8Field  # noqa
from easyprotocol.fields.enum import Enum16Field as Enum16Field  # noqa
from easyprotocol.fields.enum import Enum24Field as Enum24Field  # noqa
from easyprotocol.fields.enum import Enum32Field as Enum32Field  # noqa
from easyprotocol.fields.enum import EnumField as EnumField  # noqa
from easyprotocol.fields.enum import UInt8EnumField as UInt8EnumField  # noqa
from easyprotocol.fields.enum import UInt16EnumField as UInt16EnumField  # noqa
from easyprotocol.fields.enum import UInt24EnumField as UInt24EnumField  # noqa
from easyprotocol.fields.enum import UInt32EnumField as UInt32EnumField  # noqa
from easyprotocol.fields.flags import Flags8Field as Flags8Field  # noqa
from easyprotocol.fields.flags import Flags16Field as Flags16Field  # noqa
from easyprotocol.fields.flags import Flags24Field as Flags24Field  # noqa
from easyprotocol.fields.flags import Flags32Field as Flags32Field  # noqa
from easyprotocol.fields.flags import FlagsField as FlagsField  # noqa
from easyprotocol.fields.flags import UInt8FlagsField as UInt8FlagsField  # noqa
from easyprotocol.fields.flags import UInt16FlagsField as UInt16FlagsField  # noqa
from easyprotocol.fields.flags import UInt24FlagsField as UInt24FlagsField  # noqa
from easyprotocol.fields.flags import UInt32FlagsField as UInt32FlagsField  # noqa
from easyprotocol.fields.float import Float32IEEField as Float32IEEField  # noqa
from easyprotocol.fields.float import FloatField as FloatField  # noqa
from easyprotocol.fields.signed_int import Int8Field as Int8Field  # noqa
from easyprotocol.fields.signed_int import Int16Field as Int16Field  # noqa
from easyprotocol.fields.signed_int import Int32Field as Int32Field  # noqa
from easyprotocol.fields.signed_int import Int64Field as Int64Field  # noqa
from easyprotocol.fields.signed_int import IntFieldGeneric as IntFieldGeneric  # noqa
from easyprotocol.fields.string import ByteField as ByteField  # noqa
from easyprotocol.fields.string import BytesField as BytesField  # noqa
from easyprotocol.fields.string import CharField as CharField  # noqa
from easyprotocol.fields.string import StringField as StringField  # noqa
from easyprotocol.fields.string import UInt8ByteField as UInt8ByteField  # noqa
from easyprotocol.fields.string import UInt8CharField as UInt8CharField  # noqa
from easyprotocol.fields.unsigned_int import BoolField as BoolField  # noqa
from easyprotocol.fields.unsigned_int import UInt8Field as UInt8Field  # noqa
from easyprotocol.fields.unsigned_int import UInt16Field as UInt16Field  # noqa
from easyprotocol.fields.unsigned_int import UInt32Field as UInt32Field  # noqa
from easyprotocol.fields.unsigned_int import UInt64Field as UInt64Field  # noqa
from easyprotocol.fields.unsigned_int import UIntField as UIntField  # noqa
