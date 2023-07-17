import asyncio

from caching.redis_client import RedisClient
from parsing.async_parsing import async_get_programs


async def job():
    print("parsing started")
    programs = await async_get_programs()
    print("parsing done")
    print("caching started")
    async with RedisClient() as cache:
        await cache.set_programs(programs)
    print("caching done")


if __name__ == "__main__":
    asyncio.run(job())
