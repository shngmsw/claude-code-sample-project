# Slack Bot with Dify API Integration

Slack BotとDify APIを連携したAI対話システムです。

## 🚀 クイックスタート

1. Python 3.11+がインストールされていることを確認
2. 仮想環境を作成:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. 依存関係をインストール:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```
4. 環境変数を設定:
   ```bash
   cp .env.example .env
   # .envファイルを編集してSlack BotとDify APIの設定を入力
   ```
5. アプリケーションを実行:
   ```bash
   python -m src.main
   ```

## 📖 アプリケーションURL

実行後、以下にアクセスできます:
- **Health Check**: http://localhost:8000/health

## 📁 プロジェクト構造

```
├── src/                    # メインアプリケーションコード
│   ├── __init__.py
│   ├── main.py            # FastAPIアプリケーションエントリポイント
│   ├── models.py          # Pydanticモデル（Slack、Dify API用）
│   ├── slack_bot.py       # Slack Bot with Dify API連携
│   └── utils.py           # ユーティリティ関数
├── .env.example           # 環境変数テンプレート
├── CLAUDE.md              # Claude Code開発ガイド
├── README.md              # このファイル
├── pyproject.toml         # プロジェクト設定
└── requirements.txt       # 依存関係
```

## 🎯 機能

- **Slack Bot**: ダイレクトメッセージ、メンション、スラッシュコマンド対応
- **Dify API連携**: AI応答による自然な対話
- **会話コンテキスト管理**: ユーザー別の会話履歴を保持
- **FastAPI**: 軽量なWebフレームワーク
- **非同期処理**: async/awaitによる効率的な処理

## 📋 APIエンドポイント

| メソッド | エンドポイント | 説明 |
|--------|----------|-------------|
| GET | `/health` | アプリケーションヘルスチェック |
| POST | `/slack/events` | Slackイベントwebhookエンドポイント |

## 🔧 設定

`.env.example`を`.env`にコピーして設定:

```env
# Slack Bot設定
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here
SLACK_BOT_USER_ID=your-bot-user-id-here

# Dify API設定
DIFY_API_KEY=your-dify-api-key-here
DIFY_BASE_URL=https://api.dify.ai/v1

# アプリケーション設定
LOG_LEVEL=info
ENVIRONMENT=development
```

### 🤖 Slack Bot セットアップ

1. **Slackアプリを作成**
   - https://api.slack.com/apps にアクセス
   - 「From scratch」で新しいアプリを作成
   - ワークスペースを選択

2. **Botトークンスコープの設定**
   - 「OAuth & Permissions」へ移動
   - Bot Token Scopesを追加:
     - `chat:write` - メッセージ送信
     - `app_mentions:read` - メンション読み取り
     - `im:read` - DM読み取り
     - `im:write` - DM送信

3. **イベント購読を有効化**
   - 「Event Subscriptions」へ移動
   - Eventsを有効化しRequest URLを設定: `https://your-domain.com/slack/events`
   - Bot Eventsを購読:
     - `app_mention` - Botがメンションされた時
     - `message.im` - Botへの直接メッセージ

4. **スラッシュコマンドを作成**
   - 「Slash Commands」へ移動
   - コマンドを作成: `/dify`
   - Request URL: `https://your-domain.com/slack/events`

5. **アプリをインストール**
   - 「Install App」へ移動
   - ワークスペースにアプリをインストール
   - 「Bot User OAuth Token」を`.env`ファイルにコピー

6. **署名シークレットを取得**
   - 「Basic Information」へ移動
   - 「Signing Secret」を`.env`ファイルにコピー

### 🚀 Dify API セットアップ

1. **Difyアカウントを作成**
   - https://dify.ai でアカウント作成
   
2. **アプリケーションを作成**
   - 新しいアプリケーションを作成
   - チャットボット形式を選択
   
3. **API設定を取得**
   - アプリ設定でAPI Keyを取得
   - Base URLを確認（通常は https://api.dify.ai/v1）

### 🤖 使用方法

- **ダイレクトメッセージ**: BotにDMを送信するとDify API経由で応答
- **チャンネルメンション**: `@botname 質問内容` でチャンネル内でも利用可能
- **スラッシュコマンド**: `/dify [質問内容]` でDify APIに直接クエリ

## 🆘 トラブルシューティング

### よくある問題

**Slack Bot応答しない**
- Slack App設定でwebhook URLが正しく設定されているか確認
- SLACK_BOT_TOKENとSLACK_SIGNING_SECRETが正しく設定されているか確認

**Dify API接続エラー**
- DIFY_API_KEYとDIFY_BASE_URLが正しく設定されているか確認
- Difyアプリケーションが有効になっているか確認

**ポートが使用中**
- ポートを変更: `uvicorn src.main:app --reload --port 8001`