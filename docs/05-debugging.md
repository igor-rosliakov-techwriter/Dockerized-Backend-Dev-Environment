# Debugging

Quick commands:
- view running services: `make ps`
- logs: `make logs`
- enter a container: `docker exec -it devenv_api sh`

What to check:
- API health endpoint
- Postgres readiness
- Redis ping and queue length
