# two_factor_auth テーブル詳細

---

## 概要
ユーザーの2段階認証設定を管理するテーブルです。認証方式、シークレット、バックアップコードなどを含みます。

---

## テーブル定義

| 属性名         | 型         | 必須 | 一意 | 説明                         |
|----------------|------------|------|------|------------------------------|
| id             | int        | ○    | ○    | 2FA設定ID（主キー）           |
| user_id        | int        | ○    |      | ユーザーID（外部キー）       |
| method         | varchar    | ○    |      | 認証方式（email, sms, totp等）|
| secret         | varchar    |      |      | TOTP用シークレットやSMS番号   |
| backup_codes   | text       |      |      | バックアップコード（暗号化保存）|
| status         | varchar    | ○    |      | 有効/無効/一時停止など        |
| enabled_at     | datetime   |      |      | 有効化日時                   |
| disabled_at    | datetime   |      |      | 無効化日時                   |
| created_at     | datetime   | ○    |      | 登録日時                     |
| updated_at     | datetime   |      |      | 更新日時                     |

---

## インデックス

| インデックス名 | 種類 | 説明 | カラム |
|----------------|------|------|--------|
| PRIMARY KEY | 主キー | 2FA設定IDの主キー | id |
| UNIQUE | 一意 | ユーザーIDの一意制約（1ユーザー1設定） | user_id |
| INDEX | 通常 | 認証方式検索用 | method |
| INDEX | 通常 | ステータス検索用 | status |
| INDEX | 通常 | 登録日時検索用 | created_at |

---

## 制約条件

### 主キー制約
- `id`: 自動採番（AUTO_INCREMENT）

### 一意制約
- `user_id`: ユーザーIDは一意である必要があります（1ユーザー1設定）

### 外部キー制約
- `user_id` → `users.id`: ユーザーテーブルを参照

### チェック制約
- `method`: 'email', 'sms', 'totp'のいずれかである必要があります
- `status`: 'active', 'inactive', 'suspended'のいずれかである必要があります

---

## 設計補足

### 認証方式（method）
- `email`: メール認証
- `sms`: SMS認証
- `totp`: TOTP（Time-based One-Time Password）

### シークレット（secret）
- TOTP方式の場合：Base32エンコードされたシークレットキー
- SMS方式の場合：電話番号
- メール方式の場合：null

### バックアップコード（backup_codes）
- 暗号化して保存
- 使い捨てで運用
- JSON形式で複数のコードを管理

### ステータス（status）
- `active`: 有効
- `inactive`: 無効
- `suspended`: 一時停止

---

## 関連テーブル

- `users`: 多対1の関係（ユーザー基本情報）

---

## 運用上の注意点

1. **シークレット管理**: 適切な暗号化が必要
2. **バックアップコード**: 使い捨てで運用
3. **認証方式変更**: 履歴テーブルに記録
4. **セキュリティ**: 定期的な見直しが必要

- バックアップコードは安全に保管 