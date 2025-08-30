# TypeScript + Next.js 実装版

## 🎯 実装概要

- **言語**: TypeScript
- **バックエンドフレームワーク**: Node.js 20 + Express + TypeScript
- **フロントエンドフレームワーク**: Next.js 14 (App Router)
- **データベース**: PostgreSQL 15 + Prisma ORM
- **認証**: NextAuth.js + JWT
- **API**: RESTful + GraphQL (Apollo Server)

## 🏗️ アーキテクチャ

```
typescript-nextjs/
├── backend/               # Node.js + Express API
│   ├── src/
│   │   ├── routes/        # API ルート
│   │   ├── controllers/   # コントローラー
│   │   ├── services/      # ビジネスロジック
│   │   ├── models/        # データモデル
│   │   └── middleware/    # ミドルウェア
│   ├── prisma/           # Prisma設定・スキーマ
│   ├── package.json
│   └── tsconfig.json
├── frontend/             # Next.js アプリケーション
│   ├── app/              # App Router
│   ├── components/       # Reactコンポーネント
│   ├── lib/              # ユーティリティ
│   ├── types/            # TypeScript型定義
│   ├── package.json
│   └── next.config.js
├── docker-compose.yml
└── README.md
```

## 🚀 クイックスタート

### 前提条件
- Docker & Docker Compose
- Node.js 20+
- npm または yarn

### 環境構築
```bash
# リポジトリルートから
cd implementations/typescript-nextjs

# 共通サービス起動
cd ../../shared/docker
docker-compose up -d

# 開発環境起動
cd ../../implementations/typescript-nextjs
docker-compose up -d

# または手動起動
# バックエンド
cd backend
npm install
npx prisma generate
npx prisma migrate dev
npm run dev

# フロントエンド（別ターミナル）
cd frontend
npm install
npm run dev
```

## 📱 アクセス

- **フロントエンド**: http://localhost:3000
- **バックエンドAPI**: http://localhost:4000
- **GraphQL Playground**: http://localhost:4000/graphql
- **API ドキュメント**: http://localhost:4000/api-docs

## 🛠️ 開発

### バックエンド開発
```bash
cd backend

# Prisma スキーマ更新
npx prisma db push

# マイグレーション作成
npx prisma migrate dev --name init

# Prisma Studio起動
npx prisma studio

# テスト実行
npm run test

# 型チェック
npm run type-check
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

# Storybook起動
npm run storybook
```

## 📊 特徴・学習ポイント

### TypeScript フルスタックの特徴
- **型安全性**: フロントエンド・バックエンド間の型共有
- **Next.js App Router**: 最新のReactアーキテクチャ
- **Prisma ORM**: 型安全なデータベースアクセス
- **GraphQL**: 効率的なデータフェッチング
- **NextAuth.js**: 認証・認可の統合ソリューション

### 学習目標
- TypeScript による型安全なフルスタック開発
- Next.js App Router の活用
- Prisma による現代的なORM操作
- GraphQL API の設計・実装
- 統合された開発体験（DX）の理解

## 🧪 テスト

### バックエンドテスト
```bash
cd backend

# 単体テスト
npm run test

# 統合テスト
npm run test:integration

# E2Eテスト
npm run test:e2e

# カバレッジ測定
npm run test:coverage
```

### フロントエンドテスト
```bash
cd frontend

# 単体テスト
npm run test

# コンポーネントテスト
npm run test:components

# E2Eテスト
npm run test:e2e

# Visual Regression Test
npm run test:visual
```

## 📦 デプロイ

### Vercel デプロイ
```bash
# Vercel CLI でデプロイ
npx vercel

# 環境変数設定
npx vercel env add
```

### Docker デプロイ
```bash
# プロダクションビルド
docker-compose -f docker-compose.prod.yml build

# プロダクション起動
docker-compose -f docker-compose.prod.yml up -d
```

## 🔍 パフォーマンス

### 最適化ポイント
- Next.js の Image Optimization
- App Router による自動コード分割
- GraphQL によるオーバーフェッチング防止
- Prisma クエリ最適化
- Server Components の活用

### 測定コマンド
```bash
# Next.js Bundle Analyzer
npm run analyze

# Lighthouse CI
npm run lighthouse

# パフォーマンス測定
cd ../../tools/benchmark
./measure-typescript.sh
```

## 📚 参考資料

### 公式ドキュメント
- [Next.js Documentation](https://nextjs.org/docs)
- [Prisma Documentation](https://www.prisma.io/docs)
- [Apollo GraphQL](https://www.apollographql.com/docs)

### 学習リソース
- Next.js Learn Course
- TypeScript Handbook
- GraphQL Learning Resources

---

**開発状況**: ⏳ 予定  
**開始予定**: 2025年4月  
**完成予定**: 2025年6月
