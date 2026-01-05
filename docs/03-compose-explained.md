# docker-compose explained

This document explains what each service in `docker-compose.yml` does, why it exists, and how services connect.

Topics to cover:
- `depends_on` and healthchecks
- env vars / `.env`
- ports vs internal container networking
- volumes for persistence (Postgres, Redis)
