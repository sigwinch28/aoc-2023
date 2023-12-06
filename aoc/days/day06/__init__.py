from dataclasses import dataclass
from functools import reduce
from typing import Iterable


@dataclass(frozen=True)
class Race:
    time: int
    record: int


def ways_to_win(race: Race) -> int:
    ways = 0
    for t_hold in range(0, race.time + 1):
        distance = t_hold * (race.time - t_hold)
        if distance > race.record:
            ways += 1
    return ways


def part1(raw_input: str):
    def parse_line(line: str) -> Iterable[int]:
        return map(int, line.split(":", maxsplit=1)[1].strip().split())

    races = list(
        map(
            lambda t, d: Race(time=t, record=d),
            *(map(parse_line, raw_input.splitlines()))
        )
    )

    return reduce(lambda x, y: x * y, map(ways_to_win, races))


def part2(raw_input: str):
    def parse_line(line: str) -> int:
        return int("".join(line.split(":", maxsplit=1)[1].strip().split()))

    [t, r] = list(map(parse_line, raw_input.splitlines()))
    race = Race(time=t, record=r)
    return ways_to_win(race)
