# Video Prompt Forge — AI 视频提示词工厂

> 把一句中文想法，变成可灵 / Runway / Sora / Veo 能直接用的专业英文视频提示词。
> Turn a one-line Chinese idea into production-ready English video prompts for Kling, Runway, Sora, and Veo — powered by ChatGPT.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)

## 为什么需要它 / Why

玩 AI 视频的人越来越多，但大多数创作者卡在同一关：**想得出画面，写不出英文提示词**——镜头怎么动、光线怎么描述、负面词怎么写，全靠猜。

Video Prompt Forge 解决这一关：

- 🇨🇳 **中文输入** → 🇬🇧 专业英文提示词（主体 + 动作 + 场景 + 镜头 + 光线 + 风格）
- 🎬 **按平台适配**：Kling（可灵）/ Runway / Sora / Veo 各自的参数与写法习惯
- 🎞️ **一键分镜版**：一个想法拆成 3–5 个镜头，每个镜头带时码、景别、运镜
- 🚫 **自动负面词**：变形、多指、低清、水印等常见翻车项自动补齐
- 🤖 **ChatGPT 增强模式**：接入 OpenAI API 后，由 ChatGPT 做创意扩写；没有 API Key 时，本地模板引擎也能离线出稿

## 快速开始 / Quick Start

### 网页版（零安装）

直接用浏览器打开 `web/index.html` 即可使用离线版。

### 命令行版

```bash
git clone https://github.com/<your-name>/video-prompt-forge.git
cd video-prompt-forge
python src/prompt_forge.py "巨人女子侧躺在草坡上看日落，旁边有个滑板少年" --platform kling --style cinematic
```

输出示例：

```

A giant young woman lying on her side on a grassy hillside at golden hour,
cinematic wide shot, slow scenic pan from left to right, warm sunset light,
peach and lavender clouds, distant city skyline, photorealistic, ultra detailed


deformed hands, extra fingers, blurry, low quality, watermark, distorted face

slow scenic pan, wide shot
duration 10s · aspect 16:9 · mode: image-to-video friendly
```

### ChatGPT 增强模式（可选）

```bash
export OPENAI_API_KEY="sk-..."
python src/prompt_forge.py "你的中文想法" --platform sora --use-gpt
```

接入后，ChatGPT 会在模板基础上做创意扩写、情绪和细节补全。

## 平台支持 / Platforms

| 平台 | 重点适配 |
|---|---|
| Kling 可灵 | 图生视频友好、运镜词、负面词 |
| Runway | Gen 系列镜头语言、camera controls 提示 |
| Sora | 长描述、物理真实感、分镜时码 |
| Veo | 电影感、音频提示占位 |
| Generic | 通用结构，适合其他模型 |

## 路线图 / Roadmap

- [x] v0.1 MVP：CLI + 离线模板引擎 + 网页版
- [] 提示词模板社区库（欢迎 PR 投稿你的拿手模板）
- [] 剪映草稿联动：分镜直接导出为剪辑清单
- [] 批量模式：一个选题生成整组短视频分镜包
- [] Chrome 插件：在可灵 / Runway 网页内一键填入

## 贡献 / Contributing

欢迎提 Issue 和 PR，尤其是：
- 新的运镜 / 光线 / 风格模板（编辑 `src/templates.json`）
- 新平台的适配规则
- 好用的提示词案例（放进 `examples/`）

## 许可证 / License

MIT — 见 [LICENSE](LICENSE)。
