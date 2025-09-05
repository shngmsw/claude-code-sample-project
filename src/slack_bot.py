"""Slack Bot implementation for handling events and commands."""

import json
import os
import logging
from typing import Dict, Any, Optional
import hashlib
import hmac
import time
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import httpx

logger = logging.getLogger(__name__)


class SlackBot:
    """Slack Bot for handling events, messages, and slash commands."""
    
    def __init__(self):
        self.signing_secret = os.getenv("SLACK_SIGNING_SECRET", "")
        self.bot_token = os.getenv("SLACK_BOT_TOKEN", "")
        self.client = httpx.AsyncClient()
        
    def _verify_slack_request(self, body: bytes, timestamp: str, signature: str) -> bool:
        """Verify that the request came from Slack."""
        if not self.signing_secret:
            logger.warning("SLACK_SIGNING_SECRET not set, skipping verification")
            return True
            
        if abs(time.time() - int(timestamp)) > 60 * 5:
            return False
            
        sig_basestring = f"v0:{timestamp}:{body.decode()}"
        my_signature = "v0=" + hmac.new(
            self.signing_secret.encode(),
            sig_basestring.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(my_signature, signature)
    
    async def handle_event(self, body: bytes, headers: Dict[str, str]) -> JSONResponse:
        """Handle incoming Slack events."""
        try:
            timestamp = headers.get("x-slack-request-timestamp", "")
            signature = headers.get("x-slack-signature", "")
            
            if not self._verify_slack_request(body, timestamp, signature):
                raise HTTPException(status_code=400, detail="Invalid request signature")
            
            data = json.loads(body.decode())
            
            # Handle URL verification challenge
            if data.get("type") == "url_verification":
                return JSONResponse({"challenge": data["challenge"]})
            
            # Handle events
            if data.get("type") == "event_callback":
                await self._handle_event_callback(data)
            
            # Handle slash commands
            if "command" in data:
                return await self._handle_slash_command(data)
            
            return JSONResponse({"status": "ok"})
            
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON")
        except Exception as e:
            logger.error(f"Error handling Slack event: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    async def _handle_event_callback(self, data: Dict[str, Any]) -> None:
        """Handle Slack event callbacks."""
        event = data.get("event", {})
        event_type = event.get("type")
        
        if event_type == "message" and not event.get("bot_id"):
            await self._handle_message(event)
        elif event_type == "app_mention":
            await self._handle_mention(event)
    
    async def _handle_message(self, event: Dict[str, Any]) -> None:
        """Handle direct messages to the bot."""
        text = event.get("text", "").lower()
        channel = event.get("channel")
        user = event.get("user")
        
        if "hello" in text or "hi" in text:
            response = "👋 こんにちは！私はSlack Botサンプルです。以下のコマンドが使えます:\n" \
                      "• `status` - アプリケーションの状態を確認\n" \
                      "• `help` - ヘルプを表示\n" \
                      "• `joke` - ジョークを表示"
        elif "status" in text:
            response = "✅ アプリケーションは正常に動作中です！\n🌐 Web UI: http://localhost:8000"
        elif "help" in text:
            response = "🤖 Slack Bot コマンド一覧:\n" \
                      "• `hello/hi` - 挨拶とコマンド一覧\n" \
                      "• `status` - アプリケーション状態\n" \
                      "• `joke` - ランダムなジョーク\n" \
                      "• `/sample` - スラッシュコマンドのサンプル"
        elif "joke" in text:
            jokes = [
                "なぜプログラマーは暗いところを好むのか？\nバグが光を嫌うからです！🐛",
                "コンピューターと人間の違いは？\nコンピューターは正確にやりたいことをします。",
                "なぜPythonプログラマーは蛇を飼わないのか？\nインデントが面倒だからです！🐍"
            ]
            import random
            response = random.choice(jokes)
        else:
            response = f"メッセージを受信しました: {event.get('text')}\n" \
                      f"`hello` や `help` と入力してコマンドを確認してください。"
        
        await self._send_message(channel, response)
    
    async def _handle_mention(self, event: Dict[str, Any]) -> None:
        """Handle when the bot is mentioned in a channel."""
        text = event.get("text", "")
        channel = event.get("channel")
        
        response = f"📢 メンションありがとうございます！\n" \
                  f"DMで詳細なコマンドを利用できます。\n" \
                  f"Web UI: http://localhost:8000"
        
        await self._send_message(channel, response)
    
    async def _handle_slash_command(self, data: Dict[str, Any]) -> JSONResponse:
        """Handle slash commands."""
        command = data.get("command")
        text = data.get("text", "")
        user_name = data.get("user_name")
        
        if command == "/sample":
            response_text = f"🎉 こんにちは {user_name}さん！\n" \
                           f"入力されたテキスト: '{text}'\n" \
                           f"このサンプルSlash Commandは正常に動作しています。\n" \
                           f"Web UI: http://localhost:8000"
            
            return JSONResponse({
                "response_type": "in_channel",  # or "ephemeral" for private response
                "text": response_text,
                "attachments": [
                    {
                        "color": "good",
                        "title": "Slack Bot Sample",
                        "title_link": "http://localhost:8000",
                        "fields": [
                            {
                                "title": "コマンド",
                                "value": command,
                                "short": True
                            },
                            {
                                "title": "ユーザー",
                                "value": user_name,
                                "short": True
                            }
                        ],
                        "footer": "Slack Bot Sample",
                        "ts": int(time.time())
                    }
                ]
            })
        
        return JSONResponse({
            "text": f"未知のコマンド: {command}"
        })
    
    async def _send_message(self, channel: str, text: str) -> None:
        """Send a message to a Slack channel."""
        if not self.bot_token:
            logger.warning("SLACK_BOT_TOKEN not set, cannot send message")
            return
        
        try:
            response = await self.client.post(
                "https://slack.com/api/chat.postMessage",
                headers={
                    "Authorization": f"Bearer {self.bot_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "channel": channel,
                    "text": text
                }
            )
            
            if not response.is_success:
                logger.error(f"Failed to send Slack message: {response.text}")
                
        except Exception as e:
            logger.error(f"Error sending Slack message: {e}")
    
    async def cleanup(self) -> None:
        """Cleanup resources."""
        await self.client.aclose()