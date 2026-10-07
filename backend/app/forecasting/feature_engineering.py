from __future__ import annotations

from datetime import datetime


def engineer_features(record: dict) -> dict:
    timestamp = datetime.fromisoformat(record["timestamp"]) if isinstance(record.get("timestamp"), str) else record["timestamp"]
    return {
        "hour": timestamp.hour,
        "day_of_year": timestamp.timetuple().tm_yday,
        "temperature_c": record.get("temperature_c", 20.0),
        "cloud_cover_percent": record.get("cloud_cover_percent", 30.0),
        "ghi_w_m2": record.get("ghi_w_m2", 500.0),
        "wind_speed_m_s": record.get("wind_speed_m_s", 8.0),
        "wind_direction_deg": record.get("wind_direction_deg", 180.0),
        "is_daytime": 1 if 6 <= timestamp.hour <= 18 else 0,
    }
