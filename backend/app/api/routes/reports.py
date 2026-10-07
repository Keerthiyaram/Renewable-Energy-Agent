from fastapi import APIRouter
from fastapi.responses import Response

from app.services.monitoring_service import MonitoringService
from app.services.report_service import ReportService

router = APIRouter()


@router.get("/summary")
async def summary_report():
    payload = MonitoringService.get_dashboard_snapshot()
    pdf_bytes = ReportService.generate_dashboard_report(payload)
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=renewable-report.pdf"})
