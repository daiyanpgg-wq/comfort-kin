"""Distill a 'qinren persona' profile from text/transcripts.

Input can be:
- Plain text file
- Markdown transcript file from transcribe_media.py

Output:
- A JSON profile used by chat_with_qinren.py
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from openai import OpenAI

from utils import PROFILES_DIR, ensure_file, save_json


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


def read_text(path: Path) -> str:
    txt = path.read_text(encoding="utf-8", errors="ignore")
    # Keep it bounded to reduce cost.
    if len(txt) > 120_000:
        txt = txt[-120_000:]
    return txt


def main() -> None:
    ap = argparse.ArgumentParser(description="Distill qinren persona JSON profile from text")
    ap.add_argument("input", help="Text/Markdown transcript file")
    ap.add_argument("--relationship", default="亲人", help="e.g., 妈妈/爸爸/外婆/哥哥")
    ap.add_argument("--calls-user", default="", help="How the persona calls the user")
    ap.add_argument("--name", default="default", help="Profile name (output to profiles/<name>.json)")
    args = ap.parse_args()

    inp = ensure_file(args.input)
    text = read_text(inp)

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

    profile = resp.choices[0].message.content
    # content is JSON string
    out_path = PROFILES_DIR / f"{args.name}.json"
    save_json(out_path, __import__("json").loads(profile))
    print(str(out_path))


if __name__ == "__main__":
    main()
