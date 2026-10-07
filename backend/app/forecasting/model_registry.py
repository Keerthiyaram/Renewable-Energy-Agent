from __future__ import annotations

from app.forecasting.demand_model import DemandModel
from app.forecasting.solar_model import SolarModel
from app.forecasting.wind_model import WindModel

MODEL_REGISTRY = {
    "solar": SolarModel(),
    "wind": WindModel(),
    "demand": DemandModel(),
}


def get_model(name: str):
    return MODEL_REGISTRY[name]
