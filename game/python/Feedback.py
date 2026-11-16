"""Turn a pronunciation result into one line of feedback for a child.

* Pick one encouraging message from the result of judge.judge().
* This wording is provisional. Update it after speech therapy review.
* Palatalization and interdental errors are not inferred yet. Use the low/high direction for simple guidance.
"""
from __future__ import annotations

# Provisional messages for values outside the target range, pending mentor review.
_HINTS = {
    "cog_hz": {"low": "Try moving your tongue a little farther forward.",
               "high": "Try relaxing your tongue a little."},
    "sd_hz":  {"low": "Try making a clear, focused stream of air.",
               "high": "Try sending the air through one small spot."},
    "duration_ms": {"low": "Try keeping the air flowing a little longer.",
                    "high": "Try making the airy sound a little shorter."},
    "norm_energy": {"low": "Try blowing the air a little harder.",
                    "high": "Try making the sound a little softer."},
}

_SUCCESS = "Great job! You said it clearly!"
_NEAR = "Let's get a little closer to the target!"
_NO_FRIC = "The ㅅ sound was a little faint. Try again and let the air flow!"  # Weak frication

def feedback(judge_result: dict) -> str:
    if judge_result.get("success"):
        return _SUCCESS
    if judge_result.get("segment_estimated"):
        return _NO_FRIC
    # Give one tip based on the direction of the first out-of-range feature.
    for f, p in judge_result.get("per_feature", {}).items():
        if not p["in_range"]:
            hint = _HINTS.get(f, {}).get(p["direction"])
            if hint:
                return hint
    return _NEAR