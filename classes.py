import datetime
from dataclasses import dataclass


@dataclass
class Course:
    title: str
    study_format: str
    hours: int
    address: str
    study_start_date: datetime.date
    study_end_date: datetime.date
    university: str
    teacher: str
    schedule: str


@dataclass
class Program:
    title: str
    courses: list[Course]
