from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base


class Battery(Base):
    """Battery energy storage system model."""
    
    __tablename__ = "batteries"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(String, ForeignKey("renewable_assets.asset_id"), unique=True, nullable=False)
    capacity_mwh = Column(Float, nullable=False)  # Total capacity in MWh
    current_soc_percent = Column(Float, default=0.0)  # State of charge percentage
    min_soc_percent = Column(Float, default=20.0)  # Minimum allowed SoC
    max_soc_percent = Column(Float, default=90.0)  # Maximum allowed SoC
    max_charge_power_mw = Column(Float, nullable=False)  # Maximum charge rate in MW
    max_discharge_power_mw = Column(Float, nullable=False)  # Maximum discharge rate in MW
    efficiency_percent = Column(Float, default=90.0)  # Round-trip efficiency
    availability = Column(Boolean, default=True)
    charge_discharge_status = Column(String, default="idle")  # charging, discharging, idle
    cycle_count = Column(Integer, default=0)
    last_maintenance_date = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    asset = relationship("RenewableAsset", backref="battery")
    
    @property
    def stored_energy_mwh(self) -> float:
        """Calculate stored energy based on SoC."""
        return self.capacity_mwh * (self.current_soc_percent / 100.0)
    
    @property
    def available_storage_mwh(self) -> float:
        """Calculate available storage capacity."""
        max_stored = self.capacity_mwh * (self.max_soc_percent / 100.0)
        return max_stored - self.stored_energy_mwh
    
    @property
    def available_discharge_mwh(self) -> float:
        """Calculate available discharge capacity."""
        current_stored = self.stored_energy_mwh
        min_stored = self.capacity_mwh * (self.min_soc_percent / 100.0)
        return current_stored - min_stored
    
    def __repr__(self):
        return f"<Battery {self.asset_id}: {self.current_soc_percent}% SoC, {self.stored_energy_mwh:.2f} MWh>"
