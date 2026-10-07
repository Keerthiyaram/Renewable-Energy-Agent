from fastapi import APIRouter

from app.services.forecast_service import ForecastService

router = APIRouter()


@router.get("/forecast")
async def demand_forecast():
    return ForecastService.demand_forecast()
