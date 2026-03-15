#!/usr/bin/env python3
"""百度千帆 AI PPT 生成"""

import argparse
import json
import os
import random
import sys
import time

import requests

API_BASE = "https://qianfan.baidubce.com/v2/tools/ai_ppt"
API_KEY = os.environ["BAIDU_PPT_API_KEY"]


def headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }


def get_random_theme():
    resp = requests.post(f"{API_BASE}/get_ppt_theme", headers=headers())
    data = resp.json()
    if data.get("errno", 0) != 0:
        raise RuntimeError(data.get("errmsg", "获取模板失败"))
    theme = random.choice(data["data"]["ppt_themes"])
    return theme["style_id"], theme["tpl_id"]


def get_theme_by_tpl_id(tpl_id):
    resp = requests.post(f"{API_BASE}/get_ppt_theme", headers=headers())
    data = resp.json()
    if data.get("errno", 0) != 0:
        raise RuntimeError(data.get("errmsg", "获取模板失败"))
    for theme in data["data"]["ppt_themes"]:
        if theme["tpl_id"] == tpl_id:
            return theme["style_id"], theme["tpl_id"]
    return 0, tpl_id


def generate_outline(query):
    h = headers()
    h["Accept"] = "text/event-stream"

    title = ""
    outline = ""
    chat_id = ""
    query_id = ""

    with requests.post(
        f"{API_BASE}/generate_outline", headers=h, json={"query": query}, stream=True
    ) as resp:
        for line in resp.iter_lines(decode_unicode=True):
            if line and line.startswith("data:"):
                delta = json.loads(line[5:].strip())
                if not title:
                    title = delta["title"]
                    chat_id = delta["chat_id"]
                    query_id = delta["query_id"]
                outline += delta["outline"]

    return chat_id, query_id, title, outline


def generate_ppt(query, style_id, tpl_id):
    print("正在生成大纲...", file=sys.stderr)
    chat_id, query_id, title, outline = generate_outline(query)
    print(f"大纲完成: {title}", file=sys.stderr)

    print("正在生成 PPT（需要 2-5 分钟）...", file=sys.stderr)
    h = headers()
    h["Accept"] = "text/event-stream"

    params = {
        "query_id": int(query_id),
        "chat_id": int(chat_id),
        "query": query,
        "outline": outline,
        "title": title,
        "style_id": style_id,
        "tpl_id": tpl_id,
    }

    start = int(time.time())
    with requests.post(
        f"{API_BASE}/generate_ppt_by_outline", headers=h, json=params, stream=True
    ) as resp:
        if resp.status_code != 200:
            print(f"Error: HTTP {resp.status_code} - {resp.text}", file=sys.stderr)
            sys.exit(1)
        for line in resp.iter_lines(decode_unicode=True):
            if line and line.startswith("data:"):
                data = json.loads(line[5:].strip())
                if data.get("is_end"):
                    print(json.dumps(data, ensure_ascii=False, indent=2))
                else:
                    elapsed = int(time.time()) - start
                    print(json.dumps({"status": data.get("status", "生成中"), "elapsed": elapsed}))


def main():
    parser = argparse.ArgumentParser(description="百度 AI PPT 生成")
    parser.add_argument("--query", "-q", required=True, help="PPT 主题")
    parser.add_argument("--tpl_id", "-t", type=int, help="模板 ID（不指定则随机）")
    args = parser.parse_args()

    if args.tpl_id:
        style_id, tpl_id = get_theme_by_tpl_id(args.tpl_id)
        print(f"使用模板 tpl_id={tpl_id}, style_id={style_id}", file=sys.stderr)
    else:
        style_id, tpl_id = get_random_theme()
        print(f"随机模板 tpl_id={tpl_id}, style_id={style_id}", file=sys.stderr)

    generate_ppt(args.query, style_id, tpl_id)


if __name__ == "__main__":
    main()
