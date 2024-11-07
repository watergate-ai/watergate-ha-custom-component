"""Support for Watergate sensors."""

from collections.abc import Callable, Mapping
from datetime import UTC, datetime
import logging
from typing import Any

from watergate_local_api.models import AutoShutOffReport

from homeassistant.components.sensor import (
    HomeAssistant,
    SensorDeviceClass,
    SensorEntity,
    StateType,
)
from homeassistant.const import (
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    EntityCategory,
    UnitOfPressure,
    UnitOfTemperature,
    UnitOfTime,
    UnitOfVolume,
    UnitOfVolumeFlowRate,
)
from homeassistant.core import callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import WatergateConfigEntry
from .coordinator import WatergateAgregatedRequests, WatergateDataCoordinator
from .entity import WatergateEntity

_LOGGER = logging.getLogger(__name__)

WIFI_CONNECTION_SENSOR_NAME = "Wifi connection"
MQTT_CONNECTION_SENSOR_NAME = "MQTT connection"
UPTIME_SENSOR_NAME = "Uptime"
UPTIME_SENSOR_NAME = "Uptime"
POWER_SUPPLY_SENSOR_NAME = "Power supply"
WATER_FLOWING_SENSOR_NAME = "Water flowing"
PRESSURE_SENSOR_NAME = "Water pressure"
TEMPERATURE_SENSOR_NAME = "Water temperature"
FLOW_SENSOR_NAME = "Water flow rate"
IP_SENSOR_NAME = "IP address"
GATEWAY_SENSOR_NAME = "Gateway address"
SUBNET_SENSOR_NAME = "Subnet"
SSID_SENSOR_NAME = "SSID"
RSSI_SENSOR_NAME = "RSSI"
WIFI_UPTIME_SENSOR_NAME = "WIFI Uptime"
MQTT_UPTIME_SENSOR_NAME = "MQTT Uptime"
SHUT_OFF_EVENT_SENSOR_NAME = "Last Auto Shut off event"
WATER_METER_VOLUME_SENSOR_NAME = "Water meter volume"
WATER_METER_DURATION_SENSOR_NAME = "Water meter duration"

ASO_EVENT_TYPE_ATRIBUTE = "type"
ASO_EVENT_VOLUME_ATRIBUTE = "volume"
ASO_EVENT_DURATION_ATRIBUTE = "duration"


WIFI_CONNECTION_ENTITY_NAME = "wifi_status"
MQTT_CONNECTION_ENTITY_NAME = "mqtt_status"
UPTIME_ENTITY_NAME = "uptime"
POWER_SUPPLY_ENTITY_NAME = "power_supply"
WATER_FLOWING_ENTITY_NAME = "water_flowing"
PRESSURE_ENTITY_NAME = "water_pressure"
TEMPERATURE_ENTITY_NAME = "water_temperature"
FLOW_ENTITY_NAME = "water_flow_rate"
IP_ENTITY_NAME = "ip"
GATEWAY_ENTITY_NAME = "gateway"
SUBNET_ENTITY_NAME = "subnet"
SSID_ENTITY_NAME = "ssid"
RSSI_ENTITY_NAME = "rssi"
WIFI_UPTIME_ENTITY_NAME = "wifi_uptime"
MQTT_UPTIME_ENTITY_NAME = "mqtt_uptime"
SHUT_OFF_EVENT_ENTITY_NAME = "auto_shut_off_event"
WATER_METER_VOLUME_ENTITY_NAME = "water_meter_volume"
WATER_METER_DURATION_ENTITY_NAME = "water_meter_duration"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: WatergateConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up all entries for Watergate Platform."""

    coordinator = config_entry.runtime_data

    entities: list[SensorEntity] = [
        SonicSensor(
            coordinator,
            WATER_METER_VOLUME_SENSOR_NAME,
            WATER_METER_VOLUME_ENTITY_NAME,
            UnitOfVolume.MILLILITERS,
            SensorDeviceClass.VOLUME,
            lambda data: data.state.water_meter.volume
            if data.state and data.state.water_meter
            else None,
        ),
        SonicSensor(
            coordinator,
            WATER_METER_DURATION_SENSOR_NAME,
            WATER_METER_DURATION_ENTITY_NAME,
            UnitOfTime.MILLISECONDS,
            SensorDeviceClass.DURATION,
            lambda data: data.state.water_meter.duration
            if data.state and data.state.water_meter
            else None,
        ),
        SonicSensor(
            coordinator,
            IP_SENSOR_NAME,
            IP_ENTITY_NAME,
            None,
            None,
            lambda data: data.networking.ip if data.networking else None,
            EntityCategory.DIAGNOSTIC,
        ),
        SonicSensor(
            coordinator,
            GATEWAY_SENSOR_NAME,
            GATEWAY_ENTITY_NAME,
            None,
            None,
            lambda data: data.networking.gateway if data.networking else None,
            EntityCategory.DIAGNOSTIC,
        ),
        SonicSensor(
            coordinator,
            SUBNET_SENSOR_NAME,
            SUBNET_ENTITY_NAME,
            None,
            None,
            lambda data: data.networking.subnet if data.networking else None,
            EntityCategory.DIAGNOSTIC,
        ),
        SonicSensor(
            coordinator,
            SSID_SENSOR_NAME,
            SSID_ENTITY_NAME,
            None,
            None,
            lambda data: data.networking.ssid if data.networking else None,
            EntityCategory.DIAGNOSTIC,
        ),
        SonicSensor(
            coordinator,
            RSSI_SENSOR_NAME,
            RSSI_ENTITY_NAME,
            SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            SensorDeviceClass.SIGNAL_STRENGTH,
            lambda data: data.networking.rssi if data.networking else None,
            EntityCategory.DIAGNOSTIC,
        ),
        SonicSensor(
            coordinator,
            WIFI_UPTIME_SENSOR_NAME,
            WIFI_UPTIME_ENTITY_NAME,
            UnitOfTime.MILLISECONDS,
            SensorDeviceClass.DURATION,
            lambda data: data.networking.wifi_uptime if data.networking else None,
            EntityCategory.DIAGNOSTIC,
        ),
        SonicSensor(
            coordinator,
            MQTT_UPTIME_SENSOR_NAME,
            MQTT_UPTIME_ENTITY_NAME,
            UnitOfTime.MILLISECONDS,
            SensorDeviceClass.DURATION,
            lambda data: data.networking.mqtt_uptime if data.networking else None,
            EntityCategory.DIAGNOSTIC,
        ),
        SonicSensor(
            coordinator,
            TEMPERATURE_SENSOR_NAME,
            TEMPERATURE_ENTITY_NAME,
            UnitOfTemperature.CELSIUS,
            SensorDeviceClass.TEMPERATURE,
            lambda data: data.telemetry.water_temperature
            if data.telemetry and "temperature" not in data.telemetry.errors
            else None,
        ),
        SonicSensor(
            coordinator,
            PRESSURE_SENSOR_NAME,
            PRESSURE_ENTITY_NAME,
            UnitOfPressure.MBAR,
            SensorDeviceClass.PRESSURE,
            lambda data: data.telemetry.pressure
            if data.telemetry and "pressure" not in data.telemetry.errors
            else None,
        ),
        SonicSensor(
            coordinator,
            FLOW_SENSOR_NAME,
            FLOW_ENTITY_NAME,
            UnitOfVolumeFlowRate.LITERS_PER_MINUTE,
            SensorDeviceClass.VOLUME_FLOW_RATE,
            lambda data: data.telemetry.flow / 1000
            if data.telemetry and "flow" not in data.telemetry.errors
            else None,
        ),
        SonicSensor(
            coordinator,
            UPTIME_SENSOR_NAME,
            UPTIME_ENTITY_NAME,
            UnitOfTime.MILLISECONDS,
            SensorDeviceClass.DURATION,
            lambda data: data.state.uptime if data.state else None,
            EntityCategory.DIAGNOSTIC,
        ),
        SonicSensor(
            coordinator,
            POWER_SUPPLY_SENSOR_NAME,
            POWER_SUPPLY_ENTITY_NAME,
            None,
            None,
            lambda data: data.state.power_supply if data.state else None,
            EntityCategory.DIAGNOSTIC,
        ),
        AutoShutOffEventSensor(coordinator),
    ]

    async_add_entities(entities, True)


class SonicSensor(WatergateEntity, SensorEntity):
    """Define a Sonic Valve entity."""

    _native_state: str | int | float | None = None

    def __init__(
        self,
        coordinator: WatergateDataCoordinator,
        sensor_name: str,
        entity_name: str,
        unit: str | None,
        device_class: SensorDeviceClass | None,
        extractor: Callable[[WatergateAgregatedRequests], str | int | float | None],
        entity_category: EntityCategory | None = None,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entity_name)
        self.name = sensor_name
        self._attr_native_unit_of_measurement = unit if unit else None
        self.device_class = device_class
        if entity_category:
            self.entity_category = entity_category
        self._extractor = extractor

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
        self._native_state = self._extractor(self.coordinator.data)
        self.async_write_ha_state()

    def update(self, value: str | None) -> None:
        """Update the sensor."""
        self._native_state = value
        self.async_write_ha_state()

    @property
    def native_value(self) -> StateType:
        """Return the diagnostic."""
        return self._native_state


class AutoShutOffEventSensor(WatergateEntity, SensorEntity):
    """Representation of a sensor showing the latest long flow event."""

    _attributes: dict[str, str] = {}

    def __init__(self, coordinator: WatergateDataCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, SHUT_OFF_EVENT_ENTITY_NAME)
        self.name = SHUT_OFF_EVENT_SENSOR_NAME
        self.device_class = SensorDeviceClass.TIMESTAMP

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        """Return additional attributes."""
        return self._attributes

    def update(self, report: AutoShutOffReport) -> None:
        """Update the sensor."""
        self._attr_native_value = datetime.fromtimestamp(report.timestamp, UTC)
        self._attributes = {
            ASO_EVENT_TYPE_ATRIBUTE: report.type,
            ASO_EVENT_DURATION_ATRIBUTE: report.duration,
            ASO_EVENT_VOLUME_ATRIBUTE: report.volume,
        }
        self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
        if self.coordinator.last_update_success:
            data = self.coordinator.data.auto_shut_off_report

            if data:
                self.update(data)
