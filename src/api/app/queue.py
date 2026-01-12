import json
import os
from typing import Any, Dict

import redis


def _redis_client() -> redis.Redis:
    host = os.getenv("REDIS_HOST", "redis")
    port = int(os.getenv("REDIS_PORT", "6379"))
    return redis.Redis(host=host, port=port, decode_responses=True, socket_connect_timeout=3)


def ping_redis() -> None:
    r = _redis_client()
    pong = r.ping()
    if pong is not True:
        raise RuntimeError("Redis ping failed")


def enqueue_job(payload: Dict[str, Any]) -> None:
    queue_name = os.getenv("REDIS_QUEUE_NAME", "jobs")
    r = _redis_client()
    r.lpush(queue_name, json.dumps(payload))
