from caching.cache import ProgramCache
from config import REDIS_URL
import redis.asyncio as redis


class RedisClient:
    def __init__(self):
        self.redis = None

    async def __aenter__(self):
        self.redis = await redis.from_url(REDIS_URL)
        return ProgramCache(self.redis)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.redis.close()
