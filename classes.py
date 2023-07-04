import datetime
from dataclasses import dataclass


@dataclass
class Course:
    title: str
    university: str
    study_format: str
    hours: int
    address: str
    schedule: str
    study_start_date: datetime.date = None
    study_end_date: datetime.date = None
    last_register_date: datetime.date = None


@dataclass
class Program:
    title: str
    courses: list[Course]
