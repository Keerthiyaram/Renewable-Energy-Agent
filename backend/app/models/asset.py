from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from app.database.database import Base


class RenewableAsset(Base):
    """Renewable energy asset model."""
    
    __tablename__ = "renewable_assets"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    asset_type = Column(String, nullable=False)  # solar, wind, battery
    installed_capacity_mw = Column(Float, nullable=False)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    operational_status = Column(String, default="operational")  # operational, maintenance, offline
    commissioning_date = Column(DateTime)
    configuration = Column(String)  # JSON string for additional config
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<RenewableAsset {self.asset_id} - {self.name} ({self.asset_type})>"
