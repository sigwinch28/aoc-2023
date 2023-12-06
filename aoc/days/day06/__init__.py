from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Race:
    time: int
    record: int


def parse_input(text: str) -> Iterable[Race]:
    def parse_line(line: str) -> Iterable[int]:
        return map(int, line.split(":", maxsplit=1)[1].strip().split())

    return map(
        lambda t, d: Race(time=t, record=d), *(map(parse_line, text.splitlines()))
    )


def part1(raw_input: str):
    races = parse_input(raw_input)
    ways = 1
    for race in races:
        ways_to_win_this_race = 0
        for t_hold in range(0, race.time + 1):
            distance = t_hold * (race.time - t_hold)
            if distance > race.record:
                ways_to_win_this_race += 1
        ways *= ways_to_win_this_race

    return ways


def part2(raw_input: str):
    input = parse_input(raw_input)
    return 0
