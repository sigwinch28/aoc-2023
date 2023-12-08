from itertools import count, cycle
from math import lcm
from tracemalloc import start
from typing import Callable


def parse_input(text: str) -> tuple[list[str], dict[str, tuple[str, str]]]:
    chunks = text.split("\n\n")
    instructions = list(chunks[0])
    graph: dict[str, tuple[str, str]] = {}

    for line in chunks[1].splitlines():
        name, pair = line.split(" = ")
        left, right = pair.strip("()").split(", ")
        graph[name] = (left, right)

    return (instructions, graph)


def solve(
    instructions: list[str],
    graph: dict[str, tuple[str, str]],
    starting_set: set[str],
    end_condition: Callable[[str], bool],
):
    def reachable_nodes(node: str):
        seen: set[tuple[str, int]] = set()
        result: set[tuple[str, int, int]] = set()
        current = node
        cycles = -1
        for step, instruction in cycle(enumerate(instructions)):
            if step == 0:
                cycles += 1
            if (current, step) in seen:
                # cycle found
                break

            seen.add((current, step))
            result.add((current, step, cycles))

            if instruction == "L":
                current = graph[current][0]
            elif instruction == "R":
                current = graph[current][1]
            else:
                raise ValueError(f"unknown instruction: {instruction}")

        return {item for item in result if end_condition(item[0])}

    reachability = [reachable_nodes(node) for node in starting_set]

    common_delta: int = 0
    for delta in count():
        if all(
            any(item[1] == delta for item in reachables) for reachables in reachability
        ):
            common_delta = delta
            break

    reachability = [
        {item for item in v if item[1] == common_delta} for v in reachability
    ]

    assert all(len(reachable) == 1 for reachable in reachability)

    return (
        lcm(*[reachable.pop()[2] for reachable in reachability]) * len(instructions)
    ) + common_delta


def part1(raw_input: str):
    instructions, graph = parse_input(raw_input)
    return solve(instructions, graph, {"AAA"}, end_condition=lambda x: x == "ZZZ")


def part2(raw_input: str):
    instructions, graph = parse_input(raw_input)
    starting = {node for node in graph if node.endswith("A")}
    return solve(
        instructions,
        graph,
        starting_set=starting,
        end_condition=lambda x: x.endswith("Z"),
    )
