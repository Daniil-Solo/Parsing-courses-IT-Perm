from classes import Program
from parsing.async_parsing import get_programs
from caching.redis_client import RedisClient
import asyncio


async def set_programs_in_cache(programs: [Program]):
    async with RedisClient() as cache:
        await cache.clear()
        tasks = []
        for program in programs:
            tasks.append(asyncio.create_task(cache.set_program(program)))
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    all_programs = get_programs()
    asyncio.run(set_programs_in_cache(all_programs))
