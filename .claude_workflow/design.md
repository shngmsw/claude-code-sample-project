# 設計: Dify API連携Slack Bot

## アーキテクチャ設計

### 全体構成
- **FastAPI**: 最小構成でSlack webhookとhealth checkのみ
- **Slack Bot**: イベント処理とDify API連携を担当
- **Dify API Client**: HTTP通信でDify APIとやり取り
- **環境設定**: .envファイルでDify API設定を管理

### システム構成図
```
Slack → FastAPI(/slack/events) → Slack Bot → Dify API Client → Dify API
                     ↓                              ↓
                Health Check              Response処理
```

## 実装アプローチ

### 1. 削除対象の詳細分析
**ファイル**: `src/main.py`
- `GET /` endpoint（web interface）全体削除
- `app.include_router(items.router)` 削除
- 不要なimport削除: `StaticFiles`, `src.routes.items`, `initialize_sample_data`

**ファイル**: `src/routes/items.py`
- ファイル全体削除（items管理API）

**ファイル**: `src/models.py`
- Item関連モデル削除: `ItemBase`, `ItemCreate`, `ItemUpdate`, `Item`
- 保持: `HealthCheck`, `ErrorResponse`, `SlackEvent`

**ファイル**: `src/utils.py`
- `initialize_sample_data` 関連機能削除

### 2. Dify API連携機能追加

**新規モデル**: `src/models.py`
```python
class DifyRequest(BaseModel):
    """Dify API リクエストモデル"""
    query: str
    conversation_id: Optional[str] = None
    user: str

class DifyResponse(BaseModel):  
    """Dify API レスポンスモデル"""
    answer: str
    conversation_id: str
```

**新規クライアント**: `src/dify_client.py`
```python
class DifyClient:
    def __init__(self, api_key: str, base_url: str)
    async def send_query(self, query: str, user: str, conversation_id: str = None) -> DifyResponse
```

### 3. Slack Bot機能拡張

**修正**: `src/slack_bot.py`
- Dify APIクライアント統合
- メッセージ処理でDify APIを呼び出し
- 会話履歴管理（conversation_id）
- エラーハンドリング強化

### 4. 環境変数設定

**追加**: `.env`
```
# Dify API Configuration
DIFY_API_KEY=your-dify-api-key
DIFY_BASE_URL=https://api.dify.ai/v1
DIFY_TIMEOUT=30

# Slack Bot Configuration (既存)
SLACK_BOT_TOKEN=xoxb-your-bot-token-here  
SLACK_SIGNING_SECRET=your-signing-secret-here
```

## データフロー設計

### メッセージ処理フロー
1. Slack → `/slack/events` endpoint
2. Slack Bot → request verification  
3. Message event → Dify Client
4. Dify API → query processing
5. Response → Slack channel

### エラーハンドリング
- Dify API接続エラー → フォールバック応答
- Rate limit → 適切なエラーメッセージ  
- タイムアウト → 再試行機能

## セキュリティ考慮事項

### API Key管理
- 環境変数での管理
- ローテーション対応
- ログ出力時のマスキング

### Slack認証
- Request signature verification保持
- タイムスタンプ検証

## テスト戦略

### 単体テスト対象
- DifyClient（API通信テスト）
- Slack Bot（メッセージ処理テスト）
- モデル（バリデーション）

### 統合テスト
- Slack webhook → Dify API → Response
- エラーケースの確認

## 移行手順
1. 不要機能削除（web app、items API）
2. Dify API client実装
3. Slack Bot拡張
4. 環境設定更新
5. テスト実装・実行