"""Private attendance-log preparation; missing check-outs are not inferred."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

# Explicit allowlist prevents additional columns (including free-text PII) from leaking.
REQUIRED = {"check_in", "check_out", "purpose"}
OPTIONAL = {"site"}
UTILITY_PURPOSES = {"출력", "대여"}
# Open-text location labels are not exported. Add a known site only after schema review.
KNOWN_SITES = {"본원", "외곽", "하성", "통진", "고촌", "장기", "양촌", "운양", "구래"}


def clean_log(frame: pd.DataFrame, *, source_label: str = "workbook_001", short_visit_min: int = 5) -> pd.DataFrame:
    missing = REQUIRED - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    if short_visit_min < 0:
        raise ValueError("short_visit_min must be non-negative")

    # No names, personal identifiers, dates of birth, contact details, or notes are retained.
    fields = sorted(REQUIRED | (OPTIONAL & set(frame.columns)))
    result = frame.loc[:, fields].copy()
    result["source_batch"] = source_label
    result["source_row"] = np.arange(2, len(result) + 2)
    result["check_in"] = pd.to_datetime(result["check_in"], errors="coerce")
    result["check_out"] = pd.to_datetime(result["check_out"], errors="coerce")

    # Restrict open-ended purpose text to known categories. The original value is discarded.
    purpose = result["purpose"].fillna("").astype(str).str.strip()
    known_purposes = {"프로그램", "스터디", "대관", "출력", "대여", "상담", "기타"}
    result["purpose"] = purpose.where(purpose.isin(known_purposes), "기타")
    if "site" in result:
        site = result["site"].fillna("").astype(str).str.strip()
        result["site"] = site.where(site.isin(KNOWN_SITES), "기타")

    minutes = (result["check_out"] - result["check_in"]).dt.total_seconds() / 60
    missing_checkin = result["check_in"].isna()
    missing_checkout = result["check_out"].isna()
    reversed_times = minutes.lt(0)
    valid_duration = ~(missing_checkin | missing_checkout | reversed_times)
    result["observed_minutes"] = minutes.where(valid_duration).astype("Float64")

    conditions = [
        missing_checkin,
        missing_checkout,
        reversed_times,
        result["purpose"].isin(UTILITY_PURPOSES),
        result["observed_minutes"].lt(short_visit_min).fillna(False),
    ]
    outcomes = ["invalid_checkin", "missing_checkout", "invalid_time_order", "utility_visit", "short_visit"]
    result["visit_type"] = np.select(conditions, outcomes, default="regular_visit")
    return result


def prepare_workbooks(input_dir: Path, output_file: Path, *, short_visit_min: int = 5) -> dict:
    files = sorted(input_dir.glob("*.xlsx"))
    if not files:
        raise FileNotFoundError(f"No .xlsx workbooks found in {input_dir}")
    rows = []
    for index, path in enumerate(files, 1):
        frame = pd.read_excel(path, engine="openpyxl")
        rows.append(clean_log(frame, source_label=f"batch_{index:03d}", short_visit_min=short_visit_min))
    merged = pd.concat(rows, ignore_index=True)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(output_file, index=False, encoding="utf-8-sig")
    return {
        "total_rows": len(merged),
        "missing_checkout": int((merged["visit_type"] == "missing_checkout").sum()),
        "invalid_time_order": int((merged["visit_type"] == "invalid_time_order").sum()),
        "short_visits": int((merged["visit_type"] == "short_visit").sum()),
        "utility_visits": int((merged["visit_type"] == "utility_visit").sum()),
        "note": "Row-level output is private. Review schema and authority before any external use.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=Path("data/private"))
    parser.add_argument("--output", type=Path, default=Path("data/private/processed_logs.csv"))
    parser.add_argument("--short-visit-min", type=int, default=5)
    args = parser.parse_args()
    stats = prepare_workbooks(args.input_dir, args.output, short_visit_min=args.short_visit_min)
    print(f"Local preprocessing: {stats}")


if __name__ == "__main__":
    main()
