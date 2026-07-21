# 実装バージョン（implementations）

小説投稿サイトの実装を管理するディレクトリ。

## 🎯 実装

### python-django/ - Python + Django版
- **言語**: Python 3.11
- **バックエンド**: Django 4 + Django REST Framework
- **フロントエンド**: React 18 + TypeScript
- **データベース**: PostgreSQL 15
- **状況**: 🔄 開発中

詳細は [python-django/README.md](python-django/README.md) を参照。

## 🛠️ 共通仕様

要件・エンティティ設計は 2026-07-21 に一旦削除し、[../todo.md](../todo.md) の決定事項リストを詰めてから再作成する。

### 認証方式
- JWT (JSON Web Token) による認証

## 🔧 開発環境

### 前提条件
- Docker & Docker Compose
- Git
- Python 3.11+ / Node.js 18+

### 起動手順
```bash
cd implementations/python-django/
docker-compose up -d
# 詳細は python-django/docs/初回手順.md を参照
```

---

**管理方針**: `docs/project/` の方針・`todo.md` の決定事項に従いつつ実装を進める
