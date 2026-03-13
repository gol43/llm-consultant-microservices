.PHONY: install-auth install-bot sync-all lint-all

install-auth:
	cd auth_service && uv sync

install-bot:
	cd bot_service && uv sync

sync-all: install-auth install-bot

lint-all:
	cd auth_service && uv run ruff check .
	cd bot_service && uv run ruff check .

# Запуск auth_service
run-auth:
	cd auth_service && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Запуск bot_service (FastAPI часть для healthcheck)
run-bot-api:
	cd bot_service && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8001