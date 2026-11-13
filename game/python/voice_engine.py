"""Ren'Py(또는 exe)가 부르는 단일 창구. 반환값은 모두 JSON 으로 바꿀 수 있는 dict.

주요 함수
    run_mic_test()                      마이크 테스트
    record_and_analyze(path, sec)       녹음 -> 분석 (지표까지)
    record_judge_visualize(out_dir)     녹음 -> 분석 -> 판정 -> 게이지 이미지 -> 피드백 (한 번에)
    analyze_file(path)                  이미 있는 WAV 분석 (테스트용)

exe 로 묶으면 (PyInstaller) 이 파일이 진입점.  예:
    voice_engine.exe run OUT_DIR [SEC]     # 녹음부터 이미지까지
    voice_engine.exe mic-test
    voice_engine.exe devices
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:  # 패키지로 import 될 때 / 같은 폴더에서 실행될 때 둘 다 지원
    from .Audio_recording import list_input_devices, mic_test, record
    from .Pronunciation_analysis import analyze, save_debug_plot
    from . import judge as judge_mod
    from . import gauge as gauge_mod
    from . import feedback as feedback_mod
except ImportError:
    from Audio_recording import list_input_devices, mic_test, record
    from Pronunciation_analysis import analyze, save_debug_plot
    import Judge as judge_mod
    import Gauge as gauge_mod
    import Feedback as feedback_mod

SYLLABLES = ("시", "세", "사", "서", "소", "수", "스")

def _data_dir() -> Path:
    """data 폴더 위치. exe(frozen)면 exe 폴더 기준, 아니면 이 파일 기준."""
    if getattr(sys, "frozen", False):
        # onedir exe: game/python/voice_engine/voice_engine.exe -> game/data
        base = Path(sys.executable).resolve().parent.parent.parent
    else:
        # 스크립트: game/python/Voice_engine.py -> game/data
        base = Path(__file__).resolve().parent.parent
    return base / "data"


def run_mic_test(seconds: float = 2.0, device=None) -> dict:
    return mic_test(seconds=seconds, device=device)


def record_and_analyze(wav_path, seconds: float = 3.0, device=None, capture=None) -> dict:
    kwargs = {"capture": capture} if capture is not None else {}
    rec = record(wav_path, seconds=seconds, device=device, **kwargs)
    if not rec["ok"]:
        return {"status": "unmeasurable", "reason": rec["status"], "message": rec["message"]}
    if rec["status"] in ("clipping", "too_quiet"):   # 소리가 찌그러졌거나 너무 작으면 분석하지 않는다
        return {"status": "unmeasurable", "reason": rec["status"], "message": rec["message"],
                "recording": rec["report"]}
    result = analyze(wav_path)
    result["recording"] = rec["report"]
    return result


def analyze_file(wav_path) -> dict:
    return analyze(wav_path)


def record_judge_visualize(out_dir, seconds: float = 3.0, device=None, capture=None, make_plot=False) -> dict:
    """녹음 -> 분석 -> 판정 -> 게이지 이미지 -> 피드백 까지 한 번에.

    out_dir 에 녹음(rec.wav)과 게이지 PNG 들을 저장한다.
    반환 JSON 에 판정 결과, 게이지 이미지 경로, 피드백 문구가 들어 있다.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    wav_path = out_dir / "rec.wav"

    result = record_and_analyze(wav_path, seconds=seconds, device=device, capture=capture)

    # 분석이 안 되면(측정 불가 등) 판정/게이지 없이 그대로 돌려준다
    if result.get("status") != "ok":
        result["success"] = None
        result["feedback"] = "소리를 잘 듣지 못했어요. 다시 말해 볼까요?"
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
    """try_record.py 와 같은 동작: 녹음->분석->스펙트럼/분리음성->판정->게이지->word.json.

    저장 위치:
      녹음 원본 + 분리음성 -> data/recordings/
      스펙트럼 + 게이지    -> data/out/
      분석 지표 JSON       -> data/word.json (덮어쓰기)
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
                   "success": None, "feedback": "소리를 잘 듣지 못했어요. 다시 말해 볼까요?"}
        word_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        result["success"] = None
        result["word_json"] = str(word_json)
        return result

    est = result.get("segment_estimated", False)
    save_debug_plot(wav, result, out_dir / "spectrum.png")
    # 분리 음성 -> recordings
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
    """음절 하나 녹음·분석 후 syllable_data.json 에 누적한다."""
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

    # 기존 누적 읽어서 같은 글자(order) 있으면 교체, 없으면 추가
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
    """syllable_data.json 의 7개에서 z-score 합 최소 글자 선정 + 글자 이미지 생성."""
    import json

    data_dir = _data_dir()
    out_dir = data_dir / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    data_json = data_dir / "syllable_data.json"
    result_json = data_dir / "syllable_result.json"

    if not data_json.exists():
        return {"status": "no_data", "message": "녹음 데이터가 없습니다."}
    records = json.loads(data_json.read_text(encoding="utf-8"))

    # z-score 합 계산 (판정에 쓰는 지표 = Judge.USED_FEATURES)
    ref = judge_mod.REFERENCE
    used = judge_mod.USED_FEATURES

    scores, excluded = {}, []
    for r in records:
        syl = r.get("syllable")
        # 분석 실패 or 폴백(마찰음 약함)은 후보 제외
        if r.get("status") != "ok" or r.get("segment_estimated"):
            excluded.append(syl)
            continue
        feats = r.get("features", {})
        z = 0.0
        ok = True
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

    if not scores:
        return {"status": "no_candidate", "message": "선정 가능한 글자가 없습니다.",
                "excluded": excluded}

    selected = min(scores, key=scores.get)   # z 합 최소 = 가장 정확
    img_path = out_dir / "selected_syllable.png"
    _draw_syllable_image(selected, img_path)

    out = {"status": "ok", "selected": selected,
           "image": str(img_path).replace("\\", "/"),
           "scores": scores, "excluded": excluded}
    result_json.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    if reset:   # 다음 평가를 위해 누적 데이터 비움
        data_json.unlink(missing_ok=True)
    return out


def _draw_syllable_image(syllable: str, out_png) -> None:
    """선정된 글자를 큰 텍스트로 그린 투명 PNG 저장."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patheffects as pe
    # Gauge 와 같은 한글 폰트 사용
    try:
        from Gauge import _ensure_font
        fam = _ensure_font()
        if fam:
            plt.rcParams["font.family"] = fam
    except Exception:
        pass

    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    ax.axis("off")
    txt = ax.text(0.5, 0.5, syllable, ha="center", va="center",
            fontsize=200, color="#FFFFFF")
    txt.set_path_effects([pe.withStroke(linewidth=8, foreground="#241D35")])
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
    elif cmd == "run":   # 녹음부터 이미지까지 (exe 기본 사용)
        out_dir = sys.argv[2] if len(sys.argv) > 2 else "out"
        sec = float(sys.argv[3]) if len(sys.argv) > 3 else 3.0
        out = record_judge_visualize(out_dir, seconds=sec)
    elif cmd == "try":   # 녹음부터 word.json 까지 (렌파이가 부르는 기본)
        word = sys.argv[2] if len(sys.argv) > 2 else "사과"
        sec = float(sys.argv[3]) if len(sys.argv) > 3 else 3.0
        out = record_try(word, seconds=sec)
    elif cmd == "syll-record":   # 음절 하나 녹음·누적:  syll-record 글자 순번 [초]
        syl = sys.argv[2]
        order = int(sys.argv[3])
        sec = float(sys.argv[4]) if len(sys.argv) > 4 else 3.0
        out = syll_record(syl, order, seconds=sec)
    elif cmd == "syll-select":   # 7개에서 최고 선정 + 글자 이미지
        out = syll_select()
    elif cmd == "judge":          # 3단계: 이미 있는 WAV -> 분석 + 판정 (JSON만)
        result = analyze_file(sys.argv[2])
        if result.get("status") == "ok":
            result["judge"] = judge_mod.judge(result["features"], result.get("segment_estimated", False))
            result["success"] = result["judge"]["success"]
            result["feedback"] = feedback_mod.feedback(result["judge"])
        out = result
    elif cmd == "visualize":      # 4단계: 이미 있는 WAV -> 판정 + 게이지 이미지
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