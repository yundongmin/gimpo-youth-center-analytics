"""Same-month 2025–2026 comparisons, with period-qualified rates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from charting import BLUE, GRAY, NAVY, TEAL, finish, set_korean_font
from metrics import DEFAULT_DATA, kpi_summary, load_aggregates, monthly_frame


def build_kpi_report(payload: dict, output: str | Path) -> dict:
    y25 = monthly_frame(payload, 2025).set_index("month").loc[1:6]
    y26 = monthly_frame(payload, 2026).set_index("month").loc[1:6]
    report = kpi_summary(payload)
    set_korean_font()

    fig, axes = plt.subplots(2, 2, figsize=(13.8, 8.2), dpi=170)
    labels = [f"{n}월" for n in range(1, 7)]
    xpos = np.arange(6)

    for ax, field, title in (
        (axes[0, 0], "visitors", "방문 기록 비교 (2025 vs 2026)"),
        (axes[0, 1], "enrollments", "프로그램 수강 집계 비교 (2025 vs 2026)"),
    ):
        ax.bar(xpos - 0.19, y25[field], width=0.38, color=GRAY, label="2025")
        ax.bar(xpos + 0.19, y26[field], width=0.38, color=BLUE, label="2026")
        ax.set_xticks(xpos, labels)
        ax.set_title(title, fontweight="bold", loc="left")
        ax.legend(frameon=False)
        finish(ax)

    ax = axes[1, 0]
    period_keys = [("1–5월 방문", "jan_may", "visitors"), ("1–5월 수강", "jan_may", "enrollments"),
                   ("3–6월 방문", "mar_jun", "visitors"), ("3–6월 수강", "mar_jun", "enrollments")]
    bars = [report[period][metric]["ratio"] for _, period, metric in period_keys]
    ypos = np.arange(4)
    ax.barh(ypos, bars, color=[NAVY, BLUE, TEAL, "#38BDF8"])
    ax.set_yticks(ypos, [row[0] for row in period_keys])
    ax.invert_yaxis()
    ax.set_xlim(0, 2.9)
    ax.axvline(1, color=GRAY, linestyle="--", linewidth=1)
    for i, value in enumerate(bars):
        ax.text(value + 0.05, i, f"{value:.2f}배", va="center", fontweight="bold")
    ax.set_title("동일 월 기준 전년 대비 배율", fontweight="bold", loc="left")
    ax.grid(axis="x", color="#E2E8F0", linestyle="--", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)

    ax = axes[1, 1]
    ax.axis("off")
    rate_25 = report["reported_rates"]["2025_completion"]
    rate_26 = report["reported_rates"]["2026_completion"]
    ax.text(0.03, 0.91, "보고된 강좌 이수율 (참고 지표)", fontsize=13, fontweight="bold", transform=ax.transAxes)
    ax.text(0.06, 0.71, f"2025 연간    {rate_25['percent']}%", fontsize=19, color=NAVY, transform=ax.transAxes)
    ax.text(0.06, 0.51, f"2026 1–5월   {rate_26['percent']}%", fontsize=19, color=TEAL, transform=ax.transAxes)
    ax.text(0.06, 0.28, "집계 기간과 모집단이 달라 동일 조건 비교 아님", fontsize=11, transform=ax.transAxes, color="#B45309")
    ax.text(0.06, 0.17, "동일한 출석·수료 산식 및 대상자 기준 확인 필요", fontsize=10, transform=ax.transAxes, color="#64748B")

    fig.suptitle("김포시청년지원센터 | 2025–2026 동월 비교", fontsize=17, fontweight="bold")
    fig.text(0.5, 0.014, "출처: 제공된 월별 집계값 · 단순 전년 비교로 운영 개편의 인과효과를 검증하지 않음", ha="center", fontsize=9, color="#475569")
    fig.tight_layout(rect=[0, 0.03, 1, 0.945], h_pad=2.2, w_pad=2.7)
    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    metrics_path = out_path.with_suffix(".json")
    metrics_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--output", type=Path, default=Path("outputs/2026_kpi_comparison.png"))
    args = parser.parse_args()
    report = build_kpi_report(load_aggregates(args.data), args.output)
    print(f"Saved {args.output} | Jan–May visits: {report['jan_may']['visitors']['ratio']:.2f}x")


if __name__ == "__main__":
    main()
