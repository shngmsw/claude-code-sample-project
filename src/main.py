"""Main FastAPI application with Slack Bot integration."""

import logging
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.models import HealthCheck, SlackEvent
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
    title="Dify API Slack Bot",
    description="A Slack Bot that integrates with Dify API",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize Slack Bot
slack_bot = SlackBot()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize the application on startup."""
    logger.info("Starting Dify API Slack Bot...")
    logger.info("Application startup complete")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Clean up on application shutdown."""
    logger.info("Shutting down Dify API Slack Bot...")



@app.get("/health", response_model=HealthCheck, tags=["health"])
async def health_check() -> HealthCheck:
    """Health check endpoint."""
    return HealthCheck(
        status="healthy",
        version=__version__,
        message="Dify API Slack Bot is running"
    )


# Slack webhook endpoint
@app.post("/slack/events", tags=["slack"])
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