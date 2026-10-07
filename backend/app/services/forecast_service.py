from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from scripts.generate_synthetic_data import generate_rows


def _synthetic_history(hours: int = 168) -> pd.DataFrame:
    start = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0) - timedelta(hours=hours)
    rows = list(generate_rows(start, hours))
    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_year"] = df["timestamp"].dt.dayofyear
    df["is_daytime"] = df["hour"].between(6, 18).astype(int)
    return df


class ForecastService:
    """Deterministic forecasting service using scikit-learn models."""

    @staticmethod
    def _train_model(target: str, feature_columns: list[str]) -> tuple[RandomForestRegressor, pd.DataFrame]:
        df = _synthetic_history(240)
        model = RandomForestRegressor(n_estimators=40, random_state=42)
        X = df[feature_columns]
        y = df[target]
        model.fit(X, y)
        return model, df

    @staticmethod
    def solar_forecast() -> dict[str, Any]:
        feature_columns = ["ghi_w_m2", "cloud_cover_percent", "temperature_c", "hour", "day_of_year"]
        model, df = ForecastService._train_model("solar_generation_mw", feature_columns)
        future = pd.DataFrame([
            {
                "ghi_w_m2": 700.0,
                "cloud_cover_percent": 35.0,
                "temperature_c": 25.0,
                "hour": datetime.now(timezone.utc).hour,
                "day_of_year": datetime.now(timezone.utc).timetuple().tm_yday,
            }
        ])
        predictions = model.predict(df[feature_columns])
        mae = float(np.mean(np.abs(df["solar_generation_mw"] - predictions)))
        prediction = float(model.predict(future)[0])
        return {
            "model": "RandomForestRegressor",
            "target": "solar_generation_mw",
            "forecast_time": datetime.now(timezone.utc).isoformat(),
            "predicted_generation_mw": round(max(0.0, prediction), 4),
            "confidence": round(max(0.0, 1.0 - min(mae / 10.0, 0.95)), 4),
            "features_used": feature_columns,
            "mae": round(float(mae), 4),
        }

    @staticmethod
    def wind_forecast() -> dict[str, Any]:
        feature_columns = ["wind_speed_m_s", "wind_direction_deg", "temperature_c", "hour", "day_of_year"]
        model, df = ForecastService._train_model("wind_generation_mw", feature_columns)
        future = pd.DataFrame([
            {
                "wind_speed_m_s": 9.5,
                "wind_direction_deg": 220.0,
                "temperature_c": 22.0,
                "hour": datetime.now(timezone.utc).hour,
                "day_of_year": datetime.now(timezone.utc).timetuple().tm_yday,
            }
        ])
        predictions = model.predict(df[feature_columns])
        mae = float(np.mean(np.abs(df["wind_generation_mw"] - predictions)))
        prediction = float(model.predict(future)[0])
        return {
            "model": "RandomForestRegressor",
            "target": "wind_generation_mw",
            "forecast_time": datetime.now(timezone.utc).isoformat(),
            "predicted_generation_mw": round(max(0.0, prediction), 4),
            "confidence": round(max(0.0, 1.0 - min(mae / 8.0, 0.9)), 4),
            "features_used": feature_columns,
            "mae": round(float(mae), 4),
        }

    @staticmethod
    def demand_forecast() -> dict[str, Any]:
        feature_columns = ["hour", "day_of_year", "temperature_c", "is_daytime"]
        model, df = ForecastService._train_model("demand_mw", feature_columns)
        future = pd.DataFrame([
            {
                "hour": datetime.now(timezone.utc).hour,
                "day_of_year": datetime.now(timezone.utc).timetuple().tm_yday,
                "temperature_c": 21.0,
                "is_daytime": 1,
            }
        ])
        predictions = model.predict(df[feature_columns])
        mae = float(np.mean(np.abs(df["demand_mw"] - predictions)))
        prediction = float(model.predict(future)[0])
        return {
            "model": "RandomForestRegressor",
            "target": "demand_mw",
            "forecast_time": datetime.now(timezone.utc).isoformat(),
            "predicted_generation_mw": round(max(0.0, prediction), 4),
            "confidence": round(max(0.0, 1.0 - min(mae / 12.0, 0.95)), 4),
            "features_used": feature_columns,
            "mae": round(float(mae), 4),
        }

    @staticmethod
    def get_all() -> dict[str, Any]:
        return {
            "solar": ForecastService.solar_forecast(),
            "wind": ForecastService.wind_forecast(),
            "demand": ForecastService.demand_forecast(),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
