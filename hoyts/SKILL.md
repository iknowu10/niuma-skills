---
name: hoyts
description: 查询 HOYTS 影院信息。当用户问到 HOYTS 电影、场次、影院、夜王、正在上映、即将上映等时触发。
metadata: { "openclaw": { "emoji": "🎬", "requires": { "bins": ["python3"] } } }
---

# HOYTS Cinema CLI

查询澳大利亚 HOYTS 影院的电影、场次和影院信息。

## 命令

### 正在上映
```bash
python3 scripts/movies.py [--limit 20]
```

### 即将上映
```bash
python3 scripts/coming_soon.py [--limit 20]
```

### 影院列表
```bash
python3 scripts/cinemas.py [--state NSW|VIC|QLD|WA|SA|ACT]
```

### 场次查询
```bash
python3 scripts/sessions.py --cinema <slug-or-id> [--date YYYY-MM-DD] [--movie <keyword>]
```

- `--cinema`：影院 slug（如 `forest-hill`）或 ID（如 `FHLCIN`），用 `cinemas.py` 查 ID
- `--date`：默认今天
- `--movie`：按电影名过滤（部分匹配）

### 搜索电影
```bash
python3 scripts/search.py --query <keyword> [--limit 10]
```

## 示例

```bash
# 查今天 Forest Hill 的夜王场次
python3 scripts/sessions.py --cinema forest-hill --movie "Night King"

# 查明天 Chatswood Westfield 所有场次
python3 scripts/sessions.py --cinema chatswood-westfield --date 2026-03-17

# 查 NSW 的影院
python3 scripts/cinemas.py --state NSW
```
