import datetime
import pathlib

from typing import Iterable

import pytz
import requests

DAYS_DIR = pathlib.Path(__file__).parent.parent / "days"
SESSION_TOKEN_ENV_VAR = "AOC_SESSION_TOKEN"
ALL_DAYS = list(range(1, 25 + 1))


def day_dir(day: int):
    return DAYS_DIR / f"day{day:02}"


def input_path(day: int) -> pathlib.Path:
    return day_dir(day) / "input.txt"


def sample_paths(day: int) -> Iterable[pathlib.Path]:
    for path in day_dir(day).iterdir():
        if path.is_file() and path.stem.startswith("sample") and path.suffix == ".txt":
            yield (path)


def get_input(day: int, session_token: str) -> str:
    resp = requests.get(
        f"https://adventofcode.com/2023/day/{day}/input",
        cookies={"session": session_token},
    )
    if not resp.ok:
        raise ValueError(f"Got not ok status code {resp.status_code}")

    return resp.text


def days_so_far() -> Iterable[int]:
    today = datetime.datetime.now(tz=pytz.timezone("US/Eastern")).date()
    for day in ALL_DAYS:
        if datetime.date(2023, 12, day) > today:
            return

        yield day
