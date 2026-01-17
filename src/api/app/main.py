from uuid import uuid4
from uuid import UUID

from fastapi import FastAPI, HTTPException

from app.models import TaskCreate, TaskOut
from app.db import init_db, ping_db, create_task, get_task
from app.queue import ping_redis, enqueue_job

app = FastAPI(title="dockerized-backend-dev-env", version="0.1.0")


@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_tasks(task_id: UUID):
    row = get_task(task_id)
    if not row:
        raise HTTPException(status_code=404, detail="Task not found")
    return row


@app.on_event("startup")
def on_startup() -> None:
    # For DAY2 we keep it simple: create table at startup
    init_db()


@app.get("/health")
def health():
    details = {"postgres": "ok", "redis": "ok"}
    try:
        ping_db()
    except Exception as e:
        details["postgres"] = f"error: {type(e).__name__}"
    try:
        ping_redis()
    except Exception as e:
        details["redis"] = f"error: {type(e).__name__}"

    ok = details["postgres"] == "ok" and details["redis"] == "ok"
    return {"status": "ok" if ok else "degraded", "details": details}


@app.post("/tasks", response_model=TaskOut)
def post_tasks(payload: TaskCreate):
    task_id = uuid4()
    status = "queued"

    try:
        row = create_task(task_id=task_id, title=payload.title, status=status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {type(e).__name__}") from e

    try:
        enqueue_job({"task_id": str(task_id)})
    except Exception as e:
        # В реальном мире тут было бы: компенсирующая логика / статус "failed_to_enqueue"
        raise HTTPException(status_code=500, detail=f"Redis error: {type(e).__name__}") from e

    return row
