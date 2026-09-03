# novel-site 実装（Django + React）

Phase 1（単独作者向けの設定・執筆管理ツール）の実装。`docs/domain/`・`docs/design/` の確定済み設計に基づく新規実装で、旧実装（`implementations/python-django/`）は参考のみ（todo.md A参照）。

## 構成

- `backend/` … Django 5.2 + Django REST Framework。認証はセッション方式（Django標準）
- `frontend/` … React 19 + TypeScript + Vite。`/api`・`/media` はViteのプロキシでDjango(8000)へ転送（同一オリジンでセッションクッキーを使う）
- `docker-compose.yml` … PostgreSQL 16 + Redis + Adminer

## セットアップ（バックエンド）

```powershell
docker compose up -d           # PostgreSQL / Redis / Adminer を起動
cd backend
python -m venv .venv
.venv\Scripts\pip install -r requirements-dev.txt
.venv\Scripts\python manage.py migrate
.venv\Scripts\python manage.py runserver
```

- **DBはPostgreSQL**（2026-09-03決定）。`backend/.env` の `DB_ENGINE=postgres` で接続する（`.env.example`参照）。`.env` から `DB_ENGINE` を外すとSQLiteにフォールバックする（Dockerなしで動かしたいとき用）
- **DBの中身の確認はAdminer**: `http://localhost:8080` を開き、System=PostgreSQL / Server=`db` / Username=`novel_user` / Password=`novel_password` / Database=`novel_site` でログイン（phpMyAdmin相当のWeb UI）
- Django管理画面でも確認できる: `.venv\Scripts\python manage.py createsuperuser` の上で `http://localhost:8000/admin/`

## セットアップ（フロントエンド）

```powershell
cd frontend
npm install
npm run dev        # http://localhost:5173（バックエンドが8000で起動している前提）
```

実装済み画面: SC-01登録／SC-02ログイン／SC-05アカウント設定／SC-06・07ペンネーム／SC-08〜10 World（一覧・詳細・フォーム、削除済みトグル・復元、ペンネーム0件時の強制作成モーダル含む）。ヘッダーの「設定一覧」「作品一覧」、詳細画面の「変更履歴」「テンプレート管理」は未実装のためプレースホルダ（非活性）。
- テスト: `.venv\Scripts\python -m pytest`
- パスワードを忘れた場合の回復: `.venv\Scripts\python manage.py changepassword <user_id>`（Phase 1はパスワードリセット機能を持たないため。docs/project/Phase1-確定メモ.md §3.3）

## 実装状況

| 優先順位 | 領域 | 状態 |
|---|---|---|
| 1 | ユーザー・World（最小限） | バックエンドAPI実装済み（auth/pennames/worlds）。フロントエンド未着手 |
| 2 | Setting | 未着手 |
| 3 | 作品・執筆（Novel/Chapter/Episode） | 未着手 |
| 4 | ChangeLog（差分表示） | 未着手 |
| 5 | 閲覧・検索 | 未着手 |

## API（実装済み分）

| メソッド・パス | 内容 |
|---|---|
| POST `/api/auth/register/` | ユーザー登録（成功で即ログイン） |
| POST `/api/auth/login/` | ログイン（identifier=メール or ユーザーID） |
| POST `/api/auth/logout/` | ログアウト |
| GET/PATCH/DELETE `/api/auth/me/` | 自分の情報取得・更新・アカウント削除（論理削除） |
| CRUD `/api/pennames/` | ペンネーム（World保持中は削除不可） |
| CRUD `/api/worlds/` | World（`?q=`名前検索・`?include_deleted=1`削除済み込み） |
| POST `/api/worlds/:id/restore/` | 削除済みWorldの復元 |
