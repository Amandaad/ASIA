#!/usr/bin/env bash
set -euo pipefail
mkdir -p backups
docker compose exec -T db pg_dump -U "${POSTGRES_USER:-asia}" "${POSTGRES_DB:-studio_as}" > "backups/studio_as_$(date +%Y%m%d_%H%M%S).sql"
echo "Backup salvo em backups/"
