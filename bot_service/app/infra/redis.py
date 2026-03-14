import redis.asyncio as redis

from app.core.config import settings


class RedisManager:
    def __init__(self):
        # Решил взять класс Редиса из проекта на работе,
        # думаю, что будет круто, если в учёбных целях буду применять рабочий опыт XD :)) reversed(experiense)
        self.pool = redis.ConnectionPool.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            max_connections=50
        )
        self.client = redis.Redis(connection_pool=self.pool)

    async def set_user_token(self, tg_user_id: int, token: str, expire: int = 3600):
        key = f"token:{tg_user_id}"
        await self.client.set(key, token, ex=expire)

    async def get_user_token(self, tg_user_id: int) -> str | None:
        key = f"token:{tg_user_id}"
        return await self.client.get(key)

    async def delete_user_token(self, tg_user_id: int):
        key = f"token:{tg_user_id}"
        await self.client.delete(key)

# Создаем единственный экземпляр менеджера на всё приложение (Singleton)
redis_manager = RedisManager()

def get_redis():
    return redis_manager.client