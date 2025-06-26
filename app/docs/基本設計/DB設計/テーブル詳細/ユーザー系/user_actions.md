# user_actions テーブル詳細

---

## 概要
ユーザーが行った各種アクション（いいね・ブックマーク等）を一元管理するテーブルです。多様な対象（小説・設定・話・掲示板投稿など）に対するアクションを、action_type（アクション種別、master_actions参照）で区別します。

---

## テーブル定義

| 属性名         | 型        | 必須 | 一意 | 説明                                   |
|----------------|-----------|------|------|----------------------------------------|
| id             | int       | ○    | ○    | アクションID（主キー）                 |
| user_id        | int       | ○    |      | ユーザーID（外部キー）                 |
| action_type    | int       | ○    |      | アクション種別ID（master_actions.id参照）|
| class_id       | int       | ○    |      | 対象クラスID（master_classes参照）     |
| table_id       | int       | ○    |      | 対象テーブルID（master_tables参照）    |
| target_id      | int       | ○    |      | 対象ID                                 |
| delete_flg     | tinyint   | ○    |      | 論理削除フラグ（0:有効, 1:削除）       |
| created_at     | datetime  | ○    |      | アクション日時                         |

---

## インデックス

- 主キー（id）
- 複合一意（user_id, action_type, class_id, table_id, target_id, delete_flg）
- ユーザーID検索用（user_id）
- アクション種別検索用（action_type）
- 対象検索用（class_id, table_id, target_id）
- 論理削除フラグ検索用（delete_flg）
- アクション日時検索用（created_at）

---

## 制約条件

- 主キー制約：idは自動採番
- 複合一意制約：user_id, action_type, class_id, table_id, target_id, delete_flg
- 外部キー制約：user_idはusers、action_typeはmaster_actions、class_idはmaster_classes、table_idはmaster_tablesを参照
- チェック制約：delete_flgは0または1

---

## 設計補足

- 1ユーザーが同じ対象・同じアクションを複数回行えないよう、複合一意制約で管理
- 論理削除で履歴を保持
- action_typeはmaster_actions.idを参照し、display_nameやdescriptionで用途・表示名を管理
- likes/bookmarks等の用途で分岐したい場合はaction_typeで判別

---

## 関連テーブル

- users: 多対1の関係（アクションユーザー）
- master_classes: 多対1の関係（対象クラス）
- master_tables: 多対1の関係（対象テーブル）
- master_actions: 多対1の関係（アクション種別）

---

## 運用上の注意点

- 論理削除で履歴を保持
- アクション数の集計はパフォーマンス要件に応じて別途キャッシュ・集計テーブルを検討
- 不正利用やスパム対策のための監視 