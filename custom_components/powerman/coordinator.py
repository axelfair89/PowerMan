from __future__ import annotations
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any

from homeassistant.core import HomeAssistant, State
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .advisor import AdvisorInputs, make_advice
from .const import (
    CONF_BATTERY_ENTITY,
    CONF_CHEAP_PRICE,
    CONF_EV_ENABLED,
    CONF_GRID_EXPORT_ENTITY,
    CONF_GRID_IMPORT_ENTITY,
    CONF_HIGH_PRICE,
    CONF_LOAD_POWER_ENTITY,
    CONF_PEAK_END,
    CONF_PEAK_START,
    CONF_PRICE_NEXT_ENTITY,
    CONF_PRICE_NOW_ENTITY,
    CONF_RESERVE_SOC,
    CONF_SOLAR_ENERGY_TODAY_ENTITY,
    CONF_SOLAR_FORECAST_REMAINING_ENTITY,
    CONF_SOLAR_POWER_ENTITY,
    CONF_TARGET_SOC,
    DEFAULT_CHEAP_PRICE,
    DEFAULT_EV_ENABLED,
    DEFAULT_HIGH_PRICE,
    DEFAULT_PEAK_END,
    DEFAULT_PEAK_START,
    DEFAULT_RESERVE_SOC,
    DEFAULT_TARGET_SOC,
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

    def __init__(
        self, hass: HomeAssistant, update_interval: timedelta, entry_options: dict
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="PowerMan coordinator",
            update_interval=update_interval,
        )
        self._opt = entry_options

    def _get(self, key: str) -> str | None:
        return self._opt.get(key) or None

    async def _async_update_data(self) -> dict[str, Any]:
        # Very light I/O: just read states; tiny sleep to yield.
        await asyncio.sleep(0)
        data: dict[str, Any] = {}

        if self._get(CONF_BATTERY_ENTITY):
            data["battery_percent"] = _as_float(
                self.hass.states.get(self._get(CONF_BATTERY_ENTITY))
            )
        if self._get(CONF_SOLAR_POWER_ENTITY):
            data["solar_power_w"] = _as_float(
                self.hass.states.get(self._get(CONF_SOLAR_POWER_ENTITY))
            )
        if self._get(CONF_SOLAR_ENERGY_TODAY_ENTITY):
            data["solar_energy_today_kwh"] = _as_float(
                self.hass.states.get(self._get(CONF_SOLAR_ENERGY_TODAY_ENTITY))
            )

        if self._get(CONF_GRID_IMPORT_ENTITY):
            data["grid_import_w"] = _as_float(
                self.hass.states.get(self._get(CONF_GRID_IMPORT_ENTITY))
            )
        if self._get(CONF_GRID_EXPORT_ENTITY):
            data["grid_export_w"] = _as_float(
                self.hass.states.get(self._get(CONF_GRID_EXPORT_ENTITY))
            )
        if self._get(CONF_LOAD_POWER_ENTITY):
            data["house_load_w"] = _as_float(
                self.hass.states.get(self._get(CONF_LOAD_POWER_ENTITY))
            )
        if self._get(CONF_PRICE_NOW_ENTITY):
            data["price_now"] = _as_float(
                self.hass.states.get(self._get(CONF_PRICE_NOW_ENTITY))
            )
        if self._get(CONF_PRICE_NEXT_ENTITY):
            data["price_next"] = _as_float(
                self.hass.states.get(self._get(CONF_PRICE_NEXT_ENTITY))
            )
        if self._get(CONF_SOLAR_FORECAST_REMAINING_ENTITY):
            data["solar_remaining_kwh"] = _as_float(
                self.hass.states.get(self._get(CONF_SOLAR_FORECAST_REMAINING_ENTITY))
            )

        try:
            now = dt_util.now()
            ps = datetime.strptime(
                self._opt.get(CONF_PEAK_START, DEFAULT_PEAK_START), "%H:%M"
            ).time()
            pe = datetime.strptime(
                self._opt.get(CONF_PEAK_END, DEFAULT_PEAK_END), "%H:%M"
            ).time()
            inputs = AdvisorInputs(
                now=now,
                battery_pct=data.get("battery_percent"),
                solar_w=data.get("solar_power_w"),
                load_w=data.get("house_load_w"),
                import_w=data.get("grid_import_w"),
                export_w=data.get("grid_export_w"),
                price_now=data.get("price_now"),
                price_next=data.get("price_next"),
                solar_kwh_remaining_today=data.get("solar_remaining_kwh"),
                reserve_soc=int(self._opt.get(CONF_RESERVE_SOC, DEFAULT_RESERVE_SOC)),
                target_soc=int(self._opt.get(CONF_TARGET_SOC, DEFAULT_TARGET_SOC)),
                cheap_price=float(self._opt.get(CONF_CHEAP_PRICE, DEFAULT_CHEAP_PRICE)),
                high_price=float(self._opt.get(CONF_HIGH_PRICE, DEFAULT_HIGH_PRICE)),
                peak_start=ps,
                peak_end=pe,
                ev_enabled=bool(self._opt.get(CONF_EV_ENABLED, DEFAULT_EV_ENABLED)),
            )
            advice = make_advice(inputs)
            data["advice"] = {
                "code": advice.code,
                "title": advice.title,
                "confidence": advice.confidence,
                "reasons": advice.reasons,
                "next_review_minutes": advice.next_review_minutes,
                "timestamp": now.isoformat(),
            }
        except Exception as exc:  # noqa: BLE001
            _LOGGER.exception("Advisor failed: %s", exc)

        return data
