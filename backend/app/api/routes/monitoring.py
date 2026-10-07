from fastapi import APIRouter

from app.services.monitoring_service import MonitoringService

router = APIRouter()


@router.get("/overview")
async def dashboard_overview():
    return MonitoringService.get_dashboard_snapshot()


@router.get("/current")
async def current_state():
    return MonitoringService.get_current_state()
