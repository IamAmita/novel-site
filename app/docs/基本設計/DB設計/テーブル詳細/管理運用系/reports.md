# reports テーブル詳細（通報管理）

---

## 概要
ユーザーや作品などの不適切な行為・内容を通報するための管理テーブルです。通報対象テーブルID（target_table_id）はmaster_tables.id、クラスID（class_id）はmaster_classes.id、ステータス（status）はmaster_statuses.id、通報理由（reason_id）はmaster_reasons.idを参照します。

---

## テーブル定義

| 属性名           | 型      | 必須 | 一意 | 説明                                 |
|------------------|---------|------|------|--------------------------------------|
| id               | int     | ○    | ○    | 通報ID（主キー）                     |
| class_id         | int     | ○    |      | クラスID（master_classes.id, 2桁:10〜99）|
| target_table_id  | int     | ○    |      | 通報対象テーブルID（master_tables.idを参照）|
| target_id        | int     | ○    |      | 通報対象レコードID                   |
| reported_by      | int     | ○    |      | 通報ユーザーID                       |
| reason_id        | int     | ○    |      | 通報理由ID（master_reasons.idを参照）|
| description      | text    |      |      | 補足説明・詳細（任意）               |
| status           | int     | ○    |      | ステータスID（master_statuses.idを参照）|
| created_at       | datetime| ○    |      | 通報日時                             |
| updated_at       | datetime|      |      | 更新日時                             |

---

## インデックス

| インデックス名 | 種類   | 説明                   | カラム           |
|----------------|--------|------------------------|------------------|
| PRIMARY KEY    | 主キー | 主キー                 | id               |
| INDEX          | 通常   | クラスID検索用         | class_id         |
| INDEX          | 通常   | 対象テーブル検索用     | target_table_id  |
| INDEX          | 通常   | 対象ID検索用           | target_id        |
| INDEX          | 通常   | 通報ユーザー検索用     | reported_by      |
| INDEX          | 通常   | ステータス検索用       | status           |
| INDEX          | 通常   | 通報理由検索用         | reason_id        |
| INDEX          | 通常   | 通報日時検索用         | created_at       |

---

## 設計補足
- class_idはmaster_classes.idを参照する外部キーです（2桁:10〜99）。
- target_table_idはmaster_tables.idを参照する外部キーです（4桁:1000〜9999）。
- statusはmaster_statuses.idを参照する外部キーです。
- reason_idはmaster_reasons.idを参照する外部キーです。
- descriptionは通報理由の補足や詳細を記載する任意項目です。
- target_idは通報対象テーブルの主キーIDです。
- reported_byは通報を行ったユーザーIDです。
- created_at/updated_atで通報日時・更新日時を記録します。

---

## 運用例
| id | class_id | target_table_id | target_id | reported_by | reason_id | description      | status | created_at          | updated_at          |
|----|----------|-----------------|-----------|-------------|-----------|------------------|--------|---------------------|---------------------|
| 1  | 10       | 1001            | 1001      | 10          | 100       | 不適切な発言      | 1      | 2024-06-01 12:00:00 | 2024-06-01 12:10:00 |
| 2  | 20       | 2001            | 2002      | 11          | 101       |                  | 2      | 2024-06-02 13:00:00 | 2024-06-02 13:05:00 |
| 3  | 30       | 3001            | 1002      | 12          | 150       | その他詳細説明    | 1      | 2024-06-03 14:00:00 | 2024-06-03 14:10:00 |
|... | ...      | ...             | ...       | ...         | ...       | ...              | ...    | ...                 | ...                 |

---

## 関連テーブル
- master_classes: class_idで参照（クラス種別管理）
- master_tables: target_table_idで参照（通報対象テーブル管理）
- master_statuses: statusで参照（ステータス管理）
- master_reasons: reason_idで参照（通報理由管理）
- users: reported_byで参照（通報ユーザー管理）

---

## 備考
- 通報対象テーブルやクラス、ステータス、理由の拡張・管理もマスタテーブルで容易に行えます。

---

## 制約条件

### 主キー制約
- `id`: 自動採番（AUTO_INCREMENT）

### 外部キー制約
- `class_id` → `master_classes.id`: クラス種別マスタを参照
- `reported_by` → `users.id`: 通報者ユーザーテーブルを参照
- `target_table_id` → `master_tables.id`: 対象テーブル定義マスタを参照
- `reason_id` → `master_reasons.id`: 通報理由マスタを参照

### ユニーク制約
- `reported_by, class_id, target_table_id, target_id`: 同一ユーザーの同一対象への重複通報を防止

### チェック制約
- `class_id`: 10〜99のいずれかである必要があります
- `target_table_id`: 1000〜9999のいずれかである必要があります
- `status`: 0、1のいずれかである必要があります

---

## 通報の流れ例

| 通報ID | 通報者 | class_id | target_table_id | target_id | reason_id | description | ステータス | 説明 |
|--------|--------|----------|-----------------|-----------|-----------|-------------|------------|------|
| 1 | ユーザーA | 10 | 1001 | 5 | 100 | 宣伝コメント | pending | master_reasons参照 |
| 2 | ユーザーB | 10 | 1001 | 5 | 101 | 不適切な内容 | pending | master_reasons参照 |
| 3 | ユーザーC | 20 | 2001 | 10 | 150 | 著作権侵害   | approved | master_reasons参照 |

---

## 関連テーブル

- `users`: 多対1の関係（通報者）
- `comments`: 1対多の関係（通報対象）
- `novels`: 1対多の関係（通報対象）
- その他通報対象テーブル

---

## 運用上の注意点

1. **重複防止**: 同一ユーザーの重複通報を自動検出・防止
2. **バッチ処理**: 定期的に通報数を集計し、各テーブルの`reported_count`を更新
3. **論理削除**: is_archived=1で削除済み、0で有効。全テーブルで統一。
4. **手動確認**: 重要な通報は管理者による手動確認を実施
5. **履歴管理**: 通報の処理履歴を保持し、透明性を確保
6. **プライバシー**: 通報者の情報は適切に保護
7. **アーカイブ**: 処理完了後は通報レコードをアーカイブ状態に設定 