from fastapi import APIRouter, Query

from app.services.optimization_service import OptimizationService

router = APIRouter()


@router.get("/battery")
async def optimize_battery(
    renewable_surplus_mw: float = Query(default=1.5),
    hours: int = Query(default=6, ge=1, le=24),
):
    return OptimizationService.optimize_battery_schedule(renewable_surplus_mw=renewable_surplus_mw, hours=hours)
