# Architecture

> This document uses terms defined in the [Glossary](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/glossary.md).

This repository demonstrates a typical local backend setup:

- **[API (FastAPI)](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/glossary.md#api)** — entrypoint for clients, exposes:
  - `GET /health` — checks dependencies (Postgres, Redis)
  - `POST /tasks` — creates a task record in DB and enqueues a job
- **Postgres** — persistent storage for tasks
- **Redis** — queue storage (list) used for background processing
- **[Worker](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/glossary.md#worker)** — consumes jobs from Redis and updates task status (implemented in DAY3)

## Data flow
1. Client sends `POST /tasks`.
2. API writes a new row into Postgres (`tasks` table) with status `queued` for a **[Task](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/glossary.md#task)**.
3. API pushes a [job](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/glossary.md#job) message to Redis list (queue).
4. Client receives task `id` and current status.

## Why this design
- Separates request handling (API) from background processing (worker)
- Makes dependency health visible via one endpoint (`/health`)
- Provides a realistic “happy path” for debugging and runbook examples
