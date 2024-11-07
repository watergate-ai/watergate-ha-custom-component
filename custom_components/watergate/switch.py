"""Implementation of the Watergate switch entity."""

import logging
from typing import Any

from homeassistant.components.sensor import HomeAssistant
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import WatergateConfigEntry
from .coordinator import WatergateDataCoordinator
from .entity import WatergateEntity

_LOGGER = logging.getLogger(__name__)

SHUT_OFF_ENTITY_NAME = "auto_shut_off"
SHUT_OFF_SENSOR_NAME = "Auto Shut off"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: WatergateConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up all entries for Watergate Platform."""

    entities: list[SwitchEntity] = [AutoShutOffEntity(config_entry.runtime_data)]

    async_add_entities(entities, True)


class AutoShutOffEntity(WatergateEntity, SwitchEntity):
    """Define a Sonic Water Auto Shut Off entity."""

    def __init__(
        self,
        coordinator: WatergateDataCoordinator,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, SHUT_OFF_ENTITY_NAME)
        self.name = SHUT_OFF_SENSOR_NAME
        self._attr_is_on = (
            coordinator.data.auto_shut_off_state.enabled
            if coordinator.data.auto_shut_off_state
            else False
        )
        self.icon = "mdi:water-pump"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
        self._attr_is_on = (
            self.coordinator.data.auto_shut_off_state.enabled
            if self.coordinator.data.auto_shut_off_state
            else False
        )
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self._api_client.async_patch_auto_shut_off(enabled=True)
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self._api_client.async_patch_auto_shut_off(enabled=False)
        self._attr_is_on = False
        self.async_write_ha_state()
