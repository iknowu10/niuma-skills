# 豆包语音工具使用指南

简单易用的豆包语音命令行工具，支持**文字转语音(TTS)**和**唱歌**。

## 快速开始

### 1. 配置环境变量

```bash
# 在 ~/.zshrc 或 ~/.bashrc 中添加
export DOUBAO_APP_ID="your_app_id"
export DOUBAO_ACCESS_TOKEN="your_access_token"

# 使配置生效
source ~/.zshrc
```

### 2. 安装依赖

```bash
pip install requests
```

## 使用方法

### 📝 文字转语音 (TTS)

**基础用法：**
```bash
python voice_converter.py tts "你好，我是豆包语音助手"
```

**指定输出文件和音色：**
```bash
python voice_converter.py tts "欢迎使用豆包语音" -o welcome.mp3 -v BV701_V2_streaming
```

**可用音色：**
- `BV700_V2_streaming` - 通用女声（默认，推荐）
- `BV701_V2_streaming` - 通用男声
- `BV406_streaming` - 温柔女声
- `BV158_streaming` - 活泼女声
- `BV115_streaming` - 磁性男声

### 🎵 唱歌 (Singing)

**基础用法：**
```bash
python singing.py sing "请唱一首关于春天的歌"
```

**指定输出文件：**
```bash
python singing.py sing "唱一个温柔的摇篮曲" -o lullaby.mp3
```

**交互式模式（实时对话）：**
```bash
python singing.py interactive
```

在交互模式下可以自然地与豆包对话，要求她唱歌、讲故事等。输入 `quit` 退出。

## Python 代码调用

```python
# TTS - 文字转语音
from voice_converter import DoubaoVoiceConverter

converter = DoubaoVoiceConverter()
audio_file = converter.text_to_speech(
    "你好，欢迎使用豆包语音",
    output_file="hello.mp3",
    voice_type="BV700_V2_streaming"
)
print(f"生成语音: {audio_file}")

# 唱歌
import asyncio
from singing import DoubaoSinging

async def main():
    singing = DoubaoSinging()

    # 让豆包唱歌
    audio_file = await singing.sing(
        "请唱一首情歌",
        output_file="love_song.mp3",
        language="zh-CN"
    )
    print(f"唱歌完成: {audio_file}")

    # 或启动交互模式
    # await singing.interactive_singing()

asyncio.run(main())
```

## 完整示例

### 示例1：生成通知语音

```bash
# 生成女声通知
python voice_converter.py tts "您有一条新消息，请注意查收" -o notification.mp3

# 生成男声通知
python voice_converter.py tts "系统将在5分钟后进行维护" -o maintenance.mp3 -v BV701_V2_streaming
```

### 示例2：唱歌

```bash
# 让豆包唱一首情歌
python singing.py sing "请唱一首温柔的情歌" -o love_song.mp3

# 让豆包唱一首儿歌
python singing.py sing "唱一首欢快的儿歌" -o kids_song.mp3

# 启动交互式模式与豆包对话
python singing.py interactive
```


## 错误处理

### 常见错误

**1. 环境变量未设置**
```
❌ 错误: 请先设置环境变量:
export DOUBAO_APP_ID='your_app_id'
export DOUBAO_ACCESS_TOKEN='your_access_token'
```
**解决：** 确保已正确设置环境变量并 `source ~/.zshrc`

**2. API 调用失败**
```
❌ 错误: TTS 失败 (code: 4001): Invalid token
```
**解决：** 检查 Access Token 是否正确或已过期

## 技术参数

### 音频格式要求

**TTS 输出：**
- 格式：MP3
- 采样率：16000 Hz
- 声道：单声道

### API 限制

- **TTS**: 单次最长 5000 字符
- **并发限制**: 根据购买的并发数

## 在 Claude Code 中使用

在 Claude Code 中可以直接用自然语言调用：

**TTS - 文字转语音**:
```
"把这段话转成语音：你好世界"
"用温柔女声合成：欢迎光临"
```

**唱歌**:
```
"请唱一首关于春天的歌"
"唱一个温柔的摇篮曲"
"开启与豆包的实时语音对话模式"
```

## 获取 API 凭证

1. 访问 [火山引擎控制台](https://console.volcengine.com/speech/app)
2. 创建应用
3. 获取 App ID 和 Access Token
4. 开通所需服务：
   - 豆包语音合成模型2.0

## 参考链接

- [火山引擎豆包语音文档](https://www.volcengine.com/docs/6561)
- [API 接口文档](https://www.volcengine.com/docs/6561/1096680)
- [计费说明](https://www.volcengine.com/docs/6561/1359370)
