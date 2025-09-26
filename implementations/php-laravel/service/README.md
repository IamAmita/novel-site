# Novel Site - ローカル環境セットアップ

小説投稿サイトのローカル開発環境を構築するためのサービス設定ファイル群です。

## 📋 前提条件

- **Docker Desktop**: Windows版をインストール済み
- **PowerShell**: Windows 10/11標準
- **Git**: ソースコード管理用

## 🚀 クイックスタート

### 1. 環境変数設定

PowerShellで以下の環境変数を設定:

```powershell
# PowerShellで実行（毎回必要）
$env:WWWUSER=1000
$env:WWWGROUP=1000
$env:MYSQL_EXTRA_OPTIONS=""
```

### 2. 環境設定ファイルのコピー

```powershell
# .envファイルを作成
Copy-Item "service\env.local.example" ".env"

# APP_KEYを生成（Laravel起動後に実行）
```

### 3. Docker環境起動

```powershell
# サービス起動
docker-compose -f service\docker-compose.yml up -d

# 起動確認
docker-compose -f service\docker-compose.yml ps
```

### 4. Laravel初期設定

```powershell
# コンテナに入る
docker-compose exec laravel.test bash

# Composer依存関係インストール
composer install

# APP_KEY生成
php artisan key:generate

# データベースマイグレーション
php artisan migrate

# フロントエンド依存関係インストール
npm install

# フロントエンド開発サーバー起動
npm run dev
```

## 🔧 サービス構成

### コアサービス

| サービス | ポート | 用途 | アクセスURL |
|----------|--------|------|-------------|
| **Laravel** | 80 | Webアプリケーション | http://localhost |
| **MySQL** | 3306 | メインデータベース | - |
| **Redis** | 6379 | キャッシュ・セッション・キュー | - |
| **Elasticsearch** | 9200 | 検索エンジン | http://localhost:9200 |

### データ永続化

以下のDockerボリュームでデータを永続化:

- `novel-site-mysql`: MySQLデータ
- `novel-site-redis`: Redisデータ  
- `novel-site-elasticsearch`: Elasticsearchデータ

## 🛠️ 開発コマンド

### 基本操作

```powershell
# サービス起動
docker-compose -f service\docker-compose.yml up -d

# サービス停止
docker-compose -f service\docker-compose.yml down

# ログ確認
docker-compose -f service\docker-compose.yml logs -f [サービス名]

# コンテナに入る
docker-compose exec laravel.test bash
```

### Laravel操作

```powershell
# Artisanコマンド実行
docker-compose exec laravel.test php artisan [コマンド]

# Composer操作
docker-compose exec laravel.test composer [コマンド]

# NPM操作
docker-compose exec laravel.test npm [コマンド]
```

## 🔍 ヘルスチェック

各サービスの動作確認:

```powershell
# MySQL接続確認
docker-compose exec mysql mysql -u sail -ppassword -e "SELECT 1"

# Redis接続確認
docker-compose exec redis redis-cli ping

# Elasticsearch接続確認
curl http://localhost:9200/_cluster/health
```

## 🚨 トラブルシューティング

### よくある問題

#### 1. WSLエラー
```
エラー: CreateProcessParseCommon:1008: getpwuid(0) failed 2
```
**解決策**: Laravel Sailを使わずdocker-composeを直接使用

#### 2. 環境変数エラー
```
warning: The "WWWUSER" variable is not set
```
**解決策**: PowerShellで環境変数を再設定
```powershell
$env:WWWUSER=1000; $env:WWWGROUP=1000
```

#### 3. ポート競合エラー
```
Error: Port 3306 is already in use
```
**解決策**: .envファイルでポート変更
```
FORWARD_DB_PORT=3307
```

#### 4. Elasticsearch メモリ不足
```
max virtual memory areas vm.max_map_count [65530] is too low
```
**解決策**: Docker Desktop設定でメモリを4GB以上に設定

### 完全リセット

```powershell
# 全サービス停止・削除
docker-compose -f service\docker-compose.yml down -v

# イメージ削除
docker-compose -f service\docker-compose.yml down --rmi all

# ボリューム削除（データも削除されます）
docker volume rm novel-site-mysql novel-site-redis novel-site-elasticsearch
```

## 📂 ファイル構成

```
service/
├── docker-compose.yml      # Docker構成定義
├── Dockerfile             # カスタムLaravelイメージ
├── env.local.example       # 環境変数テンプレート
├── README.md              # このファイル
├── scripts/               # 起動スクリプト群
│   ├── start-local.ps1    # Windows起動スクリプト
│   └── health-check.ps1   # ヘルスチェックスクリプト
├── mysql/                 # MySQL設定
│   └── init/              # 初期化スクリプト
└── elasticsearch/         # Elasticsearch設定
    └── config/            # 設定ファイル
```

## 🎯 開発フロー

### 日常の開発作業

1. **開発開始**
```powershell
# 環境変数設定 + サービス起動
.\service\scripts\start-local.ps1

# 開発サーバー起動
docker-compose exec laravel.test npm run dev
```

2. **開発作業**
- ソースコード編集
- ブラウザで http://localhost でテスト

3. **開発終了**
```powershell
# サービス停止
docker-compose -f service\docker-compose.yml down
```

### 機能別テスト

- **認証機能**: http://localhost/register
- **検索機能**: http://localhost:9200/_cat/indices
- **キャッシュ**: Redis CLI で確認

## 📚 参考情報

### 技術スタック
- **Backend**: PHP 8.4 + Laravel 12
- **Frontend**: Vue.js 3 + Inertia.js + Tailwind CSS
- **Database**: MySQL 8.0
- **Search**: Elasticsearch 8.11.0
- **Cache**: Redis Alpine

### 関連ドキュメント
- [Laravel公式ドキュメント](https://laravel.com/docs)
- [Vue.js 3 ガイド](https://v3.vuejs.org/guide/)
- [Inertia.js ドキュメント](https://inertiajs.com/)
- [Docker Compose リファレンス](https://docs.docker.com/compose/)

---

**更新日**: 2025年9月26日  
**環境**: Windows 10/11 + Docker Desktop
