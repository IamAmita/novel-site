# master_statuseses テーブル詳細

---

## 概要
システム全体のステータス定義を管理するマスタテーブルです。ユーザー、小説、コメント、通報など、様々な対象のステータス（状態）の定義を一元管理し、システム全体で一貫したステータス管理を可能にします。

---

## テーブル定義

| 属性名         | 型         | 必須 | 一意 | 説明                                 |
|----------------|------------|------|------|--------------------------------------|
| id             | tinyint    | ○    | ○    | ステータス定義ID（主キー）           |
| target_type    | tinyint    | ○    |      | 対象種別（master_classesテーブル参照） |
| name           | varchar    | ○    |      | ステータス名（システム内部用）       |
| description    | text       |      |      | ステータスの説明                     |
| created_at     | datetime   | ○    |      | 登録日時                             |
| updated_at     | datetime   |      |      | 更新日時                             |

---

## インデックス

| インデックス名 | 種類 | 説明 | カラム |
|----------------|------|------|--------|
| PRIMARY KEY | 主キー | ステータス定義IDの主キー | id |
| UNIQUE | 複合一意 | 対象種別・ステータス名の一意制約 | target_type, name |
| INDEX | 通常 | 対象種別検索用 | target_type |
| INDEX | 通常 | 登録日時検索用 | created_at |

---

## 制約条件

### 主キー制約
- `id`: 自動採番（AUTO_INCREMENT）

### 一意制約
- `name`: ステータス名は一意である必要があります

### 外部キー制約
- `target_type` → `master_classes.id`: 分類定義テーブルを参照

### チェック制約
- `name`: 空文字列は許可しない

---

## 設計補足

### 対象種別（target_type）
- master_classesテーブルで定義された対象種別のID
- 例：0（コメント）、1（小説）、2（設定）など
- どの対象のステータスかを識別

### ステータス名（name）
- システム内部で使用する識別子
- 対象種別内で一意である必要があります
- 例：ユーザー系「active」「warned」「suspended」「banned」
- 例：小説系「draft」「published」「private」「suspended」
- 例：通報系「pending」「processing」「completed」「rejected」

---

## データ例

| id | target_type | name | description |
|----|-------------|------|-------------|
| 0 | 1 | active | 通常のユーザー |
| 1 | 1 | warned | 警告を受けたユーザー |
| 2 | 1 | suspended | 一時的に停止されたユーザー |
| 3 | 1 | banned | 永久に停止されたユーザー |
| 4 | 2 | draft | 下書き状態の小説 |
| 5 | 2 | published | 公開中の小説 |
| 6 | 2 | private | 非公開の小説 |
| 7 | 2 | suspended | 停止された小説 |
| 8 | 3 | pending | 未処理の通報 |
| 9 | 3 | processing | 処理中の通報 |
| 10 | 3 | completed | 処理完了の通報 |
| 11 | 3 | rejected | 却下された通報 |

---

## 関連テーブル

- `master_classes`: 多対1の関係（分類定義）
- `user_statuses`: 1対多の関係（ユーザーステータス管理）
- `novel_statuses`: 1対多の関係（小説ステータス管理）
- `comment_statuses`: 1対多の関係（コメントステータス管理）
- `report_statuses`: 1対多の関係（通報ステータス管理）

---

## 運用上の注意点

1. **対象種別**: master_classesテーブルとの整合性を保つ
2. **ステータス名**: 対象種別内で一意である必要があります
3. **説明**: ステータスの意味を明確に記載
4. **拡張性**: 新しい対象種別やステータスの追加を考慮した設計
5. **一貫性**: システム全体で統一されたステータス管理 