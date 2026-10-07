from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.services.alert_service import AlertService
from app.services.battery_service import BatteryService
from app.services.forecast_service import ForecastService
from app.services.weather_service import WeatherService


class MonitoringService:
    @staticmethod
    def get_dashboard_snapshot() -> dict[str, Any]:
        solar = 4.8
        wind = 3.2
        demand = 11.5
        total = solar + wind
        balance = total - demand
        battery = BatteryService.get_status(balance, demand)
        forecast = ForecastService.get_all()
        weather = WeatherService.get_weather(37.7749, -122.4194)
        monitoring = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "current": {
                "solar_generation_mw": solar,
                "wind_generation_mw": wind,
                "total_renewable_generation_mw": total,
                "installed_capacity_mw": 16.0,
                "capacity_utilization_pct": round((total / 16.0) * 100, 2),
                "current_demand_mw": demand,
                "renewable_surplus_deficit_mw": round(balance, 2),
                "battery_soc_percent": battery["current_soc_percent"],
                "battery_stored_energy_mwh": battery["stored_energy_mwh"],
            },
            "forecast": forecast,
            "weather": weather,
            "active_anomalies": 0,
        }
        monitoring["alerts"] = AlertService.build_alerts(monitoring)
        monitoring["battery"] = battery
        return monitoring

    @staticmethod
    def get_current_state() -> dict[str, Any]:
        snapshot = MonitoringService.get_dashboard_snapshot()
        return snapshot["current"]
