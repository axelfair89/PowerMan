from __future__ import annotations
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo

from .const import (
    DOMAIN,
    DEFAULT_NAME,
    DEVICE_ID,
    CONF_BATTERY_ENTITY,
    CONF_SOLAR_POWER_ENTITY,
    CONF_SOLAR_ENERGY_TODAY_ENTITY,
)
from .coordinator import PowerManCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    coordinator: PowerManCoordinator = hass.data[DOMAIN][entry.entry_id]
    name = entry.title or DEFAULT_NAME

    sensors: list[SensorEntity] = []

    if entry.options.get(CONF_BATTERY_ENTITY):
        sensors.append(BatterySensor(coordinator, entry, f"{name} Battery"))

    if entry.options.get(CONF_SOLAR_POWER_ENTITY):
        sensors.append(SolarPowerSensor(coordinator, entry, f"{name} Solar Power"))

    if entry.options.get(CONF_SOLAR_ENERGY_TODAY_ENTITY):
        sensors.append(SolarEnergyTodaySensor(coordinator, entry, f"{name} Solar Energy Today"))

    sensors.append(AdviceSensor(coordinator, entry, f"{name} Advice"))

    if sensors:
        async_add_entities(sensors)


class _BasePowerManSensor(CoordinatorEntity[PowerManCoordinator], SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator: PowerManCoordinator, entry: ConfigEntry, name: str, unique_suffix: str) -> None:
        super().__init__(coordinator)
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{unique_suffix}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, DEVICE_ID)},
            name="PowerMan",
            manufacturer="PowerMan",
            model="Entity Bridge",
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {
            "integration": DOMAIN,
            "provenance": "Forwarded from selected entities",
        }


class BatterySensor(_BasePowerManSensor):
    _attr_native_unit_of_measurement = "%"
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT
    icon = "mdi:battery"

    def __init__(self, coordinator: PowerManCoordinator, entry: ConfigEntry, name: str) -> None:
        super().__init__(coordinator, entry, name, "battery")

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.get("battery_percent")


class SolarPowerSensor(_BasePowerManSensor):
    _attr_native_unit_of_measurement = "W"
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    icon = "mdi:solar-power"

    def __init__(self, coordinator: PowerManCoordinator, entry: ConfigEntry, name: str) -> None:
        super().__init__(coordinator, entry, name, "solar_power")

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.get("solar_power_w")


class SolarEnergyTodaySensor(_BasePowerManSensor):
    _attr_native_unit_of_measurement = "kWh"
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    icon = "mdi:solar-panel"

    def __init__(self, coordinator: PowerManCoordinator, entry: ConfigEntry, name: str) -> None:
        super().__init__(coordinator, entry, name, "solar_energy_today")

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.get("solar_energy_today_kwh")


class AdviceSensor(_BasePowerManSensor):
    icon = "mdi:lightbulb-on-outline"

    def __init__(self, coordinator: PowerManCoordinator, entry: ConfigEntry, name: str) -> None:
        super().__init__(coordinator, entry, name, "advice")

    @property
    def native_value(self) -> str:
        adv = self.coordinator.data.get("advice") or {}
        return adv.get("code") or "unknown"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:  # type: ignore[override]
        adv = self.coordinator.data.get("advice") or {}
        base = super().extra_state_attributes
        base.update(
            {
                "title": adv.get("title"),
                "confidence": adv.get("confidence"),
                "reasons": adv.get("reasons"),
                "timestamp": adv.get("timestamp"),
                "next_review_minutes": adv.get("next_review_minutes"),
            }
        )
        return base
