#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../backend"
# Mock GPIO unless set (Pi: GPIOZERO_PIN_FACTORY=lgpio). Camera: real V4L2 device; CAMERA_SOURCE=fake for none.
export GPIOZERO_PIN_FACTORY="${GPIOZERO_PIN_FACTORY:-mock}"
uv run uvicorn app.main:app --reload --port 8000
