from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ApprovalRequestBase(BaseModel):
    """Base schema for approval request."""
    workflow_id: str = Field(..., description="Associated workflow ID")
    recommendation_type: str = Field(..., description="Type of recommendation")
    recommendation_data: str = Field(..., description="Recommendation data as JSON")
    status: str = Field("pending_review", description="Approval status")
    reviewer_comments: Optional[str] = Field(None, description="Reviewer comments")


class ApprovalRequestCreate(ApprovalRequestBase):
    """Schema for creating an approval request."""
    pass


class ApprovalRequestUpdate(BaseModel):
    """Schema for updating an approval request."""
    status: str = Field(..., description="New status: approved, rejected, recalculation_requested")
    reviewer_comments: Optional[str] = Field(None, description="Reviewer comments")


class ApprovalRequest(ApprovalRequestBase):
    """Schema for approval request response."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
