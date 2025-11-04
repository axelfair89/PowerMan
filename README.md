
# PowerMan — your first Home Assistant integration

A tiny, self-contained custom integration that creates three demo sensors:

- **Power** (W)
- **Voltage** (V)
- **Current** (A)

It uses a `DataUpdateCoordinator` to simulate readings every N seconds.

## Install

1. Download the zip from your ChatGPT session and extract it.
2. Copy the `custom_components/powerman` folder into your Home Assistant configuration directory:
   `config/custom_components/powerman`
3. Restart Home Assistant.
4. Go to **Settings → Devices & services → Add Integration** and search for **PowerMan**.
5. Choose a name and update interval.

## Development tips

- All logic for fetching/updating data lives in `coordinator.py`.
- Add real I/O there later (HTTP, Modbus, serial, etc.).
- Expose more entities by extending `sensor.py` or adding platforms like `switch.py`/`number.py`.
- Adjust options via **Configure** on the integration card.
