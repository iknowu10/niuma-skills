#!/bin/bash
# 豆包语音 API 环境变量配置 (示例)
#
# ⚠️ 重要：这是示例脚本，包含占位符。
# 本地使用时，请参考 setup_env.local.sh.example 创建 setup_env.local.sh，
# 然后在其中填入您的真实凭证。.gitignore 已配置忽略 .local 文件。

export DOUBAO_APP_ID="your_app_id"
export DOUBAO_ACCESS_TOKEN="your_access_token"

# V3 API 配置 (可选，如需豆包2.0音色)
# export DOUBAO_USE_V3="true"
# export DOUBAO_RESOURCE_ID="volc.bigmodel.tts"

echo "✅ 豆包语音 API 环境变量已设置"
echo ""
echo "App ID: $DOUBAO_APP_ID"
echo "Access Token: ${DOUBAO_ACCESS_TOKEN:0:20}..."
echo ""
echo "现在可以运行:"
echo "  python3 voice_converter.py tts \"你好世界\" -o hello.mp3"
echo "  python3 voice_converter.py asr audio.mp3  # 需先启用ASR服务"
