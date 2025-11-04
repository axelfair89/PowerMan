from __future__ import annotations
import logging
from datetime import datetime, timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    DEFAULT_UPDATE_INTERVAL,
    CONF_UPDATE_INTERVAL,
    CONF_AGENT_ID,
    CONF_MINUTES_BETWEEN_AI,
    DEFAULT_MINUTES_BETWEEN_AI,
)
from .coordinator import PowerManCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor"]

LAST_AI_KEY = "last_ai_run"  # stored per entry in hass.data


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    update_seconds = entry.options.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
    coordinator = PowerManCoordinator(
        hass,
        update_interval=timedelta(seconds=update_seconds),
        entry_options=entry.options,
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "coordinator": coordinator,
        LAST_AI_KEY: None,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    # ---- Service: powerman.generate_insight ----
    async def _handle_generate_insight(call):
        store = hass.data[DOMAIN][entry.entry_id]
        coord: PowerManCoordinator = store["coordinator"]
        data = coord.data or {}

        # Build a *local* summary (no tokens used)
        now = dt_util.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        bat = data.get("battery_percent")
        pwr = data.get("solar_power_w")
        kwh = data.get("solar_energy_today_kwh")

        summary_lines = [f"PowerMan insight — {now.strftime('%Y-%m-%d %H:%M')}"]
        if kwh is not None:
            summary_lines.append(
                f"• Solar energy today: {kwh:.2f} kWh since {today_start.strftime('%H:%M')}"
            )
        if pwr is not None:
            summary_lines.append(f"• Live solar power: {pwr:.0f} W")
        if bat is not None:
            summary_lines.append(f"• Battery state: {bat:.0f} %")
        if len(summary_lines) == 1:
            summary_lines.append(
                "• No mapped entities yet. Configure in the integration options."
            )

        local_summary = "\n".join(summary_lines)

        # Always show a notification with the local summary
        await hass.services.async_call(
            "persistent_notification",
            "create",
            {"title": "PowerMan — Local insight", "message": local_summary},
            blocking=True,
        )

        # Optional AI call (rate limited)
        agent_id = (entry.options.get(CONF_AGENT_ID) or "").strip()
        if not agent_id:
            _LOGGER.debug("PowerMan: no agent_id configured; skipping AI.")
            return

        min_minutes = int(
            entry.options.get(
                CONF_MINUTES_BETWEEN_AI, DEFAULT_MINUTES_BETWEEN_AI
            )
        )
        last: datetime | None = store.get(LAST_AI_KEY)
        if last and (dt_util.now() - last) < timedelta(minutes=min_minutes):
            _LOGGER.info(
                "PowerMan: AI rate limit hit; skipping (last run %s).",
                last,
            )
            return

        prompt = (
            "You are an energy assistant. Summarise today's solar/battery situation briefly in 3–5 bullet points. "
            "Be concise and practical for a home user.\n\n"
            f"Data:\n"
            f"- Solar energy produced today (kWh): {kwh if kwh is not None else 'unknown'}\n"
            f"- Live solar power (W): {pwr if pwr is not None else 'unknown'}\n"
            f"- Battery state (%): {bat if bat is not None else 'unknown'}\n"
            f"- Current time: {now.isoformat()}\n"
        )

        # Use HA's Conversation service (agent = Google Gemini conversation the user configured)
        try:
            await hass.services.async_call(
                "conversation",
                "process",
                {"agent_id": agent_id, "text": prompt},
                blocking=True,
            )
            store[LAST_AI_KEY] = dt_util.now()

            await hass.services.async_call(
                "persistent_notification",
                "create",
                {
                    "title": "PowerMan — AI insight requested",
                    "message": "Sent prompt to your Conversation agent. Check Assist/Conversation history or any linked outputs (e.g. TTS).",
                },
                blocking=True,
            )
        except Exception as exc:  # noqa: BLE001
            _LOGGER.exception("PowerMan: AI call failed: %s", exc)
            await hass.services.async_call(
                "persistent_notification",
                "create",
                {
                    "title": "PowerMan — AI error",
                    "message": f"AI call failed: {exc}",
                },
                blocking=True,
            )

    hass.services.async_register(DOMAIN, "generate_insight", _handle_generate_insight)
    # --------------------------------------------

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    store = hass.data[DOMAIN][entry.entry_id]
    coordinator: PowerManCoordinator = store["coordinator"]
    coordinator.update_interval = timedelta(
        seconds=entry.options.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
    )
    await coordinator.async_request_refresh()
