from dataclasses import dataclass
from typing import Iterable


@dataclass
class Range:
    source_start: int
    dest_start: int
    length: int

    def map(self, src: int) -> int | None:
        if self.source_start <= src <= self.source_start + self.length:
            return (src - self.source_start) + self.dest_start

        return None


@dataclass
class Map:
    ranges: list[Range]

    def map(self, src: int) -> int:
        for r in self.ranges:
            res = r.map(src)
            if res is not None:
                return res

        return src


@dataclass
class Almanac:
    seeds: list[int]
    mapping_pipeline: list[Map]

    def map(self) -> Iterable[int]:
        res: Iterable[int] = self.seeds
        for m in self.mapping_pipeline:
            res = map(m.map, res)

        return res


def parse_input(text: str) -> Almanac:
    chunks: list[list[str]] = [[]]
    for line in text.splitlines():
        if line == "":
            chunks.append([])
        else:
            chunks[-1].append(line)

    [seeds_str] = chunks[0]
    seeds = list(map(int, seeds_str.split(":", maxsplit=1)[1].strip().split()))

    def parse_range(line: str) -> Range:
        [dest_start, source_start, length] = list(map(int, line.strip().split()))
        return Range(source_start=source_start, dest_start=dest_start, length=length)

    def parse_map(chunk: list[str]) -> Map:
        ranges = list(map(parse_range, chunk[1:]))
        return Map(ranges=ranges)

    mapping_pipeline = list(map(parse_map, chunks[1:]))

    return Almanac(seeds=seeds, mapping_pipeline=mapping_pipeline)


def part1(raw_input: str):
    almanac = parse_input(raw_input)

    return min(almanac.map())


def part2(raw_input: str):
    input = parse_input(raw_input)
    return 0
