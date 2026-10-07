from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

import httpx

from app.config import settings


class WeatherService:
    """Wrap Open-Meteo weather calls with a deterministic simulation fallback."""

    @staticmethod
    def _simulate_weather(lat: float, lon: float) -> dict[str, Any]:
        now = datetime.now(timezone.utc)
        base_temp = 18.0 + 8.0 * math.sin((now.timetuple().tm_yday / 365.0) * 2 * math.pi)
        cloud_cover = 38.0 + 18.0 * math.sin((now.hour / 24.0) * 2 * math.pi)
        irradiance = max(0.0, 700.0 * (1.0 - cloud_cover / 100.0))
        wind_speed = 8.0 + 3.0 * math.sin((now.hour + 3) / 24.0 * 2 * math.pi)
        rainfall = max(0.0, (cloud_cover - 60.0) / 15.0)
        return {
            "source": "simulation",
            "timestamp": now.isoformat(),
            "latitude": lat,
            "longitude": lon,
            "current": {
                "temperature_c": round(base_temp, 2),
                "cloud_cover_percent": round(max(0.0, min(100.0, cloud_cover)), 2),
                "irradiance_w_m2": round(irradiance, 2),
                "wind_speed_m_s": round(max(0.0, wind_speed), 2),
                "wind_direction_deg": 210.0,
                "rainfall_mm": round(rainfall, 2),
            },
            "forecast": [
                {
                    "timestamp": (now + __import__("datetime").timedelta(hours=i)).isoformat(),
                    "temperature_c": round(base_temp + 2.0 * math.sin(i / 6.0), 2),
                    "cloud_cover_percent": round(max(0.0, min(100.0, cloud_cover + 10.0 * math.sin(i / 5.0))), 2),
                    "irradiance_w_m2": round(max(0.0, 800.0 * (1.0 - (cloud_cover + 10.0 * math.sin(i / 5.0)) / 100.0)), 2),
                    "wind_speed_m_s": round(max(0.0, wind_speed + 2.0 * math.sin(i / 4.0)), 2),
                    "wind_direction_deg": round(210.0 + 20.0 * math.sin(i / 3.0), 2),
                    "rainfall_mm": round(max(0.0, rainfall + 0.2 * math.sin(i / 2.0)), 2),
                }
                for i in range(24)
            ],
        }

    @staticmethod
    def get_weather(lat: float, lon: float, *, forecast_hours: int = 24) -> dict[str, Any]:
        if settings.use_simulated_weather:
            return WeatherService._simulate_weather(lat, lon)

        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,cloud_cover,relative_humidity_2m,wind_speed_10m,wind_direction_10m,precipitation",
            "hourly": "temperature_2m,cloud_cover,shortwave_radiation,wind_speed_10m,wind_direction_10m,precipitation",
            "forecast_days": max(1, (forecast_hours + 23) // 24),
            "timezone": "auto",
        }
        try:
            response = httpx.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=15.0)
            response.raise_for_status()
            payload = response.json()
            current = payload.get("current") or {}
            hourly = payload.get("hourly") or {}
            forecast = []
            time_values = hourly.get("time") or []
            temps = hourly.get("temperature_2m") or []
            cloud_cover = hourly.get("cloud_cover") or []
            radiation = hourly.get("shortwave_radiation") or []
            wind_speed = hourly.get("wind_speed_10m") or []
            wind_direction = hourly.get("wind_direction_10m") or []
            rainfall = hourly.get("precipitation") or []
            for idx, timestamp in enumerate(time_values[:forecast_hours]):
                forecast.append(
                    {
                        "timestamp": timestamp,
                        "temperature_c": temps[idx] if idx < len(temps) else None,
                        "cloud_cover_percent": cloud_cover[idx] if idx < len(cloud_cover) else None,
                        "irradiance_w_m2": radiation[idx] if idx < len(radiation) else None,
                        "wind_speed_m_s": wind_speed[idx] if idx < len(wind_speed) else None,
                        "wind_direction_deg": wind_direction[idx] if idx < len(wind_direction) else None,
                        "rainfall_mm": rainfall[idx] if idx < len(rainfall) else None,
                    }
                )
            return {
                "source": "real_api",
                "timestamp": current.get("time") or datetime.now(timezone.utc).isoformat(),
                "latitude": lat,
                "longitude": lon,
                "current": {
                    "temperature_c": current.get("temperature_2m"),
                    "cloud_cover_percent": current.get("cloud_cover"),
                    "irradiance_w_m2": current.get("shortwave_radiation"),
                    "wind_speed_m_s": current.get("wind_speed_10m"),
                    "wind_direction_deg": current.get("wind_direction_10m"),
                    "rainfall_mm": current.get("precipitation"),
                },
                "forecast": forecast,
            }
        except Exception:
            return WeatherService._simulate_weather(lat, lon)
