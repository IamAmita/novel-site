# ===========================================
# TypeScript + Next.js 小説投稿サイト
# ローカル開発環境起動スクリプト（Windows PowerShell用）
# ===========================================

param(
    [switch]$Build,
    [switch]$Clean,
    [switch]$Stop,
    [switch]$Logs,
    [string]$Service = ""
)

$ErrorActionPreference = "Stop"

# スクリプトのディレクトリに移動
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$serviceDir = Split-Path -Parent $scriptDir
Set-Location $serviceDir

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Novel Site - Local Development" -ForegroundColor Cyan
Write-Host "  TypeScript + Next.js Version" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# -------------------------------------------
# Docker確認
# -------------------------------------------
function Test-Docker {
    $dockerInfo = docker info 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Docker is not running" -ForegroundColor Red
        Write-Host ""
        Write-Host "Docker Desktopを起動してください" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "✅ Docker is running" -ForegroundColor Green
}

# -------------------------------------------
# 環境変数ファイル確認
# -------------------------------------------
function Test-EnvFile {
    if (-not (Test-Path ".env.local")) {
        if (Test-Path "env.local.example") {
            Write-Host "⚠️  .env.local not found, creating from template..." -ForegroundColor Yellow
            Copy-Item "env.local.example" ".env.local"
            Write-Host "✅ Created .env.local" -ForegroundColor Green
        } else {
            Write-Host "❌ env.local.example not found" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "✅ .env.local exists" -ForegroundColor Green
    }
}

# -------------------------------------------
# 停止処理
# -------------------------------------------
if ($Stop) {
    Write-Host "Stopping containers..." -ForegroundColor Yellow
    docker-compose --env-file .env.local down
    Write-Host ""
    Write-Host "✅ All containers stopped" -ForegroundColor Green
    exit 0
}

# -------------------------------------------
# クリーンアップ処理
# -------------------------------------------
if ($Clean) {
    Write-Host "⚠️  This will remove all containers and volumes!" -ForegroundColor Red
    $confirm = Read-Host "Are you sure? (y/N)"
    if ($confirm -eq "y" -or $confirm -eq "Y") {
        Write-Host "Cleaning up..." -ForegroundColor Yellow
        docker-compose --env-file .env.local down -v --remove-orphans
        Write-Host "✅ Cleanup complete" -ForegroundColor Green
    } else {
        Write-Host "Cancelled" -ForegroundColor Yellow
    }
    exit 0
}

# -------------------------------------------
# ログ表示
# -------------------------------------------
if ($Logs) {
    if ($Service) {
        docker-compose --env-file .env.local logs -f $Service
    } else {
        docker-compose --env-file .env.local logs -f
    }
    exit 0
}

# -------------------------------------------
# メイン起動処理
# -------------------------------------------

Test-Docker
Write-Host ""
Test-EnvFile
Write-Host ""

# ビルドオプション
if ($Build) {
    Write-Host "Building containers..." -ForegroundColor Yellow
    docker-compose --env-file .env.local build --no-cache
    Write-Host ""
}

# コンテナ起動
Write-Host "Starting containers..." -ForegroundColor Yellow
Write-Host ""

if ($Service) {
    docker-compose --env-file .env.local up -d $Service
} else {
    docker-compose --env-file .env.local up -d
}

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Failed to start containers" -ForegroundColor Red
    exit 1
}

# ヘルスチェック待機
Write-Host ""
Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
& "$scriptDir\health-check.ps1" -Wait

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  🚀 Development environment is ready!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Frontend:  http://localhost:3000" -ForegroundColor Cyan
Write-Host "  Backend:   http://localhost:4000" -ForegroundColor Cyan
Write-Host "  GraphQL:   http://localhost:4000/graphql" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Commands:" -ForegroundColor Yellow
Write-Host "    .\scripts\start-local.ps1 -Logs      # View logs"
Write-Host "    .\scripts\start-local.ps1 -Stop      # Stop all"
Write-Host "    .\scripts\start-local.ps1 -Clean     # Remove all"
Write-Host "    .\scripts\health-check.ps1           # Check status"
Write-Host ""

