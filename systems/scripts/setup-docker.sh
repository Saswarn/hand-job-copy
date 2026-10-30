#!/usr/bin/env bash
# Pi: real camera + GPIO (docker-compose.pi.yml)
set -euo pipefail
cd "$(dirname "$0")/../../backend"
docker compose -f docker-compose.yml -f docker-compose.pi.yml build "$@"
