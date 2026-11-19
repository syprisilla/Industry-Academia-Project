"""Isolate the ㅅ frication segment and extract acoustic features.

* Return acoustic features. The scoring module handles z-scores and pass/fail decisions.
* Prefer Parselmouth (Praat) and fall back to NumPy when it is unavailable.
  The synthetic tests compare the results of the two implementations.
* These constants are provisional. Tune them with recordings from the team and children.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

# ---------------- Provisional constants ----------------
FRAME_WIN_S = 0.020          # Frame length
FRAME_HOP_S = 0.005          # Frame hop
HF_MIN_HZ = 4000.0           # Start of the high-frequency band
LF_BAND_HZ = (80.0, 2000.0)  # Low-frequency band
ACTIVE_MARGIN_DB = 8.0       # Minimum level above the noise floor to count as active
HILO_MIN_DB = 0.0            # Minimum ratio of high- to low-band energy for frication
MIN_DYNAMIC_DB = 20.0        # Minimum gap between peak level and noise for measurement
MIN_FRIC_S = 0.030           # Minimum frication duration
MAX_FRIC_S = 0.500           # Maximum frication duration
MIN_SR = 16000
PRE_EMPH_HZ = 50.0           # Apply pre-emphasis before computing the spectrum, as in Han et al. (2024).
MOMENT_POWER = 2.0           # Praat's recommended power
FALLBACK_ACTIVE_MARGIN_DB = 3.0   # Fallback activity margin for weak frication
FALLBACK_VOWEL_DB = 15.0          # Treat levels within this margin of the peak as vowels.
FALLBACK_FIXED_S = 0.120          # Fixed duration before the vowel when ㅅ is missing


def load_wav(path) -> tuple[np.ndarray, int]:
    """Read a PCM WAV file into a mono array."""
    import soundfile as sf

    x, sr = sf.read(str(path), dtype="float64", always_2d=True)
    return x.mean(axis=1), int(sr)


# ---------------- Frame-level features ----------------
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
    t = (np.arange(n) * h + w / 2) / sr          # Frame center times
    return t, e_db, hilo_db


def _voiced_mask(x: np.ndarray, sr: int, t: np.ndarray):
    """Identify voiced vowel frames with Parselmouth pitch tracking, or return None."""
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
    """Estimate the ㅅ segment as FALLBACK_FIXED_S before vowel onset, or return None."""
    loud = e_db >= peak - FALLBACK_VOWEL_DB
    vi = np.where(loud & voiced)[0] if voiced is not None else np.where(loud)[0]
    if len(vi) == 0 and voiced is not None:      # Use energy alone if pitch tracking fails.
        vi = np.where(loud)[0]
    if len(vi) == 0:
        return None
    v = int(vi[0])
    end_s = float(t[v] - FRAME_WIN_S / 2)        # End just before the vowel frame begins.
    start_s = max(0.0, end_s - FALLBACK_FIXED_S) # Count back by the fixed duration.
    if end_s - start_s < MIN_FRIC_S:
        return None
    return start_s, end_s


def _measure(x, sr, t, active, start_s, end_s, backend):
    """Extract acoustic features from the segment and report the backend used."""
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


# ---------------- Spectral moments ----------------
def spectral_moments(seg: np.ndarray, sr: int, backend: str = "auto"):
    """Apply pre-emphasis and compute the spectrum, its four moments, and backend name."""
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
    # Match Praat's pre-emphasis coefficient and use a power-of-two FFT length.
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


# ---------------- Main analysis ----------------
def _result(status, reason=None, **extra):
    out = {"status": status, "reason": reason}
    out.update(extra)
    return out


def analyze(source, sr: int | None = None, backend: str = "auto") -> dict:
    """Return the frication segment and features from a WAV path or an array and sample rate.

    status: "ok", "unmeasurable" (noisy or quiet audio), or "segmentation_failed" (no frication found).
    """
    warnings = []
    if isinstance(source, (str, Path)):
        x, sr = load_wav(source)
    else:
        x = np.asarray(source, dtype=float)
    if sr < MIN_SR:
        return _result("unmeasurable", "sample_rate_too_low", sr=sr)
    if sr < 32000:
        warnings.append("Low sample rate may cut off high frequencies in ㅅ (44.1 kHz or higher recommended).")
    if len(x) < int(0.2 * sr):
        return _result("unmeasurable", "too_short", sr=sr)

    t, e_db, hilo_db = _frame_features(x, sr)
    floor = float(np.percentile(e_db, 10))       # Background noise level
    peak = float(np.percentile(e_db, 98))        # Peak level, typically the vowel
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

    if fail_reason is None:                      # Frication detected
        feats, used = _measure(x, sr, t, active, start_s, end_s, backend)
        return _result("ok", None, sr=sr, backend=used, segment_estimated=False,
                       segment={"start_s": start_s, "end_s": end_s},
                       features=feats, quality=quality, warnings=warnings)

    # Estimate the ㅅ segment as a fallback.
    slot = _estimate_slot(t, e_db, floor, peak, voiced)
    if slot is None:
        return _result("segmentation_failed", fail_reason, quality=quality, warnings=warnings)
    start_s, end_s = slot
    active_fb = e_db > floor + FALLBACK_ACTIVE_MARGIN_DB
    feats, used = _measure(x, sr, t, active_fb, start_s, end_s, backend)
    warnings.append("No frication segment detected. Using an estimated segment before the vowel.")
    return _result("ok", None, sr=sr, backend=used,
                   segment_estimated=True, fallback_reason=fail_reason,
                   segment={"start_s": start_s, "end_s": end_s},
                   features=feats, quality=quality, warnings=warnings)


def save_debug_plot(wav_path, result: dict, out_png) -> None:
    """Save a waveform and spectrogram with the frication segment marked for review."""
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
    """Save the extracted frication as WAV for listening, or return None if no segment exists."""
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

def extract_s_syllables(sentence: str) -> list:
    """문장에서 초성이 /ㅅ/(ㅆ 제외)인 음절을 시간순(왼→오)으로 추출.
    반환: [{"syllable": "손", "index": 0}, ...]  (index = 문장 내 몇 번째 /ㅅ/)
    """
    CHO = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ",
           "ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"]
    results = []
    idx = 0
    for ch in sentence:
        code = ord(ch)
        if 0xAC00 <= code <= 0xD7A3:          # 완성형 한글
            cho = (code - 0xAC00) // 588
            if CHO[cho] == "ㅅ":              # 초성이 ㅅ (ㅆ 아님)
                results.append({"syllable": ch, "index": idx})
                idx += 1
    return results


def detect_multiple_frication(source, sr: int | None = None, n: int = 2,
                              backend: str = "auto") -> list:
    """반복&지우기로 /ㅅ/ 마찰 구간 n개를 찾아 시간순으로 반환.
    각 구간 검출 후 그 구간을 무음(0)으로 덮어쓰고 다시 찾는다.
    폴백(추정) 구간은 받지 않고, 정상 검출만 모은다.

    반환: [{"start_s","end_s","features"}, ...]  (시작 시각 오름차순)
    """
    if isinstance(source, (str, Path)):
        x, sr = load_wav(source)
    else:
        x = np.asarray(source, dtype=float).copy()

    found = []
    for _ in range(max(1, n) * 2):   # n의 2배까지 시도(일부 실패 대비), found가 n개 차면 중단
        if len(found) >= n:
            break
        res = analyze(x, sr=sr, backend=backend)
        if res.get("status") != "ok":
            break                     # 더 이상 마찰 없음(unmeasurable/segmentation_failed)
        if res.get("segment_estimated"):
            # 폴백(추정)이면 진짜 마찰이 아님 → 그 구간만 지우고 계속 시도
            seg = res["segment"]
            a, b = int(seg["start_s"] * sr), int(seg["end_s"] * sr)
            x[a:b] = 0.0
            continue
        seg = res["segment"]
        found.append({"start_s": seg["start_s"], "end_s": seg["end_s"],
                      "features": res["features"]})
        # 찾은 구간을 무음으로 덮어 다음 반복에서 다시 안 잡히게 (길이 유지)
        a, b = int(seg["start_s"] * sr), int(seg["end_s"] * sr)
        x[a:b] = 0.0

    found.sort(key=lambda d: d["start_s"])   # 시간순(왼→오) 재배치
    return found


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Analyze a WAV file and output JSON")
    ap.add_argument("wav")
    ap.add_argument("--plot", help="Path to save the debug PNG")
    ap.add_argument("--clip", help="Path to save the extracted frication segment as a WAV")
    ap.add_argument("--backend", default="auto", choices=["auto", "parselmouth", "numpy"])
    args = ap.parse_args()
    res = analyze(args.wav, backend=args.backend)
    if args.plot:
        save_debug_plot(args.wav, res, args.plot)
    if args.clip:
        save_segment_clip(args.wav, res, args.clip)
    print(json.dumps(res, ensure_ascii=False, indent=2))