# start-local.ps1
# Python Django 環境をローカルで起動するスクリプト (Windows PowerShell)

param(
    [switch]$Build,
    [switch]$Down
)

$ComposeFile = Join-Path $PSScriptRoot "..\..\docker-compose.yml"

if ($Down) {
    Write-Host "Stopping containers..." -ForegroundColor Yellow
    docker compose -f $ComposeFile down
    exit 0
}

if ($Build) {
    Write-Host "Building and starting containers..." -ForegroundColor Cyan
    docker compose -f $ComposeFile up --build -d
} else {
    Write-Host "Starting containers..." -ForegroundColor Cyan
    docker compose -f $ComposeFile up -d
}

Write-Host ""
Write-Host "Services:" -ForegroundColor Green
Write-Host "  Frontend : http://localhost:3000"
Write-Host "  Backend  : http://localhost:8000"
Write-Host "  Admin    : http://localhost:8000/admin"
Write-Host ""
Write-Host "Logs: docker compose -f $ComposeFile logs -f"
