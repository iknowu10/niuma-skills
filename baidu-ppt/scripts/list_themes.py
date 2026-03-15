#!/usr/bin/env python3
"""列出百度千帆 PPT 可用模板"""

import json
import os
import sys

import requests

API_BASE = "https://qianfan.baidubce.com/v2/tools/ai_ppt"
API_KEY = os.environ["BAIDU_PPT_API_KEY"]


def main():
    resp = requests.post(
        f"{API_BASE}/get_ppt_theme",
        headers={"Authorization": f"Bearer {API_KEY}"},
    )
    data = resp.json()
    if data.get("errno", 0) != 0:
        print(f"Error: {data.get('errmsg')}", file=sys.stderr)
        sys.exit(1)

    themes = []
    for t in data["data"]["ppt_themes"][:50]:
        themes.append({
            "tpl_id": t["tpl_id"],
            "style_id": t["style_id"],
            "styles": t.get("style_name_list", []),
        })

    print(json.dumps(themes, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
