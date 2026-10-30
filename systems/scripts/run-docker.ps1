$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\..\..\backend"
docker compose up -d
docker compose ps
