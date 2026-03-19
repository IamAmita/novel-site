# health-check.ps1
# 各サービスの起動状態を確認するスクリプト (Windows PowerShell)

function Check-Service {
    param([string]$Name, [string]$Url)
    try {
        $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
        Write-Host "  [OK] $Name ($Url)" -ForegroundColor Green
    } catch {
        Write-Host "  [NG] $Name ($Url)" -ForegroundColor Red
    }
}

Write-Host "Health Check..." -ForegroundColor Cyan
Check-Service "Frontend" "http://localhost:3000"
Check-Service "Backend"  "http://localhost:8000"
