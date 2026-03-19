# API 設計書 — Python / Django 実装版

| 項目 | 内容 |
|------|------|
| バージョン | 1.0 |
| 作成日 | 2025年3月 |
| ベースパス | `/api/v1/` |
| 認証方式 | JWT（djangorestframework-simplejwt） |

---

## 1. 設計方針

### 1.1 基本方針

- RESTful API 設計（リソース指向）
- Django REST Framework（DRF）の ViewSet + Router で実装
- バージョニング：`/api/v1/` プレフィックス
- リクエスト / レスポンス形式：JSON
- 日付：ISO 8601（`2025-03-01T12:00:00+09:00`）
- ページネーション：limit / offset 方式
- HTTP ステータスコードを適切に使用

### 1.2 DRF 設定

```python
# novel_site/settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}
```

### 1.3 URL ルーティング構成

```python
# novel_site/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('auth/',    include('apps.users.urls.auth')),
        path('users/',   include('apps.users.urls.users')),
        path('novels/',  include('apps.novels.urls')),
        path('worlds/',  include('apps.worlds.urls')),
        path('', include('apps.communications.urls')),
    ])),
]
```

---

## 2. 認証 API

### 2.1 エンドポイント一覧

| メソッド | パス | 認証要否 | 説明 |
|---------|------|---------|------|
| POST | `/api/v1/auth/register` | 不要 | ユーザー新規登録 |
| POST | `/api/v1/auth/login` | 不要 | ログイン（JWT 発行） |
| POST | `/api/v1/auth/logout` | 必要 | ログアウト（リフレッシュトークン無効化） |
| POST | `/api/v1/auth/refresh` | 不要 | アクセストークン再取得 |
| POST | `/api/v1/auth/password/change` | 必要 | パスワード変更 |

### 2.2 ユーザー新規登録

```
POST /api/v1/auth/register
```

**リクエスト**
```json
{
  "username": "novel_user",
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**バリデーション**
- `username`：3〜20文字、英数字・ハイフンのみ、一意
- `email`：正しいメール形式、一意
- `password`：8文字以上、英字・数字・記号を含む

**レスポンス（201 Created）**
```json
{
  "id": 1,
  "username": "novel_user",
  "email": "user@example.com",
  "created_at": "2025-03-01T12:00:00+09:00"
}
```

### 2.3 ログイン

```
POST /api/v1/auth/login
```

**リクエスト**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**レスポンス（200 OK）**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": 1,
    "username": "novel_user",
    "email": "user@example.com"
  }
}
```

---

## 3. ユーザー API

### 3.1 エンドポイント一覧

| メソッド | パス | 認証要否 | 説明 |
|---------|------|---------|------|
| GET | `/api/v1/users/{id}/` | 不要 | ユーザー詳細取得 |
| PUT/PATCH | `/api/v1/users/{id}/` | 必要（本人） | プロフィール更新 |
| DELETE | `/api/v1/users/{id}/` | 必要（本人） | アカウント削除 |
| GET | `/api/v1/users/{id}/novels/` | 不要 | ユーザーの作品一覧 |
| POST | `/api/v1/users/{id}/follow/` | 必要 | フォロー |
| DELETE | `/api/v1/users/{id}/follow/` | 必要 | フォロー解除 |
| GET | `/api/v1/users/{id}/followers/` | 不要 | フォロワー一覧 |
| GET | `/api/v1/users/{id}/followings/` | 不要 | フォロー中一覧 |

### 3.2 ユーザー詳細取得

```
GET /api/v1/users/{id}/
```

**レスポンス（200 OK）**
```json
{
  "id": 1,
  "username": "novel_user",
  "profile": {
    "display_name": "小説太郎",
    "icon_url": "https://...",
    "biography": "自己紹介テキスト",
    "website_url": "https://example.com"
  },
  "stats": {
    "novel_count": 5,
    "follower_count": 120,
    "following_count": 30
  },
  "created_at": "2025-03-01T12:00:00+09:00"
}
```

---

## 4. 小説 API

### 4.1 エンドポイント一覧

| メソッド | パス | 認証要否 | 説明 |
|---------|------|---------|------|
| GET | `/api/v1/novels/` | 不要 | 小説一覧取得 |
| POST | `/api/v1/novels/` | 必要（作者） | 小説新規投稿 |
| GET | `/api/v1/novels/{id}/` | 不要 | 小説詳細取得 |
| PUT/PATCH | `/api/v1/novels/{id}/` | 必要（作者本人） | 小説情報更新 |
| DELETE | `/api/v1/novels/{id}/` | 必要（作者本人） | 小説削除 |
| GET | `/api/v1/novels/{id}/sections/` | 不要 | 章一覧取得 |
| POST | `/api/v1/novels/{id}/sections/` | 必要（作者本人） | 章作成 |
| GET | `/api/v1/novels/{id}/episodes/` | 不要 | 話一覧取得 |
| POST | `/api/v1/novels/{id}/episodes/` | 必要（作者本人） | 話作成 |
| GET | `/api/v1/episodes/{id}/` | 不要 | 話詳細取得 |
| PUT/PATCH | `/api/v1/episodes/{id}/` | 必要（作者本人） | 話更新 |
| DELETE | `/api/v1/episodes/{id}/` | 必要（作者本人） | 話削除 |

### 4.2 小説一覧取得

```
GET /api/v1/novels/?limit=20&offset=0&category=1&tag=fantasy&sort=updated_at
```

**クエリパラメータ**

| パラメータ | 型 | 説明 |
|---------|---|------|
| `limit` | int | 取得件数（デフォルト: 20、最大: 100） |
| `offset` | int | 取得開始位置 |
| `category` | int | カテゴリID でフィルタ |
| `tag` | string | タグ名でフィルタ |
| `q` | string | タイトル・あらすじのキーワード検索 |
| `sort` | string | ソート（`updated_at`, `created_at`, `view_count`, `rating`） |
| `order` | string | 昇順/降順（`asc`, `desc`）デフォルト: `desc` |

**レスポンス（200 OK）**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/v1/novels/?limit=20&offset=20",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "はじまりの物語",
      "synopsis": "あらすじテキスト...",
      "cover_image_url": "https://...",
      "category": { "id": 1, "name": "ファンタジー" },
      "tags": [{ "id": 1, "name": "冒険" }],
      "author": { "id": 1, "username": "novel_user", "display_name": "小説太郎" },
      "stats": { "view_count": 1000, "episode_count": 10, "rating_avg": 4.2 },
      "updated_at": "2025-03-01T12:00:00+09:00"
    }
  ]
}
```

### 4.3 小説新規投稿

```
POST /api/v1/novels/
Authorization: Bearer {access_token}
```

**リクエスト**
```json
{
  "title": "はじまりの物語",
  "synopsis": "あらすじテキスト",
  "category_id": 1,
  "tag_ids": [1, 2, 3],
  "is_r18": false
}
```

**レスポンス（201 Created）**
```json
{
  "id": 1,
  "title": "はじまりの物語",
  "synopsis": "あらすじテキスト",
  "status": "draft",
  "created_at": "2025-03-01T12:00:00+09:00"
}
```

---

## 5. 世界観・設定 API

### 5.1 エンドポイント一覧

| メソッド | パス | 認証要否 | 説明 |
|---------|------|---------|------|
| GET | `/api/v1/novels/{novel_id}/worlds/` | 不要（公開のみ） | 世界観一覧 |
| POST | `/api/v1/novels/{novel_id}/worlds/` | 必要（作者本人） | 世界観作成 |
| GET | `/api/v1/worlds/{id}/` | 不要（公開のみ） | 世界観詳細 |
| PUT/PATCH | `/api/v1/worlds/{id}/` | 必要（作者本人） | 世界観更新 |
| DELETE | `/api/v1/worlds/{id}/` | 必要（作者本人） | 世界観削除 |
| GET | `/api/v1/worlds/{id}/settings/` | 不要（公開のみ） | 設定一覧 |
| POST | `/api/v1/worlds/{id}/settings/` | 必要（作者本人） | 設定作成 |
| GET | `/api/v1/settings/{id}/` | 不要（公開のみ） | 設定詳細 |
| PUT/PATCH | `/api/v1/settings/{id}/` | 必要（作者本人） | 設定更新 |
| DELETE | `/api/v1/settings/{id}/` | 必要（作者本人） | 設定削除 |
| GET | `/api/v1/settings/{id}/fields/` | 不要（公開のみ） | フィールド一覧 |
| POST | `/api/v1/settings/{id}/fields/` | 必要（作者本人） | フィールド追加 |
| PUT/PATCH | `/api/v1/setting-fields/{id}/` | 必要（作者本人） | フィールド更新 |
| DELETE | `/api/v1/setting-fields/{id}/` | 必要（作者本人） | フィールド削除 |

---

## 6. コミュニケーション API

### 6.1 エンドポイント一覧（Phase 2）

| メソッド | パス | 認証要否 | 説明 |
|---------|------|---------|------|
| GET | `/api/v1/novels/{id}/comments/` | 不要 | コメント一覧 |
| POST | `/api/v1/novels/{id}/comments/` | 必要 | コメント投稿 |
| GET | `/api/v1/episodes/{id}/comments/` | 不要 | 話のコメント一覧 |
| POST | `/api/v1/episodes/{id}/comments/` | 必要 | 話へのコメント投稿 |
| DELETE | `/api/v1/comments/{id}/` | 必要（投稿者・作者・管理者） | コメント削除 |
| POST | `/api/v1/novels/{id}/evaluations/` | 必要 | 小説を評価 |
| DELETE | `/api/v1/novels/{id}/evaluations/` | 必要 | 小説の評価を取り消し |
| POST | `/api/v1/novels/{id}/bookmark/` | 必要 | ブックマーク |
| DELETE | `/api/v1/novels/{id}/bookmark/` | 必要 | ブックマーク解除 |
| GET | `/api/v1/notifications/` | 必要 | 通知一覧 |
| PUT | `/api/v1/notifications/{id}/read/` | 必要 | 通知を既読にする |
| POST | `/api/v1/reports/` | 必要 | 通報 |

### 6.2 コメント投稿

```
POST /api/v1/novels/{id}/comments/
Authorization: Bearer {access_token}
```

**リクエスト**
```json
{
  "body": "面白い作品です！",
  "parent_id": null
}
```

**レスポンス（201 Created）**
```json
{
  "id": 1,
  "body": "面白い作品です！",
  "author": { "id": 1, "username": "reader_user", "display_name": "読者太郎" },
  "parent_id": null,
  "created_at": "2025-03-01T12:00:00+09:00"
}
```

---

## 7. 検索 API

### 7.1 エンドポイント一覧

| メソッド | パス | 認証要否 | 説明 |
|---------|------|---------|------|
| GET | `/api/v1/search/novels/` | 不要 | 小説検索 |
| GET | `/api/v1/search/users/` | 不要 | ユーザー検索 |
| GET | `/api/v1/categories/` | 不要 | カテゴリ一覧 |
| GET | `/api/v1/tags/` | 不要 | タグ一覧 |

---

## 8. エラーレスポンス仕様

### 8.1 エラーレスポンス形式

```json
{
  "status": "error",
  "code": "VALIDATION_ERROR",
  "message": "入力内容に誤りがあります",
  "errors": {
    "username": ["この値はすでに使用されています"],
    "password": ["8文字以上で入力してください"]
  }
}
```

### 8.2 HTTP ステータスコード一覧

| コード | 用途 |
|--------|------|
| 200 OK | 取得・更新成功 |
| 201 Created | 作成成功 |
| 204 No Content | 削除成功 |
| 400 Bad Request | バリデーションエラー |
| 401 Unauthorized | 未認証（トークンなし・期限切れ） |
| 403 Forbidden | 権限不足 |
| 404 Not Found | リソース未発見 |
| 409 Conflict | 重複（メールアドレス等） |
| 429 Too Many Requests | レートリミット超過 |
| 500 Internal Server Error | サーバー内部エラー |

---

## 9. 共通仕様

### 9.1 認証ヘッダー

```
Authorization: Bearer {access_token}
```

### 9.2 ページネーション

```
GET /api/v1/novels/?limit=20&offset=40
```

レスポンスには以下を含む：
- `count`：総件数
- `next`：次ページ URL（なければ null）
- `previous`：前ページ URL（なければ null）
- `results`：データ配列

### 9.3 ソートパラメータ

| 値 | 説明 |
|----|------|
| `created_at` | 投稿日時 |
| `updated_at` | 更新日時 |
| `view_count` | 閲覧数 |
| `rating` | 評価平均 |
| `episode_count` | 話数 |

### 9.4 論理削除リソースの扱い

- 論理削除済みリソースは API レスポンスに含めない
- 削除済みコメントは `"body": "[削除されました]"` として返す（スレッド構造保持のため）
