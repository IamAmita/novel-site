# notification_statuses テーブル詳細（通知ステータス管理）

---

## 概要
通知ごとの状態（未読・既読・重要・緊急など）を柔軟に管理する中間テーブルです。1つの通知に複数の状態を持たせることができ、状態はmaster_statusesテーブルで一元管理します。

---

## テーブル定義

| 属性名           | 型      | 必須 | 一意 | 説明                                 |
|------------------|---------|------|------|--------------------------------------|
| id               | int     | ○    | ○    | 通知ステータスID（主キー）           |
| notification_id  | int     | ○    |      | 通知ID（notifications.idを参照）     |
| status_id        | int     | ○    |      | ステータスID（master_statuses.idを参照）|
| created_at       | datetime| ○    |      | 登録日時                             |

---

## インデックス

| インデックス名 | 種類   | 説明                   | カラム           |
|----------------|--------|------------------------|------------------|
| PRIMARY KEY    | 主キー | 主キー                 | id               |
| UNIQUE         | 複合   | 1通知1状態の重複防止   | notification_id, status_id |
| INDEX          | 通常   | 通知ID検索用           | notification_id  |
| INDEX          | 通常   | ステータスID検索用     | status_id        |

---

## 制約条件

### 主キー制約
- `id`: 自動採番（AUTO_INCREMENT）

### 外部キー制約
- `notification_id` → `notifications.id`: 通知テーブルを参照
- `status_id` → `master_statuses.id`: ステータスマスタを参照

### ユニーク制約
- `notification_id, status_id`: 1通知に同じ状態を重複登録不可

---

## 運用例
| id | notification_id | status_id | created_at          |
|----|-----------------|-----------|---------------------|
| 1  | 1001            | 1         | 2024-06-10 12:00:00 |
| 2  | 1001            | 3         | 2024-06-10 12:00:00 |
| 3  | 1002            | 1         | 2024-06-10 12:01:00 |
|... | ...             | ...       | ...                 |

---

## 設計補足
- 1つの通知（notification_id）に複数の状態（status_id）を持たせることで、「重要かつ未読」などの複合状態を柔軟に表現できます。
- ステータスの種類や意味はmaster_statusesテーブルで一元管理します。
- 通知の状態追加・削除・履歴管理も容易です。
- 通知の状態を判定する際は、notification_statusesを参照して該当するstatus_idが存在するかで判定します。

---

## 関連テーブル
- notifications: notification_idで参照（通知管理）
- master_statuses: status_idで参照（状態マスタ）

---

## 備考
- 通知の状態管理を柔軟かつ拡張性高く運用できます。
- 状態の追加や意味変更もmaster_statuses側で一元管理可能です。 