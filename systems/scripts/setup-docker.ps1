# Windows dev: arm64 via QEMU, mock GPIO, no camera
$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\..\..\backend"
docker compose build @args
