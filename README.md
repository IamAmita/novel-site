# 小説投稿サイト

設定管理・共同著作対応の小説投稿サイトです。

## プロジェクト概要

- **目的**: 設定管理機能の充実した小説投稿サイトの構築
- **特徴**: 共同作成・依頼機能による創作コミュニティの形成
- **開発方針**: 品質重視、納期制限なし、継続的改善

## 技術スタック

### フロントエンド
- Vue.js 3 + TypeScript
- Vuetify 3 (UIフレームワーク)
- Pinia (状態管理)
- Vue Router 4 (ルーティング)
- Axios (HTTP通信)
- Vite (ビルドツール)

### バックエンド
- Python 3.11
- Django 4
- Django REST Framework
- Celery + Redis (タスクキュー・キャッシュ)

### データベース
- PostgreSQL 15

### インフラ・運用
- Docker + Docker Compose
- AWS (ECS, RDS, S3, CloudFront)
- GitHub Actions (CI/CD)

## プロジェクト構造

```
novel-site/
├── frontend/          # Vue.jsフロントエンド
├── backend/           # Djangoバックエンド
├── docker/            # Docker設定ファイル
├── docs/              # ドキュメント
├── config/            # 設定ファイル
└── README.md          # このファイル
```

## 開発環境の構築

### 前提条件
- Docker Desktop
- Git
- Cursor (VSCodeベースのIDE推奨)

### セットアップ手順
1. リポジトリのクローン
2. Docker環境の構築
3. 開発サーバーの起動

詳細は各ディレクトリのREADMEを参照してください。

## 開発方針

- **品質重視**: 納期よりも満足度（品質）を重視
- **段階的開発**: フェーズ分けによる段階的実装
- **実装しながら学習**: 実際の開発を通じて技術を習得
- **継続的改善**: 運用開始後も継続的な機能改善

## ライセンス

このプロジェクトは個人開発の学習目的で作成されています。

---

**作成日**: 2025年1月
**開発者**: 個人開発
