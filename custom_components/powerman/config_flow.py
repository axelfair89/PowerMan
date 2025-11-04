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
)

def _user_schema(defaults: dict | None = None) -> vol.Schema:
    d = defaults or {}
    return vol.Schema(
        {
            vol.Optional("name", default=d.get("name", DEFAULT_NAME)): str,
            vol.Optional(CONF_UPDATE_INTERVAL, default=d.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)): int,
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
        }
    )


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        if user_input is not None:
            title = user_input.get("name", DEFAULT_NAME)
            options = {
                CONF_UPDATE_INTERVAL: int(user_input.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)),
                CONF_BATTERY_ENTITY: user_input.get(CONF_BATTERY_ENTITY),
                CONF_SOLAR_POWER_ENTITY: user_input.get(CONF_SOLAR_POWER_ENTITY),
                CONF_SOLAR_ENERGY_TODAY_ENTITY: user_input.get(CONF_SOLAR_ENERGY_TODAY_ENTITY),
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
            opts.update(user_input)
            return self.async_create_entry(title="", data=opts)

        defaults = {
            "name": self.config_entry.title,
            **opts,
        }
        return self.async_show_form(step_id="init", data_schema=_user_schema(defaults))
