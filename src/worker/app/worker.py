import os
import time
from uuid import UUID

from app.db import ping_db, update_task_status
from app.queue import ping_redis, dequeue_job_blocking


def _sleep_seconds() -> float:
    return float(os.getenv("WORKER_POLL_INTERVAL_SECONDS", "1"))


def main() -> None:
    print("[worker] starting up...")

    # fail fast if deps are broken
    ping_db()
    ping_redis()
    print("[worker] postgres=ok redis=ok")

    poll_sleep = _sleep_seconds()

    while True:
        try:
            job = dequeue_job_blocking(timeout_seconds=5)
            if job is None:
                # nothing to do
                time.sleep(poll_sleep)
                continue

            task_id = UUID(job["task_id"])
            print(f"[worker] got job task_id={task_id}")

            update_task_status(task_id, "processing")
            print(f"[worker] task_id={task_id} -> processing")

            # fake work
            time.sleep(2)

            update_task_status(task_id, "done")
            print(f"[worker] task_id={task_id} -> done")

        except Exception as e:
            # best effort: mark failed (only if we have a task_id in scope)
            print(f"[worker] error: {type(e).__name__}: {e}")

            try:
                if "task_id" in locals():
                    update_task_status(task_id, "failed")  # type: ignore[name-defined]
                    print(f"[worker] task_id={task_id} -> failed")  # type: ignore[name-defined]
            except Exception as e2:
                print(f"[worker] failed to mark task as failed: {type(e2).__name__}: {e2}")

            time.sleep(poll_sleep)


if __name__ == "__main__":
    main()
