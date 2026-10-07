from pydantic import BaseModel, Field, validator
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from typing import Optional
from datetime import datetime


class BatteryBase(BaseModel):
    """Base schema for battery."""
    asset_id: str = Field(..., description="Associated asset ID")
    capacity_mwh: float = Field(..., gt=0, description="Total capacity in MWh")
    current_soc_percent: float = Field(0.0, ge=0, le=100, description="State of charge percentage")
    min_soc_percent: float = Field(20.0, ge=0, le=100, description="Minimum allowed SoC")
    max_soc_percent: float = Field(90.0, ge=0, le=100, description="Maximum allowed SoC")
    max_charge_power_mw: float = Field(..., gt=0, description="Maximum charge rate in MW")
    max_discharge_power_mw: float = Field(..., gt=0, description="Maximum discharge rate in MW")
    efficiency_percent: float = Field(90.0, ge=0, le=100, description="Round-trip efficiency")
    availability: bool = Field(True, description="Battery availability")
    charge_discharge_status: str = Field("idle", description="Current status: charging, discharging, idle")
    cycle_count: int = Field(0, ge=0, description="Cycle count")
    last_maintenance_date: Optional[datetime] = Field(None, description="Last maintenance date")
    
    @model_validator(mode="after")
    def validate_soc_limits(self):
        if self.min_soc_percent >= self.max_soc_percent:
            raise ValueError("max_soc_percent must be greater than min_soc_percent")
        if not self.min_soc_percent <= self.current_soc_percent <= self.max_soc_percent:
            raise ValueError("current_soc_percent must be within the configured SoC limits")
        return self
    
    @field_validator("charge_discharge_status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        valid_statuses = ['charging', 'discharging', 'idle']
        if value.lower() not in valid_statuses:
            raise ValueError(f"charge_discharge_status must be one of {valid_statuses}")
        return value.lower()


class BatteryCreate(BatteryBase):
    """Schema for creating a battery."""


class BatteryUpdate(BaseModel):
    """Schema for updating a battery."""
    current_soc_percent: Optional[float] = Field(None, ge=0, le=100)
    availability: Optional[bool] = None
    charge_discharge_status: Optional[str] = None
    cycle_count: Optional[int] = Field(None, ge=0)
    last_maintenance_date: Optional[datetime] = None
    
    @field_validator("charge_discharge_status")
    @classmethod
    def validate_status(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            valid_statuses = ['charging', 'discharging', 'idle']
            if value.lower() not in valid_statuses:
                raise ValueError(f"charge_discharge_status must be one of {valid_statuses}")
            return value.lower()
        return value


class Battery(BatteryBase):
    """Schema for battery response."""
    id: int
    stored_energy_mwh: float
    available_storage_mwh: float
    available_discharge_mwh: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
