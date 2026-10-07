from __future__ import annotations

import pulp


class BatteryOptimizer:
    def optimize(self, renewable_surplus_mw: float, capacity_mwh: float = 8.0, max_power_mw: float = 2.0):
        problem = pulp.LpProblem("battery_dispatch", pulp.LpMaximize)
        charge = pulp.LpVariable("charge", lowBound=0, upBound=min(max_power_mw, max(0.0, renewable_surplus_mw)))
        discharge = pulp.LpVariable("discharge", lowBound=0, upBound=max_power_mw)
        objective = charge - 0.5 * discharge
        problem += objective
        problem += charge <= max_power_mw
        problem += discharge <= max_power_mw
        problem.solve(pulp.PULP_CBC_CMD(msg=False))
        return {
            "objective_value": round(float(pulp.value(problem.objective) or 0.0), 4),
            "charge_mw": round(float(charge.value() or 0.0), 4),
            "discharge_mw": round(float(discharge.value() or 0.0), 4),
            "constraints_satisfied": pulp.LpStatus[problem.status] == "Optimal",
        }
