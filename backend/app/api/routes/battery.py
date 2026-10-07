from fastapi import APIRouter, Query

from app.services.battery_service import BatteryService

router = APIRouter()


@router.get("/status")
async def battery_status(renewable_surplus_mw: float = Query(default=1.5), demand_mw: float = Query(default=8.0)):
    return BatteryService.get_status(renewable_surplus_mw, demand_mw)


@router.get("/optimize")
async def optimize_battery(renewable_surplus_mw: float = Query(default=1.5), hours: int = Query(default=6, ge=1, le=24)):
    return BatteryService.optimize_schedule(renewable_surplus_mw, hours)
