"""Score pronunciation features.

* Read features returned by pronunciation_analysis.analyze().
  Check the reference mean ± N standard deviations and calculate gauge positions (0 to 1).
* Scoring uses CoG and spread. Update USED_FEATURES to add more features.
* All REFERENCE values are provisional. Replace them with means and standard deviations from team recordings.
"""
from __future__ import annotations

# Features used for scoring.
USED_FEATURES = ("cog_hz", "sd_hz")

# Target range is mean ± RANGE_SD * std. Replace the provisional values after team recordings.
RANGE_SD = 1.5

# Provisional means and standard deviations from the typical articulation table in Han et al. (2024).

REFERENCE = {
    "cog_hz":      {"mean": 9096.04, "std": 445.55, "label": "Center of gravity"},
    "sd_hz":       {"mean": 2800.68, "std": 350.0, "label": "Spread"},
    "skewness":    {"mean": 2.08, "std": 0.37, "label": "Skewness"},
    "kurtosis":    {"mean": 7.2, "std": 3.04, "label": "Kurtosis"},
    "duration_ms": {"mean": 98.75, "std": 13.27, "label": "Frication duration"},
    "norm_energy": {"mean": 0.01, "std": 0.01, "label": "Normalized energy"},
}

# Draw the axis over mean ± GAUGE_SPAN_SD so the target range is centered.
GAUGE_SPAN_SD = 3.0


def _one(feature: str, value: float) -> dict:
    ref = REFERENCE[feature]
    mean, std = ref["mean"], ref["std"]
    low, high = mean - RANGE_SD * std, mean + RANGE_SD * std
    in_range = low <= value <= high

    # Normalize the gauge position to 0–1 and clamp out-of-range values.
    axis_low, axis_high = mean - GAUGE_SPAN_SD * std, mean + GAUGE_SPAN_SD * std
    def norm(v):
        return max(0.0, min(1.0, (v - axis_low) / (axis_high - axis_low)))

    direction = "in"
    if value < low:
        direction = "low"      # Below the target
    elif value > high:
        direction = "high"     # Above the target

    return {
        "feature": feature,
        "label": ref["label"],
        "value": float(value),
        "range_low": float(low),
        "range_high": float(high),
        "in_range": bool(in_range),
        "direction": direction,
        "gauge": {                      # Normalized position values for drawing the gauge
            "value_pos": norm(value),
            "range_low_pos": norm(low),
            "range_high_pos": norm(high),
        },
    }


def judge(features: dict, segment_estimated: bool = False) -> dict:
    """Return per-feature scores and the overall pronunciation result.

    Success requires every scored feature in range and a detected frication segment.
    """
    per = {}
    for f in USED_FEATURES:
        if f in features and features[f] is not None:
            per[f] = _one(f, features[f])
    all_in = len(per) > 0 and all(p["in_range"] for p in per.values())
    success = all_in and not segment_estimated
    return {"success": success, "segment_estimated": bool(segment_estimated),
            "used_features": list(USED_FEATURES), "per_feature": per}