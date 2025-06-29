# 設定履歴テーブル（setting_histories）

---

## 概要
設定の変更履歴を管理するテーブル。設定の作成、編集、削除、公開状態変更などの全ての操作を記録し、変更の追跡と復元を可能にする。

---

## テーブル定義

| 属性名 | 型 | 必須 | 一意 | 説明 |
|--------|----|------|------|------|
| id | int | ○ | ○ | 履歴ID（主キー） |
| setting_id | int | ○ | | 設定ID（settings.id） |
| action | varchar(50) | ○ | | アクション（create, update, delete, publish, unpublish, restore等） |
| user_id | int | ○ | | 実行ユーザーID（users.id） |
| target_version | int | ○ | | 対象バージョン番号 |
| changes | json | | | 変更内容の詳細（変更前後の値） |
| summary | text | | | 変更内容の要約 |
| reason | text | | | 変更理由 |
| ip_address | varchar(45) | | | 実行者のIPアドレス |
| user_agent | text | | | 実行者のユーザーエージェント |
| created_at | datetime | ○ | | 実行日時 |

---

## インデックス

| インデックス名 | 種類 | 説明 | カラム |
|----------------|------|------|--------|
| PRIMARY KEY | 主キー | 履歴IDの主キー | id |
| INDEX | 通常 | 設定検索用 | setting_id |
| INDEX | 通常 | ユーザー検索用 | user_id |
| INDEX | 通常 | アクション検索用 | action |
| INDEX | 通常 | 実行日時検索用 | created_at |
| INDEX | 複合 | 設定・バージョン検索用 | setting_id, target_version |
| INDEX | 複合 | 設定・アクション検索用 | setting_id, action |
| INDEX | 複合 | ユーザー・アクション検索用 | user_id, action |

---

## 制約条件

### 主キー制約
- `id`: 自動採番（AUTO_INCREMENT）

### 外部キー制約
- `setting_id` → `settings.id`
- `user_id` → `users.id`

### チェック制約
- `action` IN ('create', 'update', 'delete', 'publish', 'unpublish', 'restore', 'archive', 'move', 'permission_change')

---

## 設計補足

### 完全性
- 全ての設定変更を記録
- 変更の追跡と復元が可能

### 詳細性
- `changes`フィールドで変更前後の値を保持
- JSON形式により柔軟なデータ構造

### 追跡性
- 誰がいつ何を変更したかを追跡可能
- IPアドレス・ユーザーエージェントも記録

### 復元性
- 過去の状態への復元が可能
- バージョン管理機能をサポート

---

## 関連テーブル

- `settings`: 多対1の関係（設定）
- `users`: 多対1の関係（実行ユーザー）

---

## 運用上の注意点

1. **完全性**: 全ての設定変更を記録
2. **詳細性**: `changes`フィールドで変更前後の値を保持
3. **追跡性**: 誰がいつ何を変更したかを追跡可能
4. **復元性**: 過去の状態への復元が可能
5. **パフォーマンス**: 大量の履歴データに対する適切なインデックス設定
6. **セキュリティ**: 機密情報の履歴管理に注意

---

## アクション詳細

### create（作成）
- 新規設定の作成
- `changes`には初期データを記録

### update（更新）
- 設定内容の編集
- `changes`には変更前後の値を記録

### delete（削除）
- 設定の論理削除
- `changes`には削除前のデータを記録

### publish（公開）
- 非公開設定の公開
- `changes`には公開状態の変更を記録

### unpublish（非公開）
- 公開設定の非公開化
- `changes`には非公開状態の変更を記録

### restore（復元）
- 削除された設定の復元
- `changes`には復元データを記録

### archive（アーカイブ）
- 設定のアーカイブ
- `changes`にはアーカイブ状態の変更を記録

### move（移動）
- 設定の階層移動
- `changes`には移動前後の階層情報を記録

### permission_change（権限変更）
- 設定の権限変更
- `changes`には変更前後の権限情報を記録

---

## 注意事項

1. **完全性**: 全ての設定変更を記録
2. **詳細性**: `changes`フィールドで変更前後の値を保持
3. **追跡性**: 誰がいつ何を変更したかを追跡可能
4. **復元性**: 過去の状態への復元が可能
5. **パフォーマンス**: 大量の履歴データに対する適切なインデックス設定
6. **セキュリティ**: 機密情報の履歴管理に注意 