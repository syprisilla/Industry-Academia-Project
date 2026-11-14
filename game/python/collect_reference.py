"""'사과'를 여러 번 녹음해 6개 지표의 mean/std 를 산출한다.
정상 검출(폴백 아님)된 녹음만 집계에 넣는다.

실행:  python collect_reference.py          (20회, 3초)
       python collect_reference.py 15 3     (15회, 3초)
중간에 그만두려면 녹음 안내에서 q 입력.
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
LABELS = {"cog_hz": "무게중심", "sd_hz": "분산", "skewness": "왜도",
          "kurtosis": "첨도", "duration_ms": "마찰 지속시간", "norm_energy": "정규화 에너지"}


def main(n: int = 20, seconds: float = 3.0):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    wav = OUT_DIR / "ref_tmp.wav"
    rows = []          # 정상 검출된 것만: 각 녹음의 feature dict
    skipped = 0

    print(f"\n'사과'를 또렷하게 {n}번 녹음합니다. 매번 엔터를 누르면 {seconds:.0f}초 녹음.")
    print("(ㅅ 바람소리를 분명히. q + 엔터 = 중단)\n")

    i = 0
    while i < n:
        ans = input(f"[{i+1}/{n}] 엔터로 녹음 (q=중단): ").strip().lower()
        if ans == "q":
            break
        rec = record(wav, seconds=seconds)
        if not rec["ok"] or rec["status"] in ("clipping", "too_quiet", "noisy"):
            print(f"    ✗ 녹음 품질 문제({rec['status']}) — 이 회차 제외, 다시 시도")
            continue
        r = analyze(wav)
        if r["status"] != "ok":
            print(f"    ✗ 분석 실패({r.get('reason')}) — 제외")
            skipped += 1
            i += 1
            continue
        if r.get("segment_estimated"):
            print(f"    ✗ 마찰음 약함(폴백) — 기준 산출에서 제외")
            skipped += 1
            i += 1
            continue
        feats = r["features"]
        rows.append(feats)
        seg = r["segment"]
        print(f"    ○ 수집됨  cog={feats['cog_hz']:.0f} sd={feats['sd_hz']:.0f} "
              f"dur={feats['duration_ms']:.0f}ms  구간 {seg['start_s']*1000:.0f}~{seg['end_s']*1000:.0f}ms")
        i += 1

    valid = len(rows)
    print(f"\n유효 표본 {valid}개 (제외 {skipped}개)")
    if valid < 5:
        print("표본이 너무 적습니다(5개 미만). std 가 불안정하니 더 녹음하세요.")
        return

    # 6개 지표 mean/std
    ref = {}
    print("\n지표            평균(mean)      표준편차(std)")
    for f in FEATURES:
        vals = np.array([row[f] for row in rows], dtype=float)
        m, s = float(vals.mean()), float(vals.std(ddof=1))
        ref[f] = {"mean": round(m, 2), "std": round(s, 2), "label": LABELS[f]}
        print(f"  {LABELS[f]:<8} {m:>12.2f} {s:>14.2f}")

    # REFERENCE 붙여넣기용 출력
    print("\n--- 아래를 Pronunciation_analysis 의 REFERENCE 에 붙여넣으세요 ---\n")
    print("REFERENCE = {")
    for f in FEATURES:
        r = ref[f]
        print(f'    "{f}":{" "*(12-len(f))}'
              f'{{"mean": {r["mean"]}, "std": {r["std"]}, "label": "{r["label"]}"}},')
    print("}")

    # JSON 저장
    out_json = OUT_DIR / "reference.json"
    out_json.write_text(json.dumps({"n_valid": valid, "n_skipped": skipped, "reference": ref},
                                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n저장됨: {out_json}")


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    sec = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
    main(n, sec)