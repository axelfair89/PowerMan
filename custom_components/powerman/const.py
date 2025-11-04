DOMAIN = "powerman"
DEFAULT_NAME = "PowerMan"
DEFAULT_UPDATE_INTERVAL = 30  # seconds

# Options/Config keys
CONF_UPDATE_INTERVAL = "update_interval"
CONF_BATTERY_ENTITY = "battery_entity"
CONF_SOLAR_POWER_ENTITY = "solar_power_entity"
CONF_SOLAR_ENERGY_TODAY_ENTITY = "solar_energy_today_entity"

# New optional inputs
CONF_GRID_IMPORT_ENTITY = "grid_import_power_entity"
CONF_GRID_EXPORT_ENTITY = "grid_export_power_entity"
CONF_LOAD_POWER_ENTITY = "house_load_power_entity"
CONF_PRICE_NOW_ENTITY = "current_price_entity"
CONF_PRICE_NEXT_ENTITY = "price_next_hour_entity"
CONF_SOLAR_FORECAST_REMAINING_ENTITY = "solar_forecast_remaining_today_entity"

# Advisor options
CONF_RESERVE_SOC = "reserve_soc_percent"
CONF_TARGET_SOC = "target_soc_percent"
CONF_CHEAP_PRICE = "cheap_price_threshold"
CONF_HIGH_PRICE = "high_price_threshold"
CONF_PEAK_START = "peak_start"
CONF_PEAK_END = "peak_end"
CONF_EV_ENABLED = "ev_recommendation_enabled"
CONF_NOTIFY_CHANGE = "notify_on_change"
CONF_ADVISOR_INTERVAL_MIN = "advisor_interval_minutes"
DEFAULT_RESERVE_SOC = 30
DEFAULT_TARGET_SOC = 80
DEFAULT_CHEAP_PRICE = 0.15
DEFAULT_HIGH_PRICE = 0.30
DEFAULT_PEAK_START = "15:00"
DEFAULT_PEAK_END = "21:00"
DEFAULT_EV_ENABLED = True
DEFAULT_NOTIFY_CHANGE = True
DEFAULT_ADVISOR_INTERVAL_MIN = 10

# AI options
CONF_AGENT_ID = "agent_id"  # conversation agent id (from Google Gemini conversation)
CONF_MINUTES_BETWEEN_AI = "min_minutes_between_ai"  # rate limit in minutes
DEFAULT_MINUTES_BETWEEN_AI = 180  # 3 hours

DEVICE_ID = "powerman_hub"
