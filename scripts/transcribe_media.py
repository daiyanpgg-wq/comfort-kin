"""Transcribe audio/video via anygen-speech-to-text.

- For video: extract audio with ffmpeg first.
- Output transcript as .md (plain text is also acceptable).

This script is intentionally deterministic and uses CLI tools.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

from utils import ensure_file, run


def extract_audio(video_path: Path, out_wav: Path) -> None:
    # 16k mono WAV is sufficient for ASR.
    run([
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "pcm_s16le",
        str(out_wav),
    ])


def transcribe(media_path: Path, out_md: Path) -> None:
    if shutil.which("anygen-speech-to-text") is None:
        raise RuntimeError("anygen-speech-to-text not found in PATH")

    out_md.parent.mkdir(parents=True, exist_ok=True)

    # Prefer markdown output for readability.
    run([
        "anygen-speech-to-text",
        str(media_path),
        "--format",
        "md",
        "-o",
        str(out_md),
    ])


def main() -> None:
    ap = argparse.ArgumentParser(description="Transcribe audio or video to Markdown transcript")
    ap.add_argument("input", help="Audio/Video file path")
    ap.add_argument("--out", required=True, help="Output transcript .md path")
    args = ap.parse_args()

    inp = ensure_file(args.input)
    out_md = Path(args.out).expanduser().resolve()

    suffix = inp.suffix.lower()
    video_exts = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v"}

    if suffix in video_exts:
        with tempfile.TemporaryDirectory() as td:
            wav = Path(td) / "audio.wav"
            extract_audio(inp, wav)
            transcribe(wav, out_md)
    else:
        transcribe(inp, out_md)


if __name__ == "__main__":
    main()
