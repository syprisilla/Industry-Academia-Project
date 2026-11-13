"""마이크 테스트 + 녹음 모듈 (PC 내장/외부 마이크).

- sounddevice / soundfile 은 함수 안에서 import 한다 (PortAudio 가 없는 PC 에서도 모듈 import 는 되도록).
- 모든 반환값은 JSON 으로 바꿀 수 있는 dict.
- 아래 임계값(CLIP/MIN/SNR)은 '임시값' 이다. 실제 마이크로 녹음해 보며 조정할 것.
- 윈도우에서는 '마이크 향상/오디오 향상' 을 끄고 녹음해야 /ㅅ/ 바람소리가 깎이지 않는다.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

DEFAULT_SR = 48000          # /ㅅ/ 고주파 대역을 담기 위해 48kHz 로 녹음
CLIP_PEAK_DBFS = -1.0       # 이보다 크면 소리가 찌그러진 것으로 본다
MIN_SPEECH_DBFS = -45.0     # 말하는 구간의 RMS 가 이보다 작으면 너무 작음
MIN_SNR_DB = 20.0           # 말소리와 주변 소음의 차이가 이보다 작으면 소음이 큼

_MESSAGES = {
    "ok": "마이크 상태가 좋아요!",
    "clipping": "소리가 너무 커요. 마이크에서 조금 떨어져 말해 볼까요?",
    "too_quiet": "소리가 너무 작아요. 조금 더 크게 말해 볼까요?",
    "noisy": "주변이 시끄러워요. 조용한 곳에서 다시 해 볼까요?",
    "no_device": "마이크를 찾을 수 없어요. 마이크 연결을 확인해 주세요.",
}


def _db(x: float) -> float:
    return float(20.0 * np.log10(max(float(x), 1e-12)))


def list_input_devices() -> list[dict]:
    """입력 가능한 오디오 장치 목록."""
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
    """마이크에서 seconds 초 녹음 -> (float32 모노 배열, 실제 샘플레이트)."""
    import sounddevice as sd

    try:  # 장치가 48kHz 를 지원하지 않으면 장치 기본값으로 대체
        sd.check_input_settings(device=device, channels=1, samplerate=sr)
    except Exception:
        sr = int(sd.query_devices(device, "input")["default_samplerate"])
    rec = sd.rec(int(seconds * sr), samplerate=sr, channels=1, dtype="float32", device=device)
    sd.wait()
    return rec[:, 0].copy(), sr


def level_report(x: np.ndarray, win_s: float = 0.05, sr: int = DEFAULT_SR) -> dict:
    """녹음 레벨 요약: 최대치, 말소리 레벨, 소음 레벨, 둘의 차이(SNR)."""
    x = np.asarray(x, dtype=np.float64)
    w = max(1, int(win_s * sr))
    n = len(x) // w
    if n < 4:
        return {"peak_dbfs": _db(np.max(np.abs(x)) if len(x) else 0.0),
                "speech_dbfs": -120.0, "noise_dbfs": -120.0, "snr_db": 0.0}
    rms = np.sqrt(np.mean(x[: n * w].reshape(n, w) ** 2, axis=1))
    speech = float(np.percentile(rms, 95))   # 가장 큰 구간 = 말소리
    noise = float(np.percentile(rms, 10))    # 가장 조용한 구간 = 주변 소음
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
    """마이크 테스트. 처음 0.3초는 조용히, 이후에 "아~" 하고 말하게 안내할 것.

    capture 인자는 테스트용(가짜 마이크를 넣을 수 있게).
    """
    try:
        x, sr_used = capture(seconds, sr, device)
    except Exception as e:  # 장치 없음, 권한 거부 등
        return {"ok": False, "status": "no_device", "message": _MESSAGES["no_device"], "error": str(e)}
    rep = level_report(x, sr=sr_used)
    status = judge_level(rep)
    return {"ok": status == "ok", "status": status, "message": _MESSAGES[status],
            "sr": sr_used, "report": rep}


def record(path, seconds: float = 3.0, sr: int = DEFAULT_SR, device=None, capture=_capture) -> dict:
    """seconds 초 녹음해서 WAV(16bit 모노)로 저장."""
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