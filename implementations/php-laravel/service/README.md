# 小説投稿サイト - Docker開発環境

Laravel 12 + Vue.js + Inertia.js + Elasticsearch による小説投稿サイトの**開発環境**

## 🐳 構成

### サービス
- **novel-app**: Laravel 12 + PHP 8.4 + Nginx + Xdebug
- **mysql**: MySQL 8.0 (データベース)
- **redis**: Redis 7 (キャッシュ・セッション・キュー)
- **elasticsearch**: Elasticsearch 8.11.0 (検索エンジン)

### 🛠️ 開発環境の特徴
- **ホットリロード**: Viteによるリアルタイム更新
- **デバッグ支援**: Xdebug + エラー表示有効
- **ボリュームマウント**: ソースコードの即座反映
- **開発依存関係**: Laravel telescope、debugbar等含む
- **ポート公開**: Laravel(80), Vite(5173)

### 技術スタック
- PHP 8.4 + Laravel 12
- Vue.js 3 + Inertia.js + Vite + Tailwind CSS
- MySQL 8.0 (utf8mb4対応)
- Redis 7 (キャッシュ・セッション・キュー統合)
- Elasticsearch 8.11.0 (日本語検索対応)
- Nginx (Webサーバー)
- Supervisor (プロセス管理)

## 🚀 起動方法

### 前提条件
- Docker Desktop インストール済み
- 4GB以上のメモリ割り当て

### Windows環境
```powershell
# 環境変数設定
$env:WWWUSER=1000
$env:WWWGROUP=1000

# Docker Compose起動
docker-compose up -d

# 起動確認
docker-compose ps
```

### Linux/Mac環境
```bash
# Docker Compose起動
docker-compose up -d

# 起動確認
docker-compose ps
```

## 📦 サービス詳細

### Laravel アプリケーション (novel-app)
- **ポート**: 80
- **ログ**: `/var/log/nginx/`, `/var/log/supervisor/`
- **機能**: 
  - PHP 8.4 + Laravel 12
  - Vue.js + Inertia.js (フロントエンド)
  - Intervention Image (画像処理)
  - Laravel Scout + Elasticsearch (検索)

### MySQL (mysql)
- **ポート**: 3306
- **データベース**: `novel_site`
- **ユーザー**: `novel_user` / `novel_pass`
- **文字セット**: utf8mb4 (日本語対応)

### Redis (redis)
- **ポート**: 6379
- **用途**: キャッシュ・セッション・キュー統合

### Elasticsearch (elasticsearch)
- **ポート**: 9200
- **設定**: 日本語解析対応
- **メモリ**: 1GB割り当て

## 🔧 開発用コマンド

### Laravel コマンド
```bash
# コンテナ内でコマンド実行
docker-compose exec novel-app php artisan migrate
docker-compose exec novel-app php artisan serve
docker-compose exec novel-app composer install
```

### フロントエンド
```bash
# Vue.js + Vite開発サーバー
docker-compose exec novel-app npm run dev

# ビルド
docker-compose exec novel-app npm run build
```

### データベース
```bash
# MySQL接続
docker-compose exec mysql mysql -u novel_user -p novel_site

# マイグレーション
docker-compose exec novel-app php artisan migrate

# シーダー実行
docker-compose exec novel-app php artisan db:seed
```

### Elasticsearch
```bash
# インデックス作成
docker-compose exec novel-app php artisan scout:import "App\Models\Novel"

# 検索テスト
curl "http://localhost:9200/novels/_search?q=title:恋愛"
```

## 📁 ディレクトリ構造

```
service/
├── Dockerfile              # Laravel アプリケーション
├── docker-compose.yml      # Docker Compose設定
├── php.ini                 # PHP設定
├── nginx.conf              # Nginx基本設定
├── site.conf               # サイト設定
├── supervisord.conf        # プロセス管理設定
├── mysql/
│   └── init.sql           # MySQL初期化
├── storage/               # Laravel ストレージ
├── logs/                  # ログファイル
└── README.md              # このファイル
```

## 🐛 トラブルシューティング

### よくある問題

#### 1. メモリ不足
```
Elasticsearch: max virtual memory areas vm.max_map_count is too low
```
**解決策**: Docker Desktop設定でメモリを4GB以上に設定

#### 2. ポート競合
```
Error: Port 80 is already in use
```
**解決策**: `docker-compose.yml` でポート番号変更

#### 3. 権限エラー
```
Permission denied: /var/www/html/storage
```
**解決策**: 
```bash
docker-compose exec novel-app chown -R www-data:www-data /var/www/html/storage
```

### ログ確認
```bash
# アプリケーションログ
docker-compose logs novel-app

# 全サービスログ
docker-compose logs

# リアルタイムログ
docker-compose logs -f novel-app
```

## 🔄 更新・メンテナンス

### イメージ更新
```bash
# イメージ再ビルド
docker-compose build --no-cache

# 再起動
docker-compose down && docker-compose up -d
```

### データバックアップ
```bash
# MySQL バックアップ
docker-compose exec mysql mysqldump -u novel_user -p novel_site > backup.sql

# Elasticsearch バックアップ
curl -X PUT "localhost:9200/_snapshot/backup" -H 'Content-Type: application/json' -d'{"type": "fs", "settings": {"location": "/backup"}}'
```

---

**作成日**: 2025年1月  
**対象**: 小説投稿サイト開発環境
