"""Simple data models for Dify API integration."""

from typing import Optional, Dict, Any


class DifyAPIRequest:
    """Dify API request model."""
    
    def __init__(self, query: str, user: str, conversation_id: Optional[str] = None, inputs: Optional[Dict[str, Any]] = None):
        self.query = query
        self.user = user
        self.conversation_id = conversation_id
        self.inputs = inputs or {}


class DifyAPIResponse:
    """Dify API response model."""
    
    def __init__(self, answer: str, conversation_id: str, message_id: str = "", event: str = "", created_at: int = 0, metadata: Optional[Dict[str, Any]] = None):
        self.answer = answer
        self.conversation_id = conversation_id
        self.message_id = message_id
        self.event = event
        self.created_at = created_at
        self.metadata = metadata or {}