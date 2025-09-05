"""Slack Bot with Dify API integration using Socket Mode."""

import logging
import os
from dotenv import load_dotenv
from src.slack_bot import SlackBot

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """Start the Slack Bot in Socket Mode."""
    logger.info("Starting Slack Bot with Dify API in Socket Mode...")
    
    # Initialize and start Slack Bot
    slack_bot = SlackBot()
    slack_bot.start()


if __name__ == "__main__":
    main()