from pydantic import BaseModel, Field
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime


class EnergyMeasurementBase(BaseModel):
    """Base schema for energy measurement."""
    asset_id: str = Field(..., description="Asset identifier")
    timestamp: datetime = Field(..., description="Measurement timestamp")
    generation_mw: Optional[float] = Field(None, ge=0, description="Generation in MW")
    voltage_kv: Optional[float] = Field(None, ge=0, description="Voltage in kV")
    current_ka: Optional[float] = Field(None, ge=0, description="Current in kA")
    power_mw: Optional[float] = Field(None, description="Power in MW")
    energy_mwh: Optional[float] = Field(None, ge=0, description="Energy in MWh")
    asset_status: Optional[str] = Field(None, description="Asset status")
    measurement_type: str = Field("generation", description="Measurement type")
    source: str = Field("api", description="Data source")


class EnergyMeasurementCreate(EnergyMeasurementBase):
    """Schema for creating an energy measurement."""


class EnergyMeasurement(EnergyMeasurementBase):
    """Schema for energy measurement response."""
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
