from typing import Callable, Iterable, Literal


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


def extrapolate(
    ints: list[int], idx: Literal[-1, 0], op: Callable[[int, int], int]
) -> int:
    difference = list(reversed(list(all_differences(ints))))
    value = 0
    for i in range(0, len(difference)):
        value = op(difference[i][idx], value)

    return value


def part1(raw_input: str):
    input = parse_input(raw_input)
    return sum(extrapolate(i, idx=-1, op=lambda x, y: x + y) for i in input)


def part2(raw_input: str):
    input = parse_input(raw_input)
    return sum(extrapolate(i, idx=0, op=lambda x, y: x - y) for i in input)
