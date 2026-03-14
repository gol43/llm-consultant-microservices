import httpx

from app.core.config import settings


class OpenRouterClient:
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": settings.OPENROUTER_SITE_URL,
            "X-Title": settings.OPENROUTER_APP_NAME,
            "Content-Type": "application/json",
        }

    async def get_completion(self, messages: list) -> str:
        payload = {
            "model": settings.OPENROUTER_MODEL,
            "messages": messages,
            "max_tokens": 1000 # там иначе ограничения телеги вываливаются на длину сообщения в 4096 символов.
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload
                )
                
                if response.status_code != 200:
                    raise ValueError(f"OpenRouter Error {response.status_code}: {response.text}")

                result = response.json()
                
                return result["choices"][0]["message"]["content"]

            except httpx.HTTPError as e:
                raise ValueError(f"Ошибка сети при запросе к OpenRouter: {str(e)}")
            except (KeyError, IndexError):
                raise ValueError("Некорректный формат ответа от OpenRouter API")