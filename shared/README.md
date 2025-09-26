# 共通リソース（shared）

5言語実装で共有するリソースを管理するディレクトリ。

## 📁 ディレクトリ構成

```
shared/
├── business/           # ビジネス要件（技術非依存）
│   ├── user-stories.md      # ユーザーストーリー
│   ├── business-rules.md    # ビジネスルール
│   ├── functional-scope.md  # 機能範囲定義
│   └── workflow-definitions.md # 業務フロー
├── domain/            # ドメイン概念（技術非依存）
│   ├── core-entities.md     # コアエンティティ概念
│   ├── entity-relationships.md # エンティティ関係
│   ├── business-constraints.md # ビジネス制約
│   └── domain-rules.md      # ドメインルール
├── design/            # UI/UXコンセプト（技術非依存）
│   ├── user-experience-flow.md # UX フロー
│   ├── screen-concepts.md   # 画面コンセプト
│   ├── design-principles.md # デザイン原則
│   └── accessibility-rules.md # アクセシビリティ
├── assets/            # 共通アセット
│   ├── images/        # ロゴ・アイコン・UI画像
│   ├── legal/         # 利用規約・プライバシーポリシー
│   └── samples/       # サンプルデータ・小説
└── quality/           # 品質要件（技術非依存）
    ├── performance-requirements.md # パフォーマンス要件
    ├── security-requirements.md    # セキュリティ要件
    └── testing-guidelines.md       # テスト指針
```

**重要**: API設計・データベース設計・Docker設定は各実装で独自管理
```

## 🎯 使用目的

### business/（ビジネス要件）
- 全実装で共通の「何を作るか」を定義
- ユーザーストーリー・ビジネスルール
- 技術に依存しない機能要件

### domain/（ドメイン概念）
- コアエンティティの概念定義
- エンティティ間の関係性
- ビジネス制約・ドメインルール

### design/（UI/UXコンセプト）
- ユーザー体験の基本コンセプト
- 画面構成・デザイン原則
- アクセシビリティ要件

### assets/（共通アセット）
- ロゴ・アイコン・UI素材
- 法的文書（利用規約等）
- サンプルデータ・小説

### quality/（品質要件）
- パフォーマンス・セキュリティ要件
- テスト指針・品質基準
- 技術に依存しない非機能要件

**注意**: 以下は各実装で独自管理
- API設計・エンドポイント構造
- データベース設計・スキーマ
- Docker設定・インフラ構成

## 🔧 使用方法

### ⚠️ Docker環境について（重要な変更）
**新方針**: 各実装が独立したDocker環境を持つため、shared/dockerは参考用のみ

```bash
# ❌ 旧方式（非推奨）
cd shared/docker
docker-compose up -d

# ✅ 新方式（推奨）
cd implementations/{language}/
docker-compose up -d  # 各実装で独立起動
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
