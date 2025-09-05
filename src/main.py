"""Slack Bot with Dify API integration."""

import logging
import os
from fastapi import FastAPI, Request
from src.models import HealthCheck
from src.slack_bot import SlackBot
from src import __version__

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Slack Bot with Dify API",
    description="Slack Bot that integrates with Dify API for AI-powered conversations",
    version=__version__,
    docs_url=None,
    redoc_url=None
)

# Initialize Slack Bot
slack_bot = SlackBot()


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize the application on startup."""
    logger.info("Starting Slack Bot with Dify API...")
    logger.info("Application startup complete")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Clean up on application shutdown."""
    logger.info("Shutting down Slack Bot...")
    await slack_bot.cleanup()


@app.get("/health", response_model=HealthCheck)
async def health_check() -> HealthCheck:
    """Health check endpoint."""
    return HealthCheck(
        status="healthy",
        version=__version__,
        message="Slack Bot with Dify API is running"
    )


@app.post("/slack/events")
async def slack_events(request: Request):
    """Handle Slack events and slash commands."""
    body = await request.body()
    headers = dict(request.headers)
    return await slack_bot.handle_event(body, headers)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )