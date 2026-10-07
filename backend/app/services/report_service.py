from __future__ import annotations

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


class ReportService:
    @staticmethod
    def generate_dashboard_report(summary: dict) -> bytes:
        buffer = BytesIO()
        document = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        story.append(Paragraph("Renewable Energy Monitoring Report", style={"fontName": "Helvetica-Bold", "fontSize": 18}))
        story.append(Spacer(1, 18))
        metrics = [
            ["Metric", "Value"],
            ["Solar Generation (MW)", str(summary.get("current", {}).get("solar_generation_mw", 0))],
            ["Wind Generation (MW)", str(summary.get("current", {}).get("wind_generation_mw", 0))],
            ["Total Renewable (MW)", str(summary.get("current", {}).get("total_renewable_generation_mw", 0))],
            ["Demand (MW)", str(summary.get("current", {}).get("demand_mw", 0))],
            ["Balance (MW)", str(summary.get("current", {}).get("renewable_surplus_deficit_mw", 0))],
            ["Battery SoC (%)", str(summary.get("current", {}).get("battery_soc_percent", 0))],
        ]
        table = Table(metrics)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563eb")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 1, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        story.append(Paragraph("Operator recommendation: The system remains in decision-support mode and requires human approval before operational action.", style={"fontName": "Helvetica-Oblique", "fontSize": 10}))
        document.build(story)
        return buffer.getvalue()
