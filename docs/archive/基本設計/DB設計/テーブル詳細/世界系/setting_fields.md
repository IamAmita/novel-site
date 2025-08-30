# 設定フィールドテーブル（setting_fields）

---

## 概要
各設定（settings）の中で管理する項目（フィールド）を柔軟に保存するためのテーブル。例えば「アジア大陸」という設定の中に「文化」「宗教」「気候」などの項目を持たせたい場合に利用する。

---

## テーブル定義

| 属性名        | 型            | 必須 | 一意 | 説明                                 |
|---------------|---------------|------|------|--------------------------------------|
| id            | int           | ○    | ○    | フィールドID（主キー）               |
| setting_id    | int           | ○    |      | 設定ID（settings.idを参照）           |
| name          | varchar(100)  | ○    |      | 項目名（例：文化、宗教、気候など）   |
| description   | text          |      |      | 項目の説明                           |
| display_order | int           |      |      | 表示順                               |
| delete_flg    | tinyint(1)    | ○    |      | 論理削除フラグ（0:有効, 1:削除済み） |
| created_at    | datetime      | ○    |      | 作成日時                             |
| updated_at    | datetime      |      |      | 更新日時                             |
| deleted_at    | datetime      |      |      | 削除日時                             |

---

## インデックス

| インデックス名           | 種類 | 説明               | カラム                |
|------------------------|------|-------------------|----------------------|
| PRIMARY KEY            | 主キー | フィールドIDの主キー | id                   |
| INDEX                  | 通常 | 設定ID検索用       | setting_id           |
| INDEX                  | 通常 | 表示順検索用       | display_order        |
| UNIQUE                 | 複合一意 | 設定ごとの表示順一意 | setting_id, display_order |
| UNIQUE                 | 複合一意 | 設定ごとの項目名一意 | setting_id, name |

---

## 制約条件

### 主キー制約
- `id`: 自動採番（AUTO_INCREMENT）

### 外部キー制約
- `setting_id` → `settings.id`

### 一意制約
- `setting_id`, `display_order`の組み合わせは一意
- `setting_id`, `name`の組み合わせは一意

---

## 設計補足
- 各設定（settings）ごとに複数のフィールド（項目）を持たせることができる。
- 項目名（name）は自由に設定可能。
- 項目の説明（description）を柔軟に保存可能。
- 表示順（display_order）で画面表示の順序制御が可能。
- 項目の型や追加属性が必要な場合はカラム追加や拡張で対応。
- 論理削除はdelete_flgとdeleted_atで管理。

---

## 利用例
- アジア大陸（settings.id=123）
  - 文化（name=文化, description=アジア大陸の文化）
  - 宗教（name=宗教, description=アジア大陸の宗教）
  - 気候（name=気候, description=アジア大陸の気候） 