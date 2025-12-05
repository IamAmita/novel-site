# ===========================================
# TypeScript + Next.js 小説投稿サイト
# ヘルスチェックスクリプト（Windows PowerShell用）
# ===========================================

param(
    [switch]$Verbose,
    [switch]$Wait
)

$ErrorActionPreference = "Continue"

# 色付き出力用関数
function Write-Status {
    param(
        [string]$Service,
        [string]$Status,
        [string]$Message = ""
    )
    
    $icon = switch ($Status) {
        "OK"      { "✅" }
        "FAIL"    { "❌" }
        "WAIT"    { "⏳" }
        default   { "ℹ️" }
    }
    
    $color = switch ($Status) {
        "OK"      { "Green" }
        "FAIL"    { "Red" }
        "WAIT"    { "Yellow" }
        default   { "White" }
    }
    
    Write-Host "$icon " -NoNewline
    Write-Host "$Service" -ForegroundColor $color -NoNewline
    if ($Message) {
        Write-Host " - $Message"
    } else {
        Write-Host ""
    }
}

# -------------------------------------------
# サービスチェック関数
# -------------------------------------------

function Test-PostgreSQL {
    try {
        $result = docker exec novel-ts-postgresql pg_isready -U novel_user -d novel_db 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Status "PostgreSQL" "OK" "accepting connections"
            return $true
        }
    } catch {}
    Write-Status "PostgreSQL" "FAIL" "not ready"
    return $false
}

function Test-Redis {
    try {
        $result = docker exec novel-ts-redis redis-cli ping 2>&1
        if ($result -eq "PONG") {
            Write-Status "Redis" "OK" "responding"
            return $true
        }
    } catch {}
    Write-Status "Redis" "FAIL" "not responding"
    return $false
}

function Test-Backend {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:4000/health" -TimeoutSec 5 -UseBasicParsing -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Write-Status "Backend API" "OK" "healthy"
            return $true
        }
    } catch {}
    Write-Status "Backend API" "FAIL" "not responding"
    return $false
}

function Test-Frontend {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 5 -UseBasicParsing -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Write-Status "Frontend" "OK" "healthy"
            return $true
        }
    } catch {}
    Write-Status "Frontend" "FAIL" "not responding"
    return $false
}

# -------------------------------------------
# メイン処理
# -------------------------------------------

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Novel Site - Health Check" -ForegroundColor Cyan
Write-Host "  TypeScript + Next.js Version" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Docker確認
$dockerRunning = docker info 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Status "Docker" "FAIL" "Docker is not running"
    Write-Host ""
    Write-Host "Docker Desktopを起動してください" -ForegroundColor Yellow
    exit 1
}
Write-Status "Docker" "OK" "running"

Write-Host ""
Write-Host "--- Services Status ---" -ForegroundColor Yellow
Write-Host ""

# 待機モード
if ($Wait) {
    $maxRetries = 30
    $retryCount = 0
    
    Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
    Write-Host ""
    
    while ($retryCount -lt $maxRetries) {
        $pgOk = Test-PostgreSQL
        $redisOk = Test-Redis
        
        if ($pgOk -and $redisOk) {
            Write-Host ""
            Write-Host "Infrastructure services are ready!" -ForegroundColor Green
            break
        }
        
        $retryCount++
        Write-Host "Retry $retryCount/$maxRetries..." -ForegroundColor Gray
        Start-Sleep -Seconds 2
    }
    
    if ($retryCount -ge $maxRetries) {
        Write-Host ""
        Write-Host "Timeout waiting for services" -ForegroundColor Red
        exit 1
    }
} else {
    # 通常チェック
    Test-PostgreSQL | Out-Null
    Test-Redis | Out-Null
    Test-Backend | Out-Null
    Test-Frontend | Out-Null
}

Write-Host ""
Write-Host "--- Container Status ---" -ForegroundColor Yellow
Write-Host ""

# コンテナ状態表示
docker-compose ps 2>&1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

