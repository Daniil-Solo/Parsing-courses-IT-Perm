import redis
from classes import Program, Course
import hashlib

PROGRAMS_KEY = "programs"
PROGRAM_TITLE_KEY = "program_title"


class ProgramCache:
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client

    def set_program(self, program: Program) -> None:
        program_hash = hashlib.sha224(program.title.encode()).hexdigest()[:10]
        self.redis_client.hset(name=PROGRAMS_KEY, key=program_hash, value=program.title)
        self.redis_client.hset(name=program_hash, key=PROGRAM_TITLE_KEY, value=program.title)
        for course in program.courses:
            self.redis_client.hset(name=program_hash, key=course.title, value=course.json)

    def get_program_names_and_hash(self) -> [tuple[str, str]]:
        return [(value.decode(), key.decode()) for (key, value) in self.redis_client.hgetall(name=PROGRAMS_KEY).items()]

    def get_program_by_hash(self, program_hash: str) -> Program:
        program_data = self.redis_client.hgetall(program_hash)
        program_title = program_data[PROGRAM_TITLE_KEY.encode()].decode()
        del program_data[PROGRAM_TITLE_KEY.encode()]
        p = Program(program_title, [])
        p.courses = [Course.from_json(key, value) for (key, value) in program_data.items()]
        return p

    def clear(self) -> None:
        self.redis_client.flushall()
