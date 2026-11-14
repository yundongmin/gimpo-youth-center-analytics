from eda_2025_baseline import build_baseline
from evaluate_2026_kpi import build_kpi_report
from metrics import load_aggregates


def test_baseline_figure(tmp_path) -> None:
    path = tmp_path / "eda.png"
    values = build_baseline(load_aggregates(), path)
    assert path.is_file()
    assert values["annual_visits"] == 5403


def test_kpi_report(tmp_path) -> None:
    path = tmp_path / "kpi.png"
    report = build_kpi_report(load_aggregates(), path)
    assert path.is_file()
    assert path.with_suffix(".json").is_file()
    assert report["mar_jun"]["enrollments"]["ratio"] == 1.3918
