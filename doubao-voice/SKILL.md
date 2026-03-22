---
name: doubao-voice
description: 豆包语音API调用。支持语音合成(TTS)和唱歌。当用户提到语音合成、文字转语音、唱歌、豆包语音相关任务时自动激活。
---

# 豆包语音API技能

调用火山引擎豆包语音API，实现文字转语音(TTS)和唱歌功能。

## 核心功能 ⭐

### 1. 文字转语音 (TTS)

```bash
# 凭证存放在 ~/.doubao-token 文件中：
# DOUBAO_APP_ID=your_app_id
# DOUBAO_ACCESS_TOKEN=your_access_token

# 文字转语音
python scripts/voice_converter.py tts "你好世界"
```

### 2. 唱歌 🎵

```bash
# 让豆包唱歌
python scripts/singing.py sing "请唱一首关于春天的歌"

# 交互式唱歌模式
python scripts/singing.py interactive
```

## 功能概述

| 模块 | 功能 | 推荐模型 |
|------|------|---------|
| **语音合成 (TTS)** | 文字转语音、多种音色 | 豆包语音合成模型2.0 |
| **唱歌** | 实时语音交互、唱歌、角色扮演 | 豆包端到端实时语音大模型 |

---

## 环境配置

### 1. 获取火山引擎豆包语音凭证

1. 访问 [火山引擎控制台](https://console.volcengine.com/)
2. 开通「豆包语音」服务
3. 创建应用获取 `App ID` 和 `Access Token`
4. 开通所需服务：
   - 「语音合成」权限：大模型语音合成

### 2. 凭证配置

创建 `~/.doubao-token` 文件：

```
DOUBAO_APP_ID=your_app_id
DOUBAO_ACCESS_TOKEN=your_access_token
```

也支持环境变量方式（`~/.doubao-token` 优先）。

### 3. Python 依赖

```bash
# 推荐使用 uv
uv pip install requests websocket-client

# 或使用 pip
pip install requests websocket-client
```

---

## API 基础

### Base URL

```
TTS API: https://openspeech.bytedance.com/api/v1/tts
```

### 认证方式

使用 Access Token 进行认证，在请求头中添加：
```
Authorization: Bearer {access_token}
```

---

## 一、语音合成 (TTS)

### 1.1 基础语音合成

将文本转换为语音文件。

**自然语言示例**:
- "把这段文字转成语音"
- "用豆包合成语音"
- "生成语音：你好，欢迎使用豆包语音"

**Python 实现**:

```python
import os
import requests
import json
import base64

def text_to_speech(text: str, voice_type: str = "BV700_V2_streaming", output_file: str = "output.mp3"):
    """
    文字转语音

    Args:
        text: 要合成的文本
        voice_type: 音色类型 (默认: BV700_V2_streaming)
        output_file: 输出音频文件路径

    Returns:
        音频文件路径
    """
    app_id = os.environ.get("DOUBAO_APP_ID")
    access_token = os.environ.get("DOUBAO_ACCESS_TOKEN")
    cluster = os.environ.get("DOUBAO_CLUSTER", "volcano_tts")

    url = "https://openspeech.bytedance.com/api/v1/tts"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "app": {
            "appid": app_id,
            "token": access_token,
            "cluster": cluster
        },
        "user": {
            "uid": "user123"
        },
        "audio": {
            "voice_type": voice_type,
            "encoding": "mp3",
            "speed_ratio": 1.0,
            "volume_ratio": 1.0,
            "pitch_ratio": 1.0
        },
        "request": {
            "reqid": "req_" + os.urandom(8).hex(),
            "text": text,
            "text_type": "plain",
            "operation": "query"
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if data.get("code") == 3000:
        # 解码音频数据
        audio_data = base64.b64decode(data["data"])
        with open(output_file, "wb") as f:
            f.write(audio_data)
        return output_file
    else:
        raise Exception(f"TTS 失败: {data}")

# 使用示例
audio_file = text_to_speech("你好，我是豆包语音助手")
print(f"语音已生成: {audio_file}")
```

### 1.2 流式语音合成

适用于长文本，边生成边播放。

```python
import websocket
import json
import os

def stream_tts(text: str, voice_type: str = "BV700_V2_streaming"):
    """
    流式语音合成

    Args:
        text: 要合成的文本
        voice_type: 音色类型
    """
    app_id = os.environ.get("DOUBAO_APP_ID")
    access_token = os.environ.get("DOUBAO_ACCESS_TOKEN")

    ws_url = f"wss://openspeech.bytedance.com/api/v1/tts/ws?appid={app_id}&token={access_token}"

    def on_message(ws, message):
        data = json.loads(message)
        if "audio" in data:
            # 处理音频数据
            audio_chunk = base64.b64decode(data["audio"])
            # 播放或保存音频片段
            print(f"收到音频片段: {len(audio_chunk)} 字节")

    def on_open(ws):
        payload = {
            "app": {
                "appid": app_id,
                "token": access_token,
                "cluster": "volcano_tts"
            },
            "user": {
                "uid": "user123"
            },
            "audio": {
                "voice_type": voice_type,
                "encoding": "mp3"
            },
            "request": {
                "reqid": "stream_" + os.urandom(8).hex(),
                "text": text,
                "text_type": "plain",
                "operation": "submit"
            }
        }
        ws.send(json.dumps(payload))

    ws = websocket.WebSocketApp(
        ws_url,
        on_message=on_message,
        on_open=on_open
    )
    ws.run_forever()

# 使用示例
stream_tts("这是一段很长的文本，使用流式合成可以边生成边播放...")
```

### 1.3 音色选择

豆包语音提供多种音色：

| 音色代码 | 描述 | 场景 |
|---------|------|------|
| BV700_V2_streaming | 通用女声 | 通用场景 |
| BV701_V2_streaming | 通用男声 | 通用场景 |
| BV406_streaming | 温柔女声 | 客服、助手 |
| BV158_streaming | 活泼女声 | 教育、娱乐 |
| BV115_streaming | 磁性男声 | 新闻、播音 |

**查询可用音色**:

```bash
TOKEN="${DOUBAO_ACCESS_TOKEN}"
APP_ID="${DOUBAO_APP_ID}"

curl -s "https://openspeech.bytedance.com/api/v1/tts/voices?appid=$APP_ID" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 完整工具类

```python
import os
import requests
import base64
import json
from typing import Optional

class DoubaoVoice:
    """豆包语音API工具类"""

    BASE_URL = "https://openspeech.bytedance.com/api/v1"

    def __init__(self, app_id: str = None, access_token: str = None):
        self.app_id = app_id or os.environ.get("DOUBAO_APP_ID")
        self.access_token = access_token or os.environ.get("DOUBAO_ACCESS_TOKEN")
        self.cluster_tts = os.environ.get("DOUBAO_CLUSTER", "volcano_tts")

    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def text_to_speech(
        self,
        text: str,
        voice_type: str = "BV700_V2_streaming",
        output_file: str = "output.mp3"
    ) -> str:
        """文字转语音"""
        url = f"{self.BASE_URL}/tts"

        payload = {
            "app": {
                "appid": self.app_id,
                "token": self.access_token,
                "cluster": self.cluster_tts
            },
            "user": {"uid": "user123"},
            "audio": {
                "voice_type": voice_type,
                "encoding": "mp3",
                "speed_ratio": 1.0,
                "volume_ratio": 1.0,
                "pitch_ratio": 1.0
            },
            "request": {
                "reqid": "req_" + os.urandom(8).hex(),
                "text": text,
                "text_type": "plain",
                "operation": "query"
            }
        }

        response = requests.post(url, headers=self.headers, json=payload)
        data = response.json()

        if data.get("code") == 3000:
            audio_data = base64.b64decode(data["data"])
            with open(output_file, "wb") as f:
                f.write(audio_data)
            return output_file
        else:
            raise Exception(f"TTS 失败: {data}")

    def list_voices(self) -> list:
        """获取可用音色列表"""
        url = f"{self.BASE_URL}/tts/voices"
        params = {"appid": self.app_id}

        response = requests.get(url, headers=self.headers, params=params)
        data = response.json()

        if data.get("code") == 0:
            return data["voices"]
        else:
            raise Exception(f"获取音色列表失败: {data}")


# ==================== 使用示例 ====================
if __name__ == "__main__":
    voice = DoubaoVoice()

    # 示例1: 文字转语音
    audio_file = voice.text_to_speech("你好，我是豆包语音助手")
    print(f"语音已生成: {audio_file}")

    # 示例2: 查看可用音色
    voices = voice.list_voices()
    for v in voices[:5]:
        print(f"{v['voice_type']}: {v['description']}")
```

---

## 二、唱歌 (豆包端到端实时语音大模型)

### 2.1 基础唱歌

让豆包唱歌，支持任何歌曲主题。

**自然语言示例**:
- "请唱一首关于春天的歌"
- "唱一个温柔的摇篮曲"
- "来一首欢快的儿歌"

**Python 实现**:

```python
import asyncio
from scripts.singing import DoubaoSinging

async def main():
    singing = DoubaoSinging()

    # 让豆包唱歌
    audio_file = await singing.sing(
        "请唱一首关于春天的歌",
        output_file="spring_song.mp3",
        language="zh-CN"
    )
    print(f"唱歌完成: {audio_file}")

asyncio.run(main())
```

### 2.2 交互式唱歌

与豆包进行实时对话，可以要求她唱歌、讲故事等。

**Python 实现**:

```python
import asyncio
from scripts.singing import DoubaoSinging

async def main():
    singing = DoubaoSinging()

    # 启动交互式模式
    await singing.interactive_singing(language="zh-CN")

asyncio.run(main())
```

**交互示例**:
```
你: 请唱一首情歌
豆包: [生成音频] 我会为你唱一首温柔的情歌...

你: 能加点方言吗？
豆包: [用方言重新唱歌]

你: quit
再见!
```

---

## 自然语言操作示例

### TTS 操作

| 用户说 | 执行操作 |
|--------|----------|
| "把这段话转成语音：你好世界" | 调用 TTS API 生成语音 |
| "用温柔女声合成语音" | 使用 BV406_streaming 音色 |
| "生成一段播音腔的新闻语音" | 使用磁性男声音色 |

### 唱歌操作

| 用户说 | 执行操作 |
|--------|----------|
| "请唱一首关于春天的歌" | 调用端到端实时语音大模型生成唱歌音频 |
| "唱一首摇篮曲" | 生成温柔的摇篮曲 |
| "唱歌的同时讲个故事" | 交互式对话中唱歌并讲故事 |
| "开启交互式唱歌模式" | 启动实时语音交互 |

---

## 计费说明

### TTS 计费

- **并发版**: 2000元/并发/月（纯并发计费，不收取字符调用费用）
- **按量付费**: 按合成字符数计费

### 免费试用

新用户开通服务后可获得一定免费额度，具体额度以控制台显示为准。

---

## 注意事项

1. **音频格式**: TTS 支持 mp3/wav/pcm
2. **文本长度**: TTS 单次请求最长支持 5000 字符
3. **并发限制**: 注意 API 调用频率和并发数限制
4. **Token 安全**: Access Token 存储在环境变量中，不要硬编码

---

## 错误处理

```python
def safe_tts(text: str):
    """带错误处理的 TTS"""
    try:
        voice = DoubaoVoice()
        return voice.text_to_speech(text)
    except Exception as e:
        if "401" in str(e):
            print("认证失败，请检查 Access Token")
        elif "429" in str(e):
            print("请求过于频繁，请稍后重试")
        else:
            print(f"合成失败: {e}")
        return None
```

---

## 常见场景

### 场景 1: 生成多语言语音

```python
voice = DoubaoVoice()

# 中文
voice.text_to_speech("你好", voice_type="BV700_V2_streaming", output_file="zh.mp3")

# 英文
voice.text_to_speech("Hello", voice_type="EN_001", output_file="en.mp3")
```


---

## 参考资源

- [火山引擎豆包语音文档](https://www.volcengine.com/docs/6561/1359369)
- [豆包语音控制台](https://console.volcengine.com/speech/app)
- [API 接口文档](https://www.volcengine.com/docs/6561/1359370)
- [计费说明](https://www.volcengine.com/docs/6561/1359370)
