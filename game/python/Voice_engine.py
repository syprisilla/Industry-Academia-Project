"""Entry point for Ren'Py and the executable. Returns JSON-serializable dictionaries.

Main functions
    run_mic_test()                      Check the mic
    record_and_analyze(path, sec)       Record and extract features
    record_judge_visualize(out_dir)     Record, analyze, score, draw gauges, and give feedback
    analyze_file(path)                  Analyze an existing WAV file for testing

This is the PyInstaller entry point. For example:
    voice_engine.exe run OUT_DIR [SEC]     # Record and render gauges
    voice_engine.exe mic-test
    voice_engine.exe devices
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:  # Support package imports and running directly from this directory.
    from .Audio_recording import list_input_devices, mic_test, record
    from .Pronunciation_analysis import analyze, save_debug_plot
    from . import Judge as judge_mod
    from . import Gauge as gauge_mod
    from . import Feedback as feedback_mod
except ImportError:
    from Audio_recording import list_input_devices, mic_test, record
    from Pronunciation_analysis import analyze, save_debug_plot
    import Judge as judge_mod
    import Gauge as gauge_mod
    import Feedback as feedback_mod

SYLLABLES = ("시", "세", "사", "서", "소", "수", "스")

def _data_dir() -> Path:
    """Locate data relative to the executable when frozen or this file otherwise."""
    if getattr(sys, "frozen", False):
        # onedir exe: game/python/voice_engine/voice_engine.exe -> game/data
        base = Path(sys.executable).resolve().parent.parent.parent
    else:
        # Script layout: game/python/Voice_engine.py -> game/data
        base = Path(__file__).resolve().parent.parent
    return base / "data"


def run_mic_test(seconds: float = 2.0, device=None) -> dict:
    return mic_test(seconds=seconds, device=device)


def record_and_analyze(wav_path, seconds: float = 3.0, device=None, capture=None) -> dict:
    kwargs = {"capture": capture} if capture is not None else {}
    rec = record(wav_path, seconds=seconds, device=device, **kwargs)
    if not rec["ok"]:
        return {"status": "unmeasurable", "reason": rec["status"], "message": rec["message"]}
    if rec["status"] in ("clipping", "too_quiet"):   # Skip analysis for clipped or quiet audio.
        return {"status": "unmeasurable", "reason": rec["status"], "message": rec["message"],
                "recording": rec["report"]}
    result = analyze(wav_path)
    result["recording"] = rec["report"]
    return result


def analyze_file(wav_path) -> dict:
    return analyze(wav_path)


def record_judge_visualize(out_dir, seconds: float = 3.0, device=None, capture=None, make_plot=False) -> dict:
    """Record, analyze, score, render gauges, and give feedback in one call.

    Save rec.wav and the gauge PNGs in out_dir.
    Return the score, gauge image paths, and feedback in JSON.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    wav_path = out_dir / "rec.wav"

    result = record_and_analyze(wav_path, seconds=seconds, device=device, capture=capture)

    # Return analysis errors without scoring or generating gauges.
    if result.get("status") != "ok":
        result["success"] = None
        result["feedback"] = "We couldn't hear you clearly. Want to try again?"
        result["gauges"] = {}
        return result

    jr = judge_mod.judge(result["features"], result.get("segment_estimated", False))
    gauges = gauge_mod.draw_all(jr, out_dir)
    if make_plot:
        save_debug_plot(wav_path, result, out_dir / "debug.png")

    result["judge"] = jr
    result["success"] = jr["success"]
    result["gauges"] = gauges
    result["feedback"] = feedback_mod.feedback(jr)
    return result

def record_try(word: str = "사과", seconds: float = 3.0, device=None, capture=None) -> dict:
    """Match try_record.py: record, analyze, extract the segment, score, and write word.json.

    Output locations:
      Original recording and extracted segment -> data/recordings/
      Spectrum plot and gauges                 -> data/out/
      Analysis features                        -> data/word.json (overwritten)
    """
    import json
    from datetime import datetime

    data_dir = _data_dir()
    rec_dir = data_dir / "recordings"
    out_dir = data_dir / "out"
    word_json = data_dir / "word.json"
    rec_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    wav = rec_dir / "rec.wav"
    result = record_and_analyze(wav, seconds=seconds, device=device, capture=capture)

    if result.get("status") != "ok":
        payload = {"word": word, "timestamp": datetime.now().isoformat(timespec="seconds"),
                   "status": result.get("status"), "reason": result.get("reason"),
                   "success": None, "feedback": "We couldn't hear you clearly. Want to try again?"}
        word_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        result["success"] = None
        result["word_json"] = str(word_json)
        return result

    est = result.get("segment_estimated", False)
    save_debug_plot(wav, result, out_dir / "spectrum.png")
    # Save the extracted segment in recordings.
    from Pronunciation_analysis import save_segment_clip
    save_segment_clip(wav, result, rec_dir / "fric.wav")

    jr = judge_mod.judge(result["features"], est)
    fb = feedback_mod.feedback(jr)
    gauges = gauge_mod.draw_all(jr, out_dir)

    payload = {
        "word": word,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "status": "ok",
        "success": jr["success"],
        "segment_estimated": est,
        "segment": result["segment"],
        "features": result["features"],
        "feedback": fb,
    }
    word_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    result["judge"] = jr
    result["success"] = jr["success"]
    result["feedback"] = fb
    result["gauges"] = gauges
    result["word_json"] = str(word_json)
    return result


def syll_record(syllable: str, order: int, seconds: float = 3.0,
                device=None, capture=None) -> dict:
    """Record and analyze one sound and save it in syllable_data.json."""
    import json
    from datetime import datetime

    data_dir = _data_dir()
    rec_dir = data_dir / "recordings" / "syllables"
    rec_dir.mkdir(parents=True, exist_ok=True)
    data_json = data_dir / "syllable_data.json"

    wav = rec_dir / f"syll_{order}_{syllable}.wav"
    result = record_and_analyze(wav, seconds=seconds, device=device, capture=capture)

    entry = {"syllable": syllable, "order": order,
             "timestamp": datetime.now().isoformat(timespec="seconds")}
    if result.get("status") == "ok":
        est = result.get("segment_estimated", False)
        entry["status"] = "ok"
        entry["segment_estimated"] = est
        entry["features"] = result["features"]
    else:
        entry["status"] = result.get("status")
        entry["reason"] = result.get("reason")

    # Replace an existing entry with this order or append a new one.
    records = []
    if data_json.exists():
        try:
            records = json.loads(data_json.read_text(encoding="utf-8"))
        except Exception:
            records = []
    records = [r for r in records if r.get("order") != order]
    records.append(entry)
    records.sort(key=lambda r: r.get("order", 0))
    data_json.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    result["syllable"] = syllable
    result["order"] = order
    result["recorded_count"] = len(records)
    return result


def syll_select(reset: bool = True) -> dict:
    """7개에서 best(가장 정확) + worst(가장 부정확) 선정.
    best: 정상 분석 중 z-score 합 최소.
    worst: 폴백(마찰음 약함) 중 랜덤, 폴백 없으면 z-score 합 최대.
    best 후보가 없거나 유효 글자가 2개 미만이면 no_candidate(재녹음 유도).
    """
    import json, random


    data_dir = _data_dir()
    out_dir = data_dir / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    data_json = data_dir / "syllable_data.json"
    result_json = data_dir / "syllable_result.json"

    if not data_json.exists():
        return {"status": "no_data", "message": "There are no recordings."}
    records = json.loads(data_json.read_text(encoding="utf-8"))


    # Sum the z-scores for Judge.USED_FEATURES.

    ref = judge_mod.REFERENCE
    used = judge_mod.USED_FEATURES

    scores = {}
    fallback_syls = []
    excluded = []
    for r in records:
        syl = r.get("syllable")

        if r.get("status") != "ok":

            excluded.append(syl)
            continue
        if r.get("segment_estimated"):
            fallback_syls.append(syl)
            continue
        feats = r.get("features", {})
        z, ok = 0.0, True
        for f in used:
            if f not in feats or feats[f] is None:
                ok = False
                break
            m, s = ref[f]["mean"], ref[f]["std"]
            z += abs(feats[f] - m) / s
        if ok:
            scores[syl] = round(z, 3)
        else:
            excluded.append(syl)


    valid_count = len(scores) + len(fallback_syls)
    if len(scores) < 2:
        return {"status": "no_candidate",
                "message": "Please re-evaluate",
                "scores": scores, "fallback": fallback_syls, "excluded": excluded}

    best = min(scores, key=scores.get)

    worst_pool = [s for s in fallback_syls if s != best]
    if worst_pool:
        worst = random.choice(worst_pool)
    else:
        other = {s: z for s, z in scores.items() if s != best}
        worst = max(other, key=other.get) if other else best


    img_path = out_dir / "selected_syllable.png"
    _draw_syllable_image(best, worst, img_path)

    out = {"status": "ok",
           "best": best, "worst": worst,
           "image": str(img_path).replace("\\", "/")}
    result_json.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")


    if reset:   # Clear accumulated data for the next assessment.

        data_json.unlink(missing_ok=True)
    return out





def _draw_syllable_image(best: str, worst: str, out_png) -> None:
    """Draw the selected sound in large type on a transparent PNG."""

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patheffects as pe

    # Use the same Hangul font as Gauge.

    try:
        from Gauge import _ensure_font
        fam = _ensure_font()
        if fam:
            plt.rcParams["font.family"] = fam
    except Exception:
        pass

    fig, axes = plt.subplots(1, 2, figsize=(10, 5), dpi=100)
    fig.subplots_adjust(wspace=0.6)
    for ax, syl, label in ((axes[0], best, "Highest accuracy syllable"),
                           (axes[1], worst, "Lowest accuracy syllable")):
        ax.axis("off")
        ax.add_patch(plt.Rectangle((0.08, 0.30), 0.84, 0.62, fill=False,
                                    edgecolor="#FFFFFF", linewidth=3))
        # 글자는 네모 안에 들어오도록 약간 작게
        t = ax.text(0.5, 0.61, syl, ha="center", va="center",
                    fontsize=95, color="#342743")
        t.set_path_effects([pe.withStroke(linewidth=4, foreground="#FFFFFF")])
        # 라벨은 네모 아래, 작게
        lbl = ax.text(0.5, 0.12, label, ha="center", va="center",
                      fontsize=17, color="#342743", fontweight="bold")
        lbl.set_path_effects([pe.withStroke(linewidth=3, foreground="#FFFFFF")])
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)

    fig.savefig(str(out_png), dpi=100, transparent=True, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "devices":
        out = list_input_devices()
    elif cmd == "mic-test":
        out = run_mic_test()
    elif cmd == "record":
        out = record_and_analyze(sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 3.0)
    elif cmd == "analyze":
        out = analyze_file(sys.argv[2])
    elif cmd == "run":   # Record and render gauges (default executable workflow).
        out_dir = sys.argv[2] if len(sys.argv) > 2 else "out"
        sec = float(sys.argv[3]) if len(sys.argv) > 3 else 3.0
        out = record_judge_visualize(out_dir, seconds=sec)
    elif cmd == "try":   # Record and write word.json for Ren'Py.
        word = sys.argv[2] if len(sys.argv) > 2 else "사과"
        sec = float(sys.argv[3]) if len(sys.argv) > 3 else 3.0
        out = record_try(word, seconds=sec)
    elif cmd == "syll-record":   # Record and store one sound: syll-record SOUND ORDER [SECONDS].
        syl = sys.argv[2]
        order = int(sys.argv[3])
        sec = float(sys.argv[4]) if len(sys.argv) > 4 else 3.0
        out = syll_record(syl, order, seconds=sec)
    elif cmd == "syll-select":   # Pick the best of seven sounds and render it.
        out = syll_select()
    elif cmd == "judge":          # Stage 3: analyze and score an existing WAV (JSON only).
        result = analyze_file(sys.argv[2])
        if result.get("status") == "ok":
            result["judge"] = judge_mod.judge(result["features"], result.get("segment_estimated", False))
            result["success"] = result["judge"]["success"]
            result["feedback"] = feedback_mod.feedback(result["judge"])
        out = result
    elif cmd == "visualize":      # Stage 4: score an existing WAV and render gauges.
        out_dir = sys.argv[3] if len(sys.argv) > 3 else "out"
        result = analyze_file(sys.argv[2])
        if result.get("status") == "ok":
            jr = judge_mod.judge(result["features"], result.get("segment_estimated", False))
            result["judge"] = jr
            result["success"] = jr["success"]
            result["feedback"] = feedback_mod.feedback(jr)
            result["gauges"] = gauge_mod.draw_all(jr, out_dir)
        out = result
    else:
        out = {"usage": "voice_engine [devices | mic-test | record OUT.wav SEC | analyze FILE | judge FILE | visualize FILE OUT_DIR | run OUT_DIR SEC | try WORD SEC]"}
    print(json.dumps(out, ensure_ascii=False, indent=2))