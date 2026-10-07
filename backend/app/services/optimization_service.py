from __future__ import annotations

from typing import Any

import pulp


class OptimizationService:
    @staticmethod
    def optimize_battery_schedule(
        *,
        renewable_surplus_mw: float,
        hours: int = 6,
        capacity_mwh: float = 8.0,
        max_charge_mw: float = 2.0,
        max_discharge_mw: float = 2.0,
        min_soc_percent: float = 20.0,
        max_soc_percent: float = 90.0,
        start_soc_percent: float = 45.0,
        efficiency: float = 0.9,
    ) -> dict[str, Any]:
        problem = pulp.LpProblem("battery_dispatch", pulp.LpMaximize)
        charge = pulp.LpVariable.dicts("charge", range(hours), lowBound=0)
        discharge = pulp.LpVariable.dicts("discharge", range(hours), lowBound=0)
        soc = pulp.LpVariable.dicts("soc", range(hours + 1), lowBound=min_soc_percent, upBound=max_soc_percent)
        soc[0].setInitialValue(start_soc_percent)

        for t in range(hours):
            problem += charge[t] <= max_charge_mw
            problem += discharge[t] <= max_discharge_mw
            problem += soc[t + 1] == soc[t] + charge[t] * efficiency - discharge[t] / efficiency
            problem += soc[t + 1] <= max_soc_percent
            problem += soc[t + 1] >= min_soc_percent

        if renewable_surplus_mw >= 0:
            for t in range(hours):
                problem += charge[t] <= renewable_surplus_mw
        else:
            for t in range(hours):
                problem += discharge[t] <= abs(renewable_surplus_mw)

        problem += pulp.lpSum(charge[t] for t in range(hours)) - 0.5 * pulp.lpSum(discharge[t] for t in range(hours))
        result = problem.solve(pulp.PULP_CBC_CMD(msg=False))

        schedule = []
        for t in range(hours):
            schedule.append({
                "hour": t,
                "charge_mw": round(float(charge[t].value() or 0.0), 4),
                "discharge_mw": round(float(discharge[t].value() or 0.0), 4),
                "soc_percent": round(float(soc[t + 1].value() or start_soc_percent), 4),
            })

        return {
            "objective_value": round(float(pulp.value(problem.objective) or 0.0), 4),
            "schedule": schedule,
            "constraints_satisfied": bool(pulp.LpStatus[problem.status] == "Optimal"),
            "capacity_mwh": capacity_mwh,
            "final_soc_percent": round(float(soc[hours].value() or start_soc_percent), 4),
            "status": pulp.LpStatus[problem.status],
        }
