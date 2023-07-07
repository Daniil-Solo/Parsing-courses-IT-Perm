import datetime
import re
from bs4 import BeautifulSoup

from classes import Program, Course


class NoHereDataException(Exception):
    pass


def get_link_for_programs(document: str) -> list[str]:
    soup = BeautifulSoup(document, features="lxml")
    return [a.get('href') for a in soup.find_all("a", class_="promote")]


def find_second_span_by_string(block, string) -> str:
    first_span = block.find("span", string=re.compile(string))
    if first_span is not None:
        return first_span.findNext('span').text.strip()
    else:
        raise NoHereDataException


def find_text_in_description_by_string(block, string) -> str:
    description_block = block.find(string=re.compile(string))
    if description_block:
        return description_block.text.strip().split(":")[1]
    else:
        raise NoHereDataException


def get_study_interval(date_text: str) -> tuple[datetime.date, datetime.date]:
    start_date_text, end_date_text = re.findall(r"\d\d.\d\d.\d\d\d\d", date_text)
    start_date = get_date(start_date_text)
    end_date = get_date(end_date_text)
    return start_date, end_date


def get_date(date_text: str) -> datetime.date:
    prepared_date_text = re.findall(r"\d\d.\d\d.\d\d\d\d", date_text)[0]
    return datetime.datetime.strptime(prepared_date_text, "%d.%m.%Y").date()


def get_date_with_month_name(date_text: str, year: str) -> datetime.date:
    month_dict = {
        "января": 1, "февраля": 2, "марта": 3, "апреля": 4, "мая": 5, "июня": 6,
        "июля": 7, "августа": 8, "сентября": 9, "октября": 10, "ноября": 11, "декабря": 12
    }
    day, month_name = date_text.split()
    return datetime.date(int(year), month_dict[month_name], int(day))


def get_program_info(document: str) -> Program:
    soup = BeautifulSoup(document, features="lxml")
    title = soup.find("h1", class_="title black").text.strip()
    program = Program(title, [])

    course_blocks = soup.find_all("div", class_="item-service")
    for course_block in course_blocks:
        title = course_block.find("div", class_="name-service").text.strip()
        university = find_second_span_by_string(course_block, "Организация")
        study_format = find_second_span_by_string(course_block, "Формат обучения")
        hours = int(find_second_span_by_string(course_block, "Количество учебных часов"))
        address = find_second_span_by_string(course_block, "Адрес проведения")
        schedule_block = course_block.find("div", string=re.compile("Расписание"))
        schedule = schedule_block.findNext('div').text.strip().replace("\n", " ")
        is_actual = bool(course_block.find("a", class_="button-write"))

        course = Course(title, university, study_format, hours, address, schedule, is_actual)

        try:
            study_interval_text = find_text_in_description_by_string(course_block, "сроки обучения")
            study_start_date, study_end_date = get_study_interval(study_interval_text)
            course.study_start_date = study_start_date
            course.study_end_date = study_end_date
        except NoHereDataException:
            if course.university == "ПГНИУ":
                year = re.findall(r"\d{4}", course.title)[0]
                start_date_text, end_date_text = re.findall(r"\d+ [а-я]+", course.title)
                course.study_start_date = get_date_with_month_name(start_date_text, year)
                course.study_end_date = get_date_with_month_name(end_date_text, year)
        try:
            last_register_date_text = find_text_in_description_by_string(course_block, "регистрац")
            last_register_date = get_date(last_register_date_text)
            course.last_register_date = last_register_date
        except NoHereDataException:
            pass

        course.title = course.title.split("(")[0].strip()

        program.courses.append(course)
    return program
