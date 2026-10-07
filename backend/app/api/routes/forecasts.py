from fastapi import APIRouter

from app.services.forecast_service import ForecastService

router = APIRouter()


@router.get("/all")
async def all_forecasts():
    return ForecastService.get_all()


@router.get("/solar")
async def solar_forecast():
    return ForecastService.solar_forecast()


@router.get("/wind")
async def wind_forecast():
    return ForecastService.wind_forecast()


@router.get("/demand")
async def demand_forecast():
    return ForecastService.demand_forecast()
