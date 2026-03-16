---
name: weather
description: 天气预报。查询任意城市的天气。当用户问到天气、气温、下雨、今天/明天天气时触发。
metadata: { "openclaw": { "emoji": "🌤", "requires": { "bins": ["python3"] } } }
---

# Weather — 天气预报

基于 Open-Meteo（免费，无需 API key）的天气预报。

## 用法

```bash
# 默认 Melbourne，今天
python3 scripts/forecast.py

# 指定城市
python3 scripts/forecast.py --city sydney
python3 scripts/forecast.py --city beijing

# 指定坐标
python3 scripts/forecast.py --lat -33.87 --lon 151.21

# 多天预报
python3 scripts/forecast.py --days 3
python3 scripts/forecast.py --city melbourne --days 3
```

## 内置城市

`melbourne` `sydney` `brisbane` `beijing` `shanghai` `shenzhen`

其他城市用 `--lat` / `--lon`。

## 输出示例

```
🌍 Melbourne
  Today      🌧  17–20°C  rain 95%
  Tomorrow   🌤  15–22°C  rain 10%
```
