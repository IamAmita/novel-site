# 共通リソース（shared）

5言語実装で共有するリソースを管理するディレクトリ。

## 📁 ディレクトリ構成

```
shared/
├── database/           # データベース関連
│   ├── init.sql       # 初期化スクリプト
│   ├── schema.sql     # スキーマ定義
│   ├── seed.sql       # サンプルデータ
│   └── migrations/    # マイグレーションファイル
├── api/               # API仕様
│   ├── openapi.yaml   # OpenAPI 3.0仕様
│   ├── endpoints/     # エンドポイント詳細
│   └── examples/      # リクエスト・レスポンス例
├── docker/            # Docker設定
│   ├── docker-compose.yml        # 共通サービス
│   ├── docker-compose.dev.yml    # 開発環境
│   ├── postgres/      # PostgreSQL設定
│   └── redis/         # Redis設定
└── assets/            # 共通アセット
    ├── images/        # 画像ファイル
    ├── docs/          # ドキュメント用画像
    └── samples/       # サンプルファイル
```

## 🎯 使用目的

### database/
- 全実装で共通のデータベーススキーマ
- 統一されたサンプルデータ
- 各言語でのマイグレーション基準

### api/
- 全実装で統一されたAPI仕様
- エンドポイント・レスポンス形式の標準化
- 各言語実装での参照基準

### docker/
- PostgreSQL、Redis等の共通サービス
- 開発環境の統一
- 各実装での共通インフラ

### assets/
- UI/UX用の共通画像・アイコン
- ドキュメント用の図表
- サンプルファイル（小説、設定等）

## 🔧 使用方法

### データベース起動
```bash
cd shared/docker
docker-compose up -d postgres redis
```

### API仕様確認
```bash
# OpenAPI仕様をSwagger UIで確認
cd shared/api
swagger-ui-serve openapi.yaml
```

### 共通アセット利用
各実装から相対パスで参照：
```
../../shared/assets/images/logo.png
```

## 📝 更新ルール

1. **データベーススキーマ変更**: 全実装への影響を考慮
2. **API仕様変更**: 後方互換性の維持
3. **Docker設定変更**: 全実装での動作確認
4. **アセット追加**: 適切なディレクトリに分類

---

**管理責任**: プロジェクト全体  
**更新頻度**: 各実装フェーズで更新
