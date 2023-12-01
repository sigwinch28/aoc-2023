from pathlib import Path
from typing import Iterable, TypeVar

INPUT_PATH = Path(__file__).parent / "input.txt"
SAMPLE_PATHS = [
    Path(__file__).parent / "sample.txt",
    Path(__file__).parent / "sample2.txt",
]

DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def load_input(path: Path):
    return path.read_text().splitlines()


def part1(input):
    res = 0
    for line in input:
        digits = list(filter(lambda x: x.isdigit(), line))
        first_digit, last_digit = digits[0], digits[-1]
        res += int("".join([first_digit, last_digit]))

    return res


def parse_digit(s: str) -> int | None:
    for key, value in DIGITS.items():
        if s.startswith(key):
            return value
    if s[0].isdigit():
        return int(s[0])

    return None


T = TypeVar("T")


def tails(input: list[T]) -> Iterable[list[T]]:
    while input != []:
        yield input
        input = input[1:]


def parse_digits(s: str):
    for tail in map(lambda chars: "".join(chars), tails(list(s))):
        digit = parse_digit(tail)
        if digit is not None:
            yield (digit)


def part2(input: list[str]):
    sum = 0
    for line in input:
        digits = list(parse_digits(line))

        first_digit, last_digit = digits[0], digits[-1]
        sum += int("".join([str(first_digit), str(last_digit)]))

    return sum


if __name__ == "__main__":
    print(part1(load_input(INPUT_PATH)))
    print(part2(load_input(INPUT_PATH)))
