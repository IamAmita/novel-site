# 話テーブル（episodes）

---

## 概要
小説（novels）の話（エピソード）情報を管理するテーブル。各章（section）に複数の話を持たせることができ、話ごとにタイトルや本文、公開状態などを管理する。

---

## テーブル定義

| 属性名        | 型            | 必須 | 一意 | 説明                           |
|---------------|---------------|------|------|--------------------------------|
| id            | int           | ○    | ○    | 話ID（主キー）                 |
| novel_id      | int           | ○    |      | 小説ID（novels.idを参照、NOT NULL） |
| section_id    | int           |      |      | 章ID（sections.idを参照、NULL可） |
| episode_no    | int           | ○    |      | 話番号（小説内での表示順）     |
| title         | varchar(255)  | ○    |      | 話タイトル                     |
| body          | text          |      |      | 話本文                         |
| publish_flg   | tinyint(1)    | ○    |      | 公開フラグ（0:非公開, 1:公開） |
| delete_flg    | tinyint(1)    | ○    |      | 削除フラグ（0:有効, 1:削除済み） |
| created_at    | datetime      | ○    |      | 作成日時                       |
| updated_at    | datetime      | ○    |      | 更新日時                       |
| deleted_at    | datetime      |      |      | 削除日時                       |

---

## インデックス

| インデックス名           | 種類 | 説明               | カラム                |
|------------------------|------|-------------------|----------------------|
| PRIMARY KEY            | 主キー | 話IDの主キー       | id                   |
| INDEX                  | 通常 | 小説ID検索用       | novel_id             |
| INDEX                  | 通常 | 章ID検索用         | section_id           |
| INDEX                  | 通常 | 話番号検索用       | episode_no           |
| INDEX                  | 通常 | 公開フラグ検索用   | publish_flg          |
| INDEX                  | 通常 | 削除フラグ検索用   | delete_flg           |
| INDEX                  | 通常 | 作成日時検索用     | created_at           |
| INDEX                  | 通常 | 更新日時検索用     | updated_at           |
| INDEX                  | 通常 | 削除日時検索用     | deleted_at           |
| UNIQUE                 | 複合一意 | 小説ID・話番号の組み合わせ一意 | novel_id, episode_no |

---

## 制約条件

### 主キー制約
- `id`: 自動採番（AUTO_INCREMENT）

### 外部キー制約
- `novel_id` → `novels.id`（NOT NULL）
- `section_id` → `sections.id`（NULL可）

### チェック制約
- `publish_flg` IN (0, 1)
- `delete_flg` IN (0, 1)
- `title`: 空文字列でないこと

### 一意制約
- `novel_id`, `episode_no`の組み合わせは一意

---

## 設計補足

- **多話構成**: 小説1件に複数の話を持たせることが可能。
- **章連携**: 章（section）と紐付ける場合はsection_idを利用（NULL可で柔軟運用）。
- **論理削除**: `delete_flg`で論理削除を実現し、`deleted_at`で削除日時を記録。
- **公開状態**: `publish_flg`で話ごとの公開・非公開を管理。
- **検索機能**: 小説ID・章ID・話番号・公開状態などでの検索が容易。

---

## 関連テーブル

- `novels`: 多対1の関係（小説の基本情報）
- `sections`: 多対1の関係（章情報、NULL可）

---

## 運用上の注意点

1. **データ整合性**: 小説・話番号の重複登録防止
2. **章連携**: 章と話の紐付け運用に注意（NULL可）
3. **論理削除**: 削除された話の適切な処理
4. **公開状態管理**: 公開・非公開の切り替えに注意
5. **削除日時管理**: 削除日時の正確な記録 