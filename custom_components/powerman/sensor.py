
from __future__ import annotations
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DEFAULT_NAME
from .coordinator import PowerManCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator: PowerManCoordinator = hass.data[DOMAIN][entry.entry_id]
    name = entry.title or DEFAULT_NAME
    async_add_entities([
        PowerManPowerSensor(coordinator, f"{name} Power"),
        PowerManVoltageSensor(coordinator, f"{name} Voltage"),
        PowerManCurrentSensor(coordinator, f"{name} Current"),
    ])

class _BasePowerManSensor(CoordinatorEntity[PowerManCoordinator], SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator: PowerManCoordinator, name: str) -> None:
        super().__init__(coordinator)
        self._attr_name = name

    @property
    def extra_state_attributes(self):
        return {
            "integration": DOMAIN,
            "attribution": "Demo values generated locally",
        }

class PowerManPowerSensor(_BasePowerManSensor):
    native_unit_of_measurement = "W"
    icon = "mdi:flash"

    @property
    def native_value(self):
        return self.coordinator.data.get("power_w")

class PowerManVoltageSensor(_BasePowerManSensor):
    native_unit_of_measurement = "V"
    icon = "mdi:sine-wave"

    @property
    def native_value(self):
        return self.coordinator.data.get("voltage_v")

class PowerManCurrentSensor(_BasePowerManSensor):
    native_unit_of_measurement = "A"
    icon = "mdi:current-ac"

    @property
    def native_value(self):
        return self.coordinator.data.get("current_a")
