import pytest
import respx
from httpx import Response

from app.services.openrouter_client import OpenRouterClient


@pytest.mark.asyncio
@respx.mock
async def test_llm_client_simple():
    client = OpenRouterClient()

    respx.post("https://openrouter.ai/api/v1/chat/completions").mock(
        return_value=Response(200, json={
            "choices": [{"message": {"content": "Python - это круто"}}]
        })
    )
    
    result = await client.get_completion([{"role": "user", "content": "Привет"}])
    assert result == "Python - это круто"