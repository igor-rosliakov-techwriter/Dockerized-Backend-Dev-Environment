# docker-compose explained

This stack is intended for **local development**, not production.

## Services

### api
- Builds from `./src/api`
- Exposes port `8000` (mapped from `${API_PORT}`)
- Depends on `db` and `redis` being healthy
- Healthcheck calls `GET /health`

### worker
- Builds from `./src/worker`
- Depends on `db` and `redis` being healthy
- Runs a Python module (`python -m app.worker`)
- In DAY2 it can be a stub; in DAY3 it will consume jobs from Redis

### db (Postgres 16)
- Stores tasks in a persistent volume `db_data`
- Port `5432` is mapped from `${POSTGRES_PORT}`
- Healthcheck uses `pg_isready`

### redis (Redis 7)
- Stores the queue as a Redis list
- Uses persistent volume `redis_data`
- Healthcheck uses `redis-cli ping`

### adminer (optional)
- Web UI for Postgres, useful for demos and debugging
- Available on `${ADMINER_PORT}`

## Volumes
- `db_data` — persists Postgres data between restarts
- `redis_data` — persists Redis data between restarts (useful for demos)
