# reviews テーブル詳細

## 概要
ユーザーが投稿したレビューを管理するテーブルです。多様な対象（小説・設定等）にレビューでき、評価点とレビュー本文を含みます。

## テーブル定義

| 属性名         | 型         | 必須 | 一意 | 説明                                 |
|----------------|------------|------|------|--------------------------------------|
| id             | int        | ○    | ○    | レビューID（主キー）                 |
| user_id        | int        | ○    |      | 投稿者ID（外部キー）                 |
| target_type    | tinyint    | ○    |      | レビュー対象分類（master_classesテーブル参照）                     |
| target_id      | int        | ○    |      | レビュー対象ID                       |
| rating         | tinyint    | ○    |      | 評価点（1-5段階）                    |
| body           | text       |      |      | レビュー本文                         |
| is_deleted     | tinyint    | ○    |      | 通報による自動削除フラグ             |
| created_at     | datetime   | ○    |      | 投稿日時                             |
| updated_at     | datetime   |      |      | 更新日時                             |

## インデックス

| インデックス名 | 種類 | 説明 | カラム |
|----------------|------|------|--------|
| PRIMARY KEY | 主キー | レビューIDの主キー | id |
| UNIQUE | 複合一意 | 重複レビュー防止 | user_id, target_type, target_id |
| INDEX | 複合 | 対象別評価検索用 | target_type, target_id, rating |
| INDEX | 複合 | 対象別時系列検索用 | target_type, target_id, created_at |
| INDEX | 複合 | ユーザー別レビュー履歴用 | user_id, created_at |
| INDEX | 通常 | 削除状態検索用 | is_deleted |

## 制約条件

### 主キー制約
- `id`: 自動採番（AUTO_INCREMENT）

### 外部キー制約
- `user_id` → `users.id`: 投稿者ユーザーテーブルを参照
- `target_type` → `master_classes.id`: 分類定義テーブルを参照

### ユニーク制約
- `user_id, target_type, target_id`: 1ユーザーにつき1対象に1つのレビューのみ許可

### チェック制約
- `rating`: 1以上5以下の値のみ許可
- `target_type`: 1、2、3のいずれかである必要があります
- `is_deleted`: 0または1の値のみ許可

## 設計補足

### レビュー対象分類（target_type, target_id）
- master_classesテーブルで定義された分類ID
- 例：1（小説）、2（設定）、3（話）など

### 評価点（rating）
- `

## 運用上の注意点

1. **論理削除**: is_deleted=1で削除済み、0で有効。全テーブルで統一。
2. **重複レビュー防止**: 1ユーザーにつき1対象に1つのレビューのみ許可
3. **評価点制限**: 1-5段階の評価点のみ許可
4. **通報処理**: バッチ処理で通報数を集計し自動削除
5. **パフォーマンス**: 対象別のレビュー一覧表示が高速
6. **データ整合性**: 重複レビューの防止と評価点の範囲制限