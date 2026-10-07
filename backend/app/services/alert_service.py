from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class AlertService:
    @staticmethod
    def build_alerts(monitoring: dict[str, Any]) -> list[dict[str, Any]]:
        alerts: list[dict[str, Any]] = []
        current = monitoring.get("current", {})
        balance = float(current.get("renewable_surplus_deficit_mw", 0.0))
        soc = float(current.get("battery_soc_percent", 0.0))
        if abs(balance) > 2.0:
            alerts.append({
                "id": "ALERT-001",
                "severity": "high" if abs(balance) > 4.0 else "medium",
                "asset": "grid-balance",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "category": "forecast_deficit" if balance < 0 else "surplus",
                "message": "Renewable surplus/deficit exceeds operating tolerance.",
                "evidence": {"balance_mw": balance},
                "status": "active",
                "acknowledged": False,
            })
        if soc > 82 or soc < 25:
            alerts.append({
                "id": "ALERT-002",
                "severity": "medium",
                "asset": "battery",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "category": "battery_soc_limit",
                "message": "Battery state of charge is approaching operating bounds.",
                "evidence": {"soc_percent": soc},
                "status": "active",
                "acknowledged": False,
            })
        if monitoring.get("active_anomalies", 0) > 0:
            alerts.append({
                "id": "ALERT-003",
                "severity": "high",
                "asset": "solar",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "category": "anomaly_detected",
                "message": "An anomaly has been detected in renewable output.",
                "evidence": {"anomalies": monitoring.get("active_anomalies")},
                "status": "active",
                "acknowledged": False,
            })
        return alerts
