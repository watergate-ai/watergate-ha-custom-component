"""The Watergate Number entities."""

from collections.abc import Awaitable, Callable
import logging

from homeassistant.components.number import NumberEntity
from homeassistant.components.sensor import HomeAssistant
from homeassistant.const import UnitOfTime, UnitOfVolume
from homeassistant.core import callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import WatergateConfigEntry
from .coordinator import WatergateAgregatedRequests, WatergateDataCoordinator
from .entity import WatergateEntity

_LOGGER = logging.getLogger(__name__)

SHUT_OFF_VOLUME_SENSOR_NAME = "Auto Shut off volume"
SHUT_OFF_DURATION_SENSOR_NAME = "Auto Shut off duration"

SHUT_OFF_VOLUME_ENTITY_NAME = "auto_shut_off_volume"
SHUT_OFF_DURATION_ENTITY_NAME = "auto_shut_off_duration"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: WatergateConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up all entries for Watergate Platform."""

    coordinator: WatergateDataCoordinator = config_entry.runtime_data

    entities: list[NumberEntity] = [
        AutoShutOffNumberEntity(
            coordinator,
            SHUT_OFF_VOLUME_ENTITY_NAME,
            SHUT_OFF_VOLUME_SENSOR_NAME,
            50,
            1000,
            UnitOfVolume.LITERS,
            lambda data: data.auto_shut_off_state.volume_threshold
            if data.auto_shut_off_state
            else None,
            lambda value: coordinator.api.async_patch_auto_shut_off(volume=value),
        ),
        AutoShutOffNumberEntity(
            coordinator,
            SHUT_OFF_DURATION_ENTITY_NAME,
            SHUT_OFF_DURATION_SENSOR_NAME,
            5,
            500,
            UnitOfTime.MINUTES,
            lambda data: data.auto_shut_off_state.duration_threshold
            if data.auto_shut_off_state
            else None,
            lambda value: coordinator.api.async_patch_auto_shut_off(duration=value),
        ),
    ]

    async_add_entities(entities, True)


class AutoShutOffNumberEntity(WatergateEntity, NumberEntity):
    """Define a Sonic Water Auto Shut Off Number entity."""

    def __init__(
        self,
        coordinator: WatergateDataCoordinator,
        entity_name: str,
        sensor_name: str,
        min: int,
        max: int,
        unit: str,
        extractor: Callable[[WatergateAgregatedRequests], None],
        updater: Callable[[float], Awaitable[bool]],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entity_name)
        self.name = sensor_name
        self._extrafctor = extractor
        self._attr_native_value = self._extrafctor(coordinator.data)
        self._attr_native_min_value = min
        self._attr_native_max_value = max
        self._attr_native_unit_of_measurement = unit
        self._updater = updater

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
        self._attr_native_value = self._extrafctor(self.coordinator.data)
        self.async_write_ha_state()

    @property
    def native_value(self) -> float | None:
        """Return the diagnostic."""
        return self._attr_native_value

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        await self._updater(value)
        self._attr_native_value = value
        self.async_write_ha_state()
