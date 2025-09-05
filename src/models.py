"""Data models for the sample application."""

from typing import Optional
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