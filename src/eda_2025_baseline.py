"""2025 baseline figures from public, aggregated operating counts."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from charting import BLUE, GRAY, NAVY, TEAL, finish, set_korean_font
from metrics import DEFAULT_DATA, load_aggregates, monthly_frame


def build_baseline(payload: dict, output: str | Path) -> dict:
    monthly = monthly_frame(payload, 2025)
    residence = pd.DataFrame(payload["residence_2025_mar_oct"])
    q1_q4 = int(monthly["visitors"].sum())
    enrollments = int(monthly["enrollments"].sum())

    # Residence totals must match visits for the March–October interval.
    mar_oct = int(monthly.loc[monthly["month"].between(3, 10), "visitors"].sum())
    if int(residence["count"].sum()) != mar_oct:
        raise ValueError("Residence counts do not match March–October visit totals")

    set_korean_font()
    fig, axes = plt.subplots(2, 2, figsize=(13.8, 8.2), dpi=170)
    months = monthly["month"].to_numpy()

    ax = axes[0, 0]
    ax.bar(months, monthly["visitors"], color=[GRAY] * 10 + [BLUE, NAVY])
    ax.set_xticks(months, [f"{m}월" for m in months])
    ax.set_title(f"월별 방문 기록 · 연간 {q1_q4:,}건", fontweight="bold", loc="left")
    finish(ax)

    ax = axes[0, 1]
    ax.plot(months, monthly["enrollments"], color=TEAL, marker="o")
    ax.set_xticks(months, [f"{m}월" for m in months])
    ax.set_title(f"월별 프로그램 수강 집계 · 연간 {enrollments:,}건", fontweight="bold", loc="left")
    finish(ax)

    ax = axes[1, 0]
    residence = residence.assign(pct=100 * residence["count"] / mar_oct).sort_values("count")
    ax.barh(residence["zone"], residence["pct"], color=[GRAY, "#DC2626", "#60A5FA", NAVY])
    ax.set_xlim(0, 81)
    for y, value in enumerate(residence["pct"]):
        ax.text(value + 0.6, y, f"{value:.1f}%", va="center", fontsize=9)
    ax.set_title(f"거주지 권역 분포 · 3–10월, n={mar_oct:,}", fontweight="bold", loc="left")
    ax.grid(axis="x", color="#E2E8F0", linestyle="--", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)

    ax = axes[1, 1]
    first_half = monthly.loc[monthly["month"].between(1, 6), "visitors"].sum()
    second_half = monthly.loc[monthly["month"].between(7, 12), "visitors"].sum()
    ax.bar(["상반기", "하반기"], [first_half, second_half], color=[GRAY, BLUE], width=0.52)
    for i, count in enumerate((first_half, second_half)):
        ax.text(i, count + 30, f"{int(count):,}", ha="center", fontweight="bold")
    ax.set_ylim(0, max(first_half, second_half) * 1.2)
    ax.set_title("상·하반기 방문 기록 비교", fontweight="bold", loc="left")
    finish(ax)

    fig.suptitle("김포시청년지원센터 | 2025년 운영 집계 기초 분석", fontsize=17, fontweight="bold")
    fig.text(0.5, 0.015, "출처: 제공된 운영 집계값 · 방문 수는 중복 방문을 포함할 수 있음", ha="center", fontsize=9, color="#475569")
    fig.tight_layout(rect=[0, 0.03, 1, 0.945], h_pad=2.2, w_pad=2.7)
    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    return {"annual_visits": q1_q4, "annual_enrollments": enrollments, "residence_sample": mar_oct}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=Path("outputs/2025_baseline_eda.png"))
    args = parser.parse_args()
    totals = build_baseline(load_aggregates(args.data), args.output)
    print(f"Saved {args.output} | {totals}")


if __name__ == "__main__":
    main()
