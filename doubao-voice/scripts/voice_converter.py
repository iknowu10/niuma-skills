#!/usr/bin/env python3
"""
豆包语音转换工具
支持：文字转语音 (TTS)
"""

import os
import sys
import json
import base64
import requests
from pathlib import Path


def _load_doubao_credentials():
    """从 ~/.doubao-token 文件或环境变量读取凭证"""
    token_file = Path.home() / ".doubao-token"
    app_id = os.environ.get("DOUBAO_APP_ID")
    access_token = os.environ.get("DOUBAO_ACCESS_TOKEN")

    if token_file.exists():
        for line in token_file.read_text().strip().splitlines():
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key, val = key.strip(), val.strip().strip('"').strip("'")
            if key == "DOUBAO_APP_ID":
                app_id = val
            elif key == "DOUBAO_ACCESS_TOKEN":
                access_token = val

    if not app_id or not access_token:
        raise ValueError(
            "豆包凭证未配置。请创建 ~/.doubao-token 文件:\n"
            "DOUBAO_APP_ID=your_app_id\n"
            "DOUBAO_ACCESS_TOKEN=your_access_token"
        )
    return app_id, access_token


class DoubaoVoiceConverter:
    """豆包语音转换工具类"""

    def __init__(self):
        self.app_id, self.access_token = _load_doubao_credentials()

        # API版本选择: V1 (默认, 支持基础音色) 或 V3 (豆包2.0, 需额外配置)
        self.use_v3 = os.environ.get("DOUBAO_USE_V3", "false").lower() == "true"

        if self.use_v3:
            self.tts_url = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"
            self.resource_id = os.environ.get("DOUBAO_RESOURCE_ID", "volc.bigmodel.tts")
        else:
            # V1 API - 稳定可用，支持基础音色
            self.tts_url = "https://openspeech.bytedance.com/api/v1/tts"

    def text_to_speech(
        self,
        text: str,
        output_file: str = "output.mp3",
        voice_type: str = "BV700_V2_streaming"
    ) -> str:
        """
        文字转语音 (TTS)

        Args:
            text: 要转换的文字
            output_file: 输出音频文件路径
            voice_type: 音色类型
                - BV700_V2_streaming: 通用女声（推荐）
                - BV701_V2_streaming: 通用男声
                - BV406_streaming: 温柔女声
                - BV158_streaming: 活泼女声
                - BV115_streaming: 磁性男声

        Returns:
            str: 输出文件路径
        """
        print(f"📝 文字转语音中...")
        print(f"   文字: {text[:50]}{'...' if len(text) > 50 else ''}")
        print(f"   音色: {voice_type}")

        headers = {
            "Authorization": f"Bearer;{self.access_token}",
            "Content-Type": "application/json"
        }

        # V3 API需要Resource-Id (如果启用)
        if self.use_v3:
            headers["Resource-Id"] = self.resource_id

        payload = {
            "app": {
                "appid": self.app_id,
                "token": self.access_token,
                "cluster": "volcano_tts"
            },
            "user": {
                "uid": "user_001"
            },
            "audio": {
                "voice_type": voice_type,
                "encoding": "mp3",
                "speed_ratio": 1.0,
                "volume_ratio": 1.0,
                "pitch_ratio": 1.0
            },
            "request": {
                "reqid": f"tts_{os.urandom(8).hex()}",
                "text": text,
                "text_type": "plain",
                "operation": "query"
            }
        }

        try:
            response = requests.post(self.tts_url, headers=headers, json=payload, timeout=30)

            # 打印响应头信息
            print(f"\n📋 响应信息:")
            print(f"   HTTP状态码: {response.status_code}")
            if 'X-Tt-Logid' in response.headers:
                print(f"   RequestId: {response.headers['X-Tt-Logid']}")
            if 'X-Request-Id' in response.headers:
                print(f"   X-Request-Id: {response.headers['X-Request-Id']}")

            data = response.json()

            # 打印完整响应
            print(f"\n📄 完整响应:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            print()

            if data.get("code") == 3000:
                # 成功：解码并保存音频
                audio_data = base64.b64decode(data["data"])
                with open(output_file, "wb") as f:
                    f.write(audio_data)

                file_size = len(audio_data) / 1024  # KB
                print(f"✅ 语音合成成功!")
                print(f"   输出: {output_file} ({file_size:.1f} KB)")
                return output_file
            else:
                error_msg = data.get("message", "未知错误")
                reqid = data.get("reqid", "未知")
                raise Exception(f"TTS 失败\n   错误码: {data.get('code')}\n   错误信息: {error_msg}\n   RequestId: {reqid}")

        except requests.exceptions.Timeout:
            raise Exception("请求超时，请检查网络连接")
        except Exception as e:
            raise Exception(f"TTS 调用失败: {str(e)}")



def main():
    """命令行工具"""
    import argparse

    parser = argparse.ArgumentParser(description="豆包语音转换工具")
    subparsers = parser.add_subparsers(dest="command", help="选择功能")

    # TTS 命令
    tts_parser = subparsers.add_parser("tts", help="文字转语音")
    tts_parser.add_argument("text", help="要转换的文字")
    tts_parser.add_argument("-o", "--output", default="output.mp3", help="输出音频文件（默认: output.mp3）")
    tts_parser.add_argument("-v", "--voice", default="BV700_V2_streaming",
                           help="音色类型（默认: BV700_V2_streaming 通用女声）")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        converter = DoubaoVoiceConverter()

        if args.command == "tts":
            converter.text_to_speech(args.text, args.output, args.voice)

    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
