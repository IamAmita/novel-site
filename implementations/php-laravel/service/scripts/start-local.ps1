# Novel Site - ローカル環境起動スクリプト
# Windows PowerShell用

param(
    [switch]$Force,     # 強制再起動
    [switch]$Build,     # イメージ再ビルド
    [switch]$Clean      # データをクリアして起動
)

# スクリプトのディレクトリに移動
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
Set-Location $projectRoot

Write-Host "=== Novel Site ローカル環境起動 ===" -ForegroundColor Green
Write-Host "プロジェクトディレクトリ: $projectRoot" -ForegroundColor Yellow

# Docker Desktop起動確認
Write-Host "`n1. Docker Desktop起動確認..." -ForegroundColor Cyan
try {
    docker version | Out-Null
    Write-Host "✓ Docker Desktop起動中" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker Desktopが起動していません" -ForegroundColor Red
    Write-Host "Docker Desktopを起動してから再実行してください" -ForegroundColor Yellow
    exit 1
}

# 環境変数設定
Write-Host "`n2. 環境変数設定..." -ForegroundColor Cyan
$env:WWWUSER = "1000"
$env:WWWGROUP = "1000"
$env:MYSQL_EXTRA_OPTIONS = ""

Write-Host "✓ WWWUSER=$env:WWWUSER" -ForegroundColor Green
Write-Host "✓ WWWGROUP=$env:WWWGROUP" -ForegroundColor Green

# .envファイル確認・作成
Write-Host "`n3. 環境設定ファイル確認..." -ForegroundColor Cyan
if (-not (Test-Path ".env")) {
    if (Test-Path "service\env.local.example") {
        Copy-Item "service\env.local.example" ".env"
        Write-Host "✓ .envファイルを作成しました" -ForegroundColor Green
    } else {
        Write-Host "✗ service\env.local.exampleが見つかりません" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✓ .envファイル存在確認" -ForegroundColor Green
}

# クリーンモード
if ($Clean) {
    Write-Host "`n🧹 クリーンモード: データを削除しています..." -ForegroundColor Yellow
    docker-compose -f service\docker-compose.yml down -v
    docker volume rm novel-site-mysql novel-site-redis novel-site-elasticsearch -ErrorAction SilentlyContinue
}

# 強制再起動
if ($Force) {
    Write-Host "`n🔄 強制再起動モード..." -ForegroundColor Yellow
    docker-compose -f service\docker-compose.yml down
}

# イメージビルド
$buildArgs = @()
if ($Build) {
    Write-Host "`n🔨 イメージ再ビルドモード..." -ForegroundColor Yellow
    $buildArgs += "--build"
}

# サービス起動
Write-Host "`n4. Dockerサービス起動..." -ForegroundColor Cyan
try {
    docker-compose -f service\docker-compose.yml up -d @buildArgs
    Write-Host "✓ Dockerサービス起動完了" -ForegroundColor Green
} catch {
    Write-Host "✗ Dockerサービス起動失敗" -ForegroundColor Red
    Write-Host "エラー詳細: $_" -ForegroundColor Red
    exit 1
}

# サービス状態確認
Write-Host "`n5. サービス状態確認..." -ForegroundColor Cyan
Start-Sleep -Seconds 5
docker-compose -f service\docker-compose.yml ps

# ヘルスチェック
Write-Host "`n6. ヘルスチェック実行..." -ForegroundColor Cyan

# MySQL接続確認
Write-Host "MySQL接続確認..." -ForegroundColor Gray
$mysqlCheck = docker-compose -f service\docker-compose.yml exec -T mysql mysqladmin ping -h localhost -u sail -ppassword 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ MySQL接続OK" -ForegroundColor Green
} else {
    Write-Host "⚠ MySQL接続待機中..." -ForegroundColor Yellow
}

# Redis接続確認
Write-Host "Redis接続確認..." -ForegroundColor Gray
$redisCheck = docker-compose -f service\docker-compose.yml exec -T redis redis-cli ping 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Redis接続OK" -ForegroundColor Green
} else {
    Write-Host "⚠ Redis接続待機中..." -ForegroundColor Yellow
}

# Elasticsearch接続確認
Write-Host "Elasticsearch接続確認..." -ForegroundColor Gray
try {
    $esHealth = Invoke-RestMethod -Uri "http://localhost:9200/_cluster/health" -Method Get -TimeoutSec 5
    if ($esHealth.status -eq "green" -or $esHealth.status -eq "yellow") {
        Write-Host "✓ Elasticsearch接続OK" -ForegroundColor Green
    } else {
        Write-Host "⚠ Elasticsearchステータス: $($esHealth.status)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠ Elasticsearch接続待機中..." -ForegroundColor Yellow
}

# Laravelセットアップ確認
Write-Host "`n7. Laravelセットアップ確認..." -ForegroundColor Cyan

# Composer依存関係確認
if (-not (Test-Path "vendor")) {
    Write-Host "Composer依存関係をインストール中..." -ForegroundColor Gray
    docker-compose -f service\docker-compose.yml exec -T laravel.test composer install
}

# APP_KEY確認
$envContent = Get-Content ".env" -Raw
if ($envContent -match "APP_KEY=\s*$") {
    Write-Host "APP_KEYを生成中..." -ForegroundColor Gray
    docker-compose -f service\docker-compose.yml exec -T laravel.test php artisan key:generate
}

# マイグレーション実行確認
Write-Host "データベースマイグレーション確認..." -ForegroundColor Gray
docker-compose -f service\docker-compose.yml exec -T laravel.test php artisan migrate:status 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "マイグレーションを実行中..." -ForegroundColor Gray
    docker-compose -f service\docker-compose.yml exec -T laravel.test php artisan migrate --force
}

# 完了メッセージ
Write-Host "`n🎉 ローカル環境起動完了!" -ForegroundColor Green
Write-Host "`n=== アクセス情報 ===" -ForegroundColor Cyan
Write-Host "📱 Webアプリケーション: http://localhost" -ForegroundColor White
Write-Host "🔍 Elasticsearch: http://localhost:9200" -ForegroundColor White
Write-Host "`n=== 開発コマンド ===" -ForegroundColor Cyan
Write-Host "📂 コンテナに入る:" -ForegroundColor White
Write-Host "   docker-compose -f service\docker-compose.yml exec laravel.test bash" -ForegroundColor Gray
Write-Host "`n🎨 フロントエンド開発サーバー起動:" -ForegroundColor White
Write-Host "   docker-compose -f service\docker-compose.yml exec laravel.test npm run dev" -ForegroundColor Gray
Write-Host "`n🛠️ Artisanコマンド実行:" -ForegroundColor White
Write-Host "   docker-compose -f service\docker-compose.yml exec laravel.test php artisan [コマンド]" -ForegroundColor Gray

Write-Host "`n📋 使用方法:" -ForegroundColor Yellow
Write-Host "   -Force   : 強制再起動" -ForegroundColor Gray
Write-Host "   -Build   : イメージ再ビルド" -ForegroundColor Gray
Write-Host "   -Clean   : データクリア後起動" -ForegroundColor Gray
