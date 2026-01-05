"""
worker.py

Placeholder background worker.

Planned loop:
- block/pop from Redis queue (REDIS_QUEUE_NAME)
- for each job, update task status in Postgres
- log what happened (without leaking secrets)
"""
def main():
    print("worker starting... (todo)")

if __name__ == "__main__":
    main()
