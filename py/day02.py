# %%
from math import prod
import re

from helpers.load_puzzle import puzzle

# %%
N_COLORS = 3
COLORS = {"red": 0, "green": 1, "blue": 2}
MAXIMUM_BALLS_NUMBER = [12, 13, 14]

assert len(MAXIMUM_BALLS_NUMBER) == N_COLORS
assert len(COLORS) == N_COLORS


# %%
def parse_set(set_line):
    set = [0] * N_COLORS
    cubes_str = set_line.split(", ")
    for cube_str in cubes_str:
        count, color = cube_str.split(" ")
        set[COLORS[color]] = int(count)
    return set


def parse_game(game_line):
    game_id_str, sets_str = game_line.split(": ")
    game_id = int(re.search(r"\d+$", game_id_str).group())
    sets = [parse_set(set_line) for set_line in sets_str.split("; ")]
    return game_id, sets


def infer_minimum_set(sets):
    return [max(count) for count in zip(*sets)]


def is_game_possible(sets):
    min_balls_number = infer_minimum_set(sets)
    return all(
        min_balls_number[color] <= MAXIMUM_BALLS_NUMBER[color]
        for color in range(N_COLORS)
    )


# %%
if __name__ == "__main__":
    with open(puzzle(2)) as f:
        games = [parse_game(game) for game in f.read().splitlines()]

    possible_games = [game_id for game_id, sets in games if is_game_possible(sets)]
    minimum_set_powers = [prod(infer_minimum_set(sets)) for _, sets in games]

    print("Part 1 —", sum(possible_games))
    print("Part 2 —", sum(minimum_set_powers))

# %%
