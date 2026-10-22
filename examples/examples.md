# 使用案例 / Examples

## 例 1：日落宽景（图生视频友好）

输入：
```bash
python src/prompt_forge.py "巨人女子侧躺在草坡上看日落，旁边有个滑板少年" --platform kling --style cinematic --camera pan
```

要点：一个镜头只给一个明确动作；宽景用 `pan` 缓摇，比近景跟踪更稳、更不容易变形。

## 例 2：海边奔跑

```bash
python src/prompt_forge.py "猫在海边奔跑" --platform sora --style photorealistic --camera tracking --storyboard
```

## 例 3：动漫风夜景

```bash
python src/prompt_forge.py "女孩在城市夜晚走路微笑" --platform veo --style anime
```

## 例 4：ChatGPT 增强模式

```bash
export OPENAI_API_KEY="sk-..."
python src/prompt_forge.py "老人在雪中坐着看天空" --platform kling --use-gpt --storyboard
```

增强模式下，ChatGPT 会把中文想法完整英译并扩写细节（服装、表情、材质、物理运动），离线模式则给出结构完整的模板稿。
