from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from app.services.approval_service import ApprovalService

router = APIRouter()


class ApprovalRequest(BaseModel):
    workflow_id: str = Field(...)
    recommendation: str = Field(default="Battery charging window recommended.")
    operator: str = Field(default="operator")


@router.post("/request")
async def request_approval(payload: ApprovalRequest):
    return ApprovalService.create_request(workflow_id=payload.workflow_id, recommendation=payload.recommendation, operator=payload.operator)


@router.post("/{approval_id}/review")
async def review_approval(approval_id: str, approved: bool = Query(default=True), comment: str = Query(default="")):
    return ApprovalService.update_request(approval_id, approved=approved, comment=comment)
