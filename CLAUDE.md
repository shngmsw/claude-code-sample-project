# Slack Bot with Dify API Integration

Slack Bot that integrates with Dify API for AI-powered conversations.

## Project Overview

A minimal FastAPI application with Slack Bot that connects to Dify API:
- Slack Bot with direct messages and mentions support
- Dify API integration for AI responses
- Slash command support (/dify)
- Conversation context management
- FastAPI health check endpoint

## タスク実行の4段階フロー

### 1. 要件定義
- `.claude_workflow/complete.md`が存在すれば参照
- 目的の明確化、現状把握、成功基準の設定
- `.claude_workflow/requirements.md`に文書化
- **必須確認**: 「要件定義フェーズが完了しました。設計フェーズに進んでよろしいですか？」

### 2. 設計
- **必ず`.claude_workflow/requirements.md`を読み込んでから開始**
- アプローチ検討、実施手順決定、問題点の特定
- `.claude_workflow/design.md`に文書化
- **必須確認**: 「設計フェーズが完了しました。タスク化フェーズに進んでよろしいですか？」

### 3. タスク化
- **必ず`.claude_workflow/design.md`を読み込んでから開始**
- タスクを実行可能な単位に分解、優先順位設定
- `.claude_workflow/tasks.md`に文書化
- **必須確認**: 「タスク化フェーズが完了しました。実行フェーズに進んでよろしいですか？」

### 4. 実行
- **必ず`.claude_workflow/tasks.md`を読み込んでから開始**
- タスクを順次実行、進捗を`.claude_workflow/tasks.md`に更新
- 各タスク完了時に報告

## 実行ルール
### ファイル操作
- 新規タスク開始時: 既存ファイルの**内容を全て削除して白紙から書き直す**
- ファイル編集前に必ず現在の内容を確認

### フェーズ管理
- 各段階開始時: 「前段階のmdファイルを読み込みました」と報告
- 各段階の最後に、期待通りの結果になっているか確認
- 要件定義なしにいきなり実装を始めない

### 実行方針
- 段階的に進める: 一度に全てを変更せず、小さな変更を積み重ねる
- 複数のタスクを同時並行で進めない
- エラーは解決してから次へ進む
- エラーを無視して次のステップに進まない
- 指示にない機能を勝手に追加しない

## Development Setup

### Environment
- Python 3.11+
- FastAPI for web framework
- Pydantic for data validation
- httpx for HTTP client (Slack API and Dify API)
- python-dotenv for environment variables

### Installation Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Install project in editable mode
pip install -e .
```

### Development Commands
```bash
# Run the application
python -m src.main

# Run with hot reload (development)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Project Structure
```
├── src/                    # Main application code
│   ├── __init__.py
│   ├── main.py            # FastAPI app entry point
│   ├── models.py          # Pydantic models for Slack events and Dify API
│   ├── slack_bot.py       # Slack Bot with Dify API integration
│   └── utils.py           # Utility functions
├── .env.example          # Environment variables template
├── requirements.txt       # Runtime dependencies
├── pyproject.toml         # Project configuration
└── CLAUDE.md             # Claude Code instructions
```

## API Endpoints

### Health Check
- `GET /health` - Health check endpoint

### Slack Bot
- `POST /slack/events` - Slack events webhook endpoint

## Slack Bot Features

### Direct Messages
- Bot responds to direct messages via Dify API
- Maintains conversation context per user

### Channel Mentions
- Bot responds when mentioned in channels
- Processes message through Dify API

### Slash Commands
- `/dify [質問内容]` - Query Dify API directly

## Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):
```
# Slack Bot Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here
SLACK_BOT_USER_ID=your-bot-user-id-here

# Dify API Configuration
DIFY_API_KEY=your-dify-api-key-here
DIFY_BASE_URL=https://api.dify.ai/v1

# Application Configuration
LOG_LEVEL=info
ENVIRONMENT=development
```

### Slack Bot Setup

1. Create a new Slack app at https://api.slack.com/apps
2. Enable the following bot token scopes:
   - `chat:write` - Send messages
   - `app_mentions:read` - Read mentions
   - `im:read` - Read direct messages
   - `im:write` - Send direct messages
3. Enable Event Subscriptions and add your webhook URL: `https://your-domain.com/slack/events`
4. Subscribe to bot events:
   - `app_mention` - When the bot is mentioned
   - `message.im` - Direct messages to the bot
5. Create slash commands:
   - Command: `/dify`
   - Request URL: `https://your-domain.com/slack/events`
6. Install the app to your workspace and copy the Bot User OAuth Token

### Dify API Setup

1. Sign up for a Dify account
2. Create a new application
3. Get your API key from the API settings
4. Copy the API endpoint URL