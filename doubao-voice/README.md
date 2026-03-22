# 豆包语音插件 (Doubao Voice Plugin)

火山引擎豆包语音API集成插件，支持文字转语音(TTS)和唱歌功能。

## 功能特性

- **✅ 语音合成 (TTS)**: 文字转语音，支持多种音色 - **已测试可用**
- **🎵 唱歌**: 让豆包唱歌，支持实时语音交互 - **已开通端到端大模型**
- **简单易用**: 命令行工具，一行命令即可使用
- **多种音色**: 支持女声/男声等多种基础音色
- **实时交互**: 支持与豆包进行实时对话和唱歌

## 快速开始

### 1. 获取API凭证

访问 [火山引擎控制台](https://console.volcengine.com/speech/app) 创建应用并获取：
- **App ID** (数字)
- **Access Token** (长字符串)

开通所需服务：
1. 在控制台勾选 **"语音合成"** 服务 (TTS)

### 2. 配置环境变量

**方式1: 使用配置脚本 (推荐)**
```bash
cd scripts
source setup_env.sh  # 自动设置环境变量
```

**方式2: 手动设置**
```bash
export DOUBAO_APP_ID="your_app_id"
export DOUBAO_ACCESS_TOKEN="your_access_token"
```

### 3. 安装依赖

```bash
pip3 install requests --break-system-packages
```

### 4. 检查凭证

```bash
# 检查凭证配置
python3 scripts/check_credentials.py
```

### 5. 使用示例

#### TTS 文字转语音（命令行）

```bash
cd scripts

# 基础用法 - ✅ 已测试可用
python3 voice_converter.py tts "你好，我是豆包语音助手" -o output.mp3

# 使用不同音色
python3 voice_converter.py tts "测试男声" -o male.mp3 -v BV701_V2_streaming
```

#### 唱歌（命令行）🎵

```bash
cd scripts

# 让豆包唱歌
python3 singing.py sing "请唱一首关于春天的歌" -o spring.mp3

# 交互式唱歌模式（实时对话）
python3 singing.py interactive
```

#### Python 代码方式

```python
# TTS - 文字转语音
from scripts.voice_converter import DoubaoVoiceConverter

converter = DoubaoVoiceConverter()
audio_file = converter.text_to_speech("你好，欢迎使用豆包", output_file="hello.mp3")

# 唱歌
import asyncio
from scripts.singing import DoubaoSinging

async def sing():
    singing = DoubaoSinging()
    audio_file = await singing.sing("请唱一首情歌", output_file="love_song.mp3")

asyncio.run(sing())
```

## 自然语言调用

在 Claude Code 中可以使用自然语言调用：

**TTS 文字转语音**:
- "把这段话转成语音：你好世界"
- "用温柔女声合成语音"
- "用男声朗读这段文字"

**唱歌**:
- "请唱一首关于春天的歌"
- "唱一个温柔的摇篮曲"
- "开启与豆包的实时语音对话模式"

示例：
```
用户: "帮我把'欢迎使用豆包语音'转成语音"
Claude: 调用TTS服务生成output.mp3
```

## 价格说明

### TTS (语音合成)
- 大模型并发版: 2000元/并发/月
- 按量付费: 按字符数计费

### 免费试用
新用户开通服务后可获得免费额度。

## 支持的音色

| 音色代码 | 描述 | 场景 | 状态 |
|---------|------|------|------|
| BV700_V2_streaming | 通用女声 | 通用场景 | ✅ V1 可用 |
| BV701_V2_streaming | 通用男声 | 通用场景 | ✅ V1 可用 |
| BV406_streaming | 温柔女声 | 客服、助手 | ✅ V1 可用 |
| BV158_streaming | 活泼女声 | 教育、娱乐 | ✅ V1 可用 |
| BV115_streaming | 磁性男声 | 新闻、播音 | ✅ V1 可用 |

**注意**: 豆包2.0高级音色需要使用V3 API，目前正在调试中。

## 常见问题

### TTS 返回 "requested resource not granted"
**解决方法**: 在控制台勾选"语音合成"服务选项

### Authorization 头格式错误
确保使用 `Bearer;{token}` 格式（注意分号），而不是 `Bearer {token}`

### 环境变量未生效
```bash
# 检查环境变量
echo $DOUBAO_APP_ID
echo $DOUBAO_ACCESS_TOKEN

# 如果为空，重新设置
source setup_env.sh
```

## API 版本说明

### V1 API (当前使用) ✅
- **状态**: 已测试，稳定可用
- **认证**: Bearer Token
- **音色**: 支持基础音色
- **推荐**: 日常使用推荐

### V3 API (豆包2.0) ⚠️
- **状态**: 调试中，存在 "get resource id empty" 问题
- **认证**: Bearer Token + Resource-Id
- **音色**: 支持豆包2.0高级音色
- **说明**: 需要联系火山引擎技术支持获取正确配置

## 技术支持

- [官方文档](https://www.volcengine.com/docs/6561/1359369)
- [控制台](https://console.volcengine.com/speech/app)
- [计费说明](https://www.volcengine.com/docs/6561/1359370)

## 许可证

本插件遵循 MIT 许可证。

## 作者

niuma-ranch
