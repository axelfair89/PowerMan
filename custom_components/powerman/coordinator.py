from __future__ import annotations
import asyncio
import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant, State
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    CONF_BATTERY_ENTITY,
    CONF_SOLAR_POWER_ENTITY,
    CONF_SOLAR_ENERGY_TODAY_ENTITY,
)

_LOGGER = logging.getLogger(__name__)


def _as_float(state: State | None) -> float | None:
    if state is None:
        return None
    try:
        val = float(state.state)
    except (ValueError, TypeError):
        return None
    return val


class PowerManCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator that reads selected entity states each interval."""

    def __init__(self, hass: HomeAssistant, update_interval: timedelta, entry_options: dict) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="PowerMan coordinator",
            update_interval=update_interval,
        )
        self._battery = entry_options.get(CONF_BATTERY_ENTITY)
        self._solar_power = entry_options.get(CONF_SOLAR_POWER_ENTITY)
        self._solar_energy_today = entry_options.get(CONF_SOLAR_ENERGY_TODAY_ENTITY)

    async def _async_update_data(self) -> dict[str, Any]:
        # Very light I/O: just read states; tiny sleep to yield.
        await asyncio.sleep(0)
        data: dict[str, Any] = {}

        if self._battery:
            data["battery_percent"] = _as_float(self.hass.states.get(self._battery))
        if self._solar_power:
            data["solar_power_w"] = _as_float(self.hass.states.get(self._solar_power))
        if self._solar_energy_today:
            data["solar_energy_today_kwh"] = _as_float(self.hass.states.get(self._solar_energy_today))

        return data
