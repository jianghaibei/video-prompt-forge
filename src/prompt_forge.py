#!/usr/bin/env python3
"""
Video Prompt Forge - AI video prompt factory (MVP)
Offline mode (default): local template engine, no key needed.
GPT mode (--use-gpt): needs OPENAI_API_KEY, ChatGPT expands the idea.
"""
import argparse
import json
import os
import sys
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))


def load_templates():
    with open(os.path.join(BASE, "templates.json"), encoding="utf-8") as f:
        return json.load(f)


def expand_keywords(text, keyword_map):
    hits = []
    for zh, en in keyword_map:
        if zh in text and en not in hits:
            hits.append(en)
    return hits


def build_offline(idea, platform, style, camera, tpl):
    style_cfg = tpl["styles"].get(style, tpl["styles"]["cinematic"])
    cam_text = tpl["cameras"].get(camera, tpl["cameras"]["auto"])
    fragments = expand_keywords(idea, tpl["keyword_map"])
    subject = ", ".join(fragments) if fragments else "the described subject in motion"
    prompt_parts = [
        subject,
        "original idea: " + idea,
        cam_text,
        style_cfg["lighting_default"],
        style_cfg["suffix"],
    ]
    return {
        "main_prompt": ", ".join(prompt_parts),
        "negative": tpl["platforms"][platform]["negative"],
        "camera": cam_text,
        "platform": tpl["platforms"][platform]["label"],
        "suggested": tpl["platforms"][platform]["suggested"],
    }


def build_with_gpt(idea, platform, style, camera):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("No OPENAI_API_KEY found, falling back to offline mode.", file=sys.stderr)
        return None
    system = (
        "You are an expert AI-video prompt engineer. Given a Chinese idea, "
        "write a production-ready English video prompt for the target platform. "
        "Structure: subject + action + scene + camera movement + lighting + style. "
        'Reply with JSON only: {"main_prompt": "...", "negative": "...", "camera": "...", "suggested": "..."}'
    )
    user = "Idea (Chinese): %s\nPlatform: %s\nStyle: %s\nCamera preference: %s" % (idea, platform, style, camera)
    body = json.dumps({
        "model": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.7,
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + api_key},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.load(resp)
    content = data["choices"][0]["message"]["content"].strip()
    if content.startswith("```"):
        content = content.strip("`")
        if content.startswith("json"):
            content = content[4:]
    result = json.loads(content)
    result["platform"] = platform
    return result


def storyboard(idea, result):
    shots = [
        ("00:00-00:03", "Wide shot", "establish scene and subject, slow push-in"),
        ("00:03-00:06", "Medium shot", "core action of the subject, camera follows"),
        ("00:06-00:10", "Close-up / detail", "emotional or detail close-up, slow pull-out to end"),
    ]
    lines = ["", "[Storyboard - " + idea + "]"]
    for tc, framing, note in shots:
        lines.append("- %s | %s | %s" % (tc, framing, note))
        lines.append("  Prompt base: " + result["main_prompt"])
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Video Prompt Forge")
    ap.add_argument("idea", help="one-line Chinese idea")
    ap.add_argument("--platform", default="kling", choices=["kling", "runway", "sora", "veo", "generic"])
    ap.add_argument("--style", default="cinematic", choices=["cinematic", "photorealistic", "anime", "commercial"])
    ap.add_argument("--camera", default="auto", help="push_in / pan / tracking / orbit / aerial / static / handheld / pull_out")
    ap.add_argument("--storyboard", action="store_true")
    ap.add_argument("--use-gpt", action="store_true")
    args = ap.parse_args()

    tpl = load_templates()
    result = None
    if args.use_gpt:
        try:
            result = build_with_gpt(args.idea, args.platform, args.style, args.camera)
        except Exception as e:
            print("GPT call failed (%s), falling back to offline mode." % e, file=sys.stderr)
    if result is None:
        result = build_offline(args.idea, args.platform, args.style, args.camera, tpl)

    print("[Platform] " + str(result["platform"]))
    print("\n[Main Prompt]\n" + result["main_prompt"])
    print("\n[Negative Prompt]\n" + result["negative"])
    print("\n[Camera] " + result["camera"])
    print("\n[Suggested] " + result["suggested"])
    if args.storyboard:
        print(storyboard(args.idea, result))


if __name__ == "__main__":
    main()
