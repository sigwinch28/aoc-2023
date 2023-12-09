from typing import Iterable


def parse_input(text: str) -> list[list[int]]:
    return [[int(s) for s in line.split()] for line in text.splitlines()]


def differences(ints: Iterable[int]) -> Iterable[int]:
    it = iter(ints)
    last = next(it)
    for i in it:
        yield i - last
        last = i


def all_differences(ints: Iterable[int]) -> Iterable[list[int]]:
    current = list(ints)
    while not all(i == 0 for i in current):
        yield current
        current = list(differences(current))

    yield current


def extrapolate(ints: Iterable[int]) -> int:
    difference = list(reversed(list(all_differences(ints))))
    value = 0
    for i in range(0, len(difference)):
        value = difference[i][-1] + value

    return value


def part1(raw_input: str):
    input = parse_input(raw_input)
    return sum(extrapolate(i) for i in input)


def part2(raw_input: str):
    input = parse_input(raw_input)
    return 0
