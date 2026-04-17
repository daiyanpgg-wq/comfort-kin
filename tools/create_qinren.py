"""CLI entry to create a qinren profile from uploaded media/text.

This mimics colleague-skill's 'creator' pattern, but focused on family-companion.

Workflow:
1) transcribe (optional)
2) distill persona JSON

Note: This is standalone and uses environment OPENAI_API_KEY.
"""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from scripts.transcribe_media import transcribe, extract_audio
from scripts.distill_persona import read_text
from scripts.utils import PROFILES_DIR, ensure_file, save_json

import os
import json
from openai import OpenAI


SYSTEM = """你是一个‘口吻与习惯’蒸馏器。
任务：从用户提供的语料中，蒸馏出一位‘亲人’的聊天口吻、习惯与陪伴方式，输出严格的 JSON。

要求：
- 只输出 JSON，不要输出任何解释。
- 不要编造语料里没有的信息；如果缺失就给空字符串或空数组。
- 重点抽取：称呼、语气、常用语/口头禅、关心方式、说话节奏、禁忌话题、安慰/鼓励模板。
- 语气：温柔、耐心、少说教（除非语料明显说教）。

JSON 结构（必须完全一致）：
{
  "relationship": "string",
  "calls_user": "string",
  "tone_keywords": ["string"],
  "catchphrases": ["string"],
  "dos": ["string"],
  "donts": ["string"],
  "comfort_templates": ["string"],
  "small_talk_topics": ["string"],
  "signature": "string"
}
"""


def load_media_as_text(path: Path) -> str:
    suffix = path.suffix.lower()
    video_exts = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v"}
    audio_exts = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"}

    if suffix in video_exts or suffix in audio_exts:
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            wav = td / "audio.wav"
            if suffix in video_exts:
                extract_audio(path, wav)
                media = wav
            else:
                media = path
            out_md = td / "transcript.md"
            transcribe(media, out_md)
            return read_text(out_md)

    # treat as text
    return read_text(path)


def main() -> None:
    ap = argparse.ArgumentParser(description="Create qinren profile JSON from media/text")
    ap.add_argument("input", help="Audio/Video/Text file")
    ap.add_argument("--relationship", default="亲人")
    ap.add_argument("--calls-user", default="")
    ap.add_argument("--name", default="default", help="profiles/<name>.json")
    args = ap.parse_args()

    inp = ensure_file(args.input)
    text = load_media_as_text(inp)

    client = OpenAI()
    user_prompt = f"""亲人关系（外部指定）：{args.relationship}\n你称呼用户：{args.calls_user}\n\n语料如下（用三引号包裹）：\n\n\"\"\"\n{text}\n\"\"\"\n"""

    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        temperature=0.4,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
    )

    profile = json.loads(resp.choices[0].message.content)
    out_path = PROFILES_DIR / f"{args.name}.json"
    save_json(out_path, profile)
    print(str(out_path))


if __name__ == "__main__":
    main()
