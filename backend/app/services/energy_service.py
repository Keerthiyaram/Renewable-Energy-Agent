from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.services.validation_service import ValidationService


class EnergyService:
    @staticmethod
    def ingest_rows(rows: list[dict[str, Any]], *, asset_type: str = "solar", capacity_mw: float = 10.0) -> dict[str, Any]:
        processed = []
        for row in rows:
            normalized = dict(row)
            if "timestamp" not in normalized:
                normalized["timestamp"] = datetime.now(timezone.utc).isoformat()
            if "asset_type" not in normalized:
                normalized["asset_type"] = asset_type
            if "generation_mw" not in normalized:
                normalized["generation_mw"] = 0.0
            processed.append(normalized)

        result = ValidationService.validate_rows(processed, capacity_mw=capacity_mw)
        return {
            "accepted_rows": result["accepted_rows"],
            "rejected_rows": result["rejected_rows"],
            "validation_errors": result["validation_errors"],
            "duplicate_count": result["duplicate_count"],
            "processing_summary": result["processing_summary"],
            "source": "ingestion-service",
        }

    @staticmethod
    def get_live_state() -> dict[str, Any]:
        return {
            "current_solar_generation_mw": 4.8,
            "current_wind_generation_mw": 3.2,
            "total_renewable_generation_mw": 8.0,
            "installed_capacity_mw": 16.0,
            "capacity_utilization_pct": 50.0,
            "battery_soc_percent": 29.25,
            "current_demand_mw": 11.5,
            "renewable_surplus_deficit_mw": -3.5,
        }
