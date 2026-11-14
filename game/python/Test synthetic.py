"""마이크/실제 아동 음성 없이 돌려 보는 합성 신호 테스트.   실행:  python test_synthetic.py

확인하는 것
 1) Parselmouth 백엔드와 numpy 백엔드가 같은 지표를 내는가
 2) 합성 단어(무음 + /ㅅ/ 비슷한 잡음 + 모음)에서 마찰구간 경계를 잘 찾는가, 소음이 크면 '측정 불가'로 빠지는가
 3) 마이크 테스트 판정(ok / clipping / too_quiet / noisy / no_device)
 4) record_and_analyze 전체 흐름(가짜 마이크 사용)이 JSON 으로 나오는가
주의: 합성 신호라서 실제 아동 음성에서의 성능을 보장하지 않는다.
"""
import json
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

import Audio_recording as ar
import Pronunciation_analysis as pa
from Voice_engine import record_and_analyze, record_judge_visualize
import Judge as judge_mod
import Gauge as gauge_mod
import Feedback as feedback_mod

SR = 48000
rng = np.random.default_rng(3)


def make_word(snr_db, lead_s=0.3, fric_s=None):
    """무음(lead) + 마찰 잡음(-10dB re 모음) + 모음. 배경 소음은 모음 대비 snr_db."""
    fric_s = fric_s or rng.uniform(0.10, 0.20)
    f0 = rng.uniform(200, 320)
    nz = rng.normal(0, 1, int(fric_s * SR))
    nz = np.diff(nz, prepend=0)
    nz = np.diff(nz, prepend=0)
    t = np.arange(int(0.30 * SR)) / SR
    vow = sum((1 / k) * np.sin(2 * np.pi * f0 * k * t) for k in range(1, 9))
    vow = vow / np.sqrt(np.mean(vow ** 2)) * 0.2
    nz = nz / np.sqrt(np.mean(nz ** 2)) * 0.2 * 0.3
    sig = np.concatenate([np.zeros(int(lead_s * SR)), nz, vow])
    sig = sig + rng.normal(0, 0.2 / (10 ** (snr_db / 20)), sig.size)
    return sig, lead_s, lead_s + fric_s

def make_word_weak(kind, lead_s=0.3, fric_s=None):
    """ㅅ 탈락/약화 단어. kind='drop'(완전 탈락) | 'weak'(약한 마찰)."""
    fric_s = fric_s or rng.uniform(0.10, 0.20)
    f0 = rng.uniform(200, 320)
    nz = rng.normal(0, 1, int(fric_s * SR))
    nz = np.diff(nz, prepend=0)
    nz = np.diff(nz, prepend=0)
    t = np.arange(int(0.30 * SR)) / SR
    vow = sum((1 / k) * np.sin(2 * np.pi * f0 * k * t) for k in range(1, 9))
    vow = vow / np.sqrt(np.mean(vow ** 2)) * 0.2
    scale = {"drop": 0.0, "weak": 0.05}[kind]        # 정상은 0.3
    nz = nz / np.sqrt(np.mean(nz ** 2)) * 0.2 * scale if scale else np.zeros_like(nz)
    sig = np.concatenate([np.zeros(int(lead_s * SR)), nz, vow])
    sig = sig + rng.normal(0, 0.2 / (10 ** (40 / 20)), sig.size)   # SNR 40dB 고정
    return sig, lead_s, lead_s + fric_s

def test_backends_equal(tmp):
    sig, _, _ = make_word(40)
    p = tmp / "w.wav"
    sf.write(str(p), sig, SR, subtype="PCM_16")
    a = pa.analyze(p, backend="parselmouth")["features"]
    b = pa.analyze(p, backend="numpy")["features"]
    for k in a:
        assert np.isclose(a[k], b[k], rtol=1e-6, atol=1e-6), (k, a[k], b[k])
    print("1) 백엔드 일치: OK ", {k: round(v, 2) for k, v in a.items()})


def test_segmentation(tmp):
    print("2) 마찰구간 경계 오차 / 판정 (단어 40개씩)")
    print("   모음 대비 소음  ok(경계 40ms 이내)  ok인데 틀림  unmeasurable  segmentation_failed")
    for snr in (40, 30, 20, 10):
        good = wrong = unm = fail = 0
        errs = []
        for i in range(40):
            sig, s0, e0 = make_word(snr)
            r = pa.analyze(sig, sr=SR)
            if r["status"] == "unmeasurable":
                unm += 1
            elif r["status"] == "segmentation_failed":
                fail += 1
            else:
                es = abs(r["segment"]["start_s"] - s0) * 1000
                ee = abs(r["segment"]["end_s"] - e0) * 1000
                if es < 40 and ee < 40:
                    good += 1
                    errs.append((es, ee))
                else:
                    wrong += 1
        med = np.median(errs, axis=0) if errs else (float("nan"),) * 2
        print(f"   {snr:>4} dB       {good:>3} (시작 {med[0]:.1f} / 끝 {med[1]:.1f} ms)   {wrong:>3}         {unm:>3}           {fail:>3}")
        if snr >= 30:
            assert good >= 38, "소음이 작을 때는 거의 다 맞아야 함"
        assert wrong <= 4, "틀린 값을 ok 로 돌려주는 경우가 많으면 안 됨"

def test_fallback(tmp):
    print("5) 폴백(마찰음 약함/탈락) — 분석은 되고 success는 False여야 함 (각 30개)")
    for kind in ("drop", "weak"):
        est = ok_status = judged_false = 0
        for _ in range(30):
            sig, _, _ = make_word_weak(kind)
            r = pa.analyze(sig, sr=SR)
            if r["status"] != "ok":
                continue
            ok_status += 1
            if r.get("segment_estimated"):
                est += 1
            jr = judge_mod.judge(r["features"], r.get("segment_estimated", False))
            if jr["success"] is False:
                judged_false += 1
        print(f"   {kind:>4}:  status=ok {ok_status:>3}   폴백추정 {est:>3}   success=False {judged_false:>3}")
        # 경로는 둘 중 하나: (a) 약한 구간을 검출해서 값으로 실패, (b) 못 찾아 폴백으로 실패.
        # 어느 쪽이든 '분석까지 가고(ok) 전부 실패(success=False)' 이기만 하면 목표 달성.
        assert ok_status >= 25, f"{kind}: 분석 단계(ok)까지 못 간 게 많음"
        assert judged_false == ok_status, f"{kind}: ok인데 성공 처리된 게 있음(목표 위반)"

def test_mic_test():
    def room(level_db=-20, noise_db=-70, peak_boost=1.0, sr=SR):
        n = 2 * sr
        x = rng.normal(0, 10 ** (noise_db / 20), n)
        t = np.arange(int(0.8 * sr)) / sr
        voice = 10 ** (level_db / 20) * np.sqrt(2) * np.sin(2 * np.pi * 250 * t)
        x[int(0.6 * sr): int(0.6 * sr) + len(t)] += voice * peak_boost
        return x.astype("float32")

    cases = {
        "ok": room(),
        "clipping": room(level_db=-3, peak_boost=1.4),
        "too_quiet": room(level_db=-55, noise_db=-90),
        "noisy": room(level_db=-25, noise_db=-35),
    }
    for want, x in cases.items():
        r = ar.mic_test(capture=lambda s, sr, d, x=x: (x, SR))
        assert r["status"] == want, (want, r)
    def boom(*a):
        raise OSError("no mic")
    assert ar.mic_test(capture=boom)["status"] == "no_device"
    print("3) 마이크 테스트 판정: OK (ok/clipping/too_quiet/noisy/no_device)")


def test_pipeline(tmp):
    sig, _, _ = make_word(40, lead_s=0.4)
    sig = (sig / np.max(np.abs(sig)) * 0.5).astype("float32")      # 최대치 약 -6 dBFS
    out = record_and_analyze(tmp / "rec.wav", seconds=1.0, capture=lambda s, sr, d: (sig, SR))
    json.dumps(out, ensure_ascii=False)                              # JSON 직렬화 확인
    assert out["status"] == "ok", out
    print("4) 녹음->분석 전체 흐름: OK ", json.dumps(out["features"], ensure_ascii=False))


def test_judge_and_gauge(tmp):
    # CoG/분산을 기준 평균으로 넣으면 범위 안 -> success
    feats_ok = {"cog_hz": 8884.0, "sd_hz": 2777.0, "skewness": 0.2, "kurtosis": 1.5,
                "duration_ms": 150.0, "norm_energy": 0.78}
    jr = judge_mod.judge(feats_ok)
    assert jr["success"] is True and set(jr["per_feature"]) == {"cog_hz", "sd_hz"}, jr
    assert feedback_mod.feedback(jr).startswith("좋아요"), feedback_mod.feedback(jr)

    # CoG를 아주 낮게 -> 범위 밖, direction low, 실패
    feats_bad = dict(feats_ok, cog_hz=3000.0)
    jr2 = judge_mod.judge(feats_bad)
    assert jr2["success"] is False and jr2["per_feature"]["cog_hz"]["direction"] == "low", jr2

    # 게이지 PNG 2장 생성
    paths = gauge_mod.draw_all(jr2, tmp)
    assert set(paths) == {"cog_hz", "sd_hz"}, paths
    for p in paths.values():
        assert Path(p).exists() and Path(p).stat().st_size > 0
    # 폴백이면 'ㅅ 소리를 내자' 쪽 문구가 나와야 함
    jr_fb = judge_mod.judge(feats_ok, segment_estimated=True)
    assert jr_fb["success"] is False, jr_fb
    assert "바람소리" in feedback_mod.feedback(jr_fb) or "ㅅ" in feedback_mod.feedback(jr_fb)
    print("6) 판정+게이지: OK ", {k: Path(v).name for k, v in paths.items()})


def test_full_pipeline(tmp):
    sig, _, _ = make_word(40, lead_s=0.4)
    sig = (sig / np.max(np.abs(sig)) * 0.5).astype("float32")
    out = record_judge_visualize(tmp / "run", seconds=1.0, capture=lambda s, sr, d: (sig, SR))
    json.dumps(out, ensure_ascii=False)
    assert out["status"] == "ok" and "judge" in out and out["gauges"], out
    assert isinstance(out["feedback"], str)
    print("7) 녹음->판정->게이지 전체: OK  success =", out["success"], "| gauges:", len(out["gauges"]))


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        test_backends_equal(d)
        test_segmentation(d)
        test_fallback(d)
        test_mic_test()
        test_pipeline(d)
        test_judge_and_gauge(d)
        test_full_pipeline(d)
    print("\n모든 합성 테스트 통과")