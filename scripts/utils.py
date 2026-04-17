"""Common utilities for qinren-companion scripts."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
PROFILES_DIR = ROOT_DIR / "profiles"
PROFILES_DIR.mkdir(parents=True, exist_ok=True)


def run(cmd: list[str]) -> None:
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed ({p.returncode}): {' '.join(cmd)}\n\n{p.stdout}")


def ensure_file(path: str | os.PathLike) -> Path:
    p = Path(path).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(str(p))
    if not p.is_file():
        raise FileNotFoundError(f"Not a file: {p}")
    return p


def load_json(path: str | os.PathLike) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str | os.PathLike, obj: dict) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
