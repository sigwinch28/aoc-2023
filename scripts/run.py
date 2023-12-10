import argparse
import importlib


from typing import cast, Protocol

from aoc import lib


class Day(Protocol):
    def part1(self, raw_input: str) -> int:
        ...

    def part2(self, raw_input: str) -> int:
        ...


def run(day: int) -> None:
    print(f"Day {day}")
    mod = cast(Day, importlib.import_module(f".day{day:02}", "aoc.days"))
    inputs = sorted(list(lib.sample_paths(day)))

    input_path = lib.input_path(day)
    if input_path.exists():
        inputs.append(input_path)

    for path in inputs:
        input = path.read_text()
        print(f"  {path.name}:")
        print(f"    Part 1: {mod.part1(input)}")
        print(f"    Part 2: {mod.part2(input)}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("days", nargs="+", type=int)

    args = parser.parse_args()
    for day in args.days:
        run(day)


if __name__ == "__main__":
    main()
