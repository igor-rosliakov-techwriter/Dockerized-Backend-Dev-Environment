# Architecture

## Components
- **api** (FastAPI): HTTP interface, validates inputs, writes to DB, enqueues jobs
- **worker**: consumes jobs from Redis and updates DB status
- **db** (Postgres): stores tasks
- **redis**: queue backend
- **adminer** (optional): view DB tables in a browser

## Data flow (happy path)
1. Client calls `POST /tasks`
2. API inserts a row into Postgres (status = `queued`)
3. API pushes a job into Redis list/queue
4. Worker pops job, processes it, updates Postgres (status = `done`)
