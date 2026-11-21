"""Build per-syllable /ㅅ/ reference values (mean/std) from recorded audio.

Audio layout (one folder per syllable group; one /ㅅ/ per file):
    <root>/시/*.wav   <root>/세/*.wav   <root>/사/*.wav ...
Run:
    python build_reference.py [AUDIO_ROOT] [OUT_JSON]
Defaults: AUDIO_ROOT=../data/reference_audio, OUT_JSON=../data/reference_by_syllable.json
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np

from Pronunciation_analysis import analyze

FEATURES = ("cog_hz", "sd_hz", "skewness", "kurtosis", "duration_ms", "norm_energy")
AUDIO_EXT = {".wav", ".flac", ".ogg", ".mp3", ".m4a"}


def main(root, out_path):
    root = Path(root)
    if not root.is_dir():
        print(f"Folder not found: {root}")
        return
    ref = {}
    for sub in sorted(p for p in root.iterdir() if p.is_dir()):
        group = sub.name
        files = [f for f in sub.iterdir() if f.suffix.lower() in AUDIO_EXT]
        vals = {k: [] for k in FEATURES}
        n_ok = n_skip = 0
        for f in files:
            try:
                r = analyze(str(f))
            except Exception as e:
                print(f"  x {f.name}: analysis error {e}")
                n_skip += 1
                continue
            # Exclude no-frication / weak (fallback) / unmeasurable; keep only clean /ㅅ/.
            if r.get("status") != "ok" or r.get("segment_estimated"):
                n_skip += 1
                continue
            feats = r["features"]
            for k in FEATURES:
                vals[k].append(feats[k])
            n_ok += 1
        if n_ok == 0:
            print(f"[{group}] no valid samples -- skipped (files {len(files)}, excluded {n_skip})")
            continue
        entry = {"n": n_ok}
        for k in FEATURES:
            a = np.array(vals[k], float)
            entry[k] = {"mean": round(float(a.mean()), 3),
                        "std": round(float(a.std(ddof=1)) if n_ok > 1 else 0.0, 3)}
        ref[group] = entry
        warn = "  (warning: n<10, std unstable)" if n_ok < 10 else ""
        print(f"[{group}] valid {n_ok} / excluded {n_skip}   "
              f"cog {entry['cog_hz']['mean']}+/-{entry['cog_hz']['std']}  "
              f"sd {entry['sd_hz']['mean']}+/-{entry['sd_hz']['std']}{warn}")

    Path(out_path).write_text(json.dumps(ref, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSaved: {out_path}  ({len(ref)} syllable groups)")


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    root = sys.argv[1] if len(sys.argv) > 1 else here.parent / "data" / "reference_audio"
    out = sys.argv[2] if len(sys.argv) > 2 else here.parent / "data" / "reference_by_syllable.json"
    main(root, out)