
from __future__ import annotations
import asyncio
import random
import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

class PowerManCoordinator(DataUpdateCoordinator[dict]):
    """Simple coordinator that simulates reading power data (in Watts)."""

    def __init__(self, hass: HomeAssistant, update_interval: timedelta) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="PowerMan coordinator",
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> dict:
        # Simulate I/O latency
        await asyncio.sleep(0.1)
        # Produce deterministic-ish pseudo values so it's visible in HA
        watts = random.randint(150, 850)
        voltage = random.choice([228, 229, 230, 231, 232])
        amps = round(watts / voltage, 2)
        return {
            "power_w": watts,
            "voltage_v": voltage,
            "current_a": amps,
        }
