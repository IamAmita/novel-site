# operation_histories テーブル詳細（統合履歴テーブル）

---

## 概要
全テーブルの操作履歴を一元管理するテーブルです。対象テーブルはtable_id（master_tables.table_id）で管理します。

---

## テーブル定義

| 属性名        | 型      | 必須 | 一意 | 説明                                 |
|---------------|---------|------|------|--------------------------------------|
| id            | int     | ○    | ○    | 主キー（AUTO_INCREMENT）             |
| table_id      | int     | ○    |      | 対象テーブルID（master_tables.table_id）|
| target_id     | int     | ○    |      | 対象レコードID                       |
| operation_id  | int     | ○    |      | 操作種別ID（master_operations.id）   |
| before_value  | text    |      |      | 変更前の値                           |
| after_value   | text    |      |      | 変更後の値                           |
| description   | text    |      |      | 操作内容・理由                       |
| operated_by   | int     |      |      | 操作ユーザーID（users.id）           |
| operated_at   | datetime| ○    |      | 操作日時                             |

---

## インデックス

| インデックス名 | 種類   | カラム        | 説明           |
|----------------|--------|--------------|----------------|
| PRIMARY KEY    | 主キー | id           | 主キー         |
| INDEX          | 通常   | table_id     | テーブルID検索 |
| INDEX          | 通常   | target_id    | レコード検索   |
| INDEX          | 通常   | operation_id | 操作種別検索   |
| INDEX          | 通常   | operated_by  | ユーザー検索   |
| INDEX          | 通常   | operated_at  | 日時検索       |

---

## 設計補足
- table_idで対象テーブルを、operation_idで操作種別を一元管理します。
- target_idは対象テーブルの主キーIDです。
- before_value/after_valueで変更内容、descriptionで操作内容や理由を記録します。
- operated_by/operated_atで「誰が・いつ」操作したかを記録します。
- データ量増加に備え、インデックスやアーカイブ運用を推奨します。

---

## 運用例
| id | table_id | target_id | operation_id | before_value | after_value | description | operated_by | operated_at |
|----|----------|-----------|--------------|--------------|-------------|-------------|-------------|-------------|
| 1  | 0        | 1001      | 1            | ...          | ...         | ...         | 10          | 2024-06-01  |
| 2  | 1        | 2002      | 2            | ...          | ...         | ...         | 11          | 2024-06-02  |
|... | ...      | ...       | ...          | ...          | ...         | ...         | ...         | ...         |

---

## 関連テーブル
- master_tables: table_idで参照（対象テーブル管理）
- master_operations: operation_idで参照（操作種別管理）
- users: operated_byで参照（操作ユーザー管理）

---

## 備考
- 全テーブルの履歴を一元管理します。新しいテーブル追加時もtable_idを登録するだけで履歴管理が可能です。
- データ量増加に備え、アーカイブやパーティショニング運用を推奨します。 