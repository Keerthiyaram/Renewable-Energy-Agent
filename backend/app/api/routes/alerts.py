from fastapi import APIRouter

from app.services.monitoring_service import MonitoringService

router = APIRouter()


@router.get("/")
async def list_alerts():
    return MonitoringService.get_dashboard_snapshot().get("alerts", [])
