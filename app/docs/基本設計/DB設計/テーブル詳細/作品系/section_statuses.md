# 章ステータステーブル（section_statuses）

---

## 概要
章（sections）の公開状態や管理状態を表すステータス履歴テーブル。各章の状態履歴や現在の状態を管理し、システム全体で一貫したステータス管理を実現する。

---

## テーブル定義

| 属性名        | 型            | 必須 | 一意 | 説明                           |
|---------------|---------------|------|------|--------------------------------|
| id            | int           | ○    | ○    | ステータス履歴ID（主キー）     |
| section_id    | int           | ○    |      | 章ID（sections.idを参照、NOT NULL） |
| status_id     | int           | ○    |      | ステータスマスタID（master_statuses.id等を参照、NOT NULL） |
| status_value  | tinyint(1)    | ○    |      | ステータス値（0:下書き, 1:公開, 2:非公開, 3:凍結など） |
| delete_flg    | tinyint(1)    | ○    |      | 削除フラグ（0:有効, 1:削除済み） |
| created_at    | datetime      | ○    |      | 作成日時                       |
| updated_at    | datetime      | ○    |      | 更新日時                       |
| deleted_at    | datetime      |      |      | 削除日時                       |

---

## インデックス

| インデックス名           | 種類 | 説明               | カラム                |
|------------------------|------|-------------------|----------------------|
| PRIMARY KEY            | 主キー | ステータス履歴IDの主キー | id                   |
| INDEX                  | 通常 | 章ID検索用         | section_id           |
| INDEX                  | 通常 | ステータスID検索用     | status_id            |
| INDEX                  | 通常 | ステータス値検索用     | status_value         |
| INDEX                  | 通常 | 削除フラグ検索用       | delete_flg           |
| INDEX                  | 通常 | 作成日時検索用         | created_at           |
| INDEX                  | 通常 | 更新日時検索用         | updated_at           |
| INDEX                  | 通常 | 削除日時検索用         | deleted_at           |
| UNIQUE                 | 複合一意 | 章ID・ステータスマスタIDの組み合わせ一意 | section_id, status_id |

---

## 制約条件

### 主キー制約
- `id`: 自動採番（AUTO_INCREMENT）

### 外部キー制約
- `section_id` → `sections.id`（NOT NULL）
- `status_id` → `master_statuses.id`等（NOT NULL）

### チェック制約
- `status_value` IN (0, 1, 2, 3)
- `delete_flg` IN (0, 1)

### 一意制約
- `section_id`, `status_id`の組み合わせは一意

---

## 設計補足

- **論理削除**: `delete_flg`で論理削除を実現し、`deleted_at`で削除日時を記録。
- **履歴管理**: 章ごとに複数の状態履歴を持つことができる。
- **拡張性**: ステータス種別や値の追加・変更が容易。
- **一意性**: 章ごとに同じステータスマスタIDの重複登録は不可。

---

## 代表的なステータス値例

| status_value | 説明           |
|--------------|----------------|
| 0            | 下書き         |
| 1            | 公開           |
| 2            | 非公開         |
| 3            | 凍結           |

---

## 関連テーブル

- `sections`: 多対1の関係（章の状態管理）
- `master_statuses`: 多対1の関係（ステータスマスタ）

---

## 運用上の注意点

1. **データ整合性**: 章の状態は必ず本テーブルのIDを参照
2. **拡張性**: ステータス追加時は値の一意性に注意
3. **論理削除**: 削除されたステータスは通常の選択肢から除外
4. **削除日時管理**: 削除日時の正確な記録 