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


def tokenize(text: str) -> Iterable[Token]:
    for y, line in enumerate(text.splitlines(), 1):
        for x, value in enumerate(list(line), 1):
            yield Token(x, y, value)


def parse_input(text: str) -> tuple[Coord, dict[Coord, set[Coord]]]:
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


def find_loop(start: Coord, graph: dict[Coord, set[Coord]]):
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

    return [start] + paths[0]


def part1(raw_input: str):
    start, graph = parse_input(raw_input)
    loop = find_loop(start, graph)
    return (len(loop)) // 2


def part2(raw_input: str):
    start, graph = parse_input(raw_input)
    if graph[start] == {(start[0], start[1] + 1), (start[0], start[1] - 1)}:
        start_char = "|"
    elif graph[start] == {(start[0] - 1, start[1]), (start[0] + 1, start[1])}:
        start_char = "-"
    elif graph[start] == {(start[0] + 1, start[1]), (start[0], start[1] + 1)}:
        start_char = "F"
    elif graph[start] == {(start[0] - 1, start[1]), (start[0], start[1] - 1)}:
        start_char = "J"
    elif graph[start] == {(start[0] + 1, start[1]), (start[0], start[1] - 1)}:
        start_char = "L"
    elif graph[start] == {(start[0] - 1, start[1]), (start[0], start[1] + 1)}:
        start_char = "7"
    else:
        raise ValueError("unknown start char")

    loop = find_loop(start, graph)
    tiles_in_loop = []

    for y, line in enumerate(raw_input.splitlines(), 1):
        in_loop = False
        last_corner = None
        for x, char in enumerate(list(line), 1):
            if (x, y) == start:
                char = start_char
            if (x, y) in loop:
                match char:
                    case "|":
                        in_loop = not in_loop
                    case "F" | "L":
                        last_corner = char
                    case "7" | "J":
                        assert last_corner
                        expected = "F" if char == "J" else "L"
                        if last_corner == expected:
                            in_loop = not in_loop
                        last_corner = None
                    case "-":
                        pass
                    case _:
                        raise ValueError("bork")
            elif in_loop:
                tiles_in_loop.append((x, y))

    return len(tiles_in_loop)
