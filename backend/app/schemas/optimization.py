from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class OptimizationScheduleItem(BaseModel):
    """Single time slot in optimization schedule."""
    timestamp: datetime
    charge_mw: float = Field(..., description="Charge power in MW (negative for discharge)")
    soc_percent: float = Field(..., description="State of charge percentage")


class OptimizationResult(BaseModel):
    """Optimization result schema."""
    objective_value: float
    schedule: List[OptimizationScheduleItem]
    constraints_satisfied: bool
    solver_status: str


class OptimizationRunBase(BaseModel):
    """Base schema for optimization run."""
    workflow_id: str = Field(..., description="Associated workflow ID")
    objective_function: str = Field(..., description="Objective function used")
    optimization_horizon_hours: int = Field(..., gt=0, description="Optimization horizon in hours")
    result: OptimizationResult


class OptimizationRunCreate(OptimizationRunBase):
    """Schema for creating an optimization run."""
    pass


class OptimizationRun(OptimizationRunBase):
    """Schema for optimization run response."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
