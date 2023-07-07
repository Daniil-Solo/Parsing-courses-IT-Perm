import redis
from classes import Program, Course


class ProgramCache:
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client

    def set_courses_by_program(self, program: Program) -> None:
        for course in program.courses:
            self.redis_client.hset(name=program.title, key=course.title, value=course.json)

    def get_program_names(self) -> [str]:
        return [key.decode() for key in self.redis_client.keys()]

    def get_courses_by_program(self, program_name: str) -> list[Course]:
        data = self.redis_client.hgetall(program_name)
        return [Course.from_json(key, value) for (key, value) in data.items()]

    def clear(self) -> None:
        self.redis_client.flushall()
