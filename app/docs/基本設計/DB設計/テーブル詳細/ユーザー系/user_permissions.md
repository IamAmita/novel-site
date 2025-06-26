# user_permissions テーブル詳細

---

## 概要
ユーザーに付与された権限を管理するテーブルです。ユーザーID、権限ID、テーブルID、付与日時などを含みます。

---

## テーブル定義

| 属性名         | 型         | 必須 | 一意 | 説明                                 |
|----------------|------------|------|------|--------------------------------------|
| id             | int        | ○    | ○    | 権限管理ID（主キー）                 |
| user_id        | int        | ○    |      | ユーザーID（外部キー）               |
| permission_id  | int        | ○    |      | 権限定義ID（外部キー）               |
| table_id       | int        | ○    |      | テーブルID（master_tablesテーブル参照）|
| target_id      | int        | ○    |      | 権限対象ID（table_idで指定されたテーブルの主キー） |
| created_at     | datetime   | ○    |      | 権限付与日時                         |

---

## インデックス

| インデックス名 | 種類 | 説明 | カラム |
|----------------|------|------|--------|
| PRIMARY KEY | 主キー | 権限管理IDの主キー | id |
| UNIQUE | 複合一意 | ユーザー・権限・テーブル・対象の組み合わせ一意制約 | user_id, permission_id, table_id, target_id |
| INDEX | 通常 | ユーザーID検索用 | user_id |
| INDEX | 通常 | 権限ID検索用 | permission_id |
| INDEX | 通常 | テーブルID検索用 | table_id |
| INDEX | 通常 | 対象ID検索用 | target_id |
| INDEX | 通常 | 付与日時検索用 | created_at |

---

## 制約条件

### 主キー制約
- `id`: 自動採番（AUTO_INCREMENT）

### 一意制約
- `user_id, permission_id, table_id, target_id`: ユーザー・権限・テーブル・対象の組み合わせは一意である必要があります

### 外部キー制約
- `user_id` → `users.id`: ユーザーテーブルを参照
- `permission_id` → `master_permissions.id`: 権限定義テーブルを参照
- `table_id` → `master_tables.id`: テーブルマスタを参照

### チェック制約
- `user_id` ≠ `granted_by`: 自分に権限を付与することはできません

---

## 設計補足

### テーブルID（table_id）
- 権限対象となるテーブルを明示的に指定
- master_tablesテーブルで管理されているテーブルIDを参照
- target_idと組み合わせて、どのテーブルのどのレコードに対する権限かを明確に管理

### ユーザーID（user_id）
- 権限を付与されるユーザー
- 存在するユーザーである必要があります

### 権限ID（permission_id）
- 付与される権限の定義
- 存在する権限である必要があります

### 権限対象ID（target_id）
- table_idで指定されたテーブルの主キーID
- 例：table_idがnovelsの場合はnovelsテーブルのid
- 例：table_idがcommentsの場合はcommentsテーブルのid

### 権限付与者（granted_by）
- 履歴追跡のために記録
- 自分に権限を付与することはできません

---

## 関連テーブル

- `users`: 多対1の関係（権限を付与されるユーザー）
- `master_permissions`: 多対1の関係（付与される権限）
- `master_tables`: 多対1の関係（テーブルマスタ）
- `users`: 多対1の関係（権限付与者）

---

## 運用上の注意点

1. **権限付与**: 適切な権限を持つユーザーのみが付与可能
2. **権限取り消し**: 論理削除で履歴を保持
3. **権限継承**: 権限の階層構造の管理
4. **監査**: 権限変更の履歴管理

## 備考
- 権限の付与・削除などの操作履歴（付与者・削除者等）はuser_historiesテーブルで一元管理する。 