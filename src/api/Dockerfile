FROM python:3.12-slim

WORKDIR /app

# install dependencies first (better layer caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy application code
COPY app /app/app

ENV PYTHONUNBUFFERED=1

# command is defined in docker-compose.yml
