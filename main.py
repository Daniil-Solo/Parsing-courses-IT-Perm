import bs4
import requests
import re
import argparse
from bs4 import BeautifulSoup
from classes import *


def get_text(element: bs4.Tag) -> str:
    """
    Возвращает текст элемента без табуляции, переноса кареток и новой строки
    """
    return element.text.replace("\n", "").replace("\t", "").replace("\r", "")


def parse_programs() -> (list, list):
    url = "https://epos.permkrai.ru/perm-itnetwork/directions/povyshenie-kvalifikaczii-dpo/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    links, titles = [], []
    programs = soup.find("div", class_="promotes-block").children
    programs = [p for p in programs if p.name]
    for program in programs:
        link = program.a.get("href")
        title = program.find("div", class_="title").text.strip()
        links.append(link)
        titles.append(title)
    return links, titles


def parse_courses(links: list, titles: list) -> list[Program]:
    programs = []
    for title, link in zip(titles, links):
        response = requests.get(link)
        soup = BeautifulSoup(response.text, features="html.parser")
        program = Program(title, link)
        div_courses = soup.find_all("div", class_="item-service")
        for div_course in div_courses:
            title = div_course.find("div", class_="name-service").text.strip()

            opened_text = div_course.find_all("div", class_="text")
            level = opened_text[0].find("span", class_="regular").text.strip()
            study_format = opened_text[1].find("span", class_="regular").text.strip()
            n_hours = opened_text[2].find("span", class_="regular").text.strip()
            address = opened_text[3].find("span", class_="regular").text.strip()

            hidden_text = div_course.find("div", class_="hidden-block").div.p.text
            dates = re.findall("\d{2}.\d{2}.\d{4}", hidden_text)
            start_date = dates[0]
            end_date = dates[1]
            try:
                start_index_uni = re.search("Вуз:", hidden_text).span()[1]
                end_index_uni = start_index_uni + re.search("\n", hidden_text[start_index_uni:]).span()[0]
                university = hidden_text[start_index_uni: end_index_uni].strip()
            except AttributeError:
                university = ""
            schedule = get_text(div_course.find("div", class_="schedule-block").find_all("div")[1])

            course = Course(title, level, study_format, n_hours, address, start_date, end_date, university, schedule)
            program.add_course(course)
        programs.append(program)
    return programs


def main(view: str, url: bool):
    links, titles = parse_programs()
    programs = parse_courses(links, titles)
    for program in programs:
        if program.course_count() > 0:
            print(program.get_info(url))
            print(program.get_info_about_courses(view))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--view", default="small", type=str,
                        help="type of view. small, medium, full")
    parser.add_argument("--url", default=False, type=bool,
                        help="outputs url of program")
    args = parser.parse_args()
    main(view=args.view, url=args.url)
