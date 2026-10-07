from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base


class EnergyMeasurement(Base):
    """Energy measurement model for renewable assets."""
    
    __tablename__ = "energy_measurements"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(String, ForeignKey("renewable_assets.asset_id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    generation_mw = Column(Float)
    voltage_kv = Column(Float)
    current_ka = Column(Float)
    power_mw = Column(Float)
    energy_mwh = Column(Float)
    asset_status = Column(String)
    measurement_type = Column(String, default="generation")  # generation, consumption, storage
    source = Column(String, default="api")  # api, csv, scada, simulated
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    asset = relationship("RenewableAsset", backref="measurements")
    
    def __repr__(self):
        return f"<EnergyMeasurement {self.asset_id} at {self.timestamp}: {self.generation_mw} MW>"
