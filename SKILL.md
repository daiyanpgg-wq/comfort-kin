---
name: qinren-companion
description: "亲人陪伴对话 Skill（对齐 colleague-skill 结构）：支持导入音频/视频/文本语料，转写并蒸馏出亲人口吻画像（称呼、口头禅、关心方式、禁忌话题、安慰模板等），然后以该口吻陪伴式聊天。适用于：蒸馏亲人说话习惯、制作可长期陪聊的亲人角色、将多模态语料沉淀为可复用 profile。"
---

# 亲人.skill（Qinren Companion）

本仓库/Skill 的目标：**把亲人蒸馏成可长期陪伴聊天的“口吻画像（profile）”**。

## 触发方式（建议）

- 你想开始蒸馏：
  - “帮我做一个亲人 skill / 蒸馏我妈妈 / 做一个外婆口吻”
- 你想追加语料：
  - “我有新语音/新视频，追加进去”

## 直接可运行入口

### A. 三步法（更可控）

1) 转写：

```bash
python3 scripts/transcribe_media.py /path/to/media.mp4 --out /tmp/transcript.md
```

2) 蒸馏画像：

```bash
python3 scripts/distill_persona.py /tmp/transcript.md --relationship 妈妈 --calls-user "宝宝" --name mom
```

3) 陪聊：

```bash
python3 scripts/chat_with_qinren.py --profile mom
```

### B. 一步法（对齐同事 skill 的“创建器”体验）

```bash
python3 tools/create_qinren.py /path/to/media_or_text --relationship 妈妈 --calls-user "宝宝" --name mom
```

## 文档

- `references/workflow.md`：完整工作流 + **高质量语料准备建议**

## 依赖与约束

- 环境变量：`OPENAI_API_KEY`
- 可选：`OPENAI_MODEL`（默认 `gpt-4.1-mini`）
- 系统命令：`ffmpeg`、`anygen-speech-to-text`

