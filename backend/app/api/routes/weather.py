from fastapi import APIRouter, Query

from app.services.weather_service import WeatherService

router = APIRouter()


@router.get("/current")
async def current_weather(lat: float = Query(37.7749), lon: float = Query(-122.4194)):
    return WeatherService.get_weather(lat, lon)
