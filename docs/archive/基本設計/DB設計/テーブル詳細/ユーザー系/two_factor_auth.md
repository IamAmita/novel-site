# two_factor_auth テーブル詳細

---

## 概要
ユーザーの2段階認証設定を管理するテーブルです。認証方式、シークレットなどを含みます。

---

## テーブル定義

| 属性名         | 型         | 必須 | 一意 | 説明                         |
|----------------|------------|------|------|------------------------------|
| id             | int        | ○    | ○    | 2FA設定ID（主キー）           |
| user_id        | int        | ○    |      | ユーザーID（外部キー）       |
| method         | tinyint    | ○    |      | 認証方式ID（master_two_factor_methods参照）|
| secret         | varchar    |      |      | TOTP用シークレットやSMS番号   |
| status         | tinyint    | ○    |      | ステータスID（master_statuses参照）|
| is_active      | tinyint    | ○    |      | 有効/無効フラグ（0:有効, 1:無効）|
| created_at     | datetime   | ○    |      | 登録日時                     |

---

## インデックス

| インデックス名 | 種類 | 説明 | カラム |
|----------------|------|------|--------|
| PRIMARY KEY | 主キー | 2FA設定IDの主キー | id |
| UNIQUE | 一意 | ユーザーIDの一意制約（1ユーザー1設定） | user_id |
| INDEX | 通常 | 認証方式検索用 | method |
| INDEX | 通常 | ステータス検索用 | status |
| INDEX | 通常 | 有効/無効フラグ検索用 | is_active |
| INDEX | 通常 | 登録日時検索用 | created_at |

---

## 制約条件

### 主キー制約
- `id`: 自動採番（AUTO_INCREMENT）

### 一意制約
- `user_id`: ユーザーIDは一意である必要があります（1ユーザー1設定）

### 外部キー制約
- `user_id` → `users.id`: ユーザーテーブルを参照
- `method` → `master_two_factor_methods.id`: 認証方式マスタを参照
- `status` → `master_statuses.id`: ステータスマスタを参照

### チェック制約
- `method`: master_two_factor_methodsで定義されたIDである必要があります
- `status`: master_statusesで定義されたIDである必要があります
- `is_active`: 0または1の値のみ許可（0:有効, 1:無効）

---

## 設計補足

### 有効/無効フラグ（is_active）
- 0:有効、1:無効として管理
- 2FA設定が有効かどうかを判定する際に利用

### 認証方式（method）
- master_two_factor_methodsテーブルで管理
- 例：0=email、1=sms、2=totp

### ステータス（status）
- master_statusesテーブルで管理
- 例：100=有効（active）、101=無効（inactive）、102=一時停止（suspended）

### シークレット（secret）
- TOTP方式の場合：Base32エンコードされたシークレットキー
- SMS方式の場合：電話番号
- メール方式の場合：null

---

## 関連テーブル

- `users`: 多対1の関係（ユーザー基本情報）
- `master_two_factor_methods`: 多対1の関係（認証方式マスタ）
- `master_statuses`: 多対1の関係（ステータスマスタ）

---

## 運用上の注意点

- is_active=1（無効）の場合、2FA認証は利用不可とする
- 新しい認証方式を追加する場合はmaster_two_factor_methodsに登録 