"""
main.py

FastAPI application entrypoint.

Planned endpoints:
- GET /health
  - checks connectivity to Postgres and Redis
- POST /tasks
  - creates a task in Postgres and enqueues a job in Redis
"""
from fastapi import FastAPI

app = FastAPI(title="Dockerized Backend Dev Env", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok", "checks": {"db": "todo", "redis": "todo"}}

@app.post("/tasks")
def create_task():
    return {"status": "todo", "note": "will create task in db and enqueue job"}
