# タスク化: Dify API連携Slack Bot実装

## タスク一覧

### フェーズ1: 不要機能削除（優先度: 高）
- [ ] **Task 1.1**: `src/main.py`からweb interface削除
  - `GET /` endpoint全体削除
  - 不要なimport削除（StaticFiles, src.routes.items, initialize_sample_data）
  - `app.include_router(items.router)`削除
  - startupイベントから`initialize_sample_data()`削除

- [ ] **Task 1.2**: `src/routes/items.py`ファイル削除
  - items管理API全体削除

- [ ] **Task 1.3**: `src/models.py`からItem関連モデル削除
  - `ItemBase`, `ItemCreate`, `ItemUpdate`, `Item`クラス削除
  - `HealthCheck`, `ErrorResponse`, `SlackEvent`は保持

- [ ] **Task 1.4**: `src/utils.py`から不要機能削除
  - `initialize_sample_data`関数削除
  - 他の不要なユーティリティ削除

### フェーズ2: Dify API連携実装（優先度: 高）
- [ ] **Task 2.1**: Dify API用モデル追加
  - `src/models.py`に`DifyRequest`, `DifyResponse`モデル追加

- [ ] **Task 2.2**: Dify APIクライアント実装
  - `src/dify_client.py`新規作成
  - `DifyClient`クラス実装
  - HTTP通信、エラーハンドリング、タイムアウト処理

- [ ] **Task 2.3**: 環境変数設定更新
  - `.env.example`にDify API設定追加
  - 設定の妥当性検証機能

### フェーズ3: Slack Bot機能拡張（優先度: 高）
- [ ] **Task 3.1**: Slack Bot拡張実装
  - `src/slack_bot.py`でDifyClientとの統合
  - メッセージ処理でDify API呼び出し
  - 会話履歴管理（conversation_id）
  - エラーハンドリング強化

- [ ] **Task 3.2**: メッセージフロー実装
  - Slackメッセージ → Dify API → Slackレスポンス
  - 固定レスポンスからDify連携へ変更

### フェーズ4: テスト・品質保証（優先度: 中）
- [ ] **Task 4.1**: 単体テスト実装
  - `tests/test_dify_client.py`作成
  - `tests/test_slack_bot.py`更新
  - モデルバリデーションテスト

- [ ] **Task 4.2**: 統合テスト実装
  - Slack webhook → Dify API → Responseの統合テスト
  - エラーケースのテスト

- [ ] **Task 4.3**: 品質チェック実行
  - `pytest`実行・カバレッジ確認
  - `flake8`, `black`, `mypy`実行
  - エラー修正

### フェーズ5: ドキュメント更新（優先度: 低）
- [ ] **Task 5.1**: README.md更新
  - web app部分の説明削除
  - Dify API連携の説明追加
  - セットアップ手順更新

- [ ] **Task 5.2**: CLAUDE.md更新
  - プロジェクト概要の変更
  - 開発コマンドの見直し

## 実行順序
1. **Phase 1** → 不要機能を完全に削除して動作確認
2. **Phase 2** → Dify API基盤を構築
3. **Phase 3** → Slack BotとDify APIを統合
4. **Phase 4** → テスト実装と品質保証
5. **Phase 5** → ドキュメント整備

## 完了基準
- [ ] web app関連のコードが完全に削除されている
- [ ] Dify APIとの通信が正常に動作する
- [ ] Slack BotからDify API経由でレスポンスが返る
- [ ] 全てのテストが通る（>90% coverage）
- [ ] リンティング・型チェックがクリアする
- [ ] 環境変数で適切にDify API設定が管理できる

## 注意事項
- エラーを解決してから次のタスクに進む
- 各タスク完了後に動作確認を行う
- 段階的に進める（一度に全てを変更しない）