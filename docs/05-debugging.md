# Debugging

This document describes practical debugging steps for the local development
environment defined in this repository.  
The goal is to quickly understand **which component is failing** and **where to look next**.

The system consists of:
- API (FastAPI)
- Worker (background job processor)
- Postgres (task storage)
- Redis (job queue)

---

## Quick commands

Most common commands are wrapped in `Makefile` targets:

- View running services:
  ```bash
  make ps
  ```
- Follow logs of all services:
  ```bash
  make logs
  ```
- Run end-to-end smoke test:
  ```bash
  make smoke
  ```
- Restart the whole stack:
  ```bash
  make restart
  ```
- If you need to inspect a single container:
  ```bash
  docker compose logs -f worker
  docker compose logs -f api
  ```
- To enter a container shell:
  ```bash
  docker exec -it devenv_api sh
  docker exec -it devenv_worker sh
  ```

---

## Step 1. Check API health

The API exposes a single health endpoint:
  ```
  curl http://localhost:8000/health
  ```

Expected response:
  ```json
  {
  "status": "ok",
  "details": {
    "postgres": "ok",
    "redis": "ok"
  }
}
```

If `status` is `degraded`, inspect `details` to see which dependency is failing.

---

## Step 2. Verify task lifecycle via API

Create a task:
  ``` bash
  curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "debug task"}'
  ```

Response example:
  ```json
  {
    "id": "…",
    "title": "debug task",
    "status": "queued"
  }
  ```

Check task status:
  ```bash
  curl http://localhost:8000/tasks/<task_id>
  ```

Expected progression:
  `queued -> processing -> done`

If the status stays `queued`, the worker is not consuming jobs.

---

## Step 3. Inspect worker logs

The worker is responsible for:
- consuming jobs from Redis;
- updating task status in Postgres.

Follow worker logs:
  ```bash
  docker compose logs -f worker
  ```

Typical healthy output:
  ```
  [worker] starting up...
  [worker] postgres=ok redis=ok
  [worker] got job task_id=...
  [worker] task_id=... -> processing
  [worker] task_id=... -> done
  ```

Errors here usually indicate:
- Redis connectivity issues;
- Postgres connectivity issues;
- unexpected job payloads.

---

## Step 4. Inspect Redis queue directly

To inspect Redis manually:
  ```bash
  docker compose exec redis redis-cli
  ```

### Useful commands

- Check queue length:
  ```bash
  LLEN jobs
  ```

- Inspect queued jobs:
  ```bash
  LRANGE jobs 0 10
  ```

If the queue grows but the worker is idle, focus on worker logs.

---

## Step 5. Inspect Postgres state

For quick inspection, use Adminer (if enabled):
  ```
  http://localhost:8081
  ```

Connection details:
- System: PostgreSQL
- Server: `db`
- Database/User/Password: from `.env`
  
Check the tasks table and verify:
- rows are created on `POST /tasks`;
- `status` changes over time
  
---

##Smoke test as a debugging tool

The smoke test (`make smoke`) performs:
1. API health check.
2. Task creation.
3. Polling until the task reaches done.

If the smoke test fails, it automatically prints:
- Container status.
- Recent worker logs.
- Recent API logs.

This makes it the fastest way to identify which component is broken.









