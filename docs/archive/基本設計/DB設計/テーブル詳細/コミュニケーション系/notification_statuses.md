# notification_statuses テーブル詳細（通知ステータス管理）

---

## 概要
通知のステータス（状態）を管理するテーブルです。通知の重要度（未読、既読、重要、緊急など）を履歴として保持し、通知の優先度管理やフィルタリング機能を提供します。

---

## テーブル定義

| 属性名           | 型      | 必須 | 一意 | 説明                                 |
|------------------|---------|------|------|--------------------------------------|
| id               | int     | ○    | ○    | ステータス履歴ID（主キー）           |
| notification_id  | int     | ○    |      | 通知ID（notifications.idを参照）     |
| status_id        | tinyint | ○    |      | ステータス定義ID（master_statuses.idを参照） |
| status_value     | tinyint | ○    |      | ステータス値（数値コード）           |
| created_at       | datetime| ○    |      | ステータス変更日時                   |
| updated_at       | datetime| ○    |      | 更新日時                             |
| deleted_at       | datetime|      |      | 削除日時                             |
| delete_flg       | tinyint | ○    |      | 削除フラグ（0：有効、1：削除済み、デフォルト：0） |

---

## インデックス

| インデックス名 | 種類   | 説明                   | カラム           |
|----------------|--------|------------------------|------------------|
| PRIMARY KEY    | 主キー | ステータス履歴IDの主キー | id               |
| UNIQUE         | 複合   | 1通知1ステータスの重複防止 | notification_id, status_id |
| INDEX          | 通常   | 通知検索用             | notification_id  |
| INDEX          | 複合   | 現在のステータス検索用 | notification_id, created_at |
| INDEX          | 通常   | ステータス検索用       | status_id        |
| INDEX          | 複合   | ユーザー別ステータス検索用 | notification_id, status_id |
| INDEX          | 通常   | 変更日時検索用         | created_at       |
| INDEX          | 通常   | 削除フラグ検索用       | delete_flg       |

---

## 制約条件

### 主キー制約
- `id`: 自動採番（AUTO_INCREMENT）

### 外部キー制約
- `notification_id` → `notifications.id`: 通知テーブルを参照
- `status_id` → `master_statuses.id`: ステータス定義テーブルを参照

### ユニーク制約
- `notification_id, status_id`: 1通知に同じステータスを重複登録不可

### チェック制約
- `status_id`: 通知用ステータス定義ID（301〜304）のみ許可
- `status_value`: 1〜255の範囲の数値のみ許可
- `delete_flg`: 0（有効）または1（削除済み）のみ許可、デフォルト値は0

---

## 設計補足

### ステータスID（status_id）
- master_statusesテーブルで定義された通知用ステータスのID
- 301〜304の範囲で管理
- 例：301（unread）、302（read）、303（important）、304（urgent）

### ステータス値（status_value）
- システム内部で使用する数値コード
- master_statusesのstatus_valueと同期を保つ
- アプリケーション側での判定に使用
- 1〜255の範囲で管理（tinyintの制限）

### 現在のステータス管理
- 各通知の最新のレコードが現在のステータス
- ステータス変更時は新しいレコードを作成
- 履歴として過去のステータスも保持

### 複合ステータス管理
- 1つの通知に対して複数のステータスを同時付与可能
- 例：「既読」かつ「重要」な通知
- 通知の優先度や分類を柔軟に管理

### 論理削除
- 論理削除により、参照整合性を保ちながらデータの履歴を保持
- 削除されたレコードは通常の検索から除外
- delete_flg = 0：有効なレコード
- delete_flg = 1：削除済みレコード

---

## ステータス例

### 通知ステータス
| status_id | status_value | ステータス名 | 説明 |
|-----------|-------------|-------------|------|
| 301 | 1 | unread | 未読 |
| 302 | 2 | read | 既読 |
| 303 | 3 | important | 重要 |
| 304 | 4 | urgent | 緊急 |

---

## 運用例
| id | notification_id | status_id | status_value | created_at          | delete_flg |
|----|----------------|-----------|-------------|---------------------|------------|
| 1  | 3001           | 301       | 1           | 2024-06-10 12:00:00 | 0          |
| 2  | 3001           | 303       | 3           | 2024-06-10 12:00:00 | 0          |
| 3  | 3001           | 302       | 2           | 2024-06-10 12:30:00 | 0          |
| 4  | 3002           | 301       | 1           | 2024-06-11 09:15:00 | 0          |
| 5  | 3002           | 304       | 4           | 2024-06-11 09:15:00 | 0          |
| 6  | 3003           | 301       | 1           | 2024-06-12 14:20:00 | 0          |
|... | ...            | ...       | ...         | ...                 | ...        |

---

## 関連テーブル

- `notifications`: notification_idで参照（通知管理）
- `master_statuses`: status_idで参照（ステータス定義）
- `users`: 通知受信ユーザー（notifications経由）

---

## 運用上の注意点

1. **ステータス変更**: 変更時は新しいレコードを作成
2. **複合ステータス**: 1通知に対して複数のステータスを同時付与可能
3. **履歴管理**: ステータス変更の履歴を保持し、透明性を確保
4. **パフォーマンス**: 現在のステータス取得は`notification_id, created_at`の複合インデックスを活用
5. **データ整合性**: 通知削除時は関連するステータスレコードも論理削除
6. **論理削除**: 削除されたレコードは通常の検索から除外し、履歴として保持
7. **重複防止**: 複合一意制約により、1通知に同じステータスの重複設定を防止
8. **自動判定**: 通知種別による自動ステータス付与
9. **フィルタリング**: ステータスによる通知一覧のフィルタリング

---

## ステータス変更フロー

### 自動付与（システム）
1. 通知作成時に自動的にステータスを付与
2. 通知種別に応じて重要度を判定
3. 新しいレコードを作成

### 手動変更（ユーザー）
1. ユーザーが通知のステータスを変更
2. 新しいレコードを作成
3. 通知一覧を更新

### 管理者設定
1. 管理者が通知の重要度を設定
2. 新しいレコードを作成
3. ユーザーに通知

---

## 通知フィルタリング例

### 未読通知
```sql
SELECT n.* FROM notifications n
JOIN notification_statuses ns ON n.id = ns.notification_id
WHERE ns.status_id = 301 AND ns.delete_flg = 0
AND ns.created_at = (
    SELECT MAX(created_at) FROM notification_statuses 
    WHERE notification_id = n.id AND status_id = 301 AND delete_flg = 0
);
```

### 重要通知
```sql
SELECT n.* FROM notifications n
JOIN notification_statuses ns ON n.id = ns.notification_id
WHERE ns.status_id = 303 AND ns.delete_flg = 0
AND ns.created_at = (
    SELECT MAX(created_at) FROM notification_statuses 
    WHERE notification_id = n.id AND status_id = 303 AND delete_flg = 0
);
```

### 緊急通知
```sql
SELECT n.* FROM notifications n
JOIN notification_statuses ns ON n.id = ns.notification_id
WHERE ns.status_id = 304 AND ns.delete_flg = 0
AND ns.created_at = (
    SELECT MAX(created_at) FROM notification_statuses 
    WHERE notification_id = n.id AND status_id = 304 AND delete_flg = 0
);
``` 