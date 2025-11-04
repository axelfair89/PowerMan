from __future__ import annotations
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    DEFAULT_NAME,
    DEFAULT_UPDATE_INTERVAL,
    CONF_UPDATE_INTERVAL,
    CONF_BATTERY_ENTITY,
    CONF_SOLAR_POWER_ENTITY,
    CONF_SOLAR_ENERGY_TODAY_ENTITY,
    CONF_GRID_IMPORT_ENTITY,
    CONF_GRID_EXPORT_ENTITY,
    CONF_LOAD_POWER_ENTITY,
    CONF_PRICE_NOW_ENTITY,
    CONF_PRICE_NEXT_ENTITY,
    CONF_SOLAR_FORECAST_REMAINING_ENTITY,
    CONF_RESERVE_SOC,
    CONF_TARGET_SOC,
    CONF_CHEAP_PRICE,
    CONF_HIGH_PRICE,
    CONF_PEAK_START,
    CONF_PEAK_END,
    CONF_EV_ENABLED,
    CONF_NOTIFY_CHANGE,
    CONF_ADVISOR_INTERVAL_MIN,
    CONF_AGENT_ID,
    CONF_MINUTES_BETWEEN_AI,
    DEFAULT_MINUTES_BETWEEN_AI,
    DEFAULT_RESERVE_SOC,
    DEFAULT_TARGET_SOC,
    DEFAULT_CHEAP_PRICE,
    DEFAULT_HIGH_PRICE,
    DEFAULT_PEAK_START,
    DEFAULT_PEAK_END,
    DEFAULT_EV_ENABLED,
    DEFAULT_NOTIFY_CHANGE,
    DEFAULT_ADVISOR_INTERVAL_MIN,
)


def _user_schema(defaults: dict | None = None) -> vol.Schema:
    d = defaults or {}
    return vol.Schema(
        {
            vol.Optional("name", default=d.get("name", DEFAULT_NAME)): str,
            vol.Optional(
                CONF_UPDATE_INTERVAL,
                default=d.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL),
            ): int,
            vol.Optional(
                CONF_BATTERY_ENTITY,
                default=d.get(CONF_BATTERY_ENTITY),
            ): selector.selector({"entity": {"domain": "sensor"}}),
            vol.Optional(
                CONF_SOLAR_POWER_ENTITY,
                default=d.get(CONF_SOLAR_POWER_ENTITY),
            ): selector.selector({"entity": {"domain": "sensor"}}),
            vol.Optional(
                CONF_SOLAR_ENERGY_TODAY_ENTITY,
                default=d.get(CONF_SOLAR_ENERGY_TODAY_ENTITY),
            ): selector.selector({"entity": {"domain": "sensor"}}),
            vol.Optional(
                CONF_GRID_IMPORT_ENTITY,
                default=d.get(CONF_GRID_IMPORT_ENTITY),
            ): selector.selector({"entity": {"domain": "sensor"}}),
            vol.Optional(
                CONF_GRID_EXPORT_ENTITY,
                default=d.get(CONF_GRID_EXPORT_ENTITY),
            ): selector.selector({"entity": {"domain": "sensor"}}),
            vol.Optional(
                CONF_LOAD_POWER_ENTITY,
                default=d.get(CONF_LOAD_POWER_ENTITY),
            ): selector.selector({"entity": {"domain": "sensor"}}),
            vol.Optional(
                CONF_PRICE_NOW_ENTITY,
                default=d.get(CONF_PRICE_NOW_ENTITY),
            ): selector.selector({"entity": {"domain": "sensor"}}),
            vol.Optional(
                CONF_PRICE_NEXT_ENTITY,
                default=d.get(CONF_PRICE_NEXT_ENTITY),
            ): selector.selector({"entity": {"domain": "sensor"}}),
            vol.Optional(
                CONF_SOLAR_FORECAST_REMAINING_ENTITY,
                default=d.get(CONF_SOLAR_FORECAST_REMAINING_ENTITY),
            ): selector.selector({"entity": {"domain": "sensor"}}),
            vol.Optional(
                CONF_RESERVE_SOC,
                default=d.get(CONF_RESERVE_SOC, DEFAULT_RESERVE_SOC),
            ): int,
            vol.Optional(
                CONF_TARGET_SOC,
                default=d.get(CONF_TARGET_SOC, DEFAULT_TARGET_SOC),
            ): int,
            vol.Optional(
                CONF_CHEAP_PRICE,
                default=d.get(CONF_CHEAP_PRICE, DEFAULT_CHEAP_PRICE),
            ): float,
            vol.Optional(
                CONF_HIGH_PRICE,
                default=d.get(CONF_HIGH_PRICE, DEFAULT_HIGH_PRICE),
            ): float,
            vol.Optional(
                CONF_PEAK_START,
                default=d.get(CONF_PEAK_START, DEFAULT_PEAK_START),
            ): str,
            vol.Optional(
                CONF_PEAK_END,
                default=d.get(CONF_PEAK_END, DEFAULT_PEAK_END),
            ): str,
            vol.Optional(
                CONF_EV_ENABLED,
                default=d.get(CONF_EV_ENABLED, DEFAULT_EV_ENABLED),
            ): selector.selector({"boolean": {}}),
            vol.Optional(
                CONF_NOTIFY_CHANGE,
                default=d.get(CONF_NOTIFY_CHANGE, DEFAULT_NOTIFY_CHANGE),
            ): selector.selector({"boolean": {}}),
            vol.Optional(
                CONF_ADVISOR_INTERVAL_MIN,
                default=d.get(CONF_ADVISOR_INTERVAL_MIN, DEFAULT_ADVISOR_INTERVAL_MIN),
            ): int,
            vol.Optional(CONF_AGENT_ID, default=d.get(CONF_AGENT_ID, "")): str,
            vol.Optional(
                CONF_MINUTES_BETWEEN_AI,
                default=d.get(CONF_MINUTES_BETWEEN_AI, DEFAULT_MINUTES_BETWEEN_AI),
            ): int,
        }
    )


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        if user_input is not None:
            title = user_input.get("name", DEFAULT_NAME)
            options = {
                CONF_UPDATE_INTERVAL: int(
                    user_input.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
                ),
                CONF_BATTERY_ENTITY: user_input.get(CONF_BATTERY_ENTITY),
                CONF_SOLAR_POWER_ENTITY: user_input.get(CONF_SOLAR_POWER_ENTITY),
                CONF_SOLAR_ENERGY_TODAY_ENTITY: user_input.get(
                    CONF_SOLAR_ENERGY_TODAY_ENTITY
                ),
                CONF_GRID_IMPORT_ENTITY: user_input.get(CONF_GRID_IMPORT_ENTITY),
                CONF_GRID_EXPORT_ENTITY: user_input.get(CONF_GRID_EXPORT_ENTITY),
                CONF_LOAD_POWER_ENTITY: user_input.get(CONF_LOAD_POWER_ENTITY),
                CONF_PRICE_NOW_ENTITY: user_input.get(CONF_PRICE_NOW_ENTITY),
                CONF_PRICE_NEXT_ENTITY: user_input.get(CONF_PRICE_NEXT_ENTITY),
                CONF_SOLAR_FORECAST_REMAINING_ENTITY: user_input.get(
                    CONF_SOLAR_FORECAST_REMAINING_ENTITY
                ),
                CONF_RESERVE_SOC: int(
                    user_input.get(CONF_RESERVE_SOC, DEFAULT_RESERVE_SOC)
                ),
                CONF_TARGET_SOC: int(
                    user_input.get(CONF_TARGET_SOC, DEFAULT_TARGET_SOC)
                ),
                CONF_CHEAP_PRICE: float(
                    user_input.get(CONF_CHEAP_PRICE, DEFAULT_CHEAP_PRICE)
                ),
                CONF_HIGH_PRICE: float(
                    user_input.get(CONF_HIGH_PRICE, DEFAULT_HIGH_PRICE)
                ),
                CONF_PEAK_START: user_input.get(CONF_PEAK_START, DEFAULT_PEAK_START),
                CONF_PEAK_END: user_input.get(CONF_PEAK_END, DEFAULT_PEAK_END),
                CONF_EV_ENABLED: bool(
                    user_input.get(CONF_EV_ENABLED, DEFAULT_EV_ENABLED)
                ),
                CONF_NOTIFY_CHANGE: bool(
                    user_input.get(CONF_NOTIFY_CHANGE, DEFAULT_NOTIFY_CHANGE)
                ),
                CONF_ADVISOR_INTERVAL_MIN: int(
                    user_input.get(
                        CONF_ADVISOR_INTERVAL_MIN, DEFAULT_ADVISOR_INTERVAL_MIN
                    )
                ),
                CONF_AGENT_ID: (user_input.get(CONF_AGENT_ID) or "").strip(),
                CONF_MINUTES_BETWEEN_AI: int(
                    user_input.get(
                        CONF_MINUTES_BETWEEN_AI, DEFAULT_MINUTES_BETWEEN_AI
                    )
                ),
            }
            return self.async_create_entry(title=title, data={}, options=options)

        return self.async_show_form(step_id="user", data_schema=_user_schema())

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        opts = dict(self.config_entry.options)
        if user_input is not None:
            new_opts = dict(opts)
            if CONF_UPDATE_INTERVAL in user_input:
                new_opts[CONF_UPDATE_INTERVAL] = int(user_input[CONF_UPDATE_INTERVAL])
            if CONF_BATTERY_ENTITY in user_input:
                new_opts[CONF_BATTERY_ENTITY] = user_input[CONF_BATTERY_ENTITY]
            if CONF_SOLAR_POWER_ENTITY in user_input:
                new_opts[CONF_SOLAR_POWER_ENTITY] = user_input[CONF_SOLAR_POWER_ENTITY]
            if CONF_SOLAR_ENERGY_TODAY_ENTITY in user_input:
                new_opts[CONF_SOLAR_ENERGY_TODAY_ENTITY] = user_input[
                    CONF_SOLAR_ENERGY_TODAY_ENTITY
                ]
            if CONF_GRID_IMPORT_ENTITY in user_input:
                new_opts[CONF_GRID_IMPORT_ENTITY] = user_input[CONF_GRID_IMPORT_ENTITY]
            if CONF_GRID_EXPORT_ENTITY in user_input:
                new_opts[CONF_GRID_EXPORT_ENTITY] = user_input[CONF_GRID_EXPORT_ENTITY]
            if CONF_LOAD_POWER_ENTITY in user_input:
                new_opts[CONF_LOAD_POWER_ENTITY] = user_input[CONF_LOAD_POWER_ENTITY]
            if CONF_PRICE_NOW_ENTITY in user_input:
                new_opts[CONF_PRICE_NOW_ENTITY] = user_input[CONF_PRICE_NOW_ENTITY]
            if CONF_PRICE_NEXT_ENTITY in user_input:
                new_opts[CONF_PRICE_NEXT_ENTITY] = user_input[CONF_PRICE_NEXT_ENTITY]
            if CONF_SOLAR_FORECAST_REMAINING_ENTITY in user_input:
                new_opts[CONF_SOLAR_FORECAST_REMAINING_ENTITY] = user_input[
                    CONF_SOLAR_FORECAST_REMAINING_ENTITY
                ]
            if CONF_RESERVE_SOC in user_input:
                new_opts[CONF_RESERVE_SOC] = int(user_input[CONF_RESERVE_SOC])
            if CONF_TARGET_SOC in user_input:
                new_opts[CONF_TARGET_SOC] = int(user_input[CONF_TARGET_SOC])
            if CONF_CHEAP_PRICE in user_input:
                new_opts[CONF_CHEAP_PRICE] = float(user_input[CONF_CHEAP_PRICE])
            if CONF_HIGH_PRICE in user_input:
                new_opts[CONF_HIGH_PRICE] = float(user_input[CONF_HIGH_PRICE])
            if CONF_PEAK_START in user_input:
                new_opts[CONF_PEAK_START] = user_input[CONF_PEAK_START]
            if CONF_PEAK_END in user_input:
                new_opts[CONF_PEAK_END] = user_input[CONF_PEAK_END]
            if CONF_EV_ENABLED in user_input:
                new_opts[CONF_EV_ENABLED] = bool(user_input[CONF_EV_ENABLED])
            if CONF_NOTIFY_CHANGE in user_input:
                new_opts[CONF_NOTIFY_CHANGE] = bool(user_input[CONF_NOTIFY_CHANGE])
            if CONF_ADVISOR_INTERVAL_MIN in user_input:
                new_opts[CONF_ADVISOR_INTERVAL_MIN] = int(
                    user_input[CONF_ADVISOR_INTERVAL_MIN]
                )
            if CONF_AGENT_ID in user_input:
                new_opts[CONF_AGENT_ID] = (user_input[CONF_AGENT_ID] or "").strip()
            if CONF_MINUTES_BETWEEN_AI in user_input:
                new_opts[CONF_MINUTES_BETWEEN_AI] = int(
                    user_input[CONF_MINUTES_BETWEEN_AI]
                )
            if "name" in user_input:
                new_opts["name"] = user_input["name"]
            return self.async_create_entry(title="", data=new_opts)

        defaults = {
            "name": self.config_entry.title,
            **opts,
        }
        return self.async_show_form(step_id="init", data_schema=_user_schema(defaults))
