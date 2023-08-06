from __future__ import annotations

from collections import OrderedDict
from typing import Any, Mapping, Sequence, cast

from easyprotocol.base import ParseFieldDict, dataT
from easyprotocol.base.parse_generic import ParseBase
from easyprotocol.protocols.modbus.constants import (
    ModbusFieldNamesEnum,
    ModbusFunctionEnum,
)
from easyprotocol.protocols.modbus.fields import (
    ModbusAddress,
    ModbusByteCount,
    ModbusCoilArray,
    ModbusCount,
    ModbusCRC,
    ModbusDeviceId,
    ModbusFunction,
)


class ModbusHeader(ParseFieldDict):
    def __init__(
        self,
        name: str = "modbusHeader",
        data: dataT | None = None,
        children: Sequence[ParseBase] = [
            ModbusDeviceId(),
            ModbusFunction(),
            ModbusAddress(),
            ModbusCRC(),
        ],
    ) -> None:
        super().__init__(
            name=name,
            data=data,
            default=children,
        )

    @property
    def deviceId(self) -> ModbusDeviceId:
        return cast(ModbusDeviceId, self[ModbusFieldNamesEnum.DeviceID.value])

    @deviceId.setter
    def deviceId(self, value: int) -> None:
        if isinstance(value, ModbusDeviceId):
            self[ModbusFieldNamesEnum.DeviceID.value] = value
        else:
            id = cast(ModbusDeviceId, self[ModbusFieldNamesEnum.DeviceID.value])
            id.value = value

    @property
    def functionCode(self) -> ModbusFunction:
        return cast(ModbusFunction, self[ModbusFieldNamesEnum.FunctionCode.value])

    @functionCode.setter
    def functionCode(self, value: ModbusFunctionEnum) -> None:
        if isinstance(value, ModbusFunction):
            self[ModbusFieldNamesEnum.FunctionCode.value] = value
        else:
            func = cast(ModbusFunction, self[ModbusFieldNamesEnum.FunctionCode.value])
            func.value = value

    @property
    def address(self) -> ModbusAddress:
        return cast(ModbusAddress, self[ModbusFieldNamesEnum.Address.value])

    @address.setter
    def address(self, value: int) -> None:
        if isinstance(value, ModbusAddress):
            self[ModbusFieldNamesEnum.Address.value] = value
        else:
            addr = cast(ModbusAddress, self[ModbusFieldNamesEnum.Address.value])
            addr.value = value

    @property
    def byteCount(self) -> ModbusByteCount:
        return cast(ModbusByteCount, self[ModbusFieldNamesEnum.ByteCount.value])

    @byteCount.setter
    def byteCount(self, value: int) -> None:
        if isinstance(value, ModbusByteCount):
            self[ModbusFieldNamesEnum.ByteCount.value] = value
        else:
            count = cast(ModbusByteCount, self[ModbusFieldNamesEnum.ByteCount.value])
            count.value = value

    @property
    def crc(self) -> ModbusCRC:
        return cast(ModbusCRC, self[ModbusFieldNamesEnum.CRC.value])

    @crc.setter
    def crc(self, value: int) -> None:
        if isinstance(value, ModbusCRC):
            self[ModbusFieldNamesEnum.CRC.value] = value
        else:
            crc = cast(ModbusCRC, self[ModbusFieldNamesEnum.CRC.value])
            crc.value = value


class ModbusReadCoilsRequest(ModbusHeader):
    def __init__(
        self,
        data: dataT | None = None,
    ) -> None:
        super().__init__(
            name=ModbusFunctionEnum.ReadCoils.name + "Request",
            data=data,
            children=[
                ModbusDeviceId(),
                ModbusFunction(),
                ModbusAddress(),
                ModbusCount(),
                ModbusCRC(),
            ],
        )


class ModbusReadCoilsResponse(ModbusHeader):
    def __init__(
        self,
        data: dataT | None = None,
    ) -> None:
        count_field = ModbusByteCount()
        super().__init__(
            name=ModbusFunctionEnum.ReadCoils.name + "Response",
            data=data,
            children=[
                ModbusDeviceId(),
                ModbusFunction(),
                count_field,
                ModbusCoilArray(count=count_field),
                ModbusCRC(),
            ],
        )

    @property
    def coilArray(self) -> ModbusCoilArray:
        return cast(ModbusCoilArray, self[ModbusFieldNamesEnum.CoilArray.value])

    @coilArray.setter
    def coilArray(self, value: Sequence[bool] | Sequence[int]) -> None:
        if isinstance(value, ModbusCoilArray):
            self[ModbusFieldNamesEnum.CoilArray.value].value = value.value
        else:
            func = cast(ModbusCoilArray, self[ModbusFieldNamesEnum.CoilArray.value])
            func.set_value(value)


class ModbusReadDiscreteInputsRequest(ModbusHeader):
    def __init__(
        self,
        data: dataT | None = None,
    ) -> None:
        super().__init__(
            name=ModbusFunctionEnum.ReadDiscreteInputs.name + "Request",
            data=data,
            children=[
                ModbusDeviceId(),
                ModbusFunction(),
                ModbusAddress(),
                ModbusCount(),
                ModbusCRC(),
            ],
        )

    @property
    def count(self) -> ModbusCount:
        return cast(ModbusCount, self[ModbusFieldNamesEnum.Count.value])

    @count.setter
    def count(self, value: int) -> None:
        if isinstance(value, ModbusCount):
            self[ModbusFieldNamesEnum.Count.value] = value
        else:
            func = cast(ModbusCount, self[ModbusFieldNamesEnum.Count.value])
            func.set_value(value)
