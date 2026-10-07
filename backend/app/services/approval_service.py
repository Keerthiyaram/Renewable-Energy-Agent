from __future__ import annotations

from typing import Any


class ApprovalService:
    @staticmethod
    def create_request(*, workflow_id: str, recommendation: str, operator: str = "system") -> dict[str, Any]:
        return {
            "approval_id": f"APP-{workflow_id}",
            "workflow_id": workflow_id,
            "status": "PENDING_REVIEW",
            "recommendation": recommendation,
            "operator": operator,
            "requires_human_approval": True,
        }

    @staticmethod
    def update_request(approval_id: str, *, approved: bool, comment: str = "") -> dict[str, Any]:
        return {
            "approval_id": approval_id,
            "status": "APPROVED" if approved else "REJECTED",
            "comment": comment,
            "requires_human_approval": True,
        }
