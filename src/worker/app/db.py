import os
from uuid import UUID

import psycopg


def get_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set")
    return url


def ping_db() -> None:
    """Raises on failure."""
    with psycopg.connect(get_database_url(), connect_timeout=3) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            cur.fetchone()


def update_task_status(task_id: UUID, status: str) -> None:
    sql = """
    UPDATE tasks
    SET status = %s
    WHERE id = %s;
    """
    with psycopg.connect(get_database_url(), connect_timeout=3) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (status, task_id))
            if cur.rowcount != 1:
                raise RuntimeError(f"Task not found: {task_id}")
        conn.commit()
