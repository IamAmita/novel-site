# 小説投稿サイト - Python/Django実装

設定管理を自由かつ詳細に行い、それを見ながら執筆できる小説投稿サイト。Python（Django + React）で実装する。

## 🎯 プロジェクト概要

- **目標**: 設定管理と執筆を軸にした創作者向けプラットフォームの構築
- **実装技術**: Python 3.11 + Django + React（TypeScript）
- **アーキテクチャ**: モノレポ構成による統一管理

## 📁 ディレクトリ構造

```
novel-site/
├── README.md                    # このファイル
├── todo.md                      # 決定すべき事項のリスト・進捗
├── docs/                        # プロジェクトドキュメント
│   ├── project/                 # プロジェクト方針・意思決定記録
│   ├── assets/                  # 共通アセット（画像等）
│   └── archive/                 # 過去の要件定義・基本設計資料（参照用）
├── implementations/
│   └── python-django/           # Python + Django版 実装
└── tools/                       # 開発支援ツール
```

> 要件・設計ドキュメント（business/domain/design/quality/architecture/specifications）は 2026-07-21 に一旦削除した。[todo.md](todo.md) の決定事項を詰めてから再作成する。

## 🚀 実装状況

| 実装 | 状況 |
|------|------|
| python-django | 🔄 開発中 |

詳細は [implementations/python-django/README.md](implementations/python-django/README.md) と [todo.md](todo.md) を参照。

## 🛠️ 開発環境

### 必要なツール
- Docker & Docker Compose
- Git
- Python 3.11+ / Node.js 18+（ローカル実行時）

### クイックスタート
```bash
git clone <repository-url>
cd novel-site/implementations/python-django
docker compose up --build
```

詳細な手順は [implementations/python-django/docs/初回手順.md](implementations/python-django/docs/初回手順.md) を参照。

## 📚 ドキュメント

### メインドキュメント
- [プロジェクト概要](docs/project/概要.md)
- [プロダクト定義](docs/project/プロダクト定義.md)
- [Phase1-確定メモ](docs/project/Phase1-確定メモ.md)
- [todo.md（決定事項リスト）](todo.md)

### 詳細資料（アーカイブ）
- [要件定義書](docs/archive/要件定義/要件定義書.md)
- [機能要件定義書](docs/archive/要件定義/機能要件定義書.md)
- [詳細DB設計](docs/archive/基本設計/DB設計/)
- [詳細API設計](docs/archive/基本設計/API設計/)

## 📄 ライセンス

MIT License

---

**作成者**: 開発者
**開始日**: 2025年1月
**最終更新**: 2026年7月
