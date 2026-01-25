# Common pitfalls

Terminology used in this document is defined in the [Glossary](glossary.md).

This document describes common mistakes and unexpected behaviors
encountered when running the system in a local development environment.

It focuses on prevention and understanding, not step-by-step incident recovery.
If something is already broken, refer to the
[Runbook — Troubleshooting](runbook/troubleshooting.md).

---

## 1. Ports already in use

### Why it happens
Ports exposed by Docker services may already be used by other local
applications (databases, previous Docker stacks, system services).

### How it shows up
- Containers fail to start.
- Docker reports “port is already allocated”.
- Services start but are unreachable from the host.

### How to prevent
- Review port mappings in `.env` before starting the stack.
- Avoid using well-known ports for local development when possible.

### If it already happened
- Stop the conflicting service.
- Or change port values in `.env`.
- Restart the stack:
  ```bash
  make restart
  ```

---

## 2. Stale containers or volumes

### Why it happens
Docker volumes persist data across container restarts.
Over time, this can lead to inconsistent or unexpected local state.

This is especially relevant for:
- Postgres data volume;
- Redis data volume.

### How it shows up
- API or worker behaves unexpectedly.
- Tasks exist in the database but do not match queue state.
- Redis queue contains old jobs.

### How to prevent
- Prefer `make restart` over manual `docker compose down` / `up`.
- Be aware that local data is intentionally persisted between restarts.

### If it already happened

- Reset local state (destructive, local only):
```bash
make reset
```
- See runbook Scenario 5 for details.

---

## 3. `.env` file not created

### Why it happens
The project relies on environment variables defined in `.env`,
but this file is not created automatically.

### How it shows up
- Services fail to start.
- Configuration values are missing or defaulted incorrectly.

### How to prevent
Always initialize the environment before the first run:
```bash
make init
```

This copies `.env.example` to `.env` if it does not already exist.

---

## 4. Database not ready yet

### Why it happens
Postgres startup may take longer than API or worker startup,
especially on the first run or on slower machines.

### How it shows up
- API starts but `/health` reports Postgres as unavailable.
- Worker logs show database connection errors.

### How to prevent
- Rely on Docker **healthchecks** (see [Glossary](glossary.md#healthcheck-docker))
  and `depends_on` configuration.
- Wait for the API `/health` endpoint to report `ok`
  before sending requests.

### If it already happened
- Restart the stack:
  ```bash
  make restart
  ```
- If the issue persists, follow runbook Scenarios 1 or 3.

---

## 5. Worker is idle while queue grows

### Why it happens
The **Worker** (see [Glossary](glossary.md#worker)) may be running,
but unable to process **Jobs** (see [Glossary](glossary.md#job))
from the **Queue** (see [Glossary](glossary.md#queue)).

Common reasons:
- database connectivity issues;
- unexpected job payload format;
- unhandled exception in the worker loop.

### How it shows up
- Task status remains `queued`;
- Redis queue length increases;
- Worker container is `Up` but idle.

### How to prevent
- Monitor worker logs during development.
- Keep job payload format simple and explicit.

### If it already happened

- Inspect worker logs:
  ```bash
  docker compose logs -f worker
  ```
- Follow runbook Scenario 2.

---

## 6. Confusing Task and Job concepts

### Why it happens
The system uses two related but distinct concepts:

- **Task** — user-facing unit of work.
- **Job** — internal message used for background processing.

See definitions in the [Glossary](glossary.md#task).

### How it shows up
- Debugging the wrong layer (API vs worker).
- Inspecting Redis when the issue is in the database (or vice versa).

### How to prevent
When debugging:
- check **Task** state via the API and database;
- check **Job** state via Redis and worker logs.

Always identify which layer is failing first.

---

## 7. Bind mount permission issues (OS-specific)

### Why it happens
File permission behavior differs across operating systems
(macOS, Linux, Windows).

Bind mounts used for local development may expose these differences.

### How it shows up
- Permission denied errors inside containers.
- Inability to write files from the application.

### How to prevent
- Avoid editing files as root inside containers.
- Prefer host-side file edits.
- Treat bind mounts as a development convenience, not a production pattern.

---

## Final note

Most issues listed here are **local-only** and expected during development.

When something breaks:
1. Try to understand *why* it happened (this document).
2. Then follow concrete recovery steps in the runbook.
3. Use the smoke test as a fast diagnostic entry point.
