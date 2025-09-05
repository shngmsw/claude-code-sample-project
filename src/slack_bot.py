"""Slack Bot implementation with Dify API integration using Socket Mode."""

import os
import logging
from typing import Optional
import httpx
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

logger = logging.getLogger(__name__)


class SlackBot:
    """Slack Bot with Dify API integration using Socket Mode."""
    
    def __init__(self):
        self.bot_token = os.getenv("SLACK_BOT_TOKEN", "")
        self.app_token = os.getenv("SLACK_APP_TOKEN", "")
        self.dify_api_key = os.getenv("DIFY_API_KEY", "")
        self.dify_base_url = os.getenv("DIFY_BASE_URL", "")
        self.client = httpx.AsyncClient()
        self.conversations = {}  # Store conversation IDs per user
        
        # Initialize Slack Bolt app
        self.app = App(token=self.bot_token)
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup Slack event handlers."""
        
        @self.app.message()
        async def handle_message(message, say):
            """Handle direct messages to the bot."""
            text = message.get("text", "")
            user = message.get("user")
            
            if not text.strip():
                return
                
            # Get response from Dify API
            dify_response = await self._query_dify_api(text, user)
            
            if dify_response:
                await say(dify_response)
            else:
                await say("申し訳ございません。現在AIサービスが利用できません。")
        
        @self.app.event("app_mention")
        async def handle_mention(event, say):
            """Handle when the bot is mentioned in a channel."""
            text = event.get("text", "")
            user = event.get("user")
            
            # Remove bot mention from text
            import re
            clean_text = re.sub(r'<@\w+>', '', text).strip()
            
            if not clean_text:
                clean_text = "こんにちは"
                
            # Get response from Dify API
            dify_response = await self._query_dify_api(clean_text, user)
            
            if dify_response:
                await say(dify_response)
            else:
                await say("申し訳ございません。現在AIサービスが利用できません。")
        
        @self.app.command("/dify")
        async def handle_dify_command(ack, respond, command):
            """Handle /dify slash command."""
            await ack()
            
            text = command.get("text", "")
            user_id = command.get("user_id")
            
            if not text.strip():
                await respond({
                    "response_type": "ephemeral",
                    "text": "使用方法: /dify [質問内容]"
                })
                return
                
            # Get response from Dify API
            dify_response = await self._query_dify_api(text, user_id)
            
            if dify_response:
                await respond({
                    "response_type": "in_channel",
                    "text": f"**質問:** {text}\n**回答:** {dify_response}"
                })
            else:
                await respond({
                    "response_type": "ephemeral",
                    "text": "申し訳ございません。現在AIサービスが利用できません。"
                })
    
    def start(self):
        """Start the Socket Mode handler."""
        if not self.app_token:
            logger.error("SLACK_APP_TOKEN not set")
            return
            
        handler = SocketModeHandler(self.app, self.app_token)
        handler.start()
    
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