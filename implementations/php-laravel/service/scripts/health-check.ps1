# Novel Site - ヘルスチェックスクリプト
# ローカル環境の各サービス状態を確認

param(
    [switch]$Detailed,  # 詳細な情報を表示
    [switch]$Json       # JSON形式で出力
)

# スクリプトのディレクトリに移動
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
Set-Location $projectRoot

# ヘルスチェック結果を格納するオブジェクト
$healthStatus = @{
    timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    services = @{}
}

Write-Host "=== Novel Site ヘルスチェック ===" -ForegroundColor Green
Write-Host "実行時刻: $($healthStatus.timestamp)" -ForegroundColor Yellow

# Docker状態確認
Write-Host "`n🐳 Docker状態確認..." -ForegroundColor Cyan
try {
    docker version | Out-Null
    $healthStatus.services.docker = @{
        status = "healthy"
        message = "Docker Desktop起動中"
    }
    Write-Host "✓ Docker Desktop起動中" -ForegroundColor Green
} catch {
    $healthStatus.services.docker = @{
        status = "error"
        message = "Docker Desktopが起動していません"
    }
    Write-Host "✗ Docker Desktopが起動していません" -ForegroundColor Red
}

# Docker Composeサービス状態確認
Write-Host "`n📋 Dockerサービス状態..." -ForegroundColor Cyan
try {
    $composePs = docker-compose -f service\docker-compose.yml ps --format json | ConvertFrom-Json
    
    $services = @("laravel.test", "mysql", "redis", "elasticsearch")
    foreach ($serviceName in $services) {
        $service = $composePs | Where-Object { $_.Service -eq $serviceName }
        
        if ($service) {
            $status = if ($service.State -eq "running") { "healthy" } else { "error" }
            $healthStatus.services.$serviceName = @{
                status = $status
                state = $service.State
                ports = $service.Publishers
            }
            
            $statusIcon = if ($status -eq "healthy") { "✓" } else { "✗" }
            $statusColor = if ($status -eq "healthy") { "Green" } else { "Red" }
            Write-Host "$statusIcon $serviceName : $($service.State)" -ForegroundColor $statusColor
            
            if ($Detailed -and $service.Publishers) {
                Write-Host "  ポート: $($service.Publishers)" -ForegroundColor Gray
            }
        } else {
            $healthStatus.services.$serviceName = @{
                status = "not_found"
                message = "サービスが見つかりません"
            }
            Write-Host "✗ $serviceName : サービスが見つかりません" -ForegroundColor Red
        }
    }
} catch {
    Write-Host "✗ Docker Composeサービス確認エラー: $_" -ForegroundColor Red
}

# 詳細ヘルスチェック
if ($healthStatus.services.docker.status -eq "healthy") {
    Write-Host "`n🔍 詳細ヘルスチェック..." -ForegroundColor Cyan
    
    # MySQL接続確認
    Write-Host "MySQL接続テスト..." -ForegroundColor Gray
    try {
        $mysqlResult = docker-compose -f service\docker-compose.yml exec -T mysql mysqladmin ping -h localhost -u sail -ppassword 2>$null
        if ($LASTEXITCODE -eq 0) {
            $healthStatus.services.mysql_connection = @{
                status = "healthy"
                message = "接続成功"
            }
            Write-Host "✓ MySQL接続成功" -ForegroundColor Green
            
            if ($Detailed) {
                # データベース一覧取得
                $databases = docker-compose -f service\docker-compose.yml exec -T mysql mysql -u sail -ppassword -e "SHOW DATABASES;" 2>$null
                Write-Host "  データベース一覧:" -ForegroundColor Gray
                $databases -split "`n" | Select-Object -Skip 1 | ForEach-Object {
                    if ($_.Trim()) { Write-Host "    $_" -ForegroundColor DarkGray }
                }
            }
        } else {
            $healthStatus.services.mysql_connection = @{
                status = "error"
                message = "接続失敗"
            }
            Write-Host "✗ MySQL接続失敗" -ForegroundColor Red
        }
    } catch {
        Write-Host "✗ MySQL接続テストエラー: $_" -ForegroundColor Red
    }
    
    # Redis接続確認
    Write-Host "Redis接続テスト..." -ForegroundColor Gray
    try {
        $redisResult = docker-compose -f service\docker-compose.yml exec -T redis redis-cli ping 2>$null
        if ($LASTEXITCODE -eq 0) {
            $healthStatus.services.redis_connection = @{
                status = "healthy"
                message = "接続成功"
                response = $redisResult.Trim()
            }
            Write-Host "✓ Redis接続成功 (応答: $($redisResult.Trim()))" -ForegroundColor Green
            
            if ($Detailed) {
                # Redis情報取得
                $redisInfo = docker-compose -f service\docker-compose.yml exec -T redis redis-cli info memory 2>$null
                $memoryUsage = ($redisInfo -split "`n" | Where-Object { $_ -match "used_memory_human" }) -replace "used_memory_human:", ""
                if ($memoryUsage) {
                    Write-Host "  メモリ使用量: $($memoryUsage.Trim())" -ForegroundColor Gray
                }
            }
        } else {
            $healthStatus.services.redis_connection = @{
                status = "error"
                message = "接続失敗"
            }
            Write-Host "✗ Redis接続失敗" -ForegroundColor Red
        }
    } catch {
        Write-Host "✗ Redis接続テストエラー: $_" -ForegroundColor Red
    }
    
    # Elasticsearch接続確認
    Write-Host "Elasticsearch接続テスト..." -ForegroundColor Gray
    try {
        $esHealth = Invoke-RestMethod -Uri "http://localhost:9200/_cluster/health" -Method Get -TimeoutSec 10
        $healthStatus.services.elasticsearch_connection = @{
            status = if ($esHealth.status -eq "green" -or $esHealth.status -eq "yellow") { "healthy" } else { "warning" }
            cluster_status = $esHealth.status
            nodes = $esHealth.number_of_nodes
            indices = $esHealth.active_primary_shards
        }
        
        $statusIcon = if ($esHealth.status -eq "green") { "✓" } elseif ($esHealth.status -eq "yellow") { "⚠" } else { "✗" }
        $statusColor = if ($esHealth.status -eq "green") { "Green" } elseif ($esHealth.status -eq "yellow") { "Yellow" } else { "Red" }
        Write-Host "$statusIcon Elasticsearch接続成功 (ステータス: $($esHealth.status))" -ForegroundColor $statusColor
        
        if ($Detailed) {
            Write-Host "  ノード数: $($esHealth.number_of_nodes)" -ForegroundColor Gray
            Write-Host "  アクティブシャード: $($esHealth.active_primary_shards)" -ForegroundColor Gray
            
            # インデックス一覧取得
            try {
                $indices = Invoke-RestMethod -Uri "http://localhost:9200/_cat/indices?format=json" -Method Get -TimeoutSec 5
                if ($indices.Count -gt 0) {
                    Write-Host "  インデックス:" -ForegroundColor Gray
                    $indices | ForEach-Object { Write-Host "    $($_.index) ($($_.status))" -ForegroundColor DarkGray }
                }
            } catch {
                Write-Host "  インデックス情報取得不可" -ForegroundColor DarkGray
            }
        }
    } catch {
        $healthStatus.services.elasticsearch_connection = @{
            status = "error"
            message = "接続失敗: $_"
        }
        Write-Host "✗ Elasticsearch接続失敗: $_" -ForegroundColor Red
    }
    
    # Laravel アプリケーション確認
    if ($healthStatus.services."laravel.test".status -eq "healthy") {
        Write-Host "Laravel アプリケーション確認..." -ForegroundColor Gray
        try {
            $laravelCheck = Invoke-WebRequest -Uri "http://localhost" -Method Get -TimeoutSec 10 -UseBasicParsing
            $healthStatus.services.laravel_app = @{
                status = "healthy"
                http_status = $laravelCheck.StatusCode
                response_time = "確認済み"
            }
            Write-Host "✓ Laravel アプリケーション応答 (HTTP $($laravelCheck.StatusCode))" -ForegroundColor Green
        } catch {
            $healthStatus.services.laravel_app = @{
                status = "error"
                message = "HTTP応答エラー: $_"
            }
            Write-Host "✗ Laravel アプリケーション応答なし: $_" -ForegroundColor Red
        }
    }
}

# 結果サマリー
Write-Host "`n📊 ヘルスチェック結果サマリー" -ForegroundColor Cyan
$totalServices = $healthStatus.services.Count
$healthyServices = ($healthStatus.services.Values | Where-Object { $_.status -eq "healthy" }).Count
$errorServices = ($healthStatus.services.Values | Where-Object { $_.status -eq "error" }).Count
$warningServices = ($healthStatus.services.Values | Where-Object { $_.status -eq "warning" }).Count

Write-Host "正常: $healthyServices / $totalServices" -ForegroundColor Green
if ($warningServices -gt 0) {
    Write-Host "警告: $warningServices" -ForegroundColor Yellow
}
if ($errorServices -gt 0) {
    Write-Host "エラー: $errorServices" -ForegroundColor Red
}

# JSON出力
if ($Json) {
    Write-Host "`n📄 JSON出力:" -ForegroundColor Cyan
    $healthStatus | ConvertTo-Json -Depth 3
}

# 終了コード設定
if ($errorServices -gt 0) {
    exit 1
} elseif ($warningServices -gt 0) {
    exit 2
} else {
    exit 0
}
