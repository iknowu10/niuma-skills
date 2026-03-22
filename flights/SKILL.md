---
name: flights
description: 机票查询。查询任意航线的机票价格。当用户问到机票、航班、飞机票、飞某个城市、几号的票时触发。
metadata: { "openclaw": { "emoji": "✈️", "requires": { "bins": ["opencli"] } } }
---

# Flights — 机票查询

基于 opencli 的机票价格查询，数据来自携程。

## 用法

```bash
# 单程（默认明天）
opencli flights search 上海 北京

# 指定日期
opencli flights search 上海 北京 --date 2026-04-22

# 往返
opencli flights search MEL 厦门 --date 2026-04-22 --return 2026-05-06

# 限制条数
opencli flights search 深圳 成都 --limit 10

# JSON 格式输出
opencli flights search 上海 北京 -f json
```

## 支持的城市

中文名或三字码均可：

**国内**: 北京(BJS) 上海(SHA) 广州(CAN) 深圳(SZX) 成都(CTU) 杭州(HGH) 重庆(CKG) 武汉(WUH) 西安(SIA) 南京(NKG) 长沙(CSX) 厦门(XMN) 昆明(KMG) 大连(DLC) 天津(TSN) 青岛(TAO) 三亚(SYX) 海口(HAK) 郑州(CGO) 福州(FOC) 合肥(HFE) 贵阳(KWE) 南宁(NNG) 哈尔滨(HRB) 沈阳(SHE) 济南(TNA) 乌鲁木齐(URC) 兰州(LHW) 拉萨(LXA) 银川(INC) 西宁(XNN) 呼和浩特(HET) 石家庄(SJW) 太原(TYN) 南昌(KHN) 珠海(ZUH) 无锡(WUX) 宁波(NGB) 温州(WNZ) 烟台(YNT)

**国际/港澳台**: 香港(HKG) 澳门(MFM) 台北(TPE) 东京(TYO) 大阪(OSA) 首尔(SEL) 曼谷(BKK) 新加坡(SIN) 吉隆坡(KUL) 伦敦(LON) 巴黎(PAR) 纽约(NYC) 洛杉矶(LAX) 旧金山(SFO) 悉尼(SYD) 墨尔本(MEL)

不在列表中的城市可直接用 IATA 三字码。

## 输出列

`rank` `airline` `flightNo` `depart` `arrive` `duration` `stops` `price`

往返查询额外显示 `leg`（去程/返程）。

## 注意

- 需要 opencli 浏览器扩展已连接（`opencli doctor` 检查）
- 数据来自携程，无需登录
- 价格为经济舱最低价（人民币）
