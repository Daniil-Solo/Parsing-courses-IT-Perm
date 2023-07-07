from caching.cache import ProgramCache
from config import REDIS_URL
import redis


class RedisClient:
    def __init__(self):
        self.redis = None

    def __enter__(self):
        self.redis = redis.from_url(REDIS_URL)
        return ProgramCache(self.redis)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.redis.close()
