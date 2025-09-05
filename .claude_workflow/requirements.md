# 要件定義: Dify API連携Slack Bot

## 目的
- 既存のFastAPI web app + Slack Botプロジェクトから、web appとAPIの部分を削除
- Dify APIを叩けるSlack Botサンプルに変更

## 現状把握
- 現在はFastAPIベースのweb application + Slack Bot統合プロジェクト
- items管理のRESTful API endpoints
- 簡単なweb interface
- Slack Botの基本的な実装あり

## 変更要件
1. **削除対象**
   - web interface (`GET /` endpoint)
   - items管理API (`/items` related endpoints)
   - 不要なモデル・ルート・ユーティリティ

2. **追加・変更対象**
   - Dify API連携機能
   - Dify APIクライアント実装
   - Slack BotからDify APIへのリクエスト処理
   - 適切な環境変数設定

3. **保持対象**
   - Slack Bot基本機能（event handling, slash commands）
   - Health check endpoint
   - FastAPI基盤（Dify API responses用）
   - テスト・リンティング・フォーマット設定

## 成功基準
- web app部分が完全に削除されている
- Dify APIとの通信が正常に動作する
- Slack Botからのメッセージに対してDify APIのレスポンスを返せる
- 既存のテスト・開発ツールが正常に動作する
- 環境変数でDify API設定が管理できる

## 技術要件
- Python 3.11+
- FastAPI（Dify APIレスポンス用最小構成）
- Slack Bot SDK
- HTTP client（Dify API通信用）
- 環境変数管理