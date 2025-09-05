# Claude Code Sample Project

This is a sample Python project optimized for development with Claude Code.

## Project Overview

A FastAPI-based web application with Slack Bot integration that demonstrates:
- RESTful API endpoints
- Slack Bot with event handling and slash commands
- Simple web interface for item management
- Data validation with Pydantic
- Async/await patterns
- Unit testing with pytest
- Linting and formatting
- Environment-based configuration

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
- pytest for testing
- httpx for HTTP client (Slack API)
- python-dotenv for environment variables

### Installation Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Install development dependencies  
pip install -r requirements-dev.txt

# Install project in editable mode
pip install -e .
```

### Development Commands
```bash
# Run the application
python -m src.main

# Run with hot reload (development)
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Lint code
flake8 src tests

# Format code
black src tests

# Type checking
mypy src
```

### Project Structure
```
├── src/                    # Main application code
│   ├── __init__.py
│   ├── main.py            # FastAPI app entry point with web interface
│   ├── models.py          # Pydantic models including Slack events
│   ├── slack_bot.py       # Slack Bot implementation
│   ├── routes/            # API route handlers
│   └── utils.py           # Utility functions
├── tests/                 # Test files
├── .devcontainer/         # VS Code dev container config
├── .env.example          # Environment variables template
├── requirements.txt       # Runtime dependencies
├── requirements-dev.txt   # Development dependencies
├── pyproject.toml         # Project configuration
├── CLAUDE.md             # This file - Claude Code instructions
└── README.md             # Project documentation
```

## API Endpoints

### Web Interface
- `GET /` - Simple web application interface

### Health Check
- `GET /health` - Health check endpoint

### Items Management
- `GET /items` - Get all items
- `POST /items` - Create new item
- `GET /items/{item_id}` - Get specific item
- `PUT /items/{item_id}` - Update item
- `DELETE /items/{item_id}` - Delete item

### Slack Bot
- `POST /slack/events` - Slack events webhook endpoint

## Development Guidelines

### Code Style
- Follow PEP 8 style guide
- Use type hints for all functions
- Write docstrings for public functions
- Keep functions focused and small

### Testing
- Write unit tests for all new features
- Aim for >90% test coverage
- Use descriptive test names
- Test both happy path and edge cases

### Git Workflow
- Create feature branches from main
- Write clear commit messages
- Ensure tests pass before pushing
- Use pull requests for code review

## Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):
```
# Slack Bot Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here

# Application Configuration
DEBUG=true
LOG_LEVEL=info

# Environment
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
   - Command: `/sample`
   - Request URL: `https://your-domain.com/slack/events`
6. Install the app to your workspace and copy the Bot User OAuth Token

## Troubleshooting

### Common Issues
- **Import errors**: Ensure you're in the project root and have installed with `pip install -e .`
- **Port conflicts**: Change the port in uvicorn command if 8000 is in use
- **Permission errors**: Check file permissions and ensure you have write access

### Getting Help
- Check the FastAPI documentation: https://fastapi.tiangolo.com/
- Review pytest docs: https://docs.pytest.org/
- Ask Claude Code for help with specific issues