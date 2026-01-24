# Dockerized Backend Dev Environment

Production-like local backend environment designed as a **technical writing portfolio project**.

This repository demonstrates how I document and explain a small backend system
built with Docker Compose, API services, background workers, queues, and operational runbooks.

The project is educational, but intentionally structured and documented
as if it were a real team-owned service.

---

## What is this?

A minimal backend system running locally with:

- **FastAPI** — HTTP API
- **PostgreSQL** — persistent storage
- **Redis** — job queue
- **Worker** — background job processor
- **Docker Compose** — orchestration
- **Makefile & scripts** — developer UX and operations

The system implements a simple **task processing workflow**:
API → DB → queue → worker → DB.

---

## Audience

- **Recruiters / hiring managers** — to evaluate my technical writing skills
- **Backend engineers** — as onboarding-style documentation
- **Junior engineers / students** — as a realistic reference setup

---

## What I documented here

This project focuses on **documentation, not features**.

Included documentation topics:

- Local environment onboarding
- Docker Compose service design
- API / worker interaction
- Health checks and dependency wiring
- Debugging and diagnostics
- Common Docker pitfalls
- Operational runbooks for typical incidents

📚 Full documentation index: [`docs/index.md`](docs/index.md)

---

## Quick start

### Requirements
- Docker + Docker Compose
- `make`
- `curl` (for smoke test)

### Setup & run
  ```bash
  make init      # create .env from .env.example
  make up        # build and start all services
  ```

### Check system health
  ```bash
  make smoke
  ```

The smoke test:
- Waits for `/health`.
- Creates a task.
- Waits until the worker processes it.
- Prints diagnostics if anything fails.

## System overview

High-level flow:
  ```
  Client
    ↓
  FastAPI (API)
    ↓
  Postgres (tasks table)
    ↓
  Redis (queue)
    ↓
  Worker
    ↓
  Postgres (status update)
  ```

Details: [docs/01-architecture.md](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/01-architecture.md)

## Operational documentation

- Debugging guide
  How to inspect containers, logs, Redis, and DB
  → [docs/05-debugging.md](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/05-debugging.md)
- Runbook (troubleshooting)
  Step-by-step actions for common failure scenarios
  → [docs/runbook/troubleshooting.md](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/runbook/troubleshooting.md)
- Common pitfalls
  Frequent mistakes in Dockerized local environments
  → [docs/06-common-pitfalls.md](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/06-common-pitfalls.md)

## Tools & technologies

- Docker / Docker Compose
- FastAPI
- PostgreSQL
- Redis
- Bash
- Makefile


## Project scope

This repository intentionally focuses on:

- end-to-end request → queue → worker flow
- health checks and dependency wiring
- operational documentation (debugging, runbooks)
- documentation quality over feature completeness
