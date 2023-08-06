"""Contains device parameter representation."""
from __future__ import annotations

from abc import ABC, abstractmethod
import asyncio
import logging
from typing import TYPE_CHECKING, Any, Final

from pyplumio.const import (
    ATTR_EXTRA,
    ATTR_NAME,
    ATTR_PRODUCT,
    ATTR_VALUE,
    STATE_OFF,
    STATE_ON,
)
from pyplumio.frames import Request
from pyplumio.helpers.factory import factory
from pyplumio.helpers.product_info import ProductTypes
from pyplumio.helpers.schedule import _collect_schedule_data
from pyplumio.helpers.typing import ParameterDataType, ParameterValueType
from pyplumio.structures.ecomax_parameters import (
    ECOMAX_I_PARAMETERS,
    ECOMAX_P_PARAMETERS,
)
from pyplumio.structures.mixer_parameters import (
    ECOMAX_I_MIXER_PARAMETERS,
    ECOMAX_P_MIXER_PARAMETERS,
)

if TYPE_CHECKING:
    from pyplumio.devices import Device

_LOGGER = logging.getLogger(__name__)

SET_TIMEOUT: Final = 5


def _normalize_parameter_value(value: ParameterValueType) -> int:
    """Normalize parameter value to integer."""
    if isinstance(value, str):
        return 1 if value == STATE_ON else 0

    if isinstance(value, tuple):
        # Value is parameter tuple.
        value = value[0]

    return int(value)


def is_binary_parameter(parameter: ParameterDataType) -> bool:
    """Check if parameter is binary."""
    _, min_value, max_value = parameter
    return min_value == 0 and max_value == 1


class Parameter(ABC):
    """Represents device parameter."""

    device: Device
    name: str
    extra: Any
    _value: int
    _min_value: int
    _max_value: int
    _change_pending: bool = False

    def __init__(
        self,
        device: Device,
        name: str,
        value: ParameterValueType,
        min_value: ParameterValueType,
        max_value: ParameterValueType,
        extra: Any = None,
    ):
        """Initialize Parameter object."""
        self.device = device
        self.name = name
        self.extra = extra
        self._value = _normalize_parameter_value(value)
        self._min_value = _normalize_parameter_value(min_value)
        self._max_value = _normalize_parameter_value(max_value)
        self._change_pending = False

    def __repr__(self) -> str:
        """Returns serializable string representation."""
        return (
            self.__class__.__name__
            + f"(device={self.device.__class__.__name__}, name={self.name}, "
            + f"value={self._value}, min_value={self._min_value}, "
            + f"max_value={self._max_value}, extra={self.extra})"
        )

    def _call_relational_method(self, method_to_call, other):
        func = getattr(self.value, method_to_call)
        return func(_normalize_parameter_value(other))

    def __int__(self) -> int:
        """Return integer representation of parameter value."""
        return self.value

    def __add__(self, other) -> int:
        """Return result of addition."""
        return self._call_relational_method("__add__", other)

    def __sub__(self, other) -> int:
        """Return result of the subtraction."""
        return self._call_relational_method("__sub__", other)

    def __truediv__(self, other):
        """Return result of true division."""
        return self._call_relational_method("__truediv__", other)

    def __floordiv__(self, other):
        """Return result of floored division."""
        return self._call_relational_method("__floordiv__", other)

    def __mul__(self, other):
        """Return result of the multiplication."""
        return self._call_relational_method("__mul__", other)

    def __eq__(self, other) -> bool:
        """Compare if parameter value is equal to other."""
        return self._call_relational_method("__eq__", other)

    def __ge__(self, other) -> bool:
        """Compare if parameter value is greater or equal to other."""
        return self._call_relational_method("__ge__", other)

    def __gt__(self, other) -> bool:
        """Compare if parameter value is greater than other."""
        return self._call_relational_method("__gt__", other)

    def __le__(self, other) -> bool:
        """Compare if parameter value is less or equal to other."""
        return self._call_relational_method("__le__", other)

    def __lt__(self, other) -> bool:
        """Compare if parameter value is less that other."""
        return self._call_relational_method("__lt__", other)

    async def _confirm_parameter_change(self, parameter: Parameter) -> None:
        """Callback for when parameter change is confirmed on the device."""
        self._change_pending = False

    async def set(self, value: ParameterValueType, retries: int = 5) -> bool:
        """Set parameter value."""
        value = _normalize_parameter_value(value)
        if value == self._value:
            return True

        if value < self.min_value or value > self.max_value:
            raise ValueError(
                f"Parameter value must be between '{self.min_value}' and '{self.max_value}'"
            )

        self._value = value
        self._change_pending = True
        self.device.subscribe_once(self.name, self._confirm_parameter_change)
        while self.change_pending:
            if retries <= 0:
                _LOGGER.error("Timed out while trying to set '%s' parameter", self.name)
                self.device.unsubscribe(self.name, self._confirm_parameter_change)
                return False

            await self.device.queue.put(self.request)
            await asyncio.sleep(SET_TIMEOUT)
            retries -= 1

        return True

    @property
    def value(self) -> int:
        """Return parameter value."""
        return self._value

    @property
    def min_value(self) -> int:
        """Return minimum allowed value."""
        return self._min_value

    @property
    def max_value(self) -> int:
        """Return maximum allowed value."""
        return self._max_value

    @property
    def change_pending(self) -> bool:
        """Parameter change has not yet confirmed on the device."""
        return self._change_pending

    @property
    @abstractmethod
    def request(self) -> Request:
        """Return request to change the parameter."""


class BinaryParameter(Parameter):
    """Represents binary device parameter."""

    async def turn_on(self) -> bool:
        """Turn parameter on."""
        return await self.set(STATE_ON)

    async def turn_off(self) -> bool:
        """Turn parameter off"""
        return await self.set(STATE_OFF)


class EcomaxParameter(Parameter):
    """Represents ecoMAX parameter."""

    @property
    def request(self) -> Request:
        """Return request to change the parameter."""

        if self.name == "ecomax_control":
            return factory(
                "frames.requests.EcomaxControlRequest",
                recipient=self.device.address,
                data={
                    ATTR_VALUE: self.value,
                },
            )

        return factory(
            "frames.requests.SetEcomaxParameterRequest",
            recipient=self.device.address,
            data={
                ATTR_NAME: (
                    ECOMAX_P_PARAMETERS.index(self.name)
                    if self.device.data[ATTR_PRODUCT].type == ProductTypes.ECOMAX_P
                    else ECOMAX_I_PARAMETERS.index(self.name)
                ),
                ATTR_VALUE: self.value,
            },
        )


class EcomaxBinaryParameter(EcomaxParameter, BinaryParameter):
    """Represents ecoMAX binary parameter."""


class MixerParameter(Parameter):
    """Represents mixer parameter."""

    @property
    def request(self) -> Request:
        """Return request to change the parameter."""
        return factory(
            "frames.requests.SetMixerParameterRequest",
            recipient=self.device.address,
            data={
                ATTR_NAME: (
                    ECOMAX_P_MIXER_PARAMETERS.index(self.name)
                    if self.device.data[ATTR_PRODUCT].type == ProductTypes.ECOMAX_P
                    else ECOMAX_I_MIXER_PARAMETERS.index(self.name)
                ),
                ATTR_VALUE: self.value,
                ATTR_EXTRA: self.extra,
            },
        )


class MixerBinaryParameter(MixerParameter, BinaryParameter):
    """Represents mixer binary parameter."""


class ScheduleParameter(Parameter):
    """Represents schedule parameter."""

    @property
    def request(self) -> Request:
        """Return request to change the parameter."""
        return factory(
            "frames.requests.SetScheduleRequest",
            recipient=self.device.address,
            data=_collect_schedule_data(self.extra, self.device),
        )


class ScheduleBinaryParameter(ScheduleParameter, BinaryParameter):
    """Represents schedule binary parameter."""
