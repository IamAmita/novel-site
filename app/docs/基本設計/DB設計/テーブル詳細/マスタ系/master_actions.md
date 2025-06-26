# master_actions テーブル詳細（アクション種別マスタ）

---

## 概要
ユーザーアクション（いいね・ブックマーク・フォロー・通知種別など）を一元管理するマスタテーブルです。user_actionsやnotifications等から参照し、拡張性・一貫性を確保します。

---

## テーブル定義

| 属性名        | 型        | 必須 | 一意 | 説明                         |
|---------------|-----------|------|------|------------------------------|
| id            | int       | ○    | ○    | アクション種別ID（主キー、3桁:100〜999）   |
| display_name  | varchar   | ○    |      | 表示名（UI用）               |
| description   | text      |      |      | 説明・備考                   |
| created_at    | datetime  | ○    |      | 登録日時                     |

---

## インデックス

- 主キー（id）
- 表示名検索用（display_name）

---

## 制約条件

- 主キー制約：idは自動採番
- idは3桁（100〜999）の範囲で管理
- display_nameは必須

---

## 設計補足
- idは3桁（100〜999）の範囲で一意に管理します。
- user_actionsテーブルのaction_typeやnotificationsテーブルのnotification_type等で参照可能
- display_nameでUIや管理画面に柔軟に表示可能
- descriptionで用途や備考を管理
- 新しいアクション種別・通知種別を追加する場合は本テーブルに1行追加

---

## 関連テーブル
- user_actions: 多対1の関係（action_type）
- notifications: 多対1の関係（notification_type）

---

## 運用上の注意点
- アクション種別・通知種別の追加・変更は本テーブルで一元管理
- display_nameやdescriptionの多言語対応も可能
- idは3桁（100〜999）で管理し、他のマスタID体系と一貫性を持たせます。 