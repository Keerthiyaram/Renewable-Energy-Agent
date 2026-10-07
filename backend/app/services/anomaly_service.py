from __future__ import annotations

from statistics import mean, pstdev
from typing import Any


class AnomalyService:
    @staticmethod
    def detect(values: list[float], *, threshold: float = 2.0) -> dict[str, Any]:
        if not values:
            return {"anomalies": [], "score": 0.0, "severity": "low"}
        avg = mean(values)
        std = pstdev(values) or 1.0
        anomalies = []
        for index, value in enumerate(values):
            score = abs(value - avg) / std
            if score > threshold:
                anomalies.append({"index": index, "value": value, "z_score": round(score, 4)})
        severity = "low"
        if anomalies:
            max_score = max(item["z_score"] for item in anomalies)
            if max_score > 4.5:
                severity = "critical"
            elif max_score > 3.0:
                severity = "high"
            elif max_score > 2.5:
                severity = "medium"
        return {"anomalies": anomalies, "score": round(max((item["z_score"] for item in anomalies), default=0.0), 4), "severity": severity}
