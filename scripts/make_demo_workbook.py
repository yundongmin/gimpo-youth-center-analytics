"""Generate synthetic attendance rows for local preprocessing smoke tests."""

import argparse
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("data/private/demo_attendance.xlsx"))
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(
        {
            "user_name": ["TEST_PERSON_001", "TEST_PERSON_002", "TEST_PERSON_003", "TEST_PERSON_004", "TEST_PERSON_005"],
            "birth_date": ["1999-01-01"] * 5,
            "check_in": ["2026-03-04 11:00", "2026-03-04 14:15", "2026-03-04 19:15", "2026-03-05 09:10", "2026-03-05 10:10"],
            "check_out": ["2026-03-04 12:30", None, "2026-03-04 19:20", "2026-03-05 09:05", "2026-03-05 10:13"],
            "purpose": ["스터디", "상담", "출력", "프로그램", "대여"],
            "site": ["본원", "본원", "본원", "본원", "본원"],
            "contact": ["010-0000-0000"] * 5,
        }
    ).to_excel(args.output, index=False)
    print(f"Created synthetic workbook: {args.output}")


if __name__ == "__main__":
    main()
