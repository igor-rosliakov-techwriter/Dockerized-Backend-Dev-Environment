import json
import os
from typing import Any, Dict, Optional, Tuple

import redis


def _redis_client() -> redis.Redis:
    host = os.getenv("REDIS_HOST", "redis")
    port = int(os.getenv("REDIS_PORT", "6379"))
    return redis.Redis(host=host, port=port, decode_responses=True, socket_connect_timeout=3)


def ping_redis() -> None:
    r = _redis_client()
    if r.ping() is not True:
        raise RuntimeError("Redis ping failed")


def dequeue_job_blocking(timeout_seconds: int = 5) -> Optional[Dict[str, Any]]:
    """
    Waits for a job from Redis list using BRPOP.
    Returns payload dict or None if timeout.
    """
    queue_name = os.getenv("REDIS_QUEUE_NAME", "jobs")
    r = _redis_client()

    # BRPOP returns (queue_name, item) or None on timeout
    result: Optional[Tuple[str, str]] = r.brpop(queue_name, timeout=timeout_seconds)
    if result is None:
        return None

    _q, raw = result
    return json.loads(raw)
