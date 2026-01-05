.PHONY: help init up down build logs ps restart smoke reset

help:
	@echo "make init    - copy .env.example -> .env"
	@echo "make up      - start services (build if needed)"
	@echo "make down    - stop services"
	@echo "make build   - build images"
	@echo "make logs    - follow logs"
	@echo "make ps      - list containers"
	@echo "make restart - restart services"
	@echo "make smoke   - run quick health checks"
	@echo "make reset   - remove containers + volumes (DANGER: deletes DB data)"

init:
	@test -f .env || cp .env.example .env
	@echo "created .env (if it did not exist)"

up:
	docker compose up --build -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f --tail=200

ps:
	docker compose ps

restart:
	docker compose down
	docker compose up --build -d

smoke:
	bash scripts/smoke.sh

reset:
	bash scripts/reset.sh
