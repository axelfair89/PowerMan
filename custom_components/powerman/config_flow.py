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
    CONF_AGENT_ID,
    CONF_MINUTES_BETWEEN_AI,
    DEFAULT_MINUTES_BETWEEN_AI,
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
