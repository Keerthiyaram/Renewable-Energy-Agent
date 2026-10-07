from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from app.database.database import SessionLocal
from app.models.workflow_run import WorkflowRun


class WorkflowService:
    @staticmethod
    def trigger_replan(event_type: str = "weather_change", details: dict[str, Any] | None = None) -> dict[str, Any]:
        workflow_id = f"workflow-{int(datetime.now(timezone.utc).timestamp())}"
        payload = {
            "state": "PENDING_REVIEW",
            "trigger_type": event_type,
            "trigger_details": details or {},
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        db = SessionLocal()
        try:
            run = WorkflowRun(
                workflow_id=workflow_id,
                status="completed",
                start_time=datetime.now(timezone.utc),
                end_time=datetime.now(timezone.utc),
                trigger_type=event_type,
                trigger_details=json.dumps(details or {}),
                input_state=json.dumps({"event_type": event_type, "details": details or {}}),
                output_state=json.dumps(payload),
            )
            db.add(run)
            db.commit()
            db.refresh(run)
        finally:
            db.close()
        return {
            "workflow_id": workflow_id,
            "status": "completed",
            "state": "PENDING_REVIEW",
            "trigger_type": event_type,
            "output_state": payload,
        }

    @staticmethod
    def approve_workflow(workflow_id: str, approved: bool = True, comment: str = "") -> dict[str, Any]:
        db = SessionLocal()
        try:
            run = db.query(WorkflowRun).filter(WorkflowRun.workflow_id == workflow_id).first()
            if not run:
                return {"workflow_id": workflow_id, "status": "not_found"}
            run.status = "completed" if approved else "rejected"
            run.output_state = json.dumps({"approved": approved, "comment": comment})
            db.commit()
            return {"workflow_id": workflow_id, "status": run.status, "approved": approved, "comment": comment}
        finally:
            db.close()
