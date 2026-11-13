"""발음 판정 모듈.

* pronunciation_analysis.analyze() 가 낸 지표(features)를 받아,
  정상 범위(기준 평균 ± N*표준편차) 안에 드는지 판정하고, 게이지용 위치(0~1)를 계산한다.
* 지금은 CoG(무게중심), 분산 2개만 판정에 쓴다. USED_FEATURES 만 바꾸면 늘릴 수 있다.
* REFERENCE 값은 전부 '임시값' 이다. 팀원 녹음으로 평균/표준편차를 구해 교체할 것.
"""
from __future__ import annotations

# 판정에 쓰는 지표 (나중에 바꾸려면 이 줄만 수정)
USED_FEATURES = ("cog_hz", "sd_hz")

# 정상 범위 = mean ± RANGE_SD * std    (임시값 — 팀원 녹음 후 교체)
RANGE_SD = 1.5

# 지표별 기준값 (mean, std) — 임시값. Han et al.(2024) 정조음 표를 참고로 넣어둠.

REFERENCE = {
    "cog_hz":      {"mean": 9096.04, "std": 445.55, "label": "무게중심"},
    "sd_hz":       {"mean": 2451.68, "std": 350.0, "label": "분산"},
    "skewness":    {"mean": 2.08, "std": 0.37, "label": "왜도"},
    "kurtosis":    {"mean": 7.2, "std": 3.04, "label": "첨도"},
    "duration_ms": {"mean": 98.75, "std": 13.27, "label": "마찰 지속시간"},
    "norm_energy": {"mean": 0.01, "std": 0.01, "label": "정규화 에너지"},
}

# 게이지 가로 축을 mean ± GAUGE_SPAN_SD 범위로 그린다 (목표 범위가 가운데쯤 오도록)
GAUGE_SPAN_SD = 3.0


def _one(feature: str, value: float) -> dict:
    ref = REFERENCE[feature]
    mean, std = ref["mean"], ref["std"]
    low, high = mean - RANGE_SD * std, mean + RANGE_SD * std
    in_range = low <= value <= high

    # 게이지 위치: 축 전체를 0~1 로 정규화 (범위 밖이면 0 또는 1 로 고정)
    axis_low, axis_high = mean - GAUGE_SPAN_SD * std, mean + GAUGE_SPAN_SD * std
    def norm(v):
        return max(0.0, min(1.0, (v - axis_low) / (axis_high - axis_low)))

    direction = "in"
    if value < low:
        direction = "low"      # 기준보다 낮음
    elif value > high:
        direction = "high"     # 기준보다 높음

    return {
        "feature": feature,
        "label": ref["label"],
        "value": float(value),
        "range_low": float(low),
        "range_high": float(high),
        "in_range": bool(in_range),
        "direction": direction,
        "gauge": {                      # 0~1 위치값 (게이지 그릴 때 사용)
            "value_pos": norm(value),
            "range_low_pos": norm(low),
            "range_high_pos": norm(high),
        },
    }


def judge(features: dict, segment_estimated: bool = False) -> dict:
    """features dict -> 지표별 판정 + 전체 성공 여부.

    success: 사용하는 지표가 모두 범위 안이고, 구간이 추정(폴백)이 아닐 때만 True.
    """
    per = {}
    for f in USED_FEATURES:
        if f in features and features[f] is not None:
            per[f] = _one(f, features[f])
    all_in = len(per) > 0 and all(p["in_range"] for p in per.values())
    success = all_in and not segment_estimated
    return {"success": success, "segment_estimated": bool(segment_estimated),
            "used_features": list(USED_FEATURES), "per_feature": per}