🧠 PowerMan

A modular Home Assistant integration for energy insights and AI-assisted summaries.

Overview

PowerMan is a lightweight custom integration that unifies your existing Home Assistant energy sensors — battery, solar production (live and daily), and more — into a single logical “energy hub.”
It collects the current readings through Home Assistant’s state system and can optionally generate AI-powered daily insights by forwarding a concise energy summary to your configured Google Gemini Conversation Agent.

PowerMan is designed as an example of how to:

Combine multiple energy-related entities using a DataUpdateCoordinator.

Offer a clean configuration flow and dynamic options.

Safely call external AI services through existing Home Assistant integrations, without any API keys stored in the component.

Features

🔋 Battery %, ☀️ Solar Power (W), ⚡ Solar Energy Today (kWh) sensors (mapped from your own HA entities).

🧩 Single “PowerMan” device card that groups all sensors neatly.

⚙️ Configurable update interval and entity mapping through the UI — no YAML required.

🤖 Optional AI insights using your own Google Gemini integration.

🛡️ Built-in rate limiting (default 3 hours between AI calls) to avoid token overuse.

💬 Local fallback summaries so you always see an energy report even if AI is disabled.

Installation

Copy the custom_components/powerman folder into your Home Assistant configuration directory:

config/custom_components/powerman


Restart Home Assistant.

Go to Settings → Devices & Services → Add Integration, search for PowerMan, and follow the prompts.

Choose your battery/solar entities and (optionally) paste the Conversation Agent ID from your existing Google Gemini setup.

Adjust the update interval and AI rate-limit as desired.

(If you use HACS, you can add this GitHub repository as a Custom Repository → Integration and install from there.)

Usage

The integration automatically updates sensor values at the interval you specify.

To generate a summary manually, call the service

powerman.generate_insight


from Developer Tools → Services.

You’ll receive a local notification summarising today’s data.

If an agent_id is configured and the rate-limit allows, PowerMan also sends the prompt to your Gemini agent for a richer AI response.

Configuration Options
OptionDescription
Battery EntitySource sensor providing battery %.
Solar Power EntityLive solar generation (W).
Solar Energy Today EntityDaily solar production (kWh).
Update IntervalHow often to poll source entities.
Conversation Agent ID(Optional) Your Gemini conversation agent to receive AI prompts.
Min Minutes Between AIMinimum time between AI calls (default 180 min).
Development

Core data logic lives in coordinator.py.

The configuration/option flow is in config_flow.py.

Sensors are defined in sensor.py.

The AI service is implemented in __init__.py (powerman.generate_insight).

Modify or extend these files to connect to real hardware, APIs, or analytics.

License

MIT License — see LICENSE
 for details.
