"""Generate a deterministic hourly renewable-energy sample dataset."""

from __future__ import annotations

import argparse
import csv
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterator


SOLAR_CAPACITY_MW = 10.0
WIND_CAPACITY_MW = 6.0
BATTERY_CAPACITY_MWH = 8.0
BATTERY_POWER_LIMIT_MW = 2.0
BATTERY_MIN_SOC_PERCENT = 20.0
BATTERY_MAX_SOC_PERCENT = 90.0
BATTERY_EFFICIENCY = 0.9
FIELDNAMES = (
    "timestamp",
    "solar_generation_mw",
    "solar_forecast_mw",
    "wind_generation_mw",
    "demand_mw",
    "ghi_w_m2",
    "cloud_cover_percent",
    "temperature_c",
    "wind_speed_m_s",
    "wind_direction_deg",
    "rainfall_mm",
    "battery_soc_percent",
    "renewable_balance_mw",
    "cloud_event",
    "underperformance_event",
)


def generate_rows(start: datetime, hours: int) -> Iterator[dict[str, str | float | int]]:
    """Yield hourly measurements with correlated weather, generation, and demand."""
    if start.tzinfo is None or start.utcoffset() is None:
        raise ValueError("start must be timezone-aware")
    if hours < 1:
        raise ValueError("hours must be at least 1")

    battery_soc = 45.0
    for offset in range(hours):
        timestamp = start + timedelta(hours=offset)
        hour = timestamp.hour + timestamp.minute / 60
        day = timestamp.timetuple().tm_yday
        seasonal_angle = 2 * math.pi * (day - 172) / 365.0
        seasonal_sun = 0.62 + 0.38 * math.cos(seasonal_angle)
        daylight_hours = 8.0 + 8.0 * (seasonal_sun - 0.24) / 0.76
        sunrise = 12.0 - daylight_hours / 2
        solar_elevation = max(0.0, math.sin(math.pi * (hour - sunrise) / daylight_hours))

        cloud_cycle = 0.15 + 0.38 * (0.5 + 0.5 * math.sin(offset * 2 * math.pi / 53.0))
        cloud_event = day == 150 and 10 <= timestamp.hour <= 15
        cloud_cover = min(0.96, 0.86 if cloud_event else cloud_cycle)
        irradiance = 950.0 * solar_elevation * seasonal_sun * (1.0 - 0.75 * cloud_cover)
        clear_sky_generation = SOLAR_CAPACITY_MW * solar_elevation * seasonal_sun * 0.95
        solar_generation = clear_sky_generation * (1.0 - 0.75 * cloud_cover)

        underperformance_event = day in range(220, 223) and 11 <= timestamp.hour <= 15
        if underperformance_event:
            solar_generation *= 0.55

        forecast_cloud = min(1.0, max(0.0, cloud_cover + 0.08 * math.sin(offset / 17.0)))
        solar_forecast = clear_sky_generation * (1.0 - 0.75 * forecast_cloud)

        wind_speed = 7.5 + 2.0 * math.cos(seasonal_angle) + 2.1 * math.sin(offset * 2 * math.pi / 31.0)
        wind_speed += 1.0 * math.sin(offset * 2 * math.pi / 7.0)
        wind_speed = min(24.0, max(0.5, wind_speed))
        if wind_speed < 3.0 or wind_speed >= 25.0:
            wind_generation = 0.0
        else:
            wind_generation = WIND_CAPACITY_MW * (wind_speed**3 - 3.0**3) / (12.0**3 - 3.0**3)
            wind_generation = min(WIND_CAPACITY_MW, max(0.0, wind_generation))

        temperature = 14.0 + 11.0 * math.cos(seasonal_angle) + 4.0 * math.sin((hour - 8) * 2 * math.pi / 24)
        demand = 7.4 + 0.9 * math.cos((hour - 8) * 2 * math.pi / 24)
        demand += 1.1 * math.cos(seasonal_angle) + max(0.0, abs(temperature - 18.0) - 6.0) * 0.12
        demand += 0.25 * math.sin(offset * 2 * math.pi / 5.0)
        balance = solar_generation + wind_generation - demand

        if balance >= 0:
            charge_power = min(BATTERY_POWER_LIMIT_MW, balance)
            charge_power = min(charge_power, (BATTERY_MAX_SOC_PERCENT - battery_soc) / 100 * BATTERY_CAPACITY_MWH / BATTERY_EFFICIENCY)
            battery_soc += charge_power * BATTERY_EFFICIENCY / BATTERY_CAPACITY_MWH * 100
        else:
            discharge_power = min(BATTERY_POWER_LIMIT_MW, -balance)
            discharge_power = min(discharge_power, (battery_soc - BATTERY_MIN_SOC_PERCENT) / 100 * BATTERY_CAPACITY_MWH * BATTERY_EFFICIENCY)
            battery_soc -= discharge_power / BATTERY_EFFICIENCY / BATTERY_CAPACITY_MWH * 100

        yield {
            "timestamp": timestamp.astimezone(timezone.utc).isoformat(),
            "solar_generation_mw": round(solar_generation, 4),
            "solar_forecast_mw": round(solar_forecast, 4),
            "wind_generation_mw": round(wind_generation, 4),
            "demand_mw": round(demand, 4),
            "ghi_w_m2": round(irradiance, 2),
            "cloud_cover_percent": round(cloud_cover * 100, 2),
            "temperature_c": round(temperature, 2),
            "wind_speed_m_s": round(wind_speed, 2),
            "wind_direction_deg": round((210 + 35 * math.sin(offset / 20.0)) % 360, 2),
            "rainfall_mm": round(max(0.0, (cloud_cover - 0.65) * 8.0), 2),
            "battery_soc_percent": round(battery_soc, 4),
            "renewable_balance_mw": round(balance, 4),
            "cloud_event": int(cloud_event),
            "underperformance_event": int(underperformance_event),
        }


def write_dataset(destination: Path, start: datetime, hours: int) -> int:
    """Write generated rows to CSV and return the number of rows written."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=FIELDNAMES)
        writer.writeheader()
        count = 0
        for row in generate_rows(start, hours):
            writer.writerow(row)
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hours", type=int, default=8760, help="Number of hourly rows (default: one year)")
    parser.add_argument("--start", help="Timezone-aware ISO-8601 start timestamp; defaults to the last complete year")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "sample" / "renewable_energy_hourly.csv",
    )
    arguments = parser.parse_args()
    start = datetime.fromisoformat(arguments.start) if arguments.start else datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0) - timedelta(hours=arguments.hours - 1)
    count = write_dataset(arguments.output, start, arguments.hours)
    print(f"Wrote {count} hourly rows to {arguments.output}")


if __name__ == "__main__":
    main()