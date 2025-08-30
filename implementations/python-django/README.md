# Python + Django 実装版

## 🎯 実装概要

- **言語**: Python 3.11
- **バックエンドフレームワーク**: Django 4 + Django REST Framework
- **フロントエンドフレームワーク**: React 18 + TypeScript
- **データベース**: PostgreSQL 15
- **キャッシュ**: Redis
- **認証**: JWT + Django Allauth

## 🏗️ アーキテクチャ

```
python-django/
├── backend/                # Django プロジェクト
│   ├── novel_site/        # プロジェクト設定
│   ├── apps/              # Django アプリケーション
│   │   ├── users/         # ユーザー管理
│   │   ├── novels/        # 小説管理
│   │   ├── settings/      # 設定管理
│   │   └── common/        # 共通機能
│   ├── requirements.txt   # Python依存関係
│   └── manage.py
├── frontend/              # React アプリケーション
│   ├── src/
│   │   ├── components/    # Reactコンポーネント
│   │   ├── pages/         # ページコンポーネント
│   │   ├── hooks/         # カスタムフック
│   │   ├── services/      # API通信
│   │   └── types/         # TypeScript型定義
│   ├── package.json
│   └── tsconfig.json
├── docker-compose.yml     # 開発環境
└── README.md             # このファイル
```

## 🚀 クイックスタート

### 前提条件
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+

### 環境構築
```bash
# リポジトリルートから
cd implementations/python-django

# 共通サービス起動（PostgreSQL, Redis）
cd ../../shared/docker
docker-compose up -d

# 開発環境起動
cd ../../implementations/python-django
docker-compose up -d

# または手動起動
# バックエンド
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# フロントエンド（別ターミナル）
cd frontend
npm install
npm run dev
```

## 📱 アクセス

- **フロントエンド**: http://localhost:3000
- **バックエンドAPI**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin
- **API ドキュメント**: http://localhost:8000/api/docs

## 🛠️ 開発

### バックエンド開発
```bash
cd backend

# マイグレーション作成
python manage.py makemigrations

# マイグレーション実行
python manage.py migrate

# スーパーユーザー作成
python manage.py createsuperuser

# テスト実行
python manage.py test

# 静的ファイル収集
python manage.py collectstatic
```

### フロントエンド開発
```bash
cd frontend

# 開発サーバー起動
npm run dev

# ビルド
npm run build

# テスト実行
npm run test

# 型チェック
npm run type-check
```

## 📊 特徴・学習ポイント

### Django の特徴
- **MTV パターン**: Model-Template-View アーキテクチャ
- **Django ORM**: 強力なO/Rマッピング
- **Django Admin**: 自動生成される管理画面
- **ミドルウェア**: リクエスト/レスポンス処理の拡張
- **Django REST Framework**: RESTful API構築フレームワーク

### 学習目標
- Django の設計思想と開発パターン
- Python による Web アプリケーション開発
- Django ORM によるデータベース操作
- Django REST Framework による API 開発
- React + TypeScript による SPA 開発

## 🧪 テスト

### バックエンドテスト
```bash
cd backend

# 全テスト実行
python manage.py test

# アプリケーション別テスト
python manage.py test apps.users
python manage.py test apps.novels

# カバレッジ測定
coverage run --source='.' manage.py test
coverage report
coverage html
```

### フロントエンドテスト
```bash
cd frontend

# 単体テスト
npm run test

# E2Eテスト
npm run test:e2e

# カバレッジ測定
npm run test:coverage
```

## 📦 デプロイ

### Docker デプロイ
```bash
# プロダクションビルド
docker-compose -f docker-compose.prod.yml build

# プロダクション起動
docker-compose -f docker-compose.prod.yml up -d
```

## 🔍 パフォーマンス

### 最適化ポイント
- Django ORM クエリ最適化（select_related, prefetch_related）
- Redis キャッシュ活用
- 静的ファイル配信最適化
- データベースインデックス最適化

### 測定コマンド
```bash
# Django Debug Toolbar での分析
# settings.py で DEBUG_TOOLBAR を有効化

# パフォーマンス測定
cd ../../tools/benchmark
./measure-python.sh
```

## 📚 参考資料

### 公式ドキュメント
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [React Documentation](https://react.dev/)

### 学習リソース
- Django Girls Tutorial
- Django for Beginners
- React TypeScript Cheatsheet

---

**開発状況**: 🔄 開発中  
**開始日**: 2025年1月  
**完成予定**: 2025年4月
