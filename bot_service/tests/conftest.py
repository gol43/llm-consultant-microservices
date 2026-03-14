from unittest.mock import AsyncMock

import fakeredis.aioredis
import pytest


@pytest.fixture
def mock_redis():
    return fakeredis.aioredis.FakeRedis(decode_responses=True)

@pytest.fixture(autouse=True)
def patch_redis(monkeypatch, mock_redis):
    monkeypatch.setattr("app.bot.handlers.get_redis", lambda: mock_redis)
    return mock_redis

@pytest.fixture
def mock_celery_task(mocker):
    return mocker.patch("app.tasks.llm_tasks.ask_llm_task.delay")

@pytest.fixture
def mock_bot():
    return AsyncMock()