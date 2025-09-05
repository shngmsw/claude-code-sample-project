# Slack Bot & Web App サンプル

FastAPIとSlack Bot連携を含むPythonサンプルプロジェクトです。Claude Codeでの開発のベストプラクティスを紹介します。

## 🚀 クイックスタート

### 方法1: Dev Containerを使用（推奨）
1. VS Codeでプロジェクトを開く
2. プロンプトが表示されたら「Reopen in Container」をクリック
3. コンテナのビルドと依存関係のインストールを待つ
4. アプリケーションを実行:
   ```bash
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

### 方法2: ローカル開発
1. Python 3.11+がインストールされていることを確認
2. 仮想環境を作成:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. 依存関係をインストール:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   pip install -e .
   ```
4. アプリケーションを実行:
   ```bash
   python -m src.main
   ```

## 📖 アプリケーションURL

実行後、以下にアクセスできます:
- **Web Interface**: http://localhost:8000/ (シンプルなWebアプリ画面)
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🧪 テスト

テストスイートの実行:
```bash
# 全テストを実行
pytest

# カバレッジレポート付きで実行
pytest --cov=src --cov-report=html

# 特定のテストファイルを実行
pytest tests/test_items.py -v
```

## 🛠️ 開発ツール

### コードフォーマット
```bash
# Blackでコードフォーマット
black src tests

# importソート
isort src tests
```

### コード品質チェック
```bash
# flake8でLint
flake8 src tests

# mypyで型チェック
mypy src
```

## 📁 プロジェクト構造

```
claude-code-sample-project/
├── .devcontainer/          # VS Code dev container設定
│   └── devcontainer.json
├── src/                    # メインアプリケーションコード
│   ├── __init__.py
│   ├── main.py            # FastAPIアプリケーション（Web UI含む）
│   ├── models.py          # Pydanticデータモデル（Slackイベント含む）
│   ├── slack_bot.py       # Slack Bot実装
│   ├── utils.py           # ユーティリティ関数とデータベース
│   └── routes/            # APIルートハンドラー
│       ├── __init__.py
│       └── items.py
├── tests/                 # テストファイル
│   ├── __init__.py
│   ├── conftest.py        # テスト設定
│   ├── test_main.py       # メインアプリテスト
│   ├── test_items.py      # アイテムAPIテスト
│   └── test_utils.py      # ユーティリティ関数テスト
├── .env.example           # 環境変数テンプレート
├── CLAUDE.md              # Claude Code開発ガイド
├── README.md              # このファイル
├── pyproject.toml         # プロジェクト設定
├── requirements.txt       # 実行時依存関係
└── requirements-dev.txt   # 開発依存関係
```

## 🎯 機能

- **FastAPI フレームワーク**: モダンで高速なWebフレームワーク、自動API文書生成
- **Slack Bot 連携**: イベント処理、スラッシュコマンド、メッセージ応答
- **シンプルなWeb UI**: アイテム管理のためのインタラクティブWeb UI
- **Pydantic モデル**: データ検証とシリアライゼーション
- **非同期サポート**: async/await パターンをビルトイン
- **包括的テスト**: pytestとテストカバレッジによるユニットテスト
- **コード品質ツール**: Black、flake8、mypy、isort
- **Dev Container**: 一貫した開発環境
- **Claude Code最適化**: プロジェクトコンテキストを含むCLAUDE.md

## 📋 APIエンドポイント

### Web Interface
| メソッド | エンドポイント | 説明 |
|--------|----------|-------------|
| GET | `/` | シンプルなWebアプリケーション画面 |

### ヘルスチェック
| メソッド | エンドポイント | 説明 |
|--------|----------|-------------|
| GET | `/health` | アプリケーションヘルスチェック |

### アイテム管理
| メソッド | エンドポイント | 説明 |
|--------|----------|-------------|
| GET | `/items/` | 全アイテム取得（ページネーション対応） |
| POST | `/items/` | 新しいアイテムを作成 |
| GET | `/items/{id}` | IDでアイテムを取得 |
| PUT | `/items/{id}` | IDでアイテムを更新 |
| DELETE | `/items/{id}` | IDでアイテムを削除 |

### Slack Bot
| メソッド | エンドポイント | 説明 |
|--------|----------|-------------|
| POST | `/slack/events` | Slackイベントwebhookエンドポイント |

## 🔧 設定

アプリケーションは環境ベースの設定をサポートしています。`.env.example`を`.env`にコピー:

```env
# Slack Bot設定
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here

# アプリケーション設定
DEBUG=true
LOG_LEVEL=info

# 環境
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
   - コマンドを作成: `/sample`
   - Request URL: `https://your-domain.com/slack/events`

5. **アプリをインストール**
   - 「Install App」へ移動
   - ワークスペースにアプリをインストール
   - 「Bot User OAuth Token」を`.env`ファイルにコピー

6. **署名シークレットを取得**
   - 「Basic Information」へ移動
   - 「Signing Secret」を`.env`ファイルにコピー

### 🧪 Botコマンド

- 「hello」または「hi」と送信して開始
- 「status」でアプリケーション状態をチェック
- 「help」でコマンドリストを表示
- 「joke」でランダムなプログラミングジョークを表示
- `/sample [テキスト]` スラッシュコマンドを使用

## 🤝 コントリビューション

このプロジェクトはClaude Code開発ワークフローを実演するサンプルプロジェクトです:

1. リポジトリをクローン
2. VS Codeでdev containerを使用して開く
3. 確立されたパターンに従って変更を行う
4. テストを実行してすべてが動作することを確認
5. Claude Codeを使用して開発タスクを支援

## 📝 ライセンス

このプロジェクトはMITライセンスの下でライセンスされています - 詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 🆘 トラブルシューティング

### よくある問題

**インポートエラー**
- パッケージを編集可能モードでインストールしていることを確認: `pip install -e .`
- 正しい仮想環境にいることを確認

**ポートが使用中**
- ポートを変更: `uvicorn src.main:app --reload --port 8001`

**Dev Containerの問題**
- コンテナを再ビルド: Command Palette → "Dev Containers: Rebuild Container"
- DockerとVS Code dev container拡張機能がインストールされていることを確認

### ヘルプを求める

- 開発ガイドラインは`CLAUDE.md`ファイルをチェック
- FastAPIドキュメントを確認
- Claude Codeを使用して問題をデバッグしたり、コードベースを理解