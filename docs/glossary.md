# Glossary

This glossary explains key terms used throughout this repository.

It is written not only for backend developers, but also for:
- technical writers reviewing the project,
- QA engineers exploring system behavior,
- junior engineers or students learning backend architecture,
- reviewers who may not work with Dockerized systems daily.

The goal is to make the documentation understandable without assuming
deep prior knowledge of the system or its tooling.

---

## API

**API (Application Programming Interface)**  
The HTTP service that acts as the system entry point.

In this project:
- implemented using FastAPI;
- exposes endpoints for health checks and task creation;
- coordinates access to Postgres and Redis.

---

## Worker

A background process that performs asynchronous work outside the API request lifecycle.

In this project:
- runs as a separate Docker service;
- consumes jobs from a Redis queue;
- updates task status in the database.

Workers allow long-running or blocking work to be handled
without delaying API responses.

---

## Task

A logical unit of work exposed to clients via the API.

In this project:
- a task is created via `POST /tasks`;
- it is stored in the database;
- its progress can be queried via `GET /tasks/{id}`.

A task represents **business-level intent**, not implementation details.

---

## Job

A technical representation of work to be performed asynchronously.

In this project:
- a job is a message pushed to Redis;
- it references a task stored in the database;
- it is consumed by the worker.

**Task ≠ Job**:
- task = what the system is doing (user-facing concept);
- job = how the system does it (internal mechanism).

---

## Queue

A data structure used to store jobs waiting to be processed.

In this project:
- implemented using a Redis list;
- job order is first-in, first-out (FIFO);
- the queue name is configurable via `REDIS_QUEUE_NAME`.

Queues decouple request handling from background processing.

---

## Redis

An in-memory data store used for fast access patterns.

In this project:
- Redis is used only as a queue backend;
- it does not store persistent application state;
- data loss is acceptable in local development.

---

## Postgres (PostgreSQL)

A relational database used for persistent storage.

In this project:
- stores task records and their statuses;
- acts as the system source of truth;
- is shared by API and worker services.

---

## Health endpoint (`/health`)

An HTTP endpoint exposed by the API to report system readiness.

In this project:
- checks connectivity to Postgres and Redis;
- reports dependency status explicitly;
- is used by Docker healthchecks and smoke tests.

Health endpoints help distinguish:
- “service is running”
- vs “service is usable”.

---

## Healthcheck (Docker)

A Docker-level mechanism for determining container health.

In this project:
- implemented via Docker Compose;
- relies on the API `/health` endpoint;
- controls startup order using `depends_on: condition: service_healthy`.

Healthchecks are infrastructure-level signals,
not application logic.

---

## Smoke test

A lightweight automated test that verifies the main system flow.

In this project:
- implemented as `scripts/smoke.sh`;
- creates a task via the API;
- waits until the worker processes it;
- prints diagnostics on failure.

Smoke tests answer the question:
> “Does the system basically work?”

---

## Runbook

A step-by-step operational guide for handling common failure scenarios.

In this project:
- focused on fast diagnosis;
- prioritizes practical actions over theory;
- intended for local development only.

Runbooks are especially useful for:
- onboarding new team members;
- reducing guesswork during failures.

---

## Debugging

The process of identifying and understanding failures.

In this repository, debugging typically involves:
- inspecting container logs;
- checking health endpoints;
- verifying Redis queue state;
- confirming database connectivity.

---

## Docker Compose

A tool for defining and running multi-container Docker applications.

In this project:
- defines API, worker, Postgres, Redis, and Adminer services;
- manages networking and startup order;
- acts as the single source of truth for local orchestration.

---

## Makefile

A convenience layer that wraps Docker Compose commands.

In this project:
- provides a consistent interface (`make up`, `make down`, `make smoke`);
- reduces command memorization;
- improves developer experience.

---

## Local development environment

A system setup intended for development and learning purposes only.

Characteristics:
- runs entirely on a developer’s machine;
- may use destructive reset commands;
- prioritizes clarity and speed over safety.

This repository is explicitly scoped to local development.
