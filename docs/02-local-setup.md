# Local setup

> This document uses terms defined in the [Glossary](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/glossary.md).

## Prerequisites
- [Docker (with Docker Compose)](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/glossary.md#docker-compose)
- [Make](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/glossary.md#makefile) (optional, but recommended)

## Start
```bash
make init
make up
make smoke
```

The `make smoke` command runs a [smoke test](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/glossary.md#smoke-test)
to verify that the system works end-to-end.
