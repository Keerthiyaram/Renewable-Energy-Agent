from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class GenerationForecastBase(BaseModel):
    """Base schema for generation forecast."""
    asset_id: str = Field(..., description="Asset identifier")
    forecast_time: datetime = Field(..., description="Forecast timestamp")
    predicted_generation_mw: float = Field(..., ge=0, description="Predicted generation in MW")
    model_name: str = Field(..., description="Forecasting model name")
    confidence: Optional[float] = Field(None, ge=0, le=1, description="Confidence score")
    features_used: Optional[List[str]] = Field(None, description="Features used in forecast")


class GenerationForecastCreate(GenerationForecastBase):
    """Schema for creating a generation forecast."""
    pass


class GenerationForecast(GenerationForecastBase):
    """Schema for generation forecast response."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class DemandForecastBase(BaseModel):
    """Base schema for demand forecast."""
    forecast_time: datetime = Field(..., description="Forecast timestamp")
    predicted_demand_mw: float = Field(..., ge=0, description="Predicted demand in MW")
    model_name: str = Field(..., description="Forecasting model name")
    confidence: Optional[float] = Field(None, ge=0, le=1, description="Confidence score")


class DemandForecastCreate(DemandForecastBase):
    """Schema for creating a demand forecast."""
    pass


class DemandForecast(DemandForecastBase):
    """Schema for demand forecast response."""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
