# notifications テーブル詳細

---

## 概要
ユーザーへの通知を管理するテーブルです。通知内容や対象情報を持ち、**既読・未読（is_read）と削除フラグ（is_deleted）は本テーブルで管理**します。通知の重要・緊急など複合的な状態はnotification_statusesテーブル（master_statuses参照）で管理します。

---

## テーブル定義

| 属性名             | 型         | 必須 | 一意 | 説明                                 |
|--------------------|------------|------|------|--------------------------------------|
| id                 | int        | ○    | ○    | 通知ID（主キー）                     |
| user_id            | int        | ○    |      | 通知対象ユーザーID                   |
| class_id           | int        | ○    |      | 通知対象クラスID（master_classes.id, 2桁:10〜99） |
| target_table_id    | int        | ○    |      | 通知対象テーブルID（master_tables.id, 4桁:1000〜9999） |
| target_id          | int        |      |      | 通知対象のID                         |
| related_user_id    | int        |      |      | 関連ユーザーID（コメントした人など） |
| is_read            | tinyint    | ○    |      | 既読/未読フラグ（0:未読, 1:既読）    |
| is_deleted         | tinyint    | ○    |      | 削除フラグ（0:有効, 1:削除）         |
| created_at         | datetime   | ○    |      | 通知日時                             |

---

## インデックス

| インデックス名 | 種類 | 説明 | カラム |
|----------------|------|------|--------|
| PRIMARY KEY | 主キー | 通知IDの主キー | id |
| INDEX | 通常 | 通知対象ユーザー検索用 | user_id |
| INDEX | 通常 | 既読状態検索用 | is_read |
| INDEX | 通常 | 削除状態検索用 | is_deleted |
| INDEX | 通常 | 通知日時検索用 | created_at |
| INDEX | 複合 | 通知対象検索用 | class_id, target_table_id, target_id |

---

## 制約条件

### 主キー制約
- `id`: 自動採番（AUTO_INCREMENT）

### 外部キー制約
- `user_id` → `users.id`: 通知受信ユーザーテーブルを参照
- `class_id` → `master_classes.id`: クラス種別マスタを参照
- `target_table_id` → `master_tables.id`: テーブル種別マスタを参照
- `related_user_id` → `users.id`: 関連ユーザーテーブルを参照

### チェック制約
- `is_read`: 0または1の値のみ許可（0:未読, 1:既読）
- `is_deleted`: 0または1の値のみ許可（0:有効, 1:削除）
- `class_id`: 10〜99のいずれかである必要があります
- `target_table_id`: 1000〜9999のいずれかである必要があります

---

## 設計補足
- 既読・未読（is_read）と削除フラグ（is_deleted）は本テーブルで管理します。
- 重要・緊急など複合的な状態はnotification_statusesテーブル（master_statuses参照）で柔軟に管理します。
- master_statusesテーブルで状態種別を一元管理できます。
- 通知本体には状態情報（is_read, is_deleted）のみ持たせ、複合状態は中間テーブルで拡張可能です。

---

## 関連テーブル
- notification_statuses: 通知状態管理（notification_id, status_id）
- master_statuses: 状態種別マスタ
- users: 通知受信ユーザー
- master_classes: クラス種別
- master_tables: テーブル種別
- templates: 通知種別からテンプレートを特定

---

## 運用上の注意点

1. **既読・未読・削除管理**: is_read, is_deletedフラグで管理（0:未読/有効, 1:既読/削除）
2. **重要・緊急など複合状態管理**: notification_statusesテーブルで柔軟に付与
3. **履歴管理**: 状態の追加・削除・履歴もnotification_statusesで管理
4. **パフォーマンス**: 通知一覧表示の最適化