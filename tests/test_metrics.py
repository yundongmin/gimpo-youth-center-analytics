import copy

import pytest

from metrics import compare_periods, kpi_summary, load_aggregates, monthly_frame


def test_2025_totals() -> None:
    payload = load_aggregates()
    annual = monthly_frame(payload, 2025)
    assert annual["visitors"].sum() == 5403
    assert annual["enrollments"].sum() == 1620
    assert annual.loc[annual["month"].between(3, 10), "visitors"].sum() == 3939


def test_comparable_months() -> None:
    summary = kpi_summary(load_aggregates())
    assert summary["jan_may"]["visitors"]["2025"] == 1420
    assert summary["jan_may"]["visitors"]["2026"] == 3315
    assert summary["jan_may"]["enrollments"]["2025"] == 594
    assert summary["jan_may"]["enrollments"]["2026"] == 1220
    assert summary["mar_jun"]["visitors"]["2025"] == 1690
    assert summary["mar_jun"]["visitors"]["2026"] == 2827
    assert summary["mar_jun"]["enrollments"]["2025"] == 661
    assert summary["mar_jun"]["enrollments"]["2026"] == 920
    assert summary["jan_may"]["visitors"]["ratio"] == pytest.approx(2.3345)
    assert summary["mar_jun"]["visitors"]["ratio"] == pytest.approx(1.6728)


def test_missing_month_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unavailable"):
        compare_periods(load_aggregates(), months=(7,))


def test_duplicate_month_is_rejected(tmp_path) -> None:
    payload = copy.deepcopy(load_aggregates())
    payload["monthly"]["2025"][1]["month"] = 1
    import json
    path = tmp_path / "wrong.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="Duplicate"):
        load_aggregates(path)
