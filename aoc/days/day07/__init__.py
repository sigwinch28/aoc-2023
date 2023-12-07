from collections import defaultdict
from dataclasses import dataclass
import pathlib
from typing import DefaultDict, Literal, Self

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
    joker: bool

    def __repr__(self):
        return self.name


@dataclass(frozen=True)
class Hand:
    cards: list[Card]
    bid: int

    def __repr__(self):
        cards_str = "".join(map(repr, self.cards))
        return f"{cards_str} {self.bid}"

    @property
    def type(self) -> HandType:
        """Determine the type of the hand, accounting for jokers.

        The general approach is:
        1. Count the number of jokers
        2. Count the occurrences of all cards excluding jokers, then add the
           number of jokers to each occurrence.
        3. Pick the highest count from (2) as the highest card.
        4. Count the occurrences of all cards excluding jokers and the card from
           (3).
        5. Pick the highest count from (4).
        6. Use the combination of (3,5) and check the value of that."""

        # count all the jokers in the hand
        jokers: DefaultDict[str, int] = defaultdict(int)
        for card in self.cards:
            if card.joker:
                jokers[card.name] += 1

        # The occurrences of all cards, plus the number of jokers.
        # For example, the hand 977JJ will be:
        # 7: 2 + 2 jokers = 4
        # 9: 1 + 2 jokers = 3
        # .
        cards_including_jokers: DefaultDict[str, int] = defaultdict(int)
        for card in self.cards:
            cards_including_jokers[card.name] += 1

        for card, count in jokers.items():
            for k in cards_including_jokers:
                if k == card:
                    continue
                cards_including_jokers[k] += count

        sorted_cards_including_jokers = sorted(
            cards_including_jokers.items(), reverse=True, key=lambda kv: kv[1]
        )
        (
            name_of_most_card_including_jokers,
            count_of_most_card_including_jokers,
        ) = sorted_cards_including_jokers[0]

        # The occurrences of all cards that are not jokers.
        # For example, the hand 977JJ will be:
        # 7: 2
        # 9: 1
        # .
        cards_excluding_jokers: DefaultDict[str, int] = defaultdict(int)
        for card in self.cards:
            if not card.joker:
                cards_excluding_jokers[card.name] += 1

        sorted_cards_excluding_jokers = sorted(
            (
                value
                for key, value in cards_excluding_jokers.items()
                if key != name_of_most_card_including_jokers
            ),
            reverse=True,
        )
        second_most_without_jokers = (
            sorted_cards_excluding_jokers[0] if sorted_cards_excluding_jokers else 0
        )

        match count_of_most_card_including_jokers, second_most_without_jokers:
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
    text: str, card_ranks: list[str], jokers: set[str] = set()
) -> list[Hand]:
    def parse_hand(line: str) -> Hand:
        [cards, bid] = line.split(" ")
        return Hand(
            cards=list(
                map(
                    lambda card: Card(
                        card, card_ranks.index(card), joker=card in jokers
                    ),
                    cards,
                )
            ),
            bid=int(bid),
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
    hands = parse_input(raw_input, card_ranks, jokers={"J"})

    return sum(
        i * card.bid for i, card in enumerate(sorted(hands, reverse=True), start=1)
    )
