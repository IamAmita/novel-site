# 小説投稿サイト - 5言語学習プロジェクト

同一仕様の小説投稿サイトを5つの異なる言語で実装し、各言語の特徴と適用領域を実体験する学習プロジェクト。

## 🎯 プロジェクト概要

- **目標**: 技術比較と学習効果の最大化
- **対象言語**: PHP、Python、TypeScript、Java、Go
- **アーキテクチャ**: モノレポ構成による統一管理

## 📁 ディレクトリ構造

```
novel-site/
├── README.md                    # このファイル
├── docs/                        # 共通設計・ドキュメント
│   ├── 要件定義/
│   ├── 基本設計/
│   └── 技術比較/
├── shared/                      # 共通リソース
│   ├── database/               # DB設計・初期データ
│   ├── api/                    # API仕様
│   ├── docker/                 # 共通Docker設定
│   └── assets/                 # 共通アセット
├── implementations/             # 各言語実装
│   ├── python-django/          # Python + Django版
│   ├── typescript-nextjs/      # TypeScript + Next.js版
│   ├── java-springboot/        # Java + Spring Boot版
│   ├── go-gin/                 # Go + Gin版
│   └── php-laravel/            # PHP + Laravel版
└── tools/                      # 開発支援ツール
    ├── benchmark/              # パフォーマンス測定
    └── analysis/               # 比較分析
```

## 🚀 各実装バージョン

| 言語 | フレームワーク | データベース | 状況 |
|------|----------------|--------------|------|
| Python | Django 4 | 未選定 | ⏳ 技術スタック定義予定 |
| TypeScript | Next.js 14 | 未選定 | ⏳ 技術スタック定義予定 |
| Java | Spring Boot 3 | 未選定 | ⏳ 技術スタック定義予定 |
| Go | Gin | 未選定 | ⏳ 技術スタック定義予定 |
| PHP | Laravel 10 | 未選定 | ⏳ 技術スタック定義予定 |

※ データベースは各技術スタック定義時に、言語・フレームワークの特性に最適なものを選定

## 🛠️ 開発環境

### 必要なツール
- Docker & Docker Compose
- Git
- 各言語の開発環境（実装時に設定）

### クイックスタート
```bash
# リポジトリクローン
git clone <repository-url>
cd novel-site

# 共通環境確認
cd shared/docker
docker-compose up -d

# 各実装の起動方法は implementations/{language}/ の README を参照
```

## 📊 学習・比較観点

### 技術比較軸
- **開発効率**: 実装速度、学習コスト、デバッグ容易性
- **パフォーマンス**: レスポンス時間、メモリ使用量、並行処理
- **保守性**: コード可読性、テスト容易性、リファクタリング
- **エコシステム**: ライブラリ充実度、コミュニティ、将来性

### 成果物
- 各言語での完全動作するWebアプリケーション
- 実体験に基づく技術比較ブログ記事
- パフォーマンス測定結果・ベンチマーク
- 学習記録・開発日誌

## 📚 ドキュメント

### メインドキュメント
- [プロジェクト概要](docs/project/概要.md)
- [技術選定方針](docs/project/技術選定方針.md)
- [システム構成](docs/architecture/システム構成.md)
- [データベース設計](docs/architecture/データベース設計.md)
- [機能仕様](docs/specifications/機能仕様.md)

### 詳細資料（アーカイブ）
- [要件定義書](docs/archive/要件定義/要件定義書.md)
- [機能要件定義書](docs/archive/要件定義/機能要件定義書.md)
- [詳細DB設計](docs/archive/基本設計/DB設計/)
- [詳細API設計](docs/archive/基本設計/API設計/)

## 🎓 学習進捗

### Phase 1: Python版（基盤構築）
- [x] 要件定義・基本設計
- [x] プロジェクト構造整理
- [ ] 技術スタック詳細定義
- [ ] データベース選定・設計
- [ ] 実装・基本機能完成

### Phase 2-5: 他言語版
- [ ] TypeScript版
- [ ] Java版  
- [ ] Go版
- [ ] PHP版

## 🤝 貢献

このプロジェクトは個人学習目的ですが、フィードバックや提案は歓迎します。

## 📄 ライセンス

MIT License

---

**作成者**: 開発者  
**開始日**: 2025年1月  
**最終更新**: 2025年1月