$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\..\..\backend"
# Windows has no GPIO or V4L2 camera: mock pins + fake frames unless already set.
if (-not $env:GPIOZERO_PIN_FACTORY) { $env:GPIOZERO_PIN_FACTORY = "mock" }
if (-not $env:CAMERA_SOURCE) { $env:CAMERA_SOURCE = "fake" }
uv run uvicorn app.main:app --reload --port 8000
