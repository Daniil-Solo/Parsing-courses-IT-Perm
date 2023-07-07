import datetime
from classes import Course


class CourseTgView:
    MONTH_DICT = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня",
        7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }

    def __init__(self, course: Course):
        self.course = course

    @staticmethod
    def __beautify_date(date: datetime.date):
        return f"{date.day} {CourseTgView.MONTH_DICT[date.month]} {date.year} г."

    def __str__(self):
        view = ""
        view += self.course.title + "\n"
        view += "Набор " + ("открыт!" if self.course.is_actual else "закрыт!") + "\n"
        if self.course.study_start_date:
            view += f"Даты проведения: {self.__beautify_date(self.course.study_start_date)} — "
            view += self.__beautify_date(self.course.study_end_date) + "\n"
        view += "Вуз: " + self.course.university + "\n"
        view += "Расписание: " + self.course.schedule
        return view
