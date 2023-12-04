# %%
import re
from math import floor

from helpers.load_puzzle import puzzle


# %%
def get_number_of_winning_numbers(card):
    _, card_numbers = card.split(": ")
    winning_str, numbers_str = card_numbers.split(" | ")

    winning_numbers = set(map(int, re.findall(r"\d+", winning_str)))
    my_numbers = set(map(int, re.findall(r"\d+", numbers_str)))

    return len(winning_numbers & my_numbers)


def get_cards_point(cards_winning_numbers):
    return [
        floor(2 ** (number_of_winning_numbers - 1))
        for number_of_winning_numbers in cards_winning_numbers
    ]


def get_cards_instances_number(cards_winning_numbers):
    total_scratch_cards = [1] * len(cards_winning_numbers)
    for i in range(len(total_scratch_cards)):
        for j in range(i + 1, i + cards_winning_numbers[i] + 1):
            total_scratch_cards[j] += total_scratch_cards[i]
    return total_scratch_cards


# %%
if __name__ == "__main__":
    with open(puzzle(4), "r") as f:
        data = f.read().splitlines()
    cards_winning_numbers = [get_number_of_winning_numbers(card) for card in data]

    print("Part 1 —", sum(get_cards_point(cards_winning_numbers)))
    print("Part 2 —", sum(get_cards_instances_number(cards_winning_numbers)))

# %%
