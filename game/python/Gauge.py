"""Render gauge images.

* Read per_feature from the judgment and save one horizontal gauge PNG per feature.
* Each gauge has a gray track, a green target band, and a marker for the measured value.
* Ren'Py loads the PNG for display.
* Set FONT_PATH to a Hangul-capable TTF if Hangul does not render.
"""
from __future__ import annotations

from pathlib import Path

# Path to the project font. The fallback font may show squares for Hangul.
import sys
from pathlib import Path

def _find_font() -> str | None:
    """Find SourceHanSansLite.ttf when running from an executable or a script."""
    name = "SourceHanSansLite.ttf"
    candidates = []
    if getattr(sys, "frozen", False):               # PyInstaller bundle directory
        candidates.append(Path(sys._MEIPASS) / name)
        candidates.append(Path(sys.executable).resolve().parent / name)
    here = Path(__file__).resolve().parent
    candidates += [here.parent / name,              # game/SourceHanSansLite.ttf when run as a script
                   here / name]
    for c in candidates:
        if c.exists():
            return str(c)
    return None                                     # Use the default font if the project font is missing.

FONT_PATH = _find_font()

# Colors for the light gray track, light green target, and orange marker.
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
    """Save a gauge PNG for one feature and return its path."""
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
    # Full track
    ax.add_patch(FancyBboxPatch((0.03, y - h / 2), 0.94, h, boxstyle="round,pad=0.0,rounding_size=0.09",
                                 facecolor=_TRACK, edgecolor="none"))
    # Target band
    rl, rh = g["range_low_pos"], g["range_high_pos"]
    x0 = 0.03 + 0.94 * rl
    w = 0.94 * (rh - rl)
    ax.add_patch(FancyBboxPatch((x0, y - h / 2), max(w, 0.01), h, boxstyle="round,pad=0.0,rounding_size=0.09",
                                 facecolor=_RANGE_IN, edgecolor="none"))
    # Marker for the measured pronunciation
    mx = 0.03 + 0.94 * g["value_pos"]
    ax.plot([mx, mx], [y - h / 2 - 0.08, y + h / 2 + 0.14], color=_MARK, lw=6, solid_capstyle="round")
    ax.plot([mx], [y + h / 2 + 0.16], marker="o", color=_MARK, markersize=11)

    # Labels
    ax.text(mx, y - h / 2 - 0.18, "Your sound", color=_MARK, ha="center", va="top", fontsize=15, fontweight="bold")
    ax.text(x0 + w / 2, y - h / 2 - 0.42, "Target range", color="#3B7A57", ha="center", va="top", fontsize=15, fontweight="bold")

    ax.text(0.5, 0.95, per_feature_item["label"], ha="center", va="top", fontsize=13, color="white")

    out_png = Path(out_png)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(out_png), dpi=100, transparent=True)
    plt.close(fig)
    return str(out_png)


def draw_all(judge_result: dict, out_dir, prefix="gauge") -> dict:
    """Save a gauge per feature and return a mapping of features to PNG paths."""
    out_dir = Path(out_dir)
    paths = {}
    for f, item in judge_result.get("per_feature", {}).items():
        paths[f] = draw_gauge(item, out_dir / f"{prefix}_{f}.png")
    return paths