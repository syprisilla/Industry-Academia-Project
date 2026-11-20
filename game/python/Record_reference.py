"""Record reference audio for one syllable group into game/data/reference_audio/<group>/.

Play the source audio (e.g., from a phone) and record it on the laptop mic.
Run:
    python record_reference.py SYLLABLE [SECONDS]
Example:
    python record_reference.py 시 3
Press Enter to record each take, q then Enter to stop. Files auto-increment and never overwrite.
"""
from __future__ import annotations
import sys
from pathlib import Path

from Audio_recording import record


def main(group, seconds=3.0):
    here = Path(__file__).resolve().parent
    out_dir = here.parent / "data" / "reference_audio" / group
    out_dir.mkdir(parents=True, exist_ok=True)

    # Continue numbering after existing files so reruns append.
    idx = len(list(out_dir.glob(f"{group}_*.wav")))

    print(f"\nRecording group '{group}' -> {out_dir}")
    print(f"Enter = record {seconds:.0f}s take, q = quit.\n")
    while True:
        ans = input(f"[{group}] take {idx + 1} (Enter=record, q=quit): ").strip().lower()
        if ans == "q":
            break
        idx += 1
        path = out_dir / f"{group}_{idx:03d}.wav"
        rec = record(path, seconds=seconds)
        status = rec.get("status")
        if not rec.get("ok"):
            print(f"    x recording failed ({status}) -- deleted")
            path.unlink(missing_ok=True)
            idx -= 1
            continue
        flag = "" if status == "ok" else f"  (warning: {status}, consider re-recording)"
        print(f"    saved {path.name}{flag}")

    print(f"\nDone. '{group}' now has {idx} file(s).")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python record_reference.py SYLLABLE [SECONDS]")
        sys.exit(1)
    main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 3.0)