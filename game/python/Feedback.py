"""판정 결과 -> 아동용 한 줄 피드백.

* judge.judge() 결과를 받아 격려 문구 하나를 고른다.
* 문구는 '임시' 다. 언어치료 멘토 확인 후 바꿀 것.
* 오류 유형(구개음화/치간음화) 추정은 아직 보류. direction(low/high) 만으로 간단히 안내.
"""
from __future__ import annotations

# 지표가 범위 밖일 때, 방향별 안내 (임시 — 멘토 확인 필요)
_HINTS = {
    "cog_hz": {"low": "혀를 조금 앞으로 해서 소리를 내 볼까요?",
               "high": "혀에 힘을 살짝 빼고 소리를 내 볼까요?"},
    "sd_hz":  {"low": "바람소리를 또렷하게 모아서 내 볼까요?",
               "high": "바람이 한 곳에서 나오도록 해 볼까요?"},
    "duration_ms": {"low": "바람소리를 조금 더 길게 이어 볼까요?",
                    "high": "바람소리를 조금 짧게 내 볼까요?"},
    "norm_energy": {"low": "바람을 조금 더 세게 내 볼까요?",
                    "high": "조금만 부드럽게 내 볼까요?"},
}

_SUCCESS = "좋아요! 정확하게 발음했어요!"
_NEAR = "목표 위치에 조금 더 가까워져 보자!"
_NO_FRIC = "'ㅅ' 바람소리를 내서 다시 말해 볼까요? 마찰음이 약해요!"   # 마찰음 자체가 약함

def feedback(judge_result: dict) -> str:
    if judge_result.get("success"):
        return _SUCCESS
    if judge_result.get("segment_estimated"):
        return _NO_FRIC
    # 범위 밖인 지표 중 첫 번째의 방향 안내를 준다 (한 번에 하나만)
    for f, p in judge_result.get("per_feature", {}).items():
        if not p["in_range"]:
            hint = _HINTS.get(f, {}).get(p["direction"])
            if hint:
                return hint
    return _NEAR