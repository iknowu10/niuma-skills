---
name: finance
description: 金融报价。查询股票、基金、黄金、期货、指数等价格。支持 A 股、港股、美股及任意 Yahoo Finance 标的。当用户问到股价、金价、涨跌、持仓、行情时触发。
metadata: { "openclaw": { "emoji": "📈", "requires": { "bins": ["python3"] } } }
---

# Finance — 金融报价

查询任意金融标的的实时报价。

## 数据源

| Symbol 格式 | 来源 | 示例 |
|-------------|------|------|
| `sh######` | 腾讯财经（沪市 A 股） | `sh600489` 中金黄金 |
| `sz######` | 腾讯财经（深市 A 股） | `sz000858` 五粮液 |
| `hk#####` | 腾讯财经（港股） | `hk00700` 腾讯 |
| 其他 | Yahoo Finance（美股、期货、指数、外汇） | `GC=F` 黄金期货, `AAPL`, `^TNX` 美债10Y |

## 用法

```bash
python3 scripts/quote.py <symbol> [symbol ...]
```

### 示例

```bash
# 单只
python3 scripts/quote.py sh600489

# 混合查询
python3 scripts/quote.py sh600489 hk00700 GC=F AAPL
```

## 输出格式

```
中金黄金 (600489)  ¥30.77  -0.57 (-1.82%)
腾讯控股 (00700)   HK$547.50  +1.00 (+0.18%)
Gold (GC=F)  USD 3,012.34  +5.20 (+0.17%)
```

每行一个标的，包含名称、代码、价格、涨跌额和涨跌幅。
