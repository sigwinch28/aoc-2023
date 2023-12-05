from dataclasses import dataclass
import itertools
from typing import Iterable, Self


@dataclass(frozen=True)
class Interval:
    """[start,finish)"""

    start: int
    finish: int

    def __str__(self) -> str:
        return f"[{self.start},{self.finish})"

    def __post_init__(self):
        assert self.start <= self.finish

    @property
    def empty(self):
        return self.start == self.finish

    def intersection(self, other: Self) -> Self | None:
        if self.finish <= other.start or self.start >= other.finish:
            return None

        return Interval(
            start=max((self.start, other.start)),
            finish=min((self.finish, other.finish)),
        )


@dataclass(frozen=True)
class Map:
    source_start: int
    dest_start: int
    length: int

    def __str__(self) -> str:
        return f"{self.source_interval} -> {self.dest_interval}"

    @property
    def source_interval(self) -> Interval:
        return Interval(start=self.source_start, finish=self.source_start + self.length)

    @property
    def dest_interval(self) -> Interval:
        return Interval(start=self.dest_start, finish=self.dest_start + self.length)

    def map(self, interval: Interval) -> None | tuple[Interval, Iterable[Interval]]:
        intersection = interval.intersection(self.source_interval)
        if intersection is None:
            return None

        delta = self.dest_start - self.source_start
        middle = Interval(
            start=intersection.start + delta, finish=intersection.finish + delta
        )

        left = Interval(start=interval.start, finish=intersection.start)
        right = Interval(start=intersection.finish, finish=interval.finish)

        return (middle, filter(lambda i: not i.empty, (left, right)))

    def yeet(
        self, intervals: Iterable[Interval]
    ) -> tuple[Iterable[Interval], Iterable[Interval]]:
        results: list[Interval] = []
        unmapped: list[Interval] = []
        for interval in intervals:
            mapped = self.map(interval)
            if mapped is None:
                unmapped.append(interval)
                continue
            (x, other) = mapped
            results.append(x)
            unmapped.extend(other)

        return (results, unmapped)


@dataclass
class Maps:
    maps: list[Map]

    def map(self, intervals: Iterable[Interval]) -> Iterable[Interval]:
        results: list[Interval] = []
        remainder: Iterable[Interval] = list(intervals)
        for m in self.maps:
            (m_results, remainder) = m.yeet(remainder)
            results.extend(m_results)

        return itertools.chain(results, remainder)


@dataclass
class Almanac:
    seeds: list[Interval]
    maps: list[Maps]

    def map(self) -> Iterable[Interval]:
        res = self.seeds
        for m in self.maps:
            res = list(m.map(res))

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
    seed_intervals: list[Interval] = []
    for i in range(0, len(seeds), 2):
        seed_intervals.append(Interval(start=seeds[i], finish=seeds[i] + seeds[i + 1]))

    def parse_map(line: str) -> Map:
        [dest_start, source_start, length] = list(map(int, line.strip().split()))
        return Map(source_start=source_start, dest_start=dest_start, length=length)

    def parse_maps(chunk: list[str]) -> Maps:
        maps = list(map(parse_map, chunk[1:]))
        return Maps(maps=maps)

    maps = list(map(parse_maps, chunks[1:]))

    return Almanac(seeds=seed_intervals, maps=maps)


def part1(raw_input: str):
    almanac = parse_input(raw_input)

    new_seeds: list[Interval] = []
    for seed_interval in almanac.seeds:
        new_seeds.append(
            Interval(start=seed_interval.start, finish=seed_interval.start + 1)
        )

        new_seeds.append(
            Interval(
                start=seed_interval.finish - seed_interval.start,
                finish=(seed_interval.finish - seed_interval.start) + 1,
            )
        )

    almanac = Almanac(seeds=new_seeds, maps=almanac.maps)

    return min(map(lambda i: i.start, almanac.map()))


def part2(raw_input: str):
    almanac = parse_input(raw_input)
    return min(map(lambda i: i.start, almanac.map()))
