from functools import reduce
from pathlib import Path

from typing import Iterator, Literal, TypedDict, Union


INPUT_PATH = Path(__file__).parent / "input.txt"
SAMPLE_PATHS = [
    Path(__file__).parent / "sample1.txt",
]


class Number(TypedDict):
    kind: Literal["number"]
    value: int
    xSpan: tuple[int, int]
    y: int


class Symbol(TypedDict):
    kind: Literal["symbol"]
    x: int
    y: int
    value: str


SchematicObject = Union[Number, Symbol]


def parse_input(text: str) -> Iterator[SchematicObject]:
    for y, line in enumerate(text.splitlines(), 1):
        currentNumber = None
        for x, char in enumerate(line, 1):
            if char.isdigit():
                if currentNumber is None:
                    currentNumber = Number(
                        kind="number", value=int(char), xSpan=(x, x), y=y
                    )
                else:
                    currentNumber["value"] = (currentNumber["value"] * 10) + int(char)
                    currentNumber["xSpan"] = (currentNumber["xSpan"][0], x)
            else:
                if currentNumber is not None:
                    yield currentNumber
                    currentNumber = None

                if char == ".":
                    continue
                else:
                    yield Symbol(kind="symbol", x=x, y=y, value=char)

        # corner case: number touching end of line
        if currentNumber is not None:
            yield currentNumber
            currentNumber = None


def number_adjacent_coords(number: Number) -> Iterator[tuple[int, int]]:
    for x in range(number["xSpan"][0] - 1, number["xSpan"][1] + 2):
        for y in range(number["y"] - 1, number["y"] + 2):
            if y == number["y"] and (
                x >= number["xSpan"][0] and x <= number["xSpan"][1]
            ):
                continue
            yield (x, y)


def part1(raw_input: str):
    objs: list[SchematicObject] = list(parse_input(raw_input))
    symbols = [x for x in objs if x["kind"] == "symbol"]
    numbers = [x for x in objs if x["kind"] == "number"]
    symbol_positions = set(((symbol["x"], symbol["y"]) for symbol in symbols))

    def number_is_adjacent_any_symbol(number: Number):
        for coord in number_adjacent_coords(number):
            if coord in symbol_positions:
                return True

        return False

    numbers_with_adjacent_symbols = [
        number for number in numbers if number_is_adjacent_any_symbol(number)
    ]
    result = sum([number["value"] for number in numbers_with_adjacent_symbols])
    return result


def part2(raw_input: str):
    objs: list[SchematicObject] = list(parse_input(raw_input))
    symbols = [x for x in objs if x["kind"] == "symbol"]
    numbers = [x for x in objs if x["kind"] == "number"]

    gear_candidates: dict[tuple[int, int], list[Number]] = {
        (symbol["x"], symbol["y"]): [] for symbol in symbols if symbol["value"] == "*"
    }

    for number in numbers:
        for coord in number_adjacent_coords(number):
            if coord in gear_candidates:
                gear_candidates[coord].append(number)

    gear_ratios = [
        reduce(lambda x, y: x * y, map(lambda x: x["value"], v))
        for v in gear_candidates.values()
        if len(v) == 2
    ]
    return sum(gear_ratios)


if __name__ == "__main__":
    # print(part1(SAMPLE_PATHS[0].read_text()))
    print(part1(INPUT_PATH.read_text()))
    print(part2(INPUT_PATH.read_text()))
