from itertools import cycle


def parse_input(text: str) -> tuple[list[str], dict[str, tuple[str, str]]]:
    chunks = text.split("\n\n")
    instructions = list(chunks[0])
    graph: dict[str, tuple[str, str]] = {}

    for line in chunks[1].splitlines():
        name, pair = line.split(" = ")
        left, right = pair.strip("()").split(", ")
        graph[name] = (left, right)

    return (instructions, graph)


def part1(raw_input: str):
    instructions, graph = parse_input(raw_input)
    current = "AAA"
    for step, instruction in enumerate(cycle(instructions), start=0):
        if current == "ZZZ":
            return step

        left, right = graph[current]
        if instruction == "L":
            current = left
        elif instruction == "R":
            current = right
        else:
            raise ValueError(f"unknown instruction: {instruction}")


def part2(raw_input: str):
    input = parse_input(raw_input)
    return 0
