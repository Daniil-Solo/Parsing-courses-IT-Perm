import datetime
from abc import ABC
from classes import Program, Course


class DateView:
    MONTH_DICT = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня",
        7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }

    @staticmethod
    def beautify_date(date: datetime.date):
        return f"{date.day} {DateView.MONTH_DICT[date.month]} {date.year} г."


class ProgramConsoleView:

    def __init__(self, program: Program, view: str, only_actual: bool):
        self.__program = program
        self.__view = view
        self.__only_actual = only_actual

    def __get_courses(self):
        return list(filter(lambda c: c.is_actual == self.__only_actual, self.__program.courses))

    def __str__(self) -> str:
        info = "------------------" + self.__program.title + "------------------\n"
        courses = self.__get_courses()
        for (idx, course) in enumerate(courses):
            info += f"{idx + 1}. {CourseConsoleView(course, self.__view)}\n"
        if not courses:
            info += "Актуальных курсов нет!\n"
        return info


class CourseView(ABC):
    def __init__(self, course: Course):
        self.course = course

    def get_short_view(self):
        return self.course.title + f" ({self.course.hours} ч.)"

    def get_full_view(self):
        view = self.get_short_view() + "\n"
        view += "Вуз: " + self.course.university + "\n"
        view += "Адрес проведения: " + self.course.address + "\n"
        if self.course.study_start_date:
            view += f"Даты проведения: {DateView.beautify_date(self.course.study_start_date)} — "
            view += DateView.beautify_date(self.course.study_end_date) + "\n"
        if self.course.last_register_date:
            view += f"День окончания регистрации: {DateView.beautify_date(self.course.last_register_date)} \n"
        view += "Расписание: " + self.course.schedule + "\n"
        return view


class CourseConsoleView(CourseView):

    def __init__(self, course: Course, view):
        super().__init__(course)
        self.__view = view

    def __str__(self) -> str:
        return self.get_full_view() if self.__view == "full" else self.get_short_view()


class CourseTgView(CourseView):

    def __str__(self):
        return self.get_full_view()
