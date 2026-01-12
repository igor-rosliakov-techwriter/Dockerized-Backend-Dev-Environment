#!/usr/bin/env bash
set -euo pipefail

API_PORT="${API_PORT:-8000}"
BASE="http://localhost:${API_PORT}"

echo "[1/3] Waiting for /health ..."
for i in {1..30}; do
  if curl -fsS "${BASE}/health" >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

echo "[2/3] Health response:"
curl -fsS "${BASE}/health"
echo
echo

echo "[3/3] Creating a task:"
curl -fsS -X POST "${BASE}/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title":"smoke-test task"}'
echo
echo

echo "OK"
