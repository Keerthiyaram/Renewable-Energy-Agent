from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pulp


@dataclass
class BatteryStatus:
    capacity_mwh: float = 8.0
    current_soc_percent: float = 45.0
    min_soc_percent: float = 20.0
    max_soc_percent: float = 90.0
    max_charge_power_mw: float = 2.0
    max_discharge_power_mw: float = 2.0
    efficiency_percent: float = 90.0
    availability: bool = True
    charge_discharge_status: str = "idle"
    stored_energy_mwh: float = 3.6

    @property
    def available_energy_mwh(self) -> float:
        return self.capacity_mwh * (self.current_soc_percent / 100.0)


class BatteryService:
    """Battery optimization and state management using deterministic linear programming."""

    @staticmethod
    def get_status(renewable_surplus_mw: float = 1.5, demand_mw: float = 8.0) -> dict[str, Any]:
        soc = min(90.0, max(20.0, 45.0 + renewable_surplus_mw * 4.5))
        status = "idle"
        if renewable_surplus_mw > 0.2:
            status = "charging"
        elif renewable_surplus_mw < -0.2:
            status = "discharging"
        return {
            "capacity_mwh": 8.0,
            "current_soc_percent": round(soc, 2),
            "min_soc_percent": 20.0,
            "max_soc_percent": 90.0,
            "max_charge_power_mw": 2.0,
            "max_discharge_power_mw": 2.0,
            "efficiency_percent": 90.0,
            "availability": True,
            "charge_discharge_status": status,
            "stored_energy_mwh": round(8.0 * (soc / 100.0), 2),
            "renewable_surplus_mw": renewable_surplus_mw,
            "demand_mw": demand_mw,
        }

    @staticmethod
    def optimize_schedule(renewable_surplus_mw: float, hours: int = 6) -> dict[str, Any]:
        capacity_mwh = 8.0
        max_soc = 90.0
        min_soc = 20.0
        starting_soc = 45.0
        efficiency = 0.9

        problem = pulp.LpProblem("battery_dispatch", pulp.LpMaximize)
        charge = pulp.LpVariable.dicts("charge", range(hours), lowBound=0)
        discharge = pulp.LpVariable.dicts("discharge", range(hours), lowBound=0)
        soc = pulp.LpVariable.dicts("soc", range(hours + 1), lowBound=min_soc, upBound=max_soc)

        for t in range(hours):
            problem += charge[t] <= 2.0
            problem += discharge[t] <= 2.0
            problem += soc[t + 1] == soc[t] + (charge[t] * efficiency) - (discharge[t] / efficiency)
            problem += soc[t + 1] <= max_soc
            problem += soc[t + 1] >= min_soc

        problem += pulp.lpSum(charge[t] * 1.0 for t in range(hours)) + pulp.lpSum(discharge[t] * 0.5 for t in range(hours))
        soc[0].setInitialValue(starting_soc)
        if renewable_surplus_mw > 0:
            for t in range(hours):
                problem += charge[t] <= max(0.0, renewable_surplus_mw)
        else:
            for t in range(hours):
                problem += discharge[t] <= max(0.0, -renewable_surplus_mw)

        problem.solve(pulp.PULP_CBC_CMD(msg=False))
        schedule = []
        for t in range(hours):
            schedule.append({
                "hour": t,
                "charge_mw": round(float(charge[t].value() or 0.0), 4),
                "discharge_mw": round(float(discharge[t].value() or 0.0), 4),
                "soc_percent": round(float(soc[t + 1].value() or starting_soc), 4),
            })
        return {
            "objective_value": round(float(pulp.value(problem.objective) or 0.0), 4),
            "schedule": schedule,
            "constraints_satisfied": bool(pulp.LpStatus[problem.status] == "Optimal"),
            "battery_capacity_mwh": capacity_mwh,
            "starting_soc_percent": starting_soc,
            "final_soc_percent": round(float(soc[hours].value() or starting_soc), 4),
        }
