from collections import defaultdict
from dataclasses import dataclass
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
class Hand:
    cards: list[int]
    bid: int

    def __repr__(self):
        cards_str = "".join(map(lambda i: CARD_RANKS[i], self.cards))
        return f"{cards_str} {self.bid}"

    @property
    def type(self) -> HandType:
        cards: DefaultDict[int, int] = defaultdict(int)
        for card in self.cards:
            cards[card] += 1

        card_counts = sorted(cards.values(), reverse=True)

        match card_counts[0], card_counts[1] if len(card_counts) > 1 else 0:
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
                if ours == theirs:
                    continue

                return ours < theirs

            return False

        return TYPE_RANKS.index(self.type) < TYPE_RANKS.index(other.type)


def parse_input(text: str) -> list[Hand]:
    def parse_hand(line: str) -> Hand:
        [cards, bid] = line.split(" ")
        return Hand(
            cards=list(map(lambda card: CARD_RANKS.index(card), cards)), bid=int(bid)
        )

    return [parse_hand(line) for line in text.splitlines()]


def part1(raw_input: str):
    hands = parse_input(raw_input)

    return sum(
        i * card.bid for i, card in enumerate(sorted(hands, reverse=True), start=1)
    )


def part2(raw_input: str):
    input = parse_input(raw_input)
    return 0


if __name__ == "__main__":
    [hand1, hand2] = parse_input("KK677 28\nKTJJT 220")
    print(hand1)
    print(hand2)
    print(hand1.type)
    print(hand2.type)
    print(hand2.__lt__(hand1))
