from enum import Enum, IntEnum


class ModbusFieldNamesEnum(str, Enum):
    DeviceID = "id"
    FunctionCode = "function"
    Address = "address"
    CRC = "crc"
    CoilArray = "bit array"
    Count = "count"
    ByteCount = "byte count"


class ModbusFunctionEnum(IntEnum):
    Unknown = 0
    ReadCoils = 1
    ReadDiscreteInputs = 2
    ReadMultipleHoldingRegisters = 3
    ReadMultipleInputRegisters = 4
    WriteSingleCoil = 5
    WriteMultipleHoldingRegister = 6
    WriteMultipleCoils = 15
    WriteMultipleHoldingRegisters = 16
