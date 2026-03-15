---
name: twitter-manager
description: 管理 X (Twitter) 账号。发推、读时间线、搜索、点赞、回复、转推、查看用户资料等。当用户提到推特、Twitter、X、发推、timeline、tweet 时触发。
allowed-tools: Bash(twitter:*)
---

# Twitter Manager

通过 twitter-cli 管理 X (Twitter) 账号，支持读取和写入操作。

## 环境变量

脚本从以下环境变量读取配置（已在容器中预设）：
- `TWITTER_AUTH_TOKEN` — X 认证 token
- `TWITTER_CT0` — X CSRF token

## 安装

首次使用时需要安装 twitter-cli（后续已缓存无需重复）：

```bash
pip3 install --break-system-packages git+https://github.com/jackwener/twitter-cli
```

## 读取操作

### 查看当前账号

```bash
twitter whoami
```

### 首页时间线

```bash
# 默认数量
twitter feed

# 指定数量
twitter feed --max 20

# Following 时间线
twitter feed --following
```

### 搜索推文

```bash
# 关键词搜索
twitter search "关键词"

# 高级搜索
twitter search "关键词" --from username --lang zh --max 10

# 按媒体类型过滤
twitter search "关键词" --filter images
twitter search "关键词" --filter videos
```

### 查看推文详情和回复

```bash
twitter tweet <tweet_id_or_url>
```

### 查看用户资料

```bash
twitter user <username>
```

### 查看用户的推文

```bash
twitter user-posts <username> --max 10
```

### 查看用户的点赞

```bash
twitter likes <username> --max 10
```

### 查看粉丝/关注列表

```bash
twitter followers <username>
twitter following <username>
```

### 查看书签

```bash
twitter bookmarks --max 10
```

## 写入操作

### 发推

```bash
# 纯文本
twitter post "推文内容"

# 带图片（最多4张）
twitter post "推文内容" --image /path/to/image.jpg
twitter post "推文内容" --image img1.jpg --image img2.jpg
```

### 回复

```bash
twitter reply <tweet_id_or_url> "回复内容"
```

### 点赞/取消点赞

```bash
twitter like <tweet_id_or_url>
twitter unlike <tweet_id_or_url>
```

### 转推/取消转推

```bash
twitter retweet <tweet_id_or_url>
twitter unretweet <tweet_id_or_url>
```

### 引用推文

```bash
twitter quote <tweet_id_or_url> "评论内容"
```

### 书签

```bash
twitter bookmark <tweet_id_or_url>
twitter unbookmark <tweet_id_or_url>
```

### 关注/取关

```bash
twitter follow <username>
twitter unfollow <username>
```

### 删推

```bash
twitter delete <tweet_id_or_url>
```

## 输出格式

所有命令支持 `--json` 或 `--yaml` 输出格式，方便程序解析：

```bash
twitter feed --max 5 --json
twitter user elonmusk --yaml
```

紧凑输出（适合 LLM 处理）：

```bash
twitter -c feed --max 10
```

## 使用流程

### 查看时间线并互动
1. `twitter feed --max 10` 获取最新推文
2. 分析内容，挑选有趣的推文
3. 对感兴趣的推文点赞或回复

### 发推
1. 起草推文内容（注意 280 字符限制）
2. 展示给用户确认（除非用户明确授权自主发布）
3. 确认后用 `twitter post "内容"` 发布

### 搜索和研究
1. `twitter search "话题"` 搜索相关推文
2. `twitter tweet <id>` 查看推文详情和回复链
3. `twitter user <username>` 了解相关用户

## 注意事项

- 发推、回复等写入操作前，除非用户明确授权，否则先展示内容让用户确认
- 注意 280 字符限制
- 不要泄露认证 token
- 搜索和阅读操作可以自由使用，无需确认
