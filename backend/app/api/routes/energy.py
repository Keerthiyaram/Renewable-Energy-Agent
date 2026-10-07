from fastapi import APIRouter, HTTPException, Query, UploadFile, File
from pydantic import BaseModel, Field

from app.services.energy_service import EnergyService
from app.services.upload_service import UploadService

router = APIRouter()


class BulkMeasurementRequest(BaseModel):
    rows: list[dict] = Field(default_factory=list)
    asset_type: str = "solar"
    capacity_mw: float = 10.0


@router.post("/ingest")
async def ingest_energy(request: BulkMeasurementRequest):
    return EnergyService.ingest_rows(request.rows, asset_type=request.asset_type, capacity_mw=request.capacity_mw)


@router.post("/upload")
async def upload_energy_file(
    file: UploadFile = File(...),
    asset_type: str = Query(default="solar"),
    capacity_mw: float = Query(default=10.0),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    file_bytes = await file.read()
    try:
        result = UploadService.process_upload(file_bytes, filename=file.filename, asset_type=asset_type, capacity_mw=capacity_mw)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/live")
async def get_live_state():
    return EnergyService.get_live_state()


@router.post("/validate")
async def validate_energy(
    asset_type: str = Query(default="solar"),
    capacity_mw: float = Query(default=10.0),
    generation_mw: float | None = Query(default=None),
    battery_soc_percent: float | None = Query(default=None),
    timestamp: str | None = Query(default=None),
):
    from app.services.validation_service import ValidationService

    return ValidationService.validate_measurement(
        asset_type=asset_type,
        capacity_mw=capacity_mw,
        generation_mw=generation_mw,
        soc_percent=battery_soc_percent,
        timestamp=timestamp,
    )
