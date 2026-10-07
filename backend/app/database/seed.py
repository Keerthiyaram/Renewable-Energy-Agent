"""Database seed script for initial data."""
import csv
from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session
from app.database.database import SessionLocal, init_db
from app.models.asset import RenewableAsset
from app.models.battery import Battery
from app.models.energy_measurement import EnergyMeasurement


def seed_database():
    """Seed assets, battery configuration, and generated solar/wind history."""
    init_db()
    db = SessionLocal()

    try:
        asset_specs = (
            ("SOLAR-001", "Main Solar PV Plant", "solar", 10.0, "Solar Farm Site A", 37.7749, -122.4194, datetime(2023, 1, 1)),
            ("WIND-001", "Coastal Wind Farm", "wind", 6.0, "Coastal Site B", 37.7849, -122.4094, datetime(2023, 3, 1)),
            ("BATTERY-001", "Grid Battery Storage", "battery", 2.0, "Substation C", 37.7649, -122.4294, datetime(2023, 6, 1)),
        )
        assets = {asset.asset_id: asset for asset in db.query(RenewableAsset).all()}
        for asset_id, name, asset_type, capacity, location, latitude, longitude, commissioned in asset_specs:
            if asset_id not in assets:
                asset = RenewableAsset(
                    asset_id=asset_id,
                    name=name,
                    asset_type=asset_type,
                    installed_capacity_mw=capacity,
                    location=location,
                    latitude=latitude,
                    longitude=longitude,
                    operational_status="operational",
                    commissioning_date=commissioned,
                )
                db.add(asset)
                assets[asset_id] = asset

        db.flush()
        battery = db.query(Battery).filter(Battery.asset_id == "BATTERY-001").first()
        if battery is None:
            battery = Battery(
                asset_id="BATTERY-001",
                capacity_mwh=8.0,
                current_soc_percent=45.0,
                min_soc_percent=20.0,
                max_soc_percent=90.0,
                max_charge_power_mw=2.0,
                max_discharge_power_mw=2.0,
                efficiency_percent=90.0,
                availability=True,
                charge_discharge_status="idle",
                cycle_count=150,
            )
            db.add(battery)

        sample_path = Path(__file__).resolve().parents[2] / "data" / "sample" / "renewable_energy_hourly.csv"
        existing_measurements = db.query(EnergyMeasurement).filter(EnergyMeasurement.source == "simulated").count()
        measurement_count = 0
        if existing_measurements == 0:
            with sample_path.open(newline="", encoding="utf-8") as sample_file:
                for row in csv.DictReader(sample_file):
                    timestamp = datetime.fromisoformat(row["timestamp"])
                    db.add_all(
                        [
                            EnergyMeasurement(
                                asset_id="SOLAR-001",
                                timestamp=timestamp,
                                generation_mw=float(row["solar_generation_mw"]),
                                power_mw=float(row["solar_generation_mw"]),
                                energy_mwh=float(row["solar_generation_mw"]),
                                asset_status="operational",
                                measurement_type="generation",
                                source="simulated",
                            ),
                            EnergyMeasurement(
                                asset_id="WIND-001",
                                timestamp=timestamp,
                                generation_mw=float(row["wind_generation_mw"]),
                                power_mw=float(row["wind_generation_mw"]),
                                energy_mwh=float(row["wind_generation_mw"]),
                                asset_status="operational",
                                measurement_type="generation",
                                source="simulated",
                            ),
                        ]
                    )
                    measurement_count += 2
                    if measurement_count % 1000 == 0:
                        db.flush()

        db.commit()
        print("Database seed complete: 3 assets, battery configuration, and "
              f"{measurement_count} generated measurements added.")
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
