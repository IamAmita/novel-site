# TypeScript + Next.js Docker環境

小説投稿サイト TypeScript/Next.js版のDocker開発環境です。

---

## 📦 サービス構成

| サービス | イメージ | ポート | 説明 |
|----------|----------|--------|------|
| **frontend** | Node.js 20 Alpine | 3000 | Next.js 14 フロントエンド |
| **backend** | Node.js 20 Alpine | 4000 | Express + TypeScript API |
| **postgresql** | PostgreSQL 15 Alpine | 5432 | メインデータベース |
| **redis** | Redis 7 Alpine | 6379 | キャッシュ・セッション |

---

## 🚀 クイックスタート

### 前提条件

- Docker Desktop がインストール・起動済み
- PowerShell 5.1以上（Windows標準）

### 環境構築

```powershell
# 1. serviceディレクトリに移動
cd implementations/typescript-nextjs/service

# 2. 環境変数ファイルを作成
Copy-Item env.local.example .env.local

# 3. 起動スクリプトを実行
.\scripts\start-local.ps1
```

### 手動起動（スクリプトを使わない場合）

```powershell
# 環境変数ファイルを作成
Copy-Item env.local.example .env.local

# コンテナ起動
docker-compose --env-file .env.local up -d

# 状態確認
docker-compose ps
```

---

## 📱 アクセスURL

| サービス | URL |
|----------|-----|
| フロントエンド | http://localhost:3000 |
| バックエンドAPI | http://localhost:4000 |
| GraphQL Playground | http://localhost:4000/graphql |

---

## 🛠️ よく使うコマンド

### 起動・停止

```powershell
# 起動
.\scripts\start-local.ps1

# 停止
.\scripts\start-local.ps1 -Stop

# 再ビルドして起動
.\scripts\start-local.ps1 -Build

# 完全クリーンアップ（データも削除）
.\scripts\start-local.ps1 -Clean
```

### ログ確認

```powershell
# 全サービスのログ
.\scripts\start-local.ps1 -Logs

# 特定サービスのログ
.\scripts\start-local.ps1 -Logs -Service backend
.\scripts\start-local.ps1 -Logs -Service frontend

# docker-compose直接
docker-compose --env-file .env.local logs -f backend
```

### ヘルスチェック

```powershell
# サービス状態確認
.\scripts\health-check.ps1

# 詳細表示
.\scripts\health-check.ps1 -Verbose
```

### コンテナ内コマンド実行

```powershell
# Backend
docker-compose --env-file .env.local exec backend npm run test
docker-compose --env-file .env.local exec backend npx prisma studio

# Frontend
docker-compose --env-file .env.local exec frontend npm run build

# PostgreSQL
docker-compose --env-file .env.local exec postgresql psql -U novel_user -d novel_db

# Redis
docker-compose --env-file .env.local exec redis redis-cli
```

---

## 🗄️ データベース操作

### Prisma コマンド

```powershell
# マイグレーション作成
docker-compose --env-file .env.local exec backend npx prisma migrate dev --name init

# マイグレーション適用
docker-compose --env-file .env.local exec backend npx prisma migrate deploy

# Prisma Studio起動（GUI）
docker-compose --env-file .env.local exec backend npx prisma studio

# スキーマをDBにプッシュ（開発用）
docker-compose --env-file .env.local exec backend npx prisma db push

# クライアント再生成
docker-compose --env-file .env.local exec backend npx prisma generate
```

### 直接SQL実行

```powershell
# PostgreSQLに接続
docker-compose --env-file .env.local exec postgresql psql -U novel_user -d novel_db

# SQLファイル実行
docker-compose --env-file .env.local exec -T postgresql psql -U novel_user -d novel_db < your_script.sql
```

---

## 🔧 トラブルシューティング

### Docker Desktop未起動

```
Error: Cannot connect to the Docker daemon
```

**解決策**: Docker Desktopアプリケーションを起動してください。

### ポート競合

```
Error: Port 3000 is already in use
```

**解決策**: `.env.local`でポートを変更

```env
FRONTEND_PORT=3001
BACKEND_PORT=4001
```

### コンテナが起動しない

```powershell
# ログを確認
docker-compose --env-file .env.local logs backend

# コンテナを再ビルド
docker-compose --env-file .env.local build --no-cache backend
docker-compose --env-file .env.local up -d backend
```

### データベース接続エラー

```powershell
# PostgreSQLの状態確認
docker-compose --env-file .env.local exec postgresql pg_isready

# コンテナ再起動
docker-compose --env-file .env.local restart postgresql
```

### ボリュームのリセット

```powershell
# 全ボリューム削除（データ全消去）
docker-compose --env-file .env.local down -v

# 特定ボリュームのみ削除
docker volume rm novel-site_postgresql_data
```

---

## 📁 ディレクトリ構成

```
service/
├── docker-compose.yml      # コンテナ構成定義
├── Dockerfile              # マルチステージビルド定義
├── env.local.example       # 環境変数テンプレート
├── README.md               # このファイル
├── postgresql/
│   └── init/
│       └── 01-init-database.sql  # DB初期化スクリプト
└── scripts/
    ├── health-check.ps1    # ヘルスチェック
    └── start-local.ps1     # 起動スクリプト
```

---

## ⚠️ 注意事項

### 開発環境専用

この設定は**開発環境専用**です。本番環境では以下を変更してください：

- 強力なパスワード・シークレットキーの設定
- 適切なリソース制限の設定
- HTTPS対応
- ログ設定の調整

### Windows環境での注意

- PowerShellの実行ポリシー確認が必要な場合があります
- パス区切り文字は自動変換されます
- Docker Desktopのメモリ設定を確認してください（推奨: 4GB以上）

---

**作成日**: 2025年1月  
**対応OS**: Windows 10/11

