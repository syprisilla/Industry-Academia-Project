"""게이지 이미지 그리기.

* judge 결과의 per_feature 를 받아, 지표마다 가로 게이지 PNG 한 장을 저장한다.
*  [회색 전체 막대] + [초록 목표 범위 띠] + [내 발음 위치 막대]  형태.
* Ren'Py 가 이 PNG 를 불러와 화면에 띄운다.
* 한글이 깨지면 FONT_PATH 에 한글 TTF 경로를 넣을 것.
"""
from __future__ import annotations

from pathlib import Path

# 한글 폰트 경로 (없으면 기본 폰트 — 한글이 □ 로 나올 수 있음). 프로젝트 폰트로 바꿀 것.\
import sys
from pathlib import Path

def _find_font() -> str | None:
    """SourceHanSansLite.ttf 를 여러 후보 경로에서 찾는다. exe/스크립트 둘 다 대응."""
    name = "SourceHanSansLite.ttf"
    candidates = []
    if getattr(sys, "frozen", False):               # exe: PyInstaller 번들 폴더
        candidates.append(Path(sys._MEIPASS) / name)
        candidates.append(Path(sys.executable).resolve().parent / name)
    here = Path(__file__).resolve().parent
    candidates += [here.parent / name,              # game/SourceHanSansLite.ttf (스크립트 실행 시)
                   here / name]
    for c in candidates:
        if c.exists():
            return str(c)
    return None                                     # 못 찾으면 기본 폰트(한글 □)

FONT_PATH = _find_font()

# 색 (연한 회색 막대, 연녹색 목표 범위, 주황 내 위치)
_TRACK = "#E7E6E1"
_RANGE_IN = "#9FD3B8"
_MARK = "#D8A13A"


def _ensure_font():
    if FONT_PATH:
        from matplotlib import font_manager
        font_manager.fontManager.addfont(FONT_PATH)
        return font_manager.FontProperties(fname=FONT_PATH).get_name()
    return None


def draw_gauge(per_feature_item: dict, out_png, width_px: int = 760, height_px: int = 300) -> str:
    """지표 하나의 게이지 PNG 를 저장하고 경로를 돌려준다."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch

    fam = _ensure_font()
    if fam:
        plt.rcParams["font.family"] = fam

    g = per_feature_item["gauge"]
    fig, ax = plt.subplots(figsize=(width_px / 100, height_px / 100), dpi=100)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")

    y, h = 0.5, 0.18
    # 전체 막대
    ax.add_patch(FancyBboxPatch((0.03, y - h / 2), 0.94, h, boxstyle="round,pad=0.0,rounding_size=0.09",
                                 facecolor=_TRACK, edgecolor="none"))
    # 목표 범위 띠
    rl, rh = g["range_low_pos"], g["range_high_pos"]
    x0 = 0.03 + 0.94 * rl
    w = 0.94 * (rh - rl)
    ax.add_patch(FancyBboxPatch((x0, y - h / 2), max(w, 0.01), h, boxstyle="round,pad=0.0,rounding_size=0.09",
                                 facecolor=_RANGE_IN, edgecolor="none"))
    # 내 발음 위치 막대
    mx = 0.03 + 0.94 * g["value_pos"]
    ax.plot([mx, mx], [y - h / 2 - 0.08, y + h / 2 + 0.14], color=_MARK, lw=6, solid_capstyle="round")
    ax.plot([mx], [y + h / 2 + 0.16], marker="o", color=_MARK, markersize=11)
    # 라벨
    ax.text(mx, y - h / 2 - 0.18, "내 발음", color=_MARK, ha="center", va="top", fontsize=15, fontweight="bold")
    ax.text(x0 + w / 2, y - h / 2 - 0.42, "목표 범위", color="#3B7A57", ha="center", va="top", fontsize=15, fontweight="bold")
    ax.text(0.5, 0.95, per_feature_item["label"], ha="center", va="top", fontsize=13, color="white")

    out_png = Path(out_png)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(out_png), dpi=100, transparent=True)
    plt.close(fig)
    return str(out_png)


def draw_all(judge_result: dict, out_dir, prefix="gauge") -> dict:
    """사용한 지표마다 게이지 PNG 를 저장하고 {feature: png경로} 를 돌려준다."""
    out_dir = Path(out_dir)
    paths = {}
    for f, item in judge_result.get("per_feature", {}).items():
        paths[f] = draw_gauge(item, out_dir / f"{prefix}_{f}.png")
    return paths