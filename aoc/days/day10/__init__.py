from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict, Iterable, TypeAlias

Coord: TypeAlias = tuple[int, int]


@dataclass(frozen=True)
class Token:
    x: int
    y: int
    value: str

    @property
    def coord(self):
        return (self.x, self.y)

    @property
    def north(self):
        return (self.x, self.y - 1)

    @property
    def south(self):
        return (self.x, self.y + 1)

    @property
    def east(self):
        return (self.x + 1, self.y)

    @property
    def west(self):
        return (self.x - 1, self.y)


def parse_input(text: str) -> tuple[Coord, dict[Coord, set[Coord]]]:
    def tokenize(text: str) -> Iterable[Token]:
        for y, line in enumerate(text.splitlines(), 1):
            for x, value in enumerate(list(line), 1):
                yield Token(x, y, value)

    start: tuple[int, int] | None = None
    outgoing: DefaultDict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)

    for token in tokenize(text):
        match token.value:
            case "S":
                start = (token.x, token.y)
                outgoing[token.coord].add(token.north)
                outgoing[token.coord].add(token.south)
                outgoing[token.coord].add(token.west)
                outgoing[token.coord].add(token.east)
            case "|":
                outgoing[token.coord].add(token.north)
                outgoing[token.coord].add(token.south)
            case "-":
                outgoing[token.coord].add(token.west)
                outgoing[token.coord].add(token.east)
            case "L":
                outgoing[token.coord].add(token.north)
                outgoing[token.coord].add(token.east)
            case "J":
                outgoing[token.coord].add(token.north)
                outgoing[token.coord].add(token.west)
            case "7":
                outgoing[token.coord].add(token.south)
                outgoing[token.coord].add(token.west)
            case "F":
                outgoing[token.coord].add(token.south)
                outgoing[token.coord].add(token.east)
            case ".":
                pass
            case _:
                raise ValueError(f"unknown token: {token}")

    assert start is not None
    graph: DefaultDict[Coord, set[Coord]] = defaultdict(set)

    for src in outgoing:
        for dest in outgoing[src]:
            if dest in outgoing and src in outgoing[dest]:
                graph[src].add(dest)

    return (start, dict(graph))


def part1(raw_input: str):
    start, graph = parse_input(raw_input)
    starts = graph[start]
    assert len(starts) == 2
    paths: list[list[Coord]] = []
    for next in starts:
        path: list[Coord] = []
        prev = start
        current = next
        while current != start:
            path.append(current)
            nexts = graph[current] - set((prev,))
            assert len(nexts) == 1
            prev = current
            current = nexts.pop()

        paths.append(path)

    assert len(paths) == 2
    assert paths[0] == list(reversed(paths[1]))

    return (len(paths[0]) + 1) // 2


def part2(raw_input: str):
    input = parse_input(raw_input)
    return 0
