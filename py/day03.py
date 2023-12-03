# %%
import re
from collections import defaultdict

from helpers.load_puzzle import puzzle


# %%
def get_neighbors_pos(x, y1, y2):
    yield (x, y1 - 1)
    yield (x, y2)
    for j in range(y1 - 1, y2 + 1):
        yield (x - 1, j)
        yield (x + 1, j)


def get_neighbors(data, x, y1, y2):
    X, Y = len(data), len(data[0])
    for i, j in get_neighbors_pos(x, y1, y2):
        if 0 <= i < X and 0 <= j < Y:
            yield i, j, data[i][j]


def find_part_numbers_and_gears(data):
    part_numbers = []
    gears_parts = defaultdict(list)
    for x, line in enumerate(data):
        for match in re.finditer(r"\d+", line):
            y1, y2 = match.span()
            number = int(match.group())
            has_neighbors = False
            for ni, nj, nvalue in get_neighbors(data, x, y1, y2):
                if nvalue != ".":
                    has_neighbors = True
                if nvalue == "*":
                    gears_parts[(ni, nj)].append(number)
            if has_neighbors:
                part_numbers.append(number)
    return part_numbers, gears_parts


# %%
if __name__ == "__main__":
    with open(puzzle(3), "r") as f:
        data = f.read().splitlines()

    part_numbers, gears_parts = find_part_numbers_and_gears(data)
    gears_ratios = [
        numbers[0] * numbers[1]
        for _, numbers in gears_parts.items()
        if len(numbers) == 2
    ]

    print("Part 1 —", sum(part_numbers))
    print("Part 2 —", sum(gears_ratios))

# %%
