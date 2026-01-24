# Dockerfile explained

> This document uses terms defined in the [Glossary](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/glossary.md).

This document explains the design decisions behind the Dockerfiles
used for the API and worker services.

The goal of these Dockerfiles is **clarity and reliability in a local
development environment**, not production image optimization.

Both services use the same Dockerfile structure.

---

## Base image

```dockerfile
FROM python:3.12-slim
```

- Uses the official Python image for predictability.
- `slim` variant keeps the image reasonably small without sacrificing usability.
- Python 3.12 is chosen explicitly to avoid ambiguity.

## Working directory

```dockerfile
WORKDIR /app
```

- All application files live under `/app`.
- Keeps paths consistent across services and documentation.

## Dependency installation (layer caching)

```dockerfile
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
```

Dependencies are installed before application code is copied.

Why:

- Improves Docker layer caching.
- Dependency installation is only re-run when requirements.txt changes.
- Faster rebuilds during development.

## Application code

```dockerfile
COPY app /app/app
```

- Copies the application source code into the image.
- In local development, this is optionally overridden by bind mounts
defined in `docker-compose.yml`.

## Environment configuration

```dockerfile
ENV PYTHONUNBUFFERED=1
```

- Forces Python to flush stdout/stderr immediately.
- Ensures logs appear in real time when using `docker compose` logs.

## Command handling

The container command is not defined in the Dockerfile.

Instead, it is provided by `docker-compose.yml`:
- API runs via `uvicorn`.
- Worker runs via `python -m app.worker`.

Why:
- Keeps Dockerfiles generic and reusable.
- Makes service behavior explicit at the orchestration level.
- Allows easier experimentation without rebuilding images.

## Development vs production note

These Dockerfiles are intentionally simplified:
- no multi-stage builds.
- no non-root user.
- no dependency pinning beyond `requirements.txt`.
- no image hardening.

This is acceptable because:
- the environment is local-only
- the focus of the project is documentation and operations
- production concerns are discussed conceptually, not implemented

In a real production setup, additional hardening would be required.
