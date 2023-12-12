# %%
from itertools import combinations
import re
from math import factorial

from helpers.load_puzzle import puzzle


# %%
def parse_line(line):
    records, griddlers = line.split(" ")
    return records, eval("[" + griddlers + "]")


def check_arrangement(arrangement, griddlers_truth):
    griddlers = []
    for m in re.finditer(r"#+", arrangement):
        griddlers.append(m.span()[1] - m.span()[0])
    return len(griddlers) == len(griddlers_truth) and all(
        [a == b for a, b in zip(griddlers, griddlers_truth)]
    )


def create_arrangement(records, positions):
    arrangement = list(records.replace("?", "."))
    for i in positions:
        arrangement[i] = "#"
    return "".join(arrangement)


def count_valid_arrangement(line):
    records, griddlers = parse_line(line)
    k = sum(griddlers) - records.count("#")
    count = 0

    for positions in combinations(
        [m.span()[0] for m in re.finditer(r"\?", records)], k
    ):
        arrangement = create_arrangement(records, positions)
        if check_arrangement(arrangement, griddlers):
            count += 1
    return count


# %%
with open(puzzle(12), "r") as f:
    data = f.read().splitlines()

print("Part 1 –", sum(map(count_valid_arrangement, data)))

# %%
