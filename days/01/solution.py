from pathlib import Path

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


def parse_digit(s: str):
    for key, value in DIGITS.items():
        if s.startswith(key):
            return value
    if s[0].isdigit():
        return int(s[0])

    return None


def parse_digits(s: str):
    res: list[int] = []
    while s != "":
        digit = parse_digit(s)
        if digit is not None:
            res.append(digit)
        s = s[1:]
    return res


def part2(input: list[str]):
    sum = 0
    for line in input:
        digits: list[int] = []
        digits = parse_digits(line)

        first_digit, last_digit = digits[0], digits[-1]
        sum += int("".join([str(first_digit), str(last_digit)]))

    return sum


if __name__ == "__main__":
    print(part1(load_input(INPUT_PATH)))
    print(part2(load_input(INPUT_PATH)))
