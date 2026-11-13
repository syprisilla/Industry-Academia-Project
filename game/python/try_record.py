"""실제 마이크로 한 번 녹음 -> 분석 -> 구간 분리(스펙트럼+WAV) -> 판정 -> 게이지 -> 피드백.

실행:  python try_record.py          (3초 녹음)
       python try_record.py 4        (4초 녹음)
출력:  녹음/분리음성 -> game/data/recordings/
       스펙트럼/게이지 -> game/data/out/
       분석 지표 JSON  -> game/data/word.json (덮어쓰기)
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from Audio_recording import record
from Pronunciation_analysis import analyze, save_debug_plot, save_segment_clip
import Judge as judge_mod
import Gauge as gauge_mod
import Feedback as feedback_mod

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
REC_DIR = DATA_DIR / "recordings"      # 녹음 원본 + 분리 음성
OUT_DIR = DATA_DIR / "out"             # 스펙트럼 + 게이지
WORD_JSON = DATA_DIR / "word.json"     # 분석 지표 (덮어쓰기)
WORD = "사과"


def main(seconds: float = 3.0):
    REC_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    wav = REC_DIR / "rec.wav"

    # 1) 녹음
    print(f"\n● {seconds:.0f}초간 녹음합니다. '{WORD}' 라고 말하세요...")
    rec = record(wav, seconds=seconds)
    print(f"  녹음됨: {rec['message']}  (상태={rec['status']})")
    if not rec["ok"]:
        print("  녹음 실패 — 마이크를 확인하세요.")
        return
    if rec["status"] in ("clipping", "too_quiet", "noisy"):
        print("  녹음 품질 문제로 분석을 건너뜁니다. 다시 녹음하세요.")
        return

    # 2) 분석 (ㅅ 구간 탐색)
    result = analyze(wav)
    print(f"\n● 분석 상태: {result['status']}  (이유={result.get('reason')})")
    if result["status"] != "ok":
        print("  분석 불가 — 마찰구간을 찾지 못했고 추정도 실패했습니다.")
        for w in result.get("warnings", []):
            print(f"  ⚠ {w}")
        return

    est = result.get("segment_estimated", False)
    seg = result["segment"]
    print(f"  ㅅ 구간: {seg['start_s']*1000:.0f}~{seg['end_s']*1000:.0f} ms"
          f"  {'(추정/폴백)' if est else '(정상 검출)'}")
    for w in result.get("warnings", []):
        print(f"  ⚠ {w}")

    # 3) 스펙트럼 PNG(out) + 구간 WAV(recordings) 생성
    spec_png = OUT_DIR / "spectrum.png"
    fric_wav = REC_DIR / "fric.wav"
    save_debug_plot(wav, result, spec_png)
    save_segment_clip(wav, result, fric_wav)
    print(f"\n● 구간 분리 자료 생성")
    print(f"  스펙트럼: {spec_png}")
    print(f"  구간 음성: {fric_wav}")

    # 4) 판정 + 피드백
    jr = judge_mod.judge(result["features"], est)
    fb = feedback_mod.feedback(jr)
    print(f"\n● 판정: success={jr['success']}  (폴백={est})")
    print(f"  피드백: {fb}")
    print("  지표:")
    for f, p in jr["per_feature"].items():
        mark = "○ 범위안" if p["in_range"] else f"✗ 범위밖({p['direction']})"
        print(f"    {p['label']:<6} {p['value']:>9.1f}   {mark}"
              f"   목표 {p['range_low']:.0f}~{p['range_high']:.0f}")

    # 5) 게이지 PNG(out)
    gauges = gauge_mod.draw_all(jr, OUT_DIR)
    print(f"\n● 게이지 이미지")
    for f, path in gauges.items():
        print(f"  {f}: {path}")

    # 6) 분석 지표 JSON -> word.json (덮어쓰기)
    payload = {
        "word": WORD,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "success": jr["success"],
        "segment_estimated": est,
        "segment": seg,
        "features": result["features"],
        "feedback": fb,
    }
    WORD_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n● 지표 저장: {WORD_JSON}")
    print(f"\n완료.\n")


if __name__ == "__main__":
    sec = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0
    main(sec)