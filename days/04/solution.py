from collections import defaultdict
from pathlib import Path

from typing import Iterator, Literal, TypedDict, Union


INPUT_PATH = Path(__file__).parent / "input.txt"
SAMPLE_PATHS = [
    Path(__file__).parent / "sample1.txt",
]


class Card(TypedDict):
    number: int
    left_side: set[int]
    right_side: set[int]


def parse_input(text: str) -> Iterator[Card]:
    for line in text.splitlines():
        [meta, contents] = line.split(":", maxsplit=1)
        card_number = int(meta.rsplit()[1])
        [lhs, rhs] = contents.split("|", maxsplit=1)
        left_side = set(map(int, lhs.strip().split()))
        right_side = set(map(int, rhs.strip().split()))

        yield Card(number=card_number, left_side=left_side, right_side=right_side)


def num_matches(card: Card) -> int:
    return len(card["left_side"] & card["right_side"])


def part1(raw_input: str):
    def result(card: Card):
        matches = num_matches(card)
        score = 0
        if matches > 0:
            score = pow(2, matches - 1)
        return score

    cards = parse_input(raw_input)

    return sum(map(result, cards))


def part2(raw_input: str):
    cards = parse_input(raw_input)

    matches = {card["number"]: num_matches(card) for card in cards}

    copies_won: defaultdict[int, int] = defaultdict(lambda: 1)
    for card_num in sorted(matches):
        copies = copies_won[card_num]
        # print(f"Card {card_num} with {copies} instances")
        for i in range(card_num + 1, card_num + matches[card_num] + 1):
            # print(f"  wins {copies} copies of {i}")
            copies_won[i] += copies

    return sum(list(copies_won.values()))


if __name__ == "__main__":
    # print(part1(SAMPLE_PATHS[0].read_text()))
    print(part1(INPUT_PATH.read_text()))
    # print(part2(SAMPLE_PATHS[0].read_text()))
    print(part2(INPUT_PATH.read_text()))
