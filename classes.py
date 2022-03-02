class Course:
    def __init__(self, title, level, study_format, n_hours, address, start_date, end_date, university, schedule):
        self.__title = title
        self.__level = level
        self.__study_format = study_format
        self.__n_hours = n_hours
        self.__address = address
        self.__start_date = start_date
        self.__end_date = end_date
        self.__university = university
        self.__schedule = schedule

    def get_title(self) -> str:
        return self.__title

    def get_info(self) -> str:
        info = ""
        info += self.__title + f"({self.__level})" + "\n"
        info += "Группа обучения: " + self.__study_format + f" ({self.__n_hours} ч.)" + "\n"
        info += "Адрес проведения: " + self.__address + "\n"
        info += "Даты проведения: " + self.__start_date + " - " + self.__end_date + "\n"
        if self.__university:
            info += "Вуз: " + self.__university + "\n"
        info += "Расписание: " + self.__schedule
        return info


class Program:
    def __init__(self, title, url):
        self.__title = title
        self.__url = url
        self.__courses = []

    def add_course(self, course: Course):
        self.__courses.append(course)

    def course_count(self) -> int:
        return len(self.__courses)

    def get_info(self, url: bool) -> str:
        info = ""
        info += "------------------" + self.__title + "------------------"
        if url:
            info += "\n" + self.__url
        return info

    def get_info_about_courses(self, view: str) -> str:
        info = ""
        if view == "small":
            info += f"Курсы ({self.course_count()}) \n"
        else:
            for idx, course in enumerate(self.__courses):
                info += f"{idx + 1}) "
                if view == "medium":
                    info += course.get_title()
                elif view == "full":
                    info += course.get_info() + "\n"
                else:
                    raise ValueError(f"Неизвестный аргумент {view}")
                info += "\n"
        return info
