# Architecture

This repository demonstrates a typical local backend setup:

- **API (FastAPI)** — entrypoint for clients, exposes:
  - `GET /health` — checks dependencies (Postgres, Redis)
  - `POST /tasks` — creates a task record in DB and enqueues a job
- **Postgres** — persistent storage for tasks
- **Redis** — queue storage (list) used for background processing
- **Worker** — consumes jobs from Redis and updates task status (implemented in DAY3)

## Data flow
1. Client sends `POST /tasks`
2. API writes a new row into Postgres (`tasks` table) with status `queued`
3. API pushes a job message to Redis list (queue)
4. Client receives task `id` and current status

## Why this design
- Separates request handling (API) from background processing (worker)
- Makes dependency health visible via one endpoint (`/health`)
- Provides a realistic “happy path” for debugging and runbook examples
