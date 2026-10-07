from datetime import datetime, timezone

import pytest

from scripts.generate_synthetic_data import generate_rows


def test_generation_is_reproducible_and_within_physical_limits():
    start = datetime(2025, 1, 1, tzinfo=timezone.utc)

    first_run = list(generate_rows(start, 48))
    second_run = list(generate_rows(start, 48))

    assert first_run == second_run
    assert all(0 <= row["solar_generation_mw"] <= 10 for row in first_run)
    assert all(0 <= row["wind_generation_mw"] <= 6 for row in first_run)
    assert all(20 <= row["battery_soc_percent"] <= 90 for row in first_run)
    assert first_run[12]["solar_generation_mw"] > first_run[0]["solar_generation_mw"]
    assert all(row["demand_mw"] > 0 for row in first_run)


@pytest.mark.parametrize(
    ("start", "hours", "message"),
    [
        (datetime(2025, 1, 1), 1, "timezone-aware"),
        (datetime(2025, 1, 1, tzinfo=timezone.utc), 0, "at least 1"),
    ],
)
def test_rejects_invalid_generation_arguments(start, hours, message):
    with pytest.raises(ValueError, match=message):
        list(generate_rows(start, hours))