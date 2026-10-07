from fastapi import APIRouter, Query

from app.services.anomaly_service import AnomalyService

router = APIRouter()


@router.get("/detect")
async def detect_anomalies(values: list[float] = Query(default_factory=list)):
    return AnomalyService.detect(values)
