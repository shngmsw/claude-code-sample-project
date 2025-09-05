"""Slack Bot implementation with Dify API integration."""

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
from src.models import DifyAPIRequest, DifyAPIResponse

logger = logging.getLogger(__name__)


class SlackBot:
    """Slack Bot with Dify API integration."""
    
    def __init__(self):
        self.signing_secret = os.getenv("SLACK_SIGNING_SECRET", "")
        self.bot_token = os.getenv("SLACK_BOT_TOKEN", "")
        self.dify_api_key = os.getenv("DIFY_API_KEY", "")
        self.dify_base_url = os.getenv("DIFY_BASE_URL", "")
        self.client = httpx.AsyncClient()
        self.conversations = {}  # Store conversation IDs per user
        
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
        """Handle direct messages to the bot via Dify API."""
        text = event.get("text", "")
        channel = event.get("channel")
        user = event.get("user")
        
        if not text.strip():
            return
            
        # Get response from Dify API
        dify_response = await self._query_dify_api(text, user)
        
        if dify_response:
            await self._send_message(channel, dify_response)
        else:
            await self._send_message(channel, "申し訳ございません。現在AIサービスが利用できません。")
    
    async def _handle_mention(self, event: Dict[str, Any]) -> None:
        """Handle when the bot is mentioned in a channel via Dify API."""
        text = event.get("text", "")
        channel = event.get("channel")
        user = event.get("user")
        
        # Remove bot mention from text
        bot_id = f"<@{os.getenv('SLACK_BOT_USER_ID', '')}>"
        clean_text = text.replace(bot_id, "").strip()
        
        if not clean_text:
            clean_text = "こんにちは"
            
        # Get response from Dify API
        dify_response = await self._query_dify_api(clean_text, user)
        
        if dify_response:
            await self._send_message(channel, dify_response)
        else:
            await self._send_message(channel, "申し訳ございません。現在AIサービスが利用できません。")
    
    async def _handle_slash_command(self, data: Dict[str, Any]) -> JSONResponse:
        """Handle slash commands via Dify API."""
        command = data.get("command")
        text = data.get("text", "")
        user_id = data.get("user_id")
        user_name = data.get("user_name")
        
        if command == "/dify":
            if not text.strip():
                return JSONResponse({
                    "response_type": "ephemeral",
                    "text": "使用方法: /dify [質問内容]"
                })
                
            # Get response from Dify API
            dify_response = await self._query_dify_api(text, user_id)
            
            if dify_response:
                return JSONResponse({
                    "response_type": "in_channel",
                    "text": f"**質問:** {text}\n**回答:** {dify_response}"
                })
            else:
                return JSONResponse({
                    "response_type": "ephemeral",
                    "text": "申し訳ございません。現在AIサービスが利用できません。"
                })
        
        return JSONResponse({
            "response_type": "ephemeral",
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
    
    async def _query_dify_api(self, query: str, user: str) -> Optional[str]:
        """Query Dify API and return response."""
        if not self.dify_api_key or not self.dify_base_url:
            logger.warning("Dify API credentials not configured")
            return None
            
        try:
            # Get conversation ID for user
            conversation_id = self.conversations.get(user)
            
            request_data = {
                "inputs": {},
                "query": query,
                "response_mode": "blocking",
                "conversation_id": conversation_id,
                "user": user
            }
            
            response = await self.client.post(
                f"{self.dify_base_url}/chat-messages",
                headers={
                    "Authorization": f"Bearer {self.dify_api_key}",
                    "Content-Type": "application/json"
                },
                json=request_data,
                timeout=30.0
            )
            
            if response.is_success:
                data = response.json()
                # Store conversation ID for future requests
                if "conversation_id" in data:
                    self.conversations[user] = data["conversation_id"]
                
                return data.get("answer", "")
            else:
                logger.error(f"Dify API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error querying Dify API: {e}")
            return None
    
    async def cleanup(self) -> None:
        """Cleanup resources."""
        await self.client.aclose()