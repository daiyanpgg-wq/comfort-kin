# qinren-companion

把**亲人**蒸馏成一个可陪伴聊天的“口吻画像”，并用该口吻与你对话。

- 支持输入：**音频 / 视频 / 文本**
- 输出：`profiles/*.json`（可版本化保存）
- 运行：`python3 scripts/chat_with_qinren.py --profile <name>`

## 安装

### 方式 1：作为 Skill

- 导入 `qinren-companion.skill`，或将本仓库放到你的 skills 目录。

### 方式 2：直接运行脚本

需要：
- `OPENAI_API_KEY`
- `ffmpeg`
- `anygen-speech-to-text`

## 用法

### 快速三步

1) 转写（音频/视频 → 文本）

```bash
python3 scripts/transcribe_media.py /path/to/media.mp4 --out /tmp/transcript.md
```

2) 蒸馏画像（文本 → profiles/*.json）

```bash
python3 scripts/distill_persona.py /tmp/transcript.md --relationship 妈妈 --calls-user "宝宝" --name mom
```

3) 陪聊

```bash
python3 scripts/chat_with_qinren.py --profile mom
```

## 像同事 skill 的“创建器”模式（可选）

我们也提供一个一键入口，把“转写 + 蒸馏”合成一步：

```bash
python3 tools/create_qinren.py /path/to/media_or_text --relationship 妈妈 --calls-user "宝宝" --name mom
```

## 文档

- `references/workflow.md`：完整工作流 + 高质量语料建议

