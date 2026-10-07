from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class ValidationService:
    @staticmethod
    def _coerce_float(value: Any) -> float | None:
        if value is None or value == "":
            return None
        if isinstance(value, bool):
            return float(value)
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            cleaned = value.strip().replace(",", "")
            if cleaned.lower() in {"", "nan", "null", "none"}:
                return None
            try:
                return float(cleaned)
            except ValueError:
                return None
        return None

    @staticmethod
    def validate_measurement(
        *,
        asset_type: str,
        capacity_mw: float,
        generation_mw: float | None,
        soc_percent: float | None,
        timestamp: str | datetime | None,
    ) -> dict[str, Any]:
        errors: list[str] = []

        normalized_generation = ValidationService._coerce_float(generation_mw)
        normalized_soc = ValidationService._coerce_float(soc_percent)

        if normalized_generation is not None and normalized_generation < 0:
            errors.append("Negative generation is not allowed for renewable output")
        if normalized_generation is not None and capacity_mw > 0 and normalized_generation > capacity_mw * 1.25:
            errors.append("Generation exceeds installed capacity")
        if normalized_soc is not None:
            if normalized_soc < 0 or normalized_soc > 100:
                errors.append("Battery SoC must be between 0 and 100 percent")
        if timestamp is None:
            errors.append("Timestamp is required")
        else:
            try:
                parsed = timestamp if isinstance(timestamp, datetime) else datetime.fromisoformat(str(timestamp).replace("Z", "+00:00"))
                if parsed.tzinfo is None:
                    errors.append("Timestamp must be timezone-aware")
            except ValueError:
                errors.append("Timestamp is invalid")

        if asset_type == "battery" and normalized_soc is None:
            errors.append("Battery measurements require SoC")

        return {"valid": not errors, "errors": errors}

    @staticmethod
    def validate_rows(rows: list[dict[str, Any]], *, capacity_mw: float) -> dict[str, Any]:
        accepted: list[dict[str, Any]] = []
        rejected: list[dict[str, Any]] = []
        duplicate_count = 0
        seen_timestamps: set[str] = set()

        for index, row in enumerate(rows):
            timestamp = row.get("timestamp")
            key = str(timestamp)
            if key in seen_timestamps:
                duplicate_count += 1
                rejected.append({"index": index, "reason": "duplicate timestamp", "row": row})
                continue
            seen_timestamps.add(key)

            result = ValidationService.validate_measurement(
                asset_type=row.get("asset_type", "solar"),
                capacity_mw=capacity_mw,
                generation_mw=row.get("generation_mw"),
                soc_percent=row.get("battery_soc_percent"),
                timestamp=timestamp,
            )

            if result["valid"]:
                accepted.append(row)
            else:
                rejected.append({"index": index, "errors": result["errors"], "row": row})

        return {
            "valid": not rejected,
            "accepted_rows": accepted,
            "rejected_rows": rejected,
            "validation_errors": [entry for entry in rejected if isinstance(entry, dict) and "errors" in entry],
            "duplicate_count": duplicate_count,
            "processing_summary": {
                "total_rows": len(rows),
                "accepted": len(accepted),
                "rejected": len(rejected),
                "duplicates": duplicate_count,
            },
        }
