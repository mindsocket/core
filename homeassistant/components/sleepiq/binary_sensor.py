"""Support for SleepIQ sensors."""
from asyncsleepiq import SleepIQBed, SleepIQSleeper

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, ICON_EMPTY, ICON_OCCUPIED, IS_IN_BED
from .coordinator import SleepIQDataUpdateCoordinator
from .entity import SleepIQSensor


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the SleepIQ bed binary sensors."""
    coordinator: SleepIQDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        IsInBedBinarySensor(coordinator, bed, sleeper)
        for bed in coordinator.client.beds.values()
        for sleeper in bed.sleepers
    )


class IsInBedBinarySensor(SleepIQSensor, BinarySensorEntity):
    """Implementation of a SleepIQ presence sensor."""

    _attr_device_class = BinarySensorDeviceClass.OCCUPANCY

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        bed: SleepIQBed,
        sleeper: SleepIQSleeper,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, bed, sleeper, IS_IN_BED)

    @callback
    def _async_update_attrs(self) -> None:
        """Update sensor attributes."""
        self._attr_is_on = self.sleeper.in_bed
        self._attr_icon = ICON_OCCUPIED if self.sleeper.in_bed else ICON_EMPTY
