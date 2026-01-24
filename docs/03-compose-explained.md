# docker-compose explained

> This document uses terms defined in the [Glossary](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/glossary.md).

This stack is intended for [local development](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/glossary.md#local-development-environment), not production.

## Services
Services are defined using [Docker Compose](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/glossary.md#docker-compose).

### api
- Builds from `./src/api`
- Exposes port `8000` (mapped from `${API_PORT}`)
- Depends on `db` and `redis` being healthy
- [Healthcheck](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/glossary.md#healthcheck-docker) calls `GET /health`

### worker
- Builds from `./src/worker`
- Depends on `db` and `redis` being healthy
- Runs a Python module (`python -m app.worker`)

### db ([Postgres 16](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/glossary.md#postgres-postgresql))
- Stores tasks in a persistent volume `db_data`
- Port `5432` is mapped from `${POSTGRES_PORT}`
- Healthcheck uses `pg_isready`

### redis (Redis 7)
- Stores the [queue](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/glossary.md#queue) as a Redis list
- Uses persistent volume `redis_data`
- Healthcheck uses `redis-cli ping`

### adminer (optional)
- Web UI for Postgres, useful for demos and debugging
- Available on `${ADMINER_PORT}`

## Volumes
- `db_data` — persists Postgres data between restarts
- `redis_data` — persists Redis data between restarts (useful for demos)
