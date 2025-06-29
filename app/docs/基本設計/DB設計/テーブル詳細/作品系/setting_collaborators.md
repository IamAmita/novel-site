# 設定協作者テーブル（setting_collaborators）

---

## 概要
設定の共同編集者を管理するテーブル。設定作成者が他のユーザーに編集権限を付与し、複数人での設定作成・編集を可能にする。

---

## テーブル定義

| 属性名 | 型 | 必須 | 一意 | 説明 |
|--------|----|------|------|------|
| id | int | ○ | ○ | 協作者ID（主キー） |
| setting_id | int | ○ | | 設定ID（settings.id） |
| user_id | int | ○ | | 協作者ユーザーID（users.id） |
| permission_level | varchar(20) | ○ | | 権限レベル（view:閲覧, edit:編集, admin:管理） |
| invited_by | int | ○ | | 招待者ユーザーID（users.id） |
| invited_at | datetime | ○ | | 招待日時 |
| accepted_at | datetime | | | 承認日時 |
| declined_at | datetime | | | 辞退日時 |
| status | varchar(20) | ○ | | ステータス（pending:招待中, accepted:承認済み, declined:辞退, removed:削除） |
| notes | text | | | 招待メッセージや備考 |
| created_at | datetime | ○ | | 作成日時 |
| updated_at | datetime | ○ | | 更新日時 |
| deleted_at | datetime | | | 論理削除日時 |

---

## インデックス

| インデックス名 | 種類 | 説明 | カラム |
|----------------|------|------|--------|
| PRIMARY KEY | 主キー | 協作者IDの主キー | id |
| INDEX | 通常 | 設定検索用 | setting_id |
| INDEX | 通常 | ユーザー検索用 | user_id |
| INDEX | 通常 | 招待者検索用 | invited_by |
| INDEX | 通常 | ステータス検索用 | status |
| INDEX | 通常 | 権限レベル検索用 | permission_level |
| UNIQUE | 一意 | 設定・ユーザーの重複防止 | setting_id, user_id |
| INDEX | 複合 | ユーザー・ステータス検索用 | user_id, status |
| INDEX | 複合 | 設定・ステータス検索用 | setting_id, status |

---

## 制約条件

### 主キー制約
- `id`: 自動採番（AUTO_INCREMENT）

### 外部キー制約
- `setting_id` → `settings.id`
- `user_id` → `users.id`
- `invited_by` → `users.id`

### 一意制約
- `setting_id`と`user_id`の組み合わせは一意

### チェック制約
- `permission_level` IN ('view', 'edit', 'admin')
- `status` IN ('pending', 'accepted', 'declined', 'removed')

---

## 設計補足

### 権限管理
- 設定作成者は常に全権限を持つ
- 3段階の権限レベル（view:閲覧, edit:編集, admin:管理）
- 権限変更時は履歴に記録

### 招待フロー
- 招待→承認→権限付与の流れ
- 招待メッセージ機能
- 辞退・削除機能

### 重複防止
- 同じ設定に同じユーザーを重複招待できない
- 一意制約によりデータ整合性を保証

### 履歴管理
- 協作者の変更履歴は`setting_histories`で管理
- 通知機能との連携

---

## 関連テーブル

- `settings`: 多対1の関係（設定）
- `users`: 多対1の関係（協作者・招待者）

---

## 運用上の注意点

1. **権限管理**: 設定作成者は常に全権限を持つ
2. **招待フロー**: 招待→承認→権限付与の流れを適切に管理
3. **重複防止**: 同じ設定に同じユーザーを重複招待できない
4. **履歴管理**: 協作者の変更履歴は`setting_histories`で管理
5. **通知機能**: 招待・承認・辞退時に通知を送信
6. **論理削除**: 協作者関係の削除は論理削除で対応 