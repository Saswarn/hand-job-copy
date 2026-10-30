$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\..\..\backend"
uv sync --locked
