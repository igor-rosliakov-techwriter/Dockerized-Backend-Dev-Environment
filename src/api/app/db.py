import os
from typing import Optional, Dict, Any
from uuid import UUID

import psycopg
from psycopg.rows import dict_row


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


def init_db() -> None:
    """Create minimal table (no migrations for DAY2)."""
    ddl = """
    CREATE TABLE IF NOT EXISTS tasks (
        id UUID PRIMARY KEY,
        title TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    """
    with psycopg.connect(get_database_url()) as conn:
        with conn.cursor() as cur:
            cur.execute(ddl)
        conn.commit()


def create_task(task_id: UUID, title: str, status: str) -> Dict[str, Any]:
    sql = """
    INSERT INTO tasks (id, title, status)
    VALUES (%s, %s, %s)
    RETURNING id, title, status;
    """
    with psycopg.connect(get_database_url(), row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (task_id, title, status))
            row = cur.fetchone()
        conn.commit()
    return row


def get_task(task_id: UUID) -> Optional[Dict[str, Any]]:
    sql = """
    SELECT id, title, status
    FROM tasks
    WHERE id = %s;
    """
    with psycopg.connect(get_database_url(), row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (task_id,))
            return cur.fetchone()
