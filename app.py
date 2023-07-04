import argparse
import datetime
import time

from parsing.async_parsing import get_programs
from classes import ProgramView


def main(view: str, only_actual: bool):
    programs = get_programs()
    for program in programs:
        pw = str(ProgramView(program, view, only_actual))
        print(pw)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--view", default="small", type=str,
                        help="type of view. small, full")
    parser.add_argument("--only_actual", default="y", type=str,
                        help="outputs only actual courses. y, n")
    args = parser.parse_args()
    main(view=args.view, only_actual=args.only_actual == "y")
