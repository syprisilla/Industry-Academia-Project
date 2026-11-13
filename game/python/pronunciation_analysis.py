"""/ㅅ/ 마찰구간 분리 + 음향 지표 추출.

* 이 모듈은 '분석해서 값을 돌려주는 것'까지만 한다. 성공/실패 판정(z-score)은 하지 않는다.
* 지표 계산은 Parselmouth(Praat) 를 우선 쓰고, 설치가 안 되면 numpy 구현으로 자동 대체한다
  (두 구현이 같은 값을 내는 것은 test_synthetic.py 에서 확인).
* 아래 상수는 '임시값' 이다. 팀원/아동 녹음으로 조정할 것.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

# ---------------- 임시 상수 ----------------
FRAME_WIN_S = 0.020          # 프레임 길이
FRAME_HOP_S = 0.005          # 프레임 간격
HF_MIN_HZ = 4000.0           # 고주파 대역 시작
LF_BAND_HZ = (80.0, 2000.0)  # 저주파 대역
ACTIVE_MARGIN_DB = 8.0       # 주변 소음보다 이만큼 커야 '소리가 있다'
HILO_MIN_DB = 0.0            # 고주파/저주파 에너지 비가 이 값보다 커야 마찰음 후보
MIN_DYNAMIC_DB = 20.0        # 가장 큰 소리와 소음의 차이가 이보다 작으면 측정 불가
MIN_FRIC_S = 0.030           # 마찰구간 최소 길이
MAX_FRIC_S = 0.500           # 마찰구간 최대 길이
MIN_SR = 16000
PRE_EMPH_HZ = 50.0           # Han et al.(2024) 처럼 pre-emphasis 후 스펙트럼 계산
MOMENT_POWER = 2.0           # Praat 권고 power 2.0
FALLBACK_ACTIVE_MARGIN_DB = 3.0   # 폴백 시 소리 시작 판단 마진 (약한 바람소리용)
FALLBACK_VOWEL_DB = 15.0          # peak - 이 값 이상이면 모음으로 간주
FALLBACK_FIXED_S = 0.120          # ㅅ 탈락 시 모음 직전 고정 길이


def load_wav(path) -> tuple[np.ndarray, int]:
    """WAV(PCM) 파일을 모노 배열로 읽는다."""
    import soundfile as sf

    x, sr = sf.read(str(path), dtype="float64", always_2d=True)
    return x.mean(axis=1), int(sr)


# ---------------- 프레임 단위 특징 ----------------
def _frame_features(x: np.ndarray, sr: int):
    w = int(round(FRAME_WIN_S * sr))
    h = int(round(FRAME_HOP_S * sr))
    n = 1 + (len(x) - w) // h
    idx = np.arange(w)[None, :] + h * np.arange(n)[:, None]
    frames = x[idx]
    e_db = 10 * np.log10(np.mean(frames ** 2, axis=1) + 1e-12)
    power = np.abs(np.fft.rfft(frames * np.hanning(w), axis=1)) ** 2
    f = np.fft.rfftfreq(w, 1.0 / sr)
    hi = power[:, f >= HF_MIN_HZ].sum(axis=1)
    lo = power[:, (f >= LF_BAND_HZ[0]) & (f < LF_BAND_HZ[1])].sum(axis=1)
    hilo_db = 10 * np.log10((hi + 1e-12) / (lo + 1e-12))
    t = (np.arange(n) * h + w / 2) / sr          # 프레임 중심 시각
    return t, e_db, hilo_db


def _voiced_mask(x: np.ndarray, sr: int, t: np.ndarray):
    """Parselmouth 피치 추적으로 유성음(모음) 프레임 표시. 없으면 None."""
    try:
        import parselmouth
    except ImportError:
        return None
    snd = parselmouth.Sound(x, sampling_frequency=sr)
    pitch = snd.to_pitch(time_step=FRAME_HOP_S, pitch_floor=100, pitch_ceiling=600)
    f0 = np.array([pitch.get_value_at_time(tt) for tt in t], dtype=float)
    return ~np.isnan(f0)


def _longest_run(mask: np.ndarray):
    best, i = None, 0
    while i < len(mask):
        if mask[i]:
            j = i
            while j + 1 < len(mask) and mask[j + 1]:
                j += 1
            if best is None or (j - i) > (best[1] - best[0]):
                best = (i, j)
            i = j + 1
        else:
            i += 1
    return best

def _estimate_slot(t, e_db, floor, peak, voiced):
    """모음 시작점에서 뒤로 FALLBACK_FIXED_S 만큼 뗀 /ㅅ/ 자리. 못 찾으면 None."""
    loud = e_db >= peak - FALLBACK_VOWEL_DB
    vi = np.where(loud & voiced)[0] if voiced is not None else np.where(loud)[0]
    if len(vi) == 0 and voiced is not None:      # 피치 추적 실패 시 에너지만 사용
        vi = np.where(loud)[0]
    if len(vi) == 0:
        return None
    v = int(vi[0])
    end_s = float(t[v] - FRAME_WIN_S / 2)        # 모음 프레임 시작 직전 = 끝점(고정)
    start_s = max(0.0, end_s - FALLBACK_FIXED_S) # 끝에서 뒤로 고정 길이만큼만
    if end_s - start_s < MIN_FRIC_S:
        return None
    return start_s, end_s


def _measure(x, sr, t, active, start_s, end_s, backend):
    """구간 -> 음향 지표 dict + 사용한 백엔드."""
    a, b = int(start_s * sr), int(end_s * sr)
    seg = x[a:b]
    cog, sd, skew, kurt, used = spectral_moments(seg, sr, backend)
    idx = np.where(active)[0]
    wa = int(max(0, (t[idx[0]] - FRAME_WIN_S / 2) * sr))
    wb = int(min(len(x), (t[idx[-1]] + FRAME_WIN_S / 2) * sr))
    whole_energy = float(np.sum(x[wa:wb] ** 2)) + 1e-18
    norm_energy = float(min(1.0, np.sum(seg ** 2) / whole_energy))
    feats = {"duration_ms": (end_s - start_s) * 1000.0, "norm_energy": norm_energy,
             "cog_hz": float(cog), "sd_hz": float(sd),
             "skewness": float(skew), "kurtosis": float(kurt)}
    return feats, used


# ---------------- 스펙트럼 모멘트 ----------------
def spectral_moments(seg: np.ndarray, sr: int, backend: str = "auto"):
    """pre-emphasis -> 스펙트럼(fast) -> (무게중심, 표준편차, 왜도, 첨도, 사용한 백엔드)."""
    if backend in ("auto", "parselmouth"):
        try:
            import parselmouth

            s = parselmouth.Sound(seg, sampling_frequency=sr)
            s.pre_emphasize(from_frequency=PRE_EMPH_HZ, normalize=False)
            sp = s.to_spectrum(fast=True)
            return (sp.get_centre_of_gravity(MOMENT_POWER), sp.get_standard_deviation(MOMENT_POWER),
                    sp.get_skewness(MOMENT_POWER), sp.get_kurtosis(MOMENT_POWER), "parselmouth")
        except ImportError:
            if backend == "parselmouth":
                raise
    # numpy 구현 (Praat 과 같은 pre-emphasis 계수, 2의 거듭제곱 FFT 길이)
    y = seg.astype(float).copy()
    alpha = np.exp(-2 * np.pi * PRE_EMPH_HZ / sr)
    y = np.concatenate([[y[0]], y[1:] - alpha * y[:-1]])
    nfft = 1 << int(np.ceil(np.log2(len(y))))
    p = np.abs(np.fft.rfft(y, nfft)) ** MOMENT_POWER
    f = np.fft.rfftfreq(nfft, 1.0 / sr)
    p = p / p.sum()
    cog = float((f * p).sum())
    sd = float(np.sqrt((((f - cog) ** 2) * p).sum()))
    skew = float((((f - cog) ** 3) * p).sum() / sd ** 3)
    kurt = float((((f - cog) ** 4) * p).sum() / sd ** 4 - 3.0)
    return cog, sd, skew, kurt, "numpy"


# ---------------- 메인 분석 ----------------
def _result(status, reason=None, **extra):
    out = {"status": status, "reason": reason}
    out.update(extra)
    return out


def analyze(source, sr: int | None = None, backend: str = "auto") -> dict:
    """WAV 경로(또는 배열+sr)를 받아 마찰구간과 음향 지표를 돌려준다.

    status:  "ok" | "unmeasurable"(소음/작은 소리 등) | "segmentation_failed"(마찰구간을 못 찾음)
    """
    warnings = []
    if isinstance(source, (str, Path)):
        x, sr = load_wav(source)
    else:
        x = np.asarray(source, dtype=float)
    if sr < MIN_SR:
        return _result("unmeasurable", "sample_rate_too_low", sr=sr)
    if sr < 32000:
        warnings.append("샘플레이트가 낮아 /ㅅ/ 고주파가 잘릴 수 있음(권장 44.1kHz 이상)")
    if len(x) < int(0.2 * sr):
        return _result("unmeasurable", "too_short", sr=sr)

    t, e_db, hilo_db = _frame_features(x, sr)
    floor = float(np.percentile(e_db, 10))       # 주변 소음 레벨
    peak = float(np.percentile(e_db, 98))        # 가장 큰 소리(모음) 레벨
    quality = {"noise_floor_db": floor, "peak_db": peak, "dynamic_db": peak - floor}
    if peak - floor < MIN_DYNAMIC_DB:
        return _result("unmeasurable", "too_quiet_or_noisy", quality=quality, warnings=warnings)


    active = e_db > floor + ACTIVE_MARGIN_DB
    voiced = _voiced_mask(x, sr, t)
    mask = active & (hilo_db > HILO_MIN_DB)
    if voiced is not None:
        mask &= ~voiced
    run = _longest_run(mask)

    fail_reason = None
    if run is None:
        fail_reason = "no_frication"
    else:
        start_s = float(t[run[0]] - FRAME_HOP_S / 2)
        end_s = float(t[run[1]] + FRAME_HOP_S / 2)
        dur = end_s - start_s
        if dur < MIN_FRIC_S:
            fail_reason = "too_short"
        elif dur > MAX_FRIC_S:
            return _result("segmentation_failed", "too_long",
                           segment={"start_s": start_s, "end_s": end_s},
                           quality=quality, warnings=warnings)

    if fail_reason is None:                      # 정상 검출
        feats, used = _measure(x, sr, t, active, start_s, end_s, backend)
        return _result("ok", None, sr=sr, backend=used, segment_estimated=False,
                       segment={"start_s": start_s, "end_s": end_s},
                       features=feats, quality=quality, warnings=warnings)

    # 폴백: /ㅅ/ 자리 추정
    slot = _estimate_slot(t, e_db, floor, peak, voiced)
    if slot is None:
        return _result("segmentation_failed", fail_reason, quality=quality, warnings=warnings)
    start_s, end_s = slot
    active_fb = e_db > floor + FALLBACK_ACTIVE_MARGIN_DB
    feats, used = _measure(x, sr, t, active_fb, start_s, end_s, backend)
    warnings.append("마찰구간 미검출 → 모음 직전 구간으로 추정 분석")
    return _result("ok", None, sr=sr, backend=used,
                   segment_estimated=True, fallback_reason=fail_reason,
                   segment={"start_s": start_s, "end_s": end_s},
                   features=feats, quality=quality, warnings=warnings)


def save_debug_plot(wav_path, result: dict, out_png) -> None:
    """파형 + 스펙트로그램에 분리한 마찰구간을 표시해 저장 (눈으로 검수용)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    x, sr = load_wav(wav_path)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 5), sharex=True)
    a1.plot(np.arange(len(x)) / sr, x, lw=0.5)
    a2.specgram(x, NFFT=512, Fs=sr, noverlap=384, cmap="magma")
    a2.set_ylim(0, min(sr / 2, 12000))
    seg = result.get("segment")
    if seg:
        for ax in (a1, a2):
            ax.axvspan(seg["start_s"], seg["end_s"], color="cyan", alpha=0.25)
    a1.set_title(f"status={result['status']} reason={result.get('reason')}")
    a2.set_xlabel("time (s)")
    fig.tight_layout()
    fig.savefig(str(out_png), dpi=120)
    plt.close(fig)

def save_segment_clip(wav_path, result: dict, out_wav) -> str | None:
    """분석이 찾은 마찰구간만 잘라 WAV 로 저장한다 (귀로 확인용). 구간이 없으면 None."""
    import soundfile as sf

    seg = result.get("segment")
    if not seg:
        return None
    x, sr = load_wav(wav_path)
    a, b = int(seg["start_s"] * sr), int(seg["end_s"] * sr)
    clip = x[a:b]
    out_wav = Path(out_wav)
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(out_wav), clip, sr, subtype="PCM_16")
    return str(out_wav)


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="WAV 하나를 분석해 JSON 출력")
    ap.add_argument("wav")
    ap.add_argument("--plot", help="디버그 PNG 저장 경로")
    ap.add_argument("--clip", help="마찰구간만 잘라 WAV 저장 경로")
    ap.add_argument("--backend", default="auto", choices=["auto", "parselmouth", "numpy"])
    args = ap.parse_args()
    res = analyze(args.wav, backend=args.backend)
    if args.plot:
        save_debug_plot(args.wav, res, args.plot)
    if args.clip:
        save_segment_clip(args.wav, res, args.clip)
    print(json.dumps(res, ensure_ascii=False, indent=2))