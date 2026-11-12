import os
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False


def calc_yoy_metrics():
    df = pd.DataFrame({
        "month": ["1월", "2월", "3월", "4월", "5월", "6월"],
        "v_2025": [61, 109, 350, 484, 416, 440],
        "v_2026": [522, 653, 730, 660, 750, 687],
        "p_2025": [3, 103, 145, 177, 166, 173],
        "p_2026": [180, 240, 290, 255, 255, 120],
    })

    # 2025년 1~2월 초기 기록 미비 구간을 제외한 3~6월 정규 운영 실질 비교
    reg = df.iloc[2:6]
    eval_1_5 = df.iloc[:5]

    metrics = {
        "v_ratio_3_6": round(reg["v_2026"].sum() / reg["v_2025"].sum(), 2),       # 1.67배
        "p_ratio_3_6": round(reg["p_2026"].sum() / reg["p_2025"].sum(), 2),       # 1.39배
        "v_ratio_1_5": round(eval_1_5["v_2026"].sum() / eval_1_5["v_2025"].sum(), 2), # 2.33배
        "p_ratio_1_5": round(eval_1_5["p_2026"].sum() / eval_1_5["p_2025"].sum(), 2), # 2.05배
        "completion_diff": round(92.4 - 57.6, 1),                                 # +34.8%p
    }
    return df, metrics


def save_kpi_chart(df, metrics, out_file="outputs/2026_kpi_verification.png"):
    fig, axes = plt.subplots(2, 2, figsize=(14, 8.5), dpi=200)
    fig.patch.set_facecolor("white")
    fig.suptitle(
        "김포시청년지원센터 2025 vs 2026 상반기 핵심 성과 지표(KPI) 검증 (기관 평가 D -> B등급)",
        fontsize=13.5, fontweight="bold", y=0.97
    )

    x = range(len(df))
    w = 0.36

    # 1. 월별 방문자 비교
    ax1 = axes[0, 0]
    ax1.bar([i - w / 2 for i in x], df["v_2025"], width=w, color="#CBD5E1", label="2025년")
    ax1.bar([i + w / 2 for i in x], df["v_2026"], width=w, color="#2563EB", label="2026년")
    ax1.axvspan(1.5, 5.5, color="#EFF6FF", alpha=0.55, zorder=0)
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(df["month"])
    ax1.set_title(f"1. 월별 방문자 비교 (3~6월 실질 {metrics['v_ratio_3_6']}배 · 1~5월 {metrics['v_ratio_1_5']}배)", fontsize=10.5, fontweight="bold", loc="left")
    ax1.legend(frameon=False, fontsize=9)
    ax1.grid(axis="y", linestyle="--", alpha=0.35)

    # 2. 월별 프로그램 수강 비교
    ax2 = axes[0, 1]
    ax2.bar([i - w / 2 for i in x], df["p_2025"], width=w, color="#CBD5E1", label="2025년")
    ax2.bar([i + w / 2 for i in x], df["p_2026"], width=w, color="#059669", label="2026년")
    ax2.axvspan(1.5, 5.5, color="#ECFDF5", alpha=0.55, zorder=0)
    ax2.set_xticks(list(x))
    ax2.set_xticklabels(df["month"])
    ax2.set_title(f"2. 프로그램 수강 비교 (3~6월 실질 {metrics['p_ratio_3_6']}배 · 1~5월 {metrics['p_ratio_1_5']}배)", fontsize=10.5, fontweight="bold", loc="left")
    ax2.legend(frameon=False, fontsize=9)
    ax2.grid(axis="y", linestyle="--", alpha=0.35)

    # 3. 강좌 평균 이수율 및 SNS 유입 전환
    ax3 = axes[1, 0]
    labels_q = ["강좌 평균 이수율\n(출석 80%↑)", "SNS 채널 유입 비중\n(5대 채널 데일리 홍보)"]
    y_pos = range(len(labels_q))
    ax3.barh([i - 0.18 for i in y_pos], [57.6, 26.3], height=0.32, color="#94A3B8", label="2025년")
    ax3.barh([i + 0.18 for i in y_pos], [92.4, 47.5], height=0.32, color="#0284C7", label="2026년")
    ax3.set_yticks(list(y_pos))
    ax3.set_yticklabels(labels_q)
    ax3.set_xlim(0, 110)
    ax3.set_title("3. 핵심 질적 지표 도약 (이수율 +34.8%p · SNS 유입 +21.2%p)", fontsize=10.5, fontweight="bold", loc="left")
    ax3.legend(frameon=False, fontsize=9)
    ax3.grid(axis="x", linestyle="--", alpha=0.35)

    # 4. 전년 동기 대비 성장 배율 요약
    ax4 = axes[1, 1]
    bar_names = ["3~6월 실질 수강", "3~6월 실질 방문자", "1~5월 프로그램 수강", "1~5월 누적 방문자"]
    bar_vals = [metrics["p_ratio_3_6"], metrics["v_ratio_3_6"], metrics["p_ratio_1_5"], metrics["v_ratio_1_5"]]
    b4 = ax4.barh(bar_names, bar_vals, color=["#10B981", "#059669", "#3B82F6", "#1E3A8A"], height=0.46)
    ax4.axvline(1.0, color="#DC2626", linestyle="--", linewidth=1)
    ax4.set_xlim(0, 2.8)
    ax4.set_title("4. 전년 동기 대비 핵심 지표(KPI) 성장 배율 요약", fontsize=10.5, fontweight="bold", loc="left")
    for b in b4:
        wv = b.get_width()
        ax4.text(wv + 0.05, b.get_y() + b.get_height() / 2, f"{wv:.2f}배", va="center", fontsize=9.5, fontweight="bold")

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    plt.savefig(out_file, dpi=200)
    plt.close()
    print(f"[Done] 2026 KPI 검증 차트 저장 완료 -> {out_file}")


if __name__ == "__main__":
    yoy_df, kpi = calc_yoy_metrics()
    save_kpi_chart(yoy_df, kpi)