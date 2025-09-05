"""Data models for the Slack Bot with Dify API integration."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class HealthCheck(BaseModel):
    """Health check response model."""
    
    status: str = Field(..., description="Application status")
    version: str = Field(..., description="Application version")
    message: str = Field(..., description="Health check message")


class ErrorResponse(BaseModel):
    """Standard error response model."""
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")


class SlackEvent(BaseModel):
    """Slack event webhook payload model."""
    
    token: str = Field(..., description="Verification token")
    challenge: Optional[str] = Field(None, description="Challenge parameter for URL verification")
    type: str = Field(..., description="Event type")
    event: Optional[dict] = Field(None, description="Event data")
    team_id: Optional[str] = Field(None, description="Team ID")
    api_app_id: Optional[str] = Field(None, description="App ID")


class DifyAPIRequest(BaseModel):
    """Dify API request model."""
    
    query: str = Field(..., description="User query text")
    user: str = Field(..., description="User identifier")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    inputs: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional input parameters")


class DifyAPIResponse(BaseModel):
    """Dify API response model."""
    
    event: str = Field(..., description="Event type")
    message_id: str = Field(..., description="Message ID")
    conversation_id: str = Field(..., description="Conversation ID")
    answer: str = Field(..., description="AI response text")
    created_at: int = Field(..., description="Creation timestamp")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")