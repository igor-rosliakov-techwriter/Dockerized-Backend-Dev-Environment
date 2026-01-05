#!/usr/bin/env bash
set -euo pipefail

echo "[reset] stopping and removing containers + volumes..."
docker compose down -v
echo "[reset] done"
