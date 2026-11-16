"""Microphone checks and recording for internal or external PC microphones.

- Import sounddevice and soundfile inside functions so this module loads without PortAudio.
- All return values are JSON-serializable dictionaries.
- CLIP, MIN, and SNR thresholds are provisional. Tune them with real microphone recordings.
- On Windows, turn off microphone and audio enhancements to preserve the airy ㅅ sound.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

DEFAULT_SR = 48000          # Capture the high frequencies of ㅅ at 48 kHz.
CLIP_PEAK_DBFS = -1.0       # Peaks above this threshold count as clipping.
MIN_SPEECH_DBFS = -45.0     # Speech RMS below this threshold is too quiet.
MIN_SNR_DB = 20.0           # A smaller gap between speech and background means too much noise.

_MESSAGES = {
    "ok": "Your mic sounds great!",
    "clipping": "That was too loud. Try moving a little farther from the mic.",
    "too_quiet": "That was too quiet. Try speaking a little louder.",
    "noisy": "It's noisy here. Try again somewhere quieter.",
    "no_device": "We couldn't find your mic. Check that it's connected.",
}


def _db(x: float) -> float:
    return float(20.0 * np.log10(max(float(x), 1e-12)))


def list_input_devices() -> list[dict]:
    """List audio input devices."""
    import sounddevice as sd

    devices = []
    for i, d in enumerate(sd.query_devices()):
        if d["max_input_channels"] > 0:
            devices.append({
                "index": i,
                "name": d["name"],
                "max_input_channels": int(d["max_input_channels"]),
                "default_samplerate": float(d["default_samplerate"]),
            })
    return devices


def _capture(seconds: float, sr: int, device=None):
    """Record for seconds and return a mono float32 array and the actual sample rate."""
    import sounddevice as sd

    try:  # Use the device default if it does not support 48 kHz.
        sd.check_input_settings(device=device, channels=1, samplerate=sr)
    except Exception:
        sr = int(sd.query_devices(device, "input")["default_samplerate"])
    rec = sd.rec(int(seconds * sr), samplerate=sr, channels=1, dtype="float32", device=device)
    sd.wait()
    return rec[:, 0].copy(), sr


def level_report(x: np.ndarray, win_s: float = 0.05, sr: int = DEFAULT_SR) -> dict:
    """Summarize peak, speech level, noise level, and signal-to-noise ratio."""
    x = np.asarray(x, dtype=np.float64)
    w = max(1, int(win_s * sr))
    n = len(x) // w
    if n < 4:
        return {"peak_dbfs": _db(np.max(np.abs(x)) if len(x) else 0.0),
                "speech_dbfs": -120.0, "noise_dbfs": -120.0, "snr_db": 0.0}
    rms = np.sqrt(np.mean(x[: n * w].reshape(n, w) ** 2, axis=1))
    speech = float(np.percentile(rms, 95))   # Loud windows represent speech.
    noise = float(np.percentile(rms, 10))    # Quiet windows represent background noise.
    return {
        "peak_dbfs": _db(np.max(np.abs(x))),
        "speech_dbfs": _db(speech),
        "noise_dbfs": _db(noise),
        "snr_db": _db(speech) - _db(noise),
    }


def judge_level(rep: dict) -> str:
    if rep["peak_dbfs"] >= CLIP_PEAK_DBFS:
        return "clipping"
    if rep["speech_dbfs"] < MIN_SPEECH_DBFS:
        return "too_quiet"
    if rep["snr_db"] < MIN_SNR_DB:
        return "noisy"
    return "ok"


def mic_test(seconds: float = 2.0, sr: int = DEFAULT_SR, device=None, capture=_capture) -> dict:
    """Check the mic. Ask for silence for the first 0.3 s, then a sustained 아.

    The capture argument allows tests to inject a fake microphone.
    """
    try:
        x, sr_used = capture(seconds, sr, device)
    except Exception as e:  # Missing device, permission denied, and similar errors.
        return {"ok": False, "status": "no_device", "message": _MESSAGES["no_device"], "error": str(e)}
    rep = level_report(x, sr=sr_used)
    status = judge_level(rep)
    return {"ok": status == "ok", "status": status, "message": _MESSAGES[status],
            "sr": sr_used, "report": rep}


def record(path, seconds: float = 3.0, sr: int = DEFAULT_SR, device=None, capture=_capture) -> dict:
    """Record for seconds and save a 16-bit mono WAV file."""
    import soundfile as sf

    try:
        x, sr_used = capture(seconds, sr, device)
    except Exception as e:
        return {"ok": False, "status": "no_device", "message": _MESSAGES["no_device"], "error": str(e)}
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(path), np.clip(x, -1.0, 1.0), sr_used, subtype="PCM_16")
    rep = level_report(x, sr=sr_used)
    status = judge_level(rep)
    return {"ok": True, "status": status, "message": _MESSAGES[status], "path": str(path),
            "sr": sr_used, "seconds": float(len(x) / sr_used), "report": rep}