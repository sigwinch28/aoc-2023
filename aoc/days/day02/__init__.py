from functools import partial, reduce
from typing import Iterable, Literal, TypedDict, NotRequired


class Round(TypedDict):
    red: NotRequired[int]
    green: NotRequired[int]
    blue: NotRequired[int]


class Game(TypedDict):
    ident: int
    rounds: Iterable[Round]


def parse_round(s: str) -> Round:
    result: Round = {}
    for yeet in s.split(","):
        [count, color] = yeet.strip().split(" ")
        if color == "red" or color == "green" or color == "blue":
            result[color] = int(count)
    return result


def parse_input(text: str) -> Iterable[Game]:
    for line in text.splitlines():
        [game_id_str, rounds] = line.split(":", maxsplit=1)
        game_id = int(game_id_str.split()[1])
        rounds = list(map(parse_round, rounds.split(";")))
        yield Game(ident=game_id, rounds=rounds)

    pass


def part1(raw_input: str):
    games = parse_input(raw_input)

    def ok_game(game: Game) -> bool:
        return all(
            map(
                lambda round: round.get("red", 0) <= 12
                and round.get("green", 0) <= 13
                and round.get("blue", 0) <= 14,
                game["rounds"],
            )
        )

    ok_games = filter(ok_game, games)

    return sum(map(lambda game: game["ident"], ok_games))


def part2(raw_input: str):
    games = parse_input(raw_input)

    def max_needed_of_color(game: Game, color: Literal["red", "green", "blue"]) -> int:
        return max(map(lambda round: round.get(color, 0), game["rounds"]), default=0)

    def power(game: Game) -> int:
        return reduce(
            lambda x, y: x * y,
            map(partial(max_needed_of_color, game), ["red", "green", "blue"]),
        )

    return sum(map(power, games))
