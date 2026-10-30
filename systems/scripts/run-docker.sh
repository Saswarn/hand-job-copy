#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../../backend"
docker compose -f docker-compose.yml -f docker-compose.pi.yml up -d
docker compose ps
