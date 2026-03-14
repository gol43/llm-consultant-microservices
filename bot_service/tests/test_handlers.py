from unittest.mock import AsyncMock

import pytest

from app.bot.handlers import cmd_token, handle_message


@pytest.mark.asyncio
async def test_cmd_token_flow(patch_redis):
    message = AsyncMock()
    message.from_user.id = 123
    message.text = "/token valid_jwt"
    with pytest.MonkeyPatch.context() as m:
        m.setattr("app.bot.handlers.decode_and_validate", lambda x: {"sub": "123"})
        await cmd_token(message)
    
    val = await patch_redis.get("token:123")
    assert val == "valid_jwt"
    message.answer.assert_called()

@pytest.mark.asyncio
async def test_handle_message_triggers_queue(patch_redis, mock_celery_task):
    message = AsyncMock()
    message.from_user.id = 123
    message.chat.id = 456
    message.text = "Вопрос к ИИ"
    
    await patch_redis.set("token:123", "some_token")
    
    with pytest.MonkeyPatch.context() as m:
        m.setattr("app.bot.handlers.decode_and_validate", lambda x: {"sub": "123"})
        await handle_message(message)

    mock_celery_task.assert_called_once_with(
        chat_id=456, 
        prompt="Вопрос к ИИ"
    )
    message.answer.assert_called_with("Запрос принят в очередь...")