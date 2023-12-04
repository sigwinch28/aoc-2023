import argparse

import os
import pathlib

from aoc import lib


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    parser_day = subparsers.add_parser(name="day")

    parser_day.add_argument("day", type=int, choices=lib.days_so_far())
    parser_day.set_defaults(func=lambda ns, token: get_input(ns.day, token))

    parser_missing = subparsers.add_parser(name="missing")
    parser_missing.set_defaults(func=lambda _ns, token: get_missing(token))

    session_token = os.getenv(lib.SESSION_TOKEN_ENV_VAR, None)
    if session_token is None:
        raise ValueError(f"{lib.SESSION_TOKEN_ENV_VAR} is not set")

    args = parser.parse_args()
    args.func(args, session_token)


def get_missing(session_token: str):
    for day in lib.days_so_far():
        path = lib.input_path(day)
        if path.exists():
            print(f"skipping day {day} because {path} already exists")
            continue

        if not path.parent.is_dir():
            print(
                f"skipping day {day} because {path.parent.relative_to(os.getcwd(), walk_up=True)} is not a directory"
            )
            continue

        get_input(day, session_token)


def get_input(day: int, session_token: str):
    input_path = lib.input_path(day)

    if not input_path.parent.is_dir():
        raise FileNotFoundError(f"{dir} does not exist")

    input = lib.get_input(day, session_token)

    with input_path.open("w+") as f:
        f.write(input)

    relpath = input_path.relative_to(pathlib.Path(os.getcwd()), walk_up=True)
    print(f"written to {relpath}")


if __name__ == "__main__":
    main()
