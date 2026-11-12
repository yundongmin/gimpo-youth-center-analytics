import os
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False


def get_2025_summary():
    # 개인정보 보호 규정상 원본 출결 로그 비공개 -> 월별 확정 집계 데이터 사용 (연간 방문 5,403명, 수강 1,620건)
    monthly = pd.DataFrame({
        "month": [f"{i}월" for i in range(1, 13)],
        "visitors": [61, 109, 350, 484, 416, 440, 406, 548, 674, 621, 711, 583],
        "enrollments": [3, 103, 145, 177, 166, 173, 98, 139, 129, 185, 187, 115],
    })

    # 3~10월 방문자(n=3,939) 거주지 권역별 집계
    residence = pd.DataFrame({
        "zone": [
            "본원 인근 3개동\n(사우·김포본·풍무)",
            "중부 도심·신도시\n(운양·구래·장기 등)",
            "외곽 읍·면 소외지역\n(고촌·양촌·통진 등)",
            "관외·소재기업·기타",
        ],
        "count": [2619, 942, 330, 48],
    })
    residence["pct"] = (residence["count"] / residence["count"].sum() * 100).round(1)

    return monthly, residence


def save_baseline_chart(monthly, residence, out_file="outputs/2025_baseline_eda.png"):
    fig, axes = plt.subplots(2, 2, figsize=(14, 8.5), dpi=200)
    fig.patch.set_facecolor("white")
    fig.suptitle(
        "김포시청년지원센터 2025년 전수(1~12월) 운영 로그 기초 EDA (방문 5,403명 · 수강 1,620건)",
        fontsize=13.5, fontweight="bold", y=0.97
    )

    # 1. 월별 방문자 및 수강 추이
    ax1 = axes[0, 0]
    colors = ["#CBD5E1", "#CBD5E1"] + ["#94A3B8"] * 8 + ["#2563EB", "#3B82F6"]
    bars = ax1.bar(monthly["month"], monthly["visitors"], color=colors, width=0.56, label="방문(명)")
    ax1.set_title("1. 월별 방문자 및 프로그램 수강 추이 (1~12월)", fontsize=11, fontweight="bold", loc="left")
    ax1.set_ylim(0, 820)
    ax1.grid(axis="y", linestyle="--", alpha=0.35)
    for b in bars:
        h = b.get_height()
        ax1.text(b.get_x() + b.get_width() / 2, h + 12, f"{int(h)}", ha="center", fontsize=8, fontweight="bold")

    ax1_r = ax1.twinx()
    ax1_r.plot(monthly["month"], monthly["enrollments"], color="#059669", marker="o", linewidth=2, label="수강(건)")
    ax1_r.set_ylim(0, 420)

    # 2. 거주지 분포 및 지역 편중
    ax2 = axes[0, 1]
    res_rev = residence.iloc[::-1]
    hbars = ax2.barh(res_rev["zone"], res_rev["pct"], color=["#CBD5E1", "#DC2626", "#60A5FA", "#1E3A8A"], height=0.55)
    ax2.set_title("2. 이용자 거주지 분포 및 지역 편중 (3~10월, n=3,939)", fontsize=11, fontweight="bold", loc="left")
    ax2.set_xlim(0, 85)
    ax2.grid(axis="x", linestyle="--", alpha=0.35)
    for b, (_, r) in zip(hbars, res_rev.iterrows()):
        ax2.text(b.get_width() + 1.5, b.get_y() + b.get_height() / 2, f"{r['pct']}% ({r['count']:,}명)", va="center", fontsize=8.5, fontweight="bold")

    # 3. 강좌 평균 이수율 및 이탈 구조 (연간 63개 강좌, 평균 6회차, 회당 평균 4.29명)
    ax3 = axes[1, 0]
    ax3.barh(["이수율 구조\n(출석 80%↑)"], [57.6], color="#0284C7", height=0.38, label="이수 완료 57.6% (약 933명)")
    ax3.barh(["이수율 구조\n(출석 80%↑)"], [42.4], left=[57.6], color="#F87171", height=0.38, label="중도 이탈 42.4% (약 687명)")
    ax3.set_title("3. 강좌 운영 효율 병목 (연 63개 · 평균 6회차 · 회당 4.29명)", fontsize=11, fontweight="bold", loc="left")
    ax3.set_xlim(0, 100)
    ax3.legend(loc="lower center", ncol=2, frameon=False, fontsize=8.5)

    # 4. 유입 경로 및 이용 목적
    ax4 = axes[1, 1]
    ax4.barh(["유입 경로", "이용 목적"], [45.4, 57.7], color="#1E3A8A", height=0.42, label="지인추천(45.4%) / 스터디(57.7%)")
    ax4.barh(["유입 경로", "이용 목적"], [28.3, 30.8], left=[45.4, 57.7], color="#60A5FA", height=0.42, label="공지(28.3%) / 프로그램(30.8%)")
    ax4.barh(["유입 경로", "이용 목적"], [26.3, 11.5], left=[73.7, 88.5], color="#F59E0B", height=0.42, label="SNS(26.3%) / 대관·출력(11.6%)")
    ax4.set_title("4. 방문 유입 채널 및 공간 이용 목적 (3~10월, n=3,939)", fontsize=11, fontweight="bold", loc="left")
    ax4.set_xlim(0, 100)
    ax4.legend(loc="lower center", ncol=1, frameon=False, fontsize=8)

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    plt.savefig(out_file, dpi=200)
    plt.close()
    print(f"[Done] 2025 Baseline EDA 차트 저장 완료 -> {out_file}")


if __name__ == "__main__":
    m_df, r_df = get_2025_summary()
    save_baseline_chart(m_df, r_df)