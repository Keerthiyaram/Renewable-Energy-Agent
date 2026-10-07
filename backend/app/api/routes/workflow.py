from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.workflow_service import WorkflowService

router = APIRouter()


class ReplanRequest(BaseModel):
    event_type: str = Field(default="weather_change")
    details: dict = Field(default_factory=dict)


@router.post("/replan")
async def trigger_replan(request: ReplanRequest):
    return WorkflowService.trigger_replan(request.event_type, request.details)


@router.post("/{workflow_id}/approve")
async def approve_workflow(workflow_id: str, approved: bool = True, comment: str = ""):
    return WorkflowService.approve_workflow(workflow_id, approved, comment)
