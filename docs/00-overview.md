# Overview

> This document uses terms defined in the [Glossary](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/glossary.md).

This project provides a **local development environment** for a typical backend system:
an API, a background worker, a database, and a queue.

## Audience
- New backend engineers joining a team
- Developers running the stack locally for debugging and feature work

## What you get
- One command to run the stack: `make up`
- A health endpoint that checks dependencies: `GET /health`
- A simple [task](https://github.com/igor-rosliakov-techwriter/Dockerized-Backend-Dev-Environment/blob/main/docs/glossary.md#task) flow (`POST /tasks`) that demonstrates API → DB → queue → worker

## Non-goals
- This is not a production deployment template.
- The focus is **developer experience + documentation**.
