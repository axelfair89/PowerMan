from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time


@dataclass
class AdvisorInputs:
    now: datetime
    battery_pct: float | None
    solar_w: float | None
    load_w: float | None
    import_w: float | None
    export_w: float | None
    price_now: float | None
    price_next: float | None
    solar_kwh_remaining_today: float | None
    reserve_soc: int
    target_soc: int
    cheap_price: float
    high_price: float
    peak_start: time
    peak_end: time
    ev_enabled: bool


@dataclass
class Advice:
    code: str
    title: str
    confidence: float
    reasons: list[str]
    next_review_minutes: int


def _within_peak(now: datetime, start: time, end: time) -> bool:
    t = now.time()
    if start == end:
        return True
    return (t >= start) and (t < end) if start < end else (t >= start or t < end)


def make_advice(i: AdvisorInputs) -> Advice:
    reasons: list[str] = []
    conf = 0.5

    # Estimate load if missing
    if (
        i.load_w is None
        and i.solar_w is not None
        and i.import_w is not None
        and i.export_w is not None
    ):
        i.load_w = max(0.0, i.solar_w - i.export_w + i.import_w)

    peak = _within_peak(i.now, i.peak_start, i.peak_end)

    # Defaults to do nothing
    code = "do_nothing_normal_day"
    title = "Normal day — no action suggested"
    reasons.append("No clear economic or energy constraint detected")

    # Suggest charging before peak if we likely won't reach reserve
    if i.battery_pct is not None:
        if i.battery_pct < i.reserve_soc:
            reasons = [
                f"Battery below reserve ({i.battery_pct:.0f}% < {i.reserve_soc}%)",
            ]
            if i.price_now is not None and i.price_now <= i.cheap_price:
                code = "charge_battery_from_grid_now"
                title = "Charge battery now (cheap price, below reserve)"
                conf = 0.85
            elif not peak:
                code = "charge_battery_from_grid_now"
                title = "Charge battery now to reach reserve before peak"
                conf = 0.7

    # If lots of excess solar now (battery full-ish & exporting), recommend EV charging
    if i.ev_enabled:
        if (
            i.battery_pct is not None
            and i.battery_pct >= i.target_soc
            and i.export_w is not None
            and i.export_w > 500
        ):
            code = "plug_in_ev_now"
            title = "Excess solar — plug in EV"
            conf = 0.8
            reasons = [
                f"Battery at/above target ({i.battery_pct:.0f}% ≥ {i.target_soc}%)",
                f"Exporting {i.export_w:.0f} W",
            ]

    # Avoid charging at high prices, especially in peak window
    if i.price_now is not None and i.price_now >= i.high_price:
        if code == "charge_battery_from_grid_now":
            code = "do_nothing_normal_day"
            title = "Hold — price is high"
            conf = 0.6
            reasons.append(
                f"Current price {i.price_now:.2f} ≥ high threshold {i.high_price:.2f}"
            )

    # If we have solar remaining forecast and it's low before peak,
    # bias towards charging to reach target.
    if i.solar_kwh_remaining_today is not None and i.battery_pct is not None:
        if i.solar_kwh_remaining_today < 1.0 and i.battery_pct < i.target_soc and not peak:
            code = "charge_battery_from_grid_now"
            title = "Low remaining solar — charge to reach target"
            conf = max(conf, 0.75)
            reasons.append(
                f"Low solar left today ({i.solar_kwh_remaining_today:.1f} kWh)"
            )

    return Advice(
        code=code,
        title=title,
        confidence=round(conf, 2),
        reasons=reasons,
        next_review_minutes=10,
    )
