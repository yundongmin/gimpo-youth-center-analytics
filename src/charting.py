"""Shared presentation settings for public aggregate charts."""

from matplotlib import font_manager, pyplot as plt

NAVY = "#1E3A8A"
BLUE = "#2563EB"
TEAL = "#0F766E"
GRAY = "#94A3B8"


def set_korean_font() -> None:
    installed = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in ("Malgun Gothic", "NanumGothic", "Noto Sans CJK KR", "AppleGothic"):
        if candidate in installed:
            plt.rcParams["font.family"] = candidate
            break
    plt.rcParams["axes.unicode_minus"] = False


def finish(ax) -> None:
    ax.grid(axis="y", color="#E2E8F0", linestyle="--", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
