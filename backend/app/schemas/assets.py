from pydantic import BaseModel, Field, validator
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from datetime import datetime


class RenewableAssetBase(BaseModel):
    """Base schema for renewable asset."""
    asset_id: str = Field(..., description="Unique asset identifier")
    name: str = Field(..., description="Asset name")
    asset_type: str = Field(..., description="Asset type: solar, wind, or battery")
    installed_capacity_mw: float = Field(..., gt=0, description="Installed capacity in MW")
    location: Optional[str] = Field(None, description="Asset location")
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Longitude coordinate")
    operational_status: str = Field("operational", description="Operational status")
    commissioning_date: Optional[datetime] = Field(None, description="Commissioning date")
    configuration: Optional[str] = Field(None, description="Additional configuration as JSON")
    
    @field_validator("asset_type")
    @classmethod
    def validate_asset_type(cls, value: str) -> str:
        valid_types = ['solar', 'wind', 'battery']
        if value.lower() not in valid_types:
            raise ValueError(f"asset_type must be one of {valid_types}")
        return value.lower()
    
    @field_validator("operational_status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        valid_statuses = ['operational', 'maintenance', 'offline']
        if value.lower() not in valid_statuses:
            raise ValueError(f"operational_status must be one of {valid_statuses}")
        return value.lower()


class RenewableAssetCreate(RenewableAssetBase):
    """Schema for creating a renewable asset."""


class RenewableAssetUpdate(BaseModel):
    """Schema for updating a renewable asset."""
    name: Optional[str] = None
    installed_capacity_mw: Optional[float] = Field(None, gt=0)
    location: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    operational_status: Optional[str] = None
    commissioning_date: Optional[datetime] = None
    configuration: Optional[str] = None
    
    @field_validator("operational_status")
    @classmethod
    def validate_status(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            valid_statuses = ['operational', 'maintenance', 'offline']
            if value.lower() not in valid_statuses:
                raise ValueError(f"operational_status must be one of {valid_statuses}")
            return value.lower()
        return value


class RenewableAsset(RenewableAssetBase):
    """Schema for renewable asset response."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
