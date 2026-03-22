#!/usr/bin/env python3
"""
豆包唱歌工具
基于豆包端到端实时语音大模型，支持让豆包唱歌
使用WebSocket实时对话和生成音频
"""

import os
import sys
import json
import asyncio
import websockets
import struct
import uuid
from typing import Optional


# 连接级事件（不需要session_id）
CONNECTION_EVENTS = {1, 2, 50, 51, 52}


def _load_doubao_credentials():
    """从 ~/.doubao-token 文件或环境变量读取凭证"""
    from pathlib import Path
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


class DoubaoSinging:
    """豆包唱歌工具类"""

    def __init__(self):
        self.app_id, self.access_token = _load_doubao_credentials()

        # 端到端实时语音WebSocket地址
        self.ws_url = "wss://openspeech.bytedance.com/api/v3/realtime/dialogue"
        self.app_key = "PlgvMymc7f3tQnJ6"  # 固定值
        self.resource_id = "volc.speech.dialog"  # 固定值

    def _build_message(self, event_id: int, payload: dict = None, session_id: str = None) -> bytes:
        """
        构建二进制消息

        协议格式:
        - header (4 bytes)
        - event_id (4 bytes, big-endian)
        - [session_id_len (4 bytes) + session_id (variable)] -- 仅非连接级事件
        - payload_len (4 bytes, big-endian)
        - payload (variable, JSON)
        """
        buf = bytearray()

        # Header (4 bytes)
        buf.append(0x11)  # version=1, header_size=1
        buf.append(0x14)  # FULL_CLIENT_REQUEST(0x1) + WITH_EVENT(0x4)
        buf.append(0x10)  # JSON serialization, no compression
        buf.append(0x00)  # reserved

        # Event ID
        buf.extend(struct.pack('>I', event_id))

        # Session ID (required for non-connection events)
        if event_id not in CONNECTION_EVENTS:
            sid_bytes = (session_id or "").encode('utf-8')
            buf.extend(struct.pack('>I', len(sid_bytes)))
            buf.extend(sid_bytes)

        # Payload
        if payload:
            payload_bytes = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        else:
            payload_bytes = b'{}'
        buf.extend(struct.pack('>I', len(payload_bytes)))
        buf.extend(payload_bytes)

        return bytes(buf)

    def _parse_response(self, data: bytes) -> dict:
        """
        解析服务端二进制消息

        Returns:
            dict with keys: msg_type, event_id, session_id, payload, payload_bytes
        """
        result = {"raw": data}
        if len(data) < 4:
            return result

        # Header
        msg_type = (data[1] >> 4) & 0x0F
        flags = data[1] & 0x0F
        result["msg_type"] = msg_type

        offset = 4

        # Event ID (if WITH_EVENT flag)
        if flags & 0x04 and len(data) >= offset + 4:
            event_id = struct.unpack('>I', data[offset:offset + 4])[0]
            result["event_id"] = event_id
            offset += 4

            # Connect ID for connection events (50, 51, 52)
            if event_id in {50, 51, 52} and len(data) >= offset + 4:
                cid_len = struct.unpack('>I', data[offset:offset + 4])[0]
                offset += 4
                if len(data) >= offset + cid_len:
                    result["connect_id"] = data[offset:offset + cid_len].decode('utf-8', errors='ignore')
                    offset += cid_len
            # Session ID for session-level events
            elif event_id not in CONNECTION_EVENTS and len(data) >= offset + 4:
                sid_len = struct.unpack('>I', data[offset:offset + 4])[0]
                offset += 4
                if len(data) >= offset + sid_len:
                    result["session_id"] = data[offset:offset + sid_len].decode('utf-8', errors='ignore')
                    offset += sid_len

        # Payload
        if len(data) >= offset + 4:
            payload_len = struct.unpack('>I', data[offset:offset + 4])[0]
            offset += 4
            if len(data) >= offset + payload_len:
                payload_raw = data[offset:offset + payload_len]
                result["payload_bytes"] = payload_raw
                # Audio-only responses (msg_type 0xB) have raw audio
                if msg_type == 0x0B:
                    result["is_audio"] = True
                else:
                    try:
                        result["payload"] = json.loads(payload_raw.decode('utf-8'))
                    except:
                        result["payload_text"] = payload_raw.decode('utf-8', errors='ignore')

        return result

    async def sing(
        self,
        song_request: str,
        output_file: str = "singing_output.mp3",
        language: str = "zh-CN",
        model: str = "1.2.1.0"
    ) -> str:
        """
        让豆包唱歌

        Args:
            song_request: 唱歌请求，如 "请唱一首关于春天的歌"
            output_file: 输出音频文件路径
            language: 语言代码 (zh-CN/en-US)
            model: 模型版本

        Returns:
            str: 输出文件路径
        """
        print(f"🎵 豆包唱歌中...")
        print(f"   请求: {song_request}")
        print(f"   模型: {model}")

        try:
            audio_data = bytearray()
            session_id = str(uuid.uuid4())

            # WebSocket连接头
            headers = {
                "X-Api-App-ID": self.app_id,
                "X-Api-Access-Key": self.access_token,
                "X-Api-Resource-Id": self.resource_id,
                "X-Api-App-Key": self.app_key,
                "X-Api-Connect-Id": str(uuid.uuid4()),
            }

            async with websockets.connect(self.ws_url, additional_headers=headers) as websocket:
                print("✅ WebSocket连接成功")

                # 1. StartConnection (event_id=1, 无需session_id)
                await websocket.send(self._build_message(1))
                response = await asyncio.wait_for(websocket.recv(), timeout=5)
                resp = self._parse_response(response)
                if resp.get("event_id") == 50:
                    print(f"✅ 连接已建立")
                else:
                    print(f"⚠️  连接响应: {resp}")

                # 2. StartSession (event_id=100, 需要session_id)
                start_session_payload = {
                    "tts": {
                        "audio_config": {
                            "channel": 1,
                            "format": "pcm",
                            "sample_rate": 24000
                        }
                    },
                    "dialog": {
                        "extra": {
                            "enable_music": True,
                            "input_mod": "text",
                            "model": model
                        }
                    }
                }
                await websocket.send(self._build_message(100, start_session_payload, session_id))
                response = await asyncio.wait_for(websocket.recv(), timeout=5)
                resp = self._parse_response(response)
                if resp.get("event_id") == 150:
                    print(f"✅ 会话已建立")
                elif resp.get("payload", {}).get("error"):
                    print(f"❌ 会话错误: {resp['payload']['error']}")
                    return None
                else:
                    print(f"📋 会话响应: {resp}")

                # 3. SayHello/ChatTextQuery (event_id=300, 需要session_id)
                chat_payload = {"content": song_request}
                await websocket.send(self._build_message(300, chat_payload, session_id))
                print(f"📤 已发送唱歌请求")

                # 4. 接收音频流（使用超时检测结束）
                print("\n📋 接收音频流...")
                tts_started = False
                recv_timeout = 5  # 5秒无数据则认为结束

                while True:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=recv_timeout)
                    except asyncio.TimeoutError:
                        break
                    except websockets.exceptions.ConnectionClosed:
                        break

                    if isinstance(message, bytes) and len(message) >= 4:
                        resp = self._parse_response(message)
                        msg_type = resp.get("msg_type", 0)
                        flags = message[1] & 0x0F

                        # Audio-only response (0xB = 11)
                        if resp.get("is_audio") and resp.get("payload_bytes"):
                            audio_data.extend(resp["payload_bytes"])
                            if not tts_started:
                                print(f"   接收音频中...", end="", flush=True)
                                tts_started = True
                            else:
                                print(".", end="", flush=True)

                            # NEG_SEQUENCE flag = last packet
                            if flags & 0x02:
                                break

                        # Server error (0xF = 15)
                        elif msg_type == 0x0F:
                            error = resp.get("payload", {}).get("error", "unknown")
                            print(f"\n❌ 服务器错误: {error}")
                            break

                        # Full server response (0x9) - session finished
                        elif msg_type == 0x09:
                            event_id = resp.get("event_id", 0)
                            if event_id in {152, 52}:
                                break

                # 5. 保存音频文件
                if audio_data:
                    # Save as PCM, convert extension if needed
                    actual_output = output_file
                    if output_file.endswith('.mp3'):
                        actual_output = output_file.replace('.mp3', '.pcm')

                    with open(actual_output, "wb") as f:
                        f.write(audio_data)

                    file_size = len(audio_data) / 1024
                    print(f"\n\n✅ 唱歌完成!")
                    print(f"   输出: {actual_output} ({file_size:.1f} KB)")
                    print(f"   格式: PCM (24000Hz, 单声道)")
                    return actual_output
                else:
                    print("\n⚠️ 未收到音频数据，请检查:")
                    print("   1. 凭证是否正确")
                    print("   2. 端到端实时语音大模型是否已开通")
                    print("   3. 网络连接是否正常")
                    return None

        except websockets.exceptions.WebSocketException as e:
            raise Exception(f"WebSocket连接错误: {str(e)}")
        except Exception as e:
            raise Exception(f"唱歌调用失败: {str(e)}")


def main():
    """命令行工具"""
    import argparse

    parser = argparse.ArgumentParser(description="豆包唱歌工具")
    subparsers = parser.add_subparsers(dest="command", help="选择功能")

    # 唱歌命令
    sing_parser = subparsers.add_parser("sing", help="让豆包唱歌")
    sing_parser.add_argument("request", help="唱歌请求，如 '请唱一首关于春天的歌'")
    sing_parser.add_argument(
        "-o", "--output", default="singing_output.mp3", help="输出音频文件（默认: singing_output.mp3）"
    )
    sing_parser.add_argument(
        "-l", "--language", default="zh-CN", help="语言代码（默认: zh-CN）"
    )
    sing_parser.add_argument(
        "-m", "--model", default="1.2.1.0", help="模型版本（默认: 1.2.1.0=O2.0版本）"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        singing = DoubaoSinging()

        if args.command == "sing":
            asyncio.run(singing.sing(args.request, args.output, args.language, args.model))

    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
