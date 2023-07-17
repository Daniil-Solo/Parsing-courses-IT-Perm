import redis.asyncio as redis
from classes import Program, Course
import hashlib
import asyncio

PROGRAMS_KEY = "programs"
PROGRAM_TITLE_KEY = "program_title"


class ProgramCache:
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client

    async def set_programs(self, programs: [Program]):
        await self.clear()
        tasks = []
        for program in programs:
            if program.has_actual_courses:
                tasks.append(asyncio.create_task(self._set_program(program)))
        await asyncio.gather(*tasks)

    async def _set_program(self, program: Program) -> None:
        program_hash = hashlib.sha224(program.title.encode()).hexdigest()[:10]
        await self.redis_client.hset(name=PROGRAMS_KEY, key=program_hash, value=program.title)
        await self.redis_client.hset(name=program_hash, key=PROGRAM_TITLE_KEY, value=program.title)
        for course in program.courses:
            if course.is_actual:
                await self.redis_client.hset(name=program_hash, key=course.title, value=course.json)

    async def get_program_names_and_hash(self) -> [tuple[str, str]]:
        programs = await self.redis_client.hgetall(name=PROGRAMS_KEY)
        return [(p_name.decode(), p_hash.decode()) for (p_hash, p_name) in programs.items()]

    async def get_program_by_hash(self, program_hash: str) -> Program:
        program_data = await self.redis_client.hgetall(program_hash)
        program_title = program_data[PROGRAM_TITLE_KEY.encode()].decode()
        del program_data[PROGRAM_TITLE_KEY.encode()]
        p = Program(program_title, [])
        p.courses = [Course.from_json(key, value) for (key, value) in program_data.items()]
        return p

    async def clear(self) -> None:
        await self.redis_client.flushall()
