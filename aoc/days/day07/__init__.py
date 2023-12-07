from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property
from typing import DefaultDict, Literal, Optional, Self

HandType = Literal[
    "five_of_a_kind",
    "four_of_a_kind",
    "full_house",
    "three_of_a_kind",
    "two_pair",
    "one_pair",
    "high_card",
]
TYPE_RANKS: list[HandType] = [
    "five_of_a_kind",
    "four_of_a_kind",
    "full_house",
    "three_of_a_kind",
    "two_pair",
    "one_pair",
    "high_card",
]

CARD_RANKS: list[str] = [
    "A",
    "K",
    "Q",
    "J",
    "T",
    "9",
    "8",
    "7",
    "6",
    "5",
    "4",
    "3",
    "2",
]


@dataclass(frozen=True)
class Card:
    name: str
    value: int

    def __repr__(self):
        return self.name


@dataclass(frozen=True)
class Hand:
    cards: list[Card]
    bid: int
    joker: Optional[str]

    def __repr__(self):
        cards_str = "".join(map(repr, self.cards))
        return f"{cards_str} {self.bid}"

    @cached_property
    def type(self) -> HandType:
        jokers = (
            len([card for card in self.cards if card.name == self.joker])
            if self.joker
            else 0
        )

        frequencies: DefaultDict[str, int] = defaultdict(int)

        for card in self.cards:
            if self.joker is None or card.name != self.joker:
                frequencies[card.name] += 1

        frequencies_desc = sorted(
            frequencies.items(), reverse=True, key=lambda kv: kv[1]
        )
        if frequencies_desc:
            highest_name, highest_count = frequencies_desc[0]
            del frequencies[highest_name]
        else:
            highest_count = 0

        second_highest_count = (
            (sorted(frequencies.values(), reverse=True)[0]) if frequencies else 0
        )

        match highest_count + jokers, second_highest_count:
            case 5, _:
                return "five_of_a_kind"
            case 4, _:
                return "four_of_a_kind"
            case 3, 2:
                return "full_house"
            case 3, _:
                return "three_of_a_kind"
            case 2, 2:
                return "two_pair"
            case 2, _:
                return "one_pair"
            case _, _:
                return "high_card"

    def __lt__(self, other: Self) -> bool:
        if TYPE_RANKS.index(self.type) == TYPE_RANKS.index(other.type):
            for ours, theirs in zip(self.cards, other.cards):
                if ours.value == theirs.value:
                    continue

                return ours.value < theirs.value

            return False

        return TYPE_RANKS.index(self.type) < TYPE_RANKS.index(other.type)


def parse_input(
    text: str,
    card_ranks: list[str],
    joker: Optional[str] = None,
) -> list[Hand]:
    def parse_hand(line: str) -> Hand:
        [cards, bid] = line.split(" ")
        return Hand(
            cards=list(
                map(
                    lambda card: Card(card, card_ranks.index(card)),
                    cards,
                )
            ),
            bid=int(bid),
            joker=joker,
        )

    return [parse_hand(line) for line in text.splitlines()]


def part1(raw_input: str):
    card_ranks = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    hands = parse_input(raw_input, card_ranks)

    return sum(
        i * card.bid for i, card in enumerate(sorted(hands, reverse=True), start=1)
    )


def part2(raw_input: str):
    card_ranks = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
    hands = parse_input(raw_input, card_ranks, joker="J")

    return sum(
        i * card.bid for i, card in enumerate(sorted(hands, reverse=True), start=1)
    )
