#!/usr/bin/env bash
# Pi kiosk: KIOSK=1 ./run-frontend.sh
set -euo pipefail
cd "$(dirname "$0")/../../frontend"
npm run dev
