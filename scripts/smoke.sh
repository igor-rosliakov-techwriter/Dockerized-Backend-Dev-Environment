#!/usr/bin/env bash
set -euo pipefail

API_PORT="${API_PORT:-8000}"
BASE="http://localhost:${API_PORT}"

# --- helpers -------------------------------------------------

pick_python() {
  if command -v python >/dev/null 2>&1; then
    echo "python"
    return 0
  fi
  if command -v python3 >/dev/null 2>&1; then
    echo "python3"
    return 0
  fi
  echo ""
}

PYBIN="$(pick_python)"

json_get() {
  # usage: json_get "$json" "id"
  local json="$1"
  local key="$2"

  if [[ -n "${PYBIN}" ]]; then
    JSON_INPUT="$json" KEY="$key" "$PYBIN" - <<'PY'
import json, os
obj = json.loads(os.environ["JSON_INPUT"])
key = os.environ["KEY"]
print(obj[key])
PY
  else
    # fallback: run python inside api container (guaranteed to exist)
    JSON_INPUT="$json" KEY="$key" docker compose exec -T api python - <<'PY'
import json, os
obj = json.loads(os.environ["JSON_INPUT"])
key = os.environ["KEY"]
print(obj[key])
PY
  fi
}

dump_diagnostics() {
  echo
  echo "========== DIAGNOSTICS =========="
  echo
  echo "--- docker compose ps ---"
  docker compose ps || true
  echo
  echo "--- worker logs (last 100 lines) ---"
  docker compose logs --tail=100 worker || true
  echo
  echo "--- api logs (last 100 lines) ---"
  docker compose logs --tail=100 api || true
  echo
  echo "================================="
}

# --- smoke ---------------------------------------------------

echo "[1/4] Waiting for /health ..."
for i in {1..30}; do
  if curl -fsS "${BASE}/health" >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

echo "[2/4] Health response:"
curl -fsS "${BASE}/health"
echo
echo

echo "[3/4] Creating a task:"
CREATE_JSON="$(curl -fsS -X POST "${BASE}/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title":"smoke-test task"}')"

echo "${CREATE_JSON}"
echo

TASK_ID="$(json_get "${CREATE_JSON}" "id")"
echo "Task id: ${TASK_ID}"
echo

echo "[4/4] Waiting for task to be processed (queued -> processing -> done) ..."

TASK_JSON=""
for i in {1..30}; do
  TASK_JSON="$(curl -fsS "${BASE}/tasks/${TASK_ID}")"
  STATUS="$(json_get "${TASK_JSON}" "status")"

  echo "  - status: ${STATUS}"

  if [[ "${STATUS}" == "done" ]]; then
    echo
    echo "OK: task processed end-to-end"
    exit 0
  fi

  if [[ "${STATUS}" == "failed" ]]; then
    echo
    echo "FAIL: task ended as failed"
    echo "Last response:"
    echo "${TASK_JSON}"
    dump_diagnostics
    exit 1
  fi

  sleep 1
done

echo
echo "FAIL: timeout waiting for status=done"
echo "Last response:"
echo "${TASK_JSON:-<empty>}"
dump_diagnostics
exit 1
