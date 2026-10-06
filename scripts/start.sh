#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
[ -f .env ] || { cp .env.example .env; echo "Edite .env antes de iniciar."; exit 1; }
docker compose up -d --build
docker compose ps
