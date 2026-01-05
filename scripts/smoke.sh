#!/usr/bin/env bash
set -euo pipefail

API_URL="http://localhost:8000/health"

echo "[smoke] checking API health: ${API_URL}"
curl -fsS "${API_URL}" >/dev/null
echo "[smoke] ok"
