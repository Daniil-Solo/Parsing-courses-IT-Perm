import datetime
import json
from dataclasses import dataclass, asdict


@dataclass
class Course:
    title: str
    university: str
    study_format: str
    hours: int
    address: str
    schedule: str
    is_actual: bool
    study_start_date: datetime.date = None
    study_end_date: datetime.date = None
    last_register_date: datetime.date = None

    @property
    def json(self):
        d = asdict(self)
        del d["title"]
        for key in d:
            if d[key] is None:
                d[key] = ""
            elif type(d[key]) == bool:
                d[key] = int(d[key])
            elif type(d[key]) == datetime.date:
                d[key] = str(d[key])
        return json.dumps(d)

    @classmethod
    def from_json(cls, title: bytes, data: bytes):
        title = title.decode()
        d = json.loads(data)
        for key in d:
            if d[key] == "":
                d[key] = None
            elif key == "is_actual":
                d[key] = bool(d[key])
            elif key in ("study_start_date", "study_end_date", "last_register_date"):
                d[key] = datetime.datetime.strptime(d[key], "%Y-%m-%d").date()
        return cls(title=title, **d)


@dataclass
class Program:
    title: str
    courses: list[Course]
