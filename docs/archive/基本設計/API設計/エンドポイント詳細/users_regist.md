# ユーザー新規登録API 詳細設計

---

## エンドポイント
POST /api/v1/users/regist

## 概要
新規ユーザーアカウントを登録するAPI。

## 認証
不要（未ログイン状態で利用可能）

## リクエスト例（JSON）
```json
{
  "username": "sampleuser",
  "email": "sample@example.com",
  "password": "password123"
}
```

### パラメータ仕様
| パラメータ | 型     | 必須 | 説明                 | バリデーション例           |
|------------|--------|------|----------------------|----------------------------|
| username   | string | 必須 | ユーザー名           | 3〜30文字、英数字・記号可  |
| email      | string | 必須 | メールアドレス       | メール形式、255文字以内    |
| password   | string | 必須 | パスワード           | 8文字以上                  |

## レスポンス例（成功時）
HTTP 201 Created
```json
{
  "id": 1,
  "username": "sampleuser",
  "email": "sample@example.com"
}
```

## バリデーション・制約
- username：必須、3〜30文字、重複不可
- email：必須、メール形式、重複不可
- password：必須、8文字以上

## エラー時のレスポンス例
### 既存ユーザー名・メールアドレス
HTTP 400 Bad Request
```json
{
  "status": "error",
  "message": "ユーザー名またはメールアドレスは既に登録されています。",
  "code": 400
}
```

### バリデーションエラー
HTTP 400 Bad Request
```json
{
  "status": "error",
  "message": "パスワードは8文字以上で入力してください。",
  "code": 400
}
```

## 備考
- パスワードはハッシュ化して保存すること
- 登録完了後、自動ログインや認証トークン発行は別APIで対応 