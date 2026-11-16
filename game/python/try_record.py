"""Record from a real mic, analyze and extract frication, then score and give feedback.

Usage: python try_record.py          (record for 3 seconds)
       python try_record.py 4        (record for 4 seconds)
Outputs: recording and segment WAV -> game/data/recordings/
         spectrum and gauges      -> game/data/out/
         acoustic features        -> game/data/word.json (overwritten)
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
REC_DIR = DATA_DIR / "recordings"      # Recording and extracted segment
OUT_DIR = DATA_DIR / "out"             # Spectrum and gauges
WORD_JSON = DATA_DIR / "word.json"     # Acoustic features (overwritten)
WORD = "사과"


def main(seconds: float = 3.0):
    REC_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    wav = REC_DIR / "rec.wav"

    # 1) Record
    print(f"\n● Recording for {seconds:.0f} seconds. Say '{WORD}'...")
    rec = record(wav, seconds=seconds)
    print(f"  Recording: {rec['message']}  (status={rec['status']})")
    if not rec["ok"]:
        print("  Recording failed. Check your mic.")
        return
    if rec["status"] in ("clipping", "too_quiet", "noisy"):
        print("  Skipping analysis because of recording quality. Please record again.")
        return

    # 2) Analyze and locate the ㅅ segment
    result = analyze(wav)
    print(f"\n● Analysis status: {result['status']}  (reason={result.get('reason')})")
    if result["status"] != "ok":
        print("  Couldn't find or estimate the frication segment.")
        for w in result.get("warnings", []):
            print(f"  ⚠ {w}")
        return

    est = result.get("segment_estimated", False)
    seg = result["segment"]
    print(f"  ㅅ segment: {seg['start_s']*1000:.0f}–{seg['end_s']*1000:.0f} ms"
          f"  {'(estimated)' if est else '(detected)'}")
    for w in result.get("warnings", []):
        print(f"  ⚠ {w}")

    # 3) Save the spectrum PNG and segment WAV
    spec_png = OUT_DIR / "spectrum.png"
    fric_wav = REC_DIR / "fric.wav"
    save_debug_plot(wav, result, spec_png)
    save_segment_clip(wav, result, fric_wav)
    print(f"\n● Segment files created")
    print(f"  Spectrum: {spec_png}")
    print(f"  Segment audio: {fric_wav}")

    # 4) Score and give feedback
    jr = judge_mod.judge(result["features"], est)
    fb = feedback_mod.feedback(jr)
    print(f"\n● Score: success={jr['success']}  (estimated={est})")
    print(f"  Feedback: {fb}")
    print("  Features:")
    for f, p in jr["per_feature"].items():
        mark = "○ In range" if p["in_range"] else f"✗ Out of range ({p['direction']})"
        print(f"    {p['label']:<6} {p['value']:>9.1f}   {mark}"
              f"   target {p['range_low']:.0f}–{p['range_high']:.0f}")

    # 5) Save gauge PNGs in out
    gauges = gauge_mod.draw_all(jr, OUT_DIR)
    print(f"\n● Gauge images")
    for f, path in gauges.items():
        print(f"  {f}: {path}")

    # 6) Write acoustic features to word.json, replacing the old file
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
    print(f"\n● Features saved to {WORD_JSON}")
    print(f"\nDone.\n")


if __name__ == "__main__":
    sec = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0
    main(sec)