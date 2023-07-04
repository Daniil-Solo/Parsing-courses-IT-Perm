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
    is_actual: bool
    study_start_date: datetime.date = None
    study_end_date: datetime.date = None
    last_register_date: datetime.date = None


@dataclass
class Program:
    title: str
    courses: list[Course]


class ProgramView:
    MONTH_DICT = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня",
        7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }

    def __init__(self, program: Program, view: str, only_actual: bool):
        self.__program = program
        self.__view = view
        self.__only_actual = only_actual

    @staticmethod
    def __beautify_date(date: datetime.date):
        return f"{date.day} {ProgramView.MONTH_DICT[date.month]} {date.year} г."

    def __get_course_view(self, course: Course):
        info = course.title + f" ({course.hours} ч.)" + "\n"
        if self.__view == "full":
            info += "Вуз: " + course.university + "\n"
            info += "Адрес проведения: " + course.address + "\n"
            if course.study_start_date:
                info += f"Даты проведения: {self.__beautify_date(course.study_start_date)} — "
                info += self.__beautify_date(course.study_end_date) + "\n"
            if course.last_register_date:
                info += f"День окончания регистрации: {self.__beautify_date(course.last_register_date)} \n"
            info += "Расписание: " + course.schedule + "\n"
        return info

    def __get_courses(self):
        return list(filter(lambda c: c.is_actual == self.__only_actual, self.__program.courses))

    def __str__(self) -> str:
        info = "------------------" + self.__program.title + "------------------\n"
        courses = self.__get_courses()
        for (idx, course) in enumerate(courses):
            info += f"{idx+1}. " + self.__get_course_view(course) + "\n"
        if not courses:
            info += "Актуальных курсов нет!\n"
        return info
