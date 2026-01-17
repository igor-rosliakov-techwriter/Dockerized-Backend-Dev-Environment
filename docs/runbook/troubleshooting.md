# Runbook — Troubleshooting

This runbook describes common failure scenarios in the local environment
and provides step-by-step recovery instructions.

The goal is **fast diagnosis**, not deep root cause analysis.

⚠️ **Destructive operations (local development only)**

Some commands used in this runbook are **destructive** and must be used
**only in local development environments**.

`make reset`:

- stops all running containers
- removes containers and Docker volumes
- deletes **all Postgres and Redis data**

Never run these commands in shared or production environments.

---

## Scenario 1. API container is running but `/health` fails

### Symptoms
- `docker compose ps` shows `api` as `Up`
- `/health` returns `degraded` or times out

### Checks
1. Inspect API logs:
   ```bash
   docker compose logs -f api
   ```

2. Check dependency status in `/health` response:
- `postgres != ok`
- `redis != ok`

### Actions

- If Postgres is failing: see _Scenario 3_
- If Redis is failing: see _Scenario 4_
- Restart services:
  ```bash
  make restar
  ```

---

## Scenario 2. Worker is running but jobs are not processed

### Symptoms

- `POST /tasks` succeeds;
- task status stays `queued`;
^ Redis queue length grows.

### Checks

1. Inspect worker logs:
  ```bash
  docker compose logs -f worker
  ```
2. Inspect Redis queue:
  ```bash
  docker compose exec redis redis-cli
  LLEN jobs
  ```

### Likely causes
- Worker cannot connect to Postgres.
- Job payload format mismatch.
- Unhandled exception in worker loop.

### Actions
- Fix configuration or code error
- Restart worker:
  ```bash
  docker compose restart worker
  ```

---

## Scenario 3. Postgres refuses connections

### Symptoms
- `/health` shows postgres error
- worker logs contain connection errors
- API fails on task creation

### Checks
  ```bash
  docker compose logs -f db
  ```

### Actions
1. Restart database:
  ```bash
  docker compose restart db
  ```
2. If state is corrupted (local dev only):
  ```bash
  make reset
  ```

---

## Scenario 4. Redis is unreachable

### Symptoms
- `/health` reports Redis error.
- API fails when enqueuing jobs.
- Worker cannot consume jobs.

### Checks

  ```bash
  docker compose logs -f redis
  ```

### Actions
- Restart Redis:
  ```bash
  docker compose restart redis
  ```
- Verify Redis health manually:
  ```bash
  docker compose exec redis redis-cli ping
  ```

  ---

## Scenario 5. Resetting state safely (local only)

### When to use
- broken local state.
- inconsistent volumes.
- development reset.

### Command
  ```bash
  make reset
  ```

---

## First response checklist

When something breaks, start here:
1. `make smoke`
2. Inspect printed diagnostics.
3. Check worker logs.
4. Check Redis queue.
5. Check Postgres state.

This sequence resolves most local issues within minutes.










