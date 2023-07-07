from classes import Program
from parsing.async_parsing import get_programs
from caching.redis_client import RedisClient


def set_programs_in_cache(programs: [Program]):
    with RedisClient() as cache:
        cache.clear()
        for program in programs:
            cache.set_program(program)


if __name__ == "__main__":
    all_programs = get_programs()
    set_programs_in_cache(all_programs)
