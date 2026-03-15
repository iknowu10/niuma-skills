---
name: baidu-ppt
description: 使用百度千帆 API 生成 PPT。当用户需要生成 PPT、演示文稿、幻灯片时触发。
metadata: { "openclaw": { "emoji": "📊", "requires": { "bins": ["python3"] } } }
---

# 百度 AI PPT 生成

通过百度千帆 API 一键生成 PPT，每天免费 5 次。

## 使用流程

### Step 1: 获取用户主题
询问用户想做什么主题的 PPT。

### Step 2: 选择模板（可选）
问用户是否想选模板风格：
- **是** → 运行 `python3 scripts/list_themes.py` 展示可选模板，让用户选一个
- **否** → 跳过，自动随机选择

### Step 3: 生成 PPT
根据用户选择执行：

```bash
# 自动选模板
python3 scripts/generate.py --query "用户主题"

# 指定模板
python3 scripts/generate.py --query "用户主题" --tpl_id 模板ID
```

**超时设置 300 秒**，生成需要 2-5 分钟。

### Step 4: 返回结果
等待输出中出现 `is_end: true`，把 PPT 下载链接给用户。

## 注意事项
- 每天免费 5 次，超出 2.5 元/次
- 生成需要几分钟，耐心等待
- 输出的是 .pptx 下载链接
