"""Record 사과 several times to compute the mean and standard deviation of six features.
Include recordings with a detected frication segment only.

Usage: python collect_reference.py          (20 recordings of 3 seconds)
       python collect_reference.py 15 3     (15 recordings of 3 seconds)
To stop early, enter q at a recording prompt.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

from Audio_recording import record
from Pronunciation_analysis import analyze

OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "out"
FEATURES = ("cog_hz", "sd_hz", "skewness", "kurtosis", "duration_ms", "norm_energy")
LABELS = {"cog_hz": "Center of gravity", "sd_hz": "Spread", "skewness": "Skewness",
          "kurtosis": "Kurtosis", "duration_ms": "Frication duration", "norm_energy": "Normalized energy"}


def main(n: int = 20, seconds: float = 3.0):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    wav = OUT_DIR / "ref_tmp.wav"
    rows = []          # Feature dictionaries for successful segment detections only.
    skipped = 0

    print(f"\nSay 사과 clearly for {n} recordings. Press Enter before each {seconds:.0f}-second recording.")
    print("Make the airy ㅅ sound clear. To stop, press q then Enter.\n")

    i = 0
    while i < n:
        ans = input(f"[{i+1}/{n}] Press Enter to record or q to stop: ").strip().lower()
        if ans == "q":
            break
        rec = record(wav, seconds=seconds)
        if not rec["ok"] or rec["status"] in ("clipping", "too_quiet", "noisy"):
            print(f"    ✗ Recording quality issue ({rec['status']}). Skipping this take. Please try again.")
            continue
        r = analyze(wav)
        if r["status"] != "ok":
            print(f"    ✗ Analysis failed ({r.get('reason')}). Skipping this take.")
            skipped += 1
            i += 1
            continue
        if r.get("segment_estimated"):
            print(f"    ✗ Frication too weak to detect. Skipping this take.")
            skipped += 1
            i += 1
            continue
        feats = r["features"]
        rows.append(feats)
        seg = r["segment"]
        print(f"    ○ Collected  cog={feats['cog_hz']:.0f} sd={feats['sd_hz']:.0f} "
              f"dur={feats['duration_ms']:.0f}ms  segment {seg['start_s']*1000:.0f}–{seg['end_s']*1000:.0f}ms")
        i += 1

    valid = len(rows)
    print(f"\nUsable samples: {valid} ({skipped} skipped)")
    if valid < 5:
        print("Fewer than five usable samples. Record more for a reliable standard deviation.")
        return

    # Mean and standard deviation for the six features
    ref = {}
    print("\nFeature               Mean             Std. dev.")
    for f in FEATURES:
        vals = np.array([row[f] for row in rows], dtype=float)
        m, s = float(vals.mean()), float(vals.std(ddof=1))
        ref[f] = {"mean": round(m, 2), "std": round(s, 2), "label": LABELS[f]}
        print(f"  {LABELS[f]:<8} {m:>12.2f} {s:>14.2f}")

    # Output for pasting into REFERENCE
    print("\n--- Paste the following into REFERENCE in Pronunciation_analysis ---\n")
    print("REFERENCE = {")
    for f in FEATURES:
        r = ref[f]
        print(f'    "{f}":{" "*(12-len(f))}'
              f'{{"mean": {r["mean"]}, "std": {r["std"]}, "label": "{r["label"]}"}},')
    print("}")

    # Save as JSON
    out_json = OUT_DIR / "reference.json"
    out_json.write_text(json.dumps({"n_valid": valid, "n_skipped": skipped, "reference": ref},
                                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSaved to {out_json}")


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    sec = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
    main(n, sec)