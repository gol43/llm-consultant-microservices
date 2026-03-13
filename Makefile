.PHONY: install-auth install-bot sync-all lint-all lint-fix

install-auth:
	cd auth_service && uv sync

install-bot:
	cd bot_service && uv sync

sync-all: install-auth install-bot

lint-all:
	cd auth_service && uv run ruff check .
	cd bot_service && uv run ruff check .

lint-fix:
	cd auth_service && uv run ruff check . --fix
	cd bot_service && uv run ruff check . --fix

run-auth:
	cd auth_service && uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
	
run-bot-api:
	cd bot_service && uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8001