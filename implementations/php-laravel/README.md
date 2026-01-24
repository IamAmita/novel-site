# Novel Site - Docker開発環境

小説投稿サイトのローカル開発環境です。Laravel + MySQL のシンプルな構成で動作します。

## 📋 前提条件

- **Docker Desktop**: Windows版インストール済み
- **Git**: ソースコード管理用

## 🚀 クイックスタート

### 1. 環境変数の設定

PowerShellで環境変数を設定します（毎回起動時に必要）:

```powershell
$env:WWWUSER=1000
$env:WWWGROUP=1000
```

### 2. 環境ファイルのコピー

```powershell
# serviceディレクトリから.envファイルをコピー
Copy-Item "env.local.example" ".env"
```

### 3. Docker起動

```powershell
# コンテナ起動
docker-compose up -d

# 起動確認
docker-compose ps
```

### 4. Laravel初期設定

```powershell
# Laravelコンテナに接続
docker-compose exec laravel bash

# Composer依存関係インストール
composer install

# アプリケーションキー生成
php artisan key:generate

# データベースマイグレーション実行
php artisan migrate

# フロントエンド依存関係インストール
npm install

# 開発サーバー起動
npm run dev
```

### 5. アクセス

ブラウザで以下にアクセス:
- **アプリケーション**: http://localhost

## 🔧 サービス構成

| サービス | ポート | 用途 |
|----------|--------|------|
| **Laravel** | 80 | Webアプリケーション |
| **MySQL** | 3306 | データベース |

## 📂 ファイル構成

```
service/
├── docker-compose.yml     # Docker構成定義
├── Dockerfile            # Laravelイメージ
├── env.local.example     # 環境変数テンプレート
├── php.ini              # PHP設定
├── start-container      # コンテナ起動スクリプト
├── supervisord.conf     # プロセス管理設定
└── README.md           # このファイル
```

## 🛠️ よく使うコマンド

### Docker操作

```powershell
# 起動
docker-compose up -d

# 停止
docker-compose down

# ログ確認
docker-compose logs -f laravel

# コンテナに接続
docker-compose exec laravel bash
```

### Laravel操作（コンテナ内）

```powershell
# Artisanコマンド
php artisan migrate
php artisan db:seed
php artisan cache:clear

# Composer操作
composer install
composer update

# NPM操作
npm install
npm run dev
npm run build
```

## 🚨 トラブルシューティング

### よくある問題

#### 1. 環境変数エラー

```
warning: The "WWWUSER" variable is not set
```

**解決策**: 
```powershell
$env:WWWUSER=1000
$env:WWWGROUP=1000
docker-compose up -d
```

#### 2. ポート競合エラー

```
Error: Port 3306 is already in use
```

**解決策**: .envファイルでポート変更
```
FORWARD_DB_PORT=3307
```

#### 3. Docker Desktop未起動

```
Error: Cannot connect to the Docker daemon
```

**解決策**: Docker Desktopを起動してから再実行

#### 4. 権限エラー

```
Permission denied
```

**解決策**: コンテナ内で権限修正
```bash
docker-compose exec laravel bash
chown -R sail:sail /var/www/html
chmod -R 755 /var/www/html
```

### 完全リセット

```powershell
# サービス停止・削除
docker-compose down -v

# イメージ削除
docker-compose down --rmi all

# ボリューム削除（データも削除されます）
docker volume rm novel-site-mysql
```

## 📚 技術スタック

- **Backend**: PHP 8.4 + Laravel 12
- **Database**: MySQL 8.0
- **Frontend**: Vue.js 3 + Inertia.js + Tailwind CSS
- **Container**: Docker + Docker Compose

## 🎯 開発フロー

### 日常の開発作業

1. **開発開始**
   ```powershell
   $env:WWWUSER=1000; $env:WWWGROUP=1000
   docker-compose up -d
   ```

2. **開発作業**
   - コードの編集
   - http://localhost でテスト

3. **開発終了**
   ```powershell
   docker-compose down
   ```

## 💡 ヒント

### PowerShellエイリアス設定（任意）

開発効率化のため、PowerShellプロファイルに追加:

```powershell
# エイリアス設定
function dc { docker-compose @args }
function dcup { docker-compose up -d }
function dcdown { docker-compose down }
function dcexec { docker-compose exec laravel @args }
```

### よく使うコマンド

```powershell
# マイグレーション実行
docker-compose exec laravel php artisan migrate

# キャッシュクリア
docker-compose exec laravel php artisan cache:clear

# データベースリセット
docker-compose exec laravel php artisan migrate:fresh --seed
```

---

**更新日**: 2026年1月24日  
**環境**: Windows 10/11 + Docker Desktop
