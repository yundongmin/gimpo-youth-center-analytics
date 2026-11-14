"""Aggregate loading and like-for-like operating metrics."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


DEFAULT_DATA = Path(__file__).resolve().parents[1] / "data" / "aggregates.json"


def load_aggregates(path: str | Path = DEFAULT_DATA) -> dict:
    with Path(path).open(encoding="utf-8") as handle:
        payload = json.load(handle)

    monthly = payload["monthly"]
    for year, rows in monthly.items():
        frame = pd.DataFrame(rows)
        if not {"month", "visitors", "enrollments"}.issubset(frame):
            raise ValueError(f"Missing monthly columns for {year}")
        if frame["month"].duplicated().any() or not frame["month"].is_monotonic_increasing:
            raise ValueError(f"Duplicate or unordered month in {year}")
        if frame["month"].tolist() != list(range(1, len(frame) + 1)):
            raise ValueError(f"Months must form a sequence from January: {year}")
        if frame[["visitors", "enrollments"]].isna().any().any():
            raise ValueError(f"Missing counts in {year}")
        if (frame[["visitors", "enrollments"]].lt(0)).any().any():
            raise ValueError(f"Negative counts in {year}")
        if not all(pd.api.types.is_integer_dtype(frame[col]) for col in ("visitors", "enrollments")):
            raise ValueError(f"Counts must be integers: {year}")

    residence = pd.DataFrame(payload["residence_2025_mar_oct"])
    if (residence["count"] < 0).any():
        raise ValueError("Negative residence counts")
    return payload


def monthly_frame(payload: dict, year: int) -> pd.DataFrame:
    return pd.DataFrame(payload["monthly"][str(year)]).copy()


def compare_periods(payload: dict, *, months: tuple[int, ...]) -> dict:
    """Compare identical calendar months; never mix annual and interim rates."""
    years = {year: monthly_frame(payload, year).set_index("month") for year in (2025, 2026)}
    missing = [month for year, df in years.items() for month in months if month not in df.index]
    if missing:
        raise ValueError(f"Unavailable comparison months: {sorted(set(missing))}")

    result = {"period": f"{min(months):02d}-{max(months):02d}"}
    for metric in ("visitors", "enrollments"):
        baseline = int(years[2025].loc[list(months), metric].sum())
        current = int(years[2026].loc[list(months), metric].sum())
        result[metric] = {
            "2025": baseline,
            "2026": current,
            "ratio": round(current / baseline, 4) if baseline else None,
        }
    return result


def kpi_summary(payload: dict) -> dict:
    return {
        "jan_may": compare_periods(payload, months=(1, 2, 3, 4, 5)),
        "mar_jun": compare_periods(payload, months=(3, 4, 5, 6)),
        "reported_rates": payload["reported_rates"],
        "note": "Only monthly counts are recomputed. Reported rates use different periods and are not causal evidence.",
    }
