# %%
from itertools import combinations, combinations_with_replacement
import re
from math import factorial

from helpers.load_puzzle import puzzle


# %%
def parse_line(line):
    records, griddlers = line.split(" ")
    return records, eval("[" + griddlers + "]")


def unfold(records, griddlers, factor=5):
    return '?'.join([records] * factor), [*griddlers] * factor


def check_arrangement_against_griddlers(arrangement, griddlers_truth):
    griddlers = []
    for m in re.finditer(r"#+", arrangement):
        griddlers.append(m.span()[1] - m.span()[0])
    return len(griddlers) == len(griddlers_truth) and all(
        [a == b for a, b in zip(griddlers, griddlers_truth)]
    )


def check_arrangement_against_records(arrangement, records):
    if len(arrangement) != len(records):
        return False
    for a, r in zip(arrangement, records):
        if r == "?":
            continue
        if a != r:
            return False
    return True


def create_arrangement(records, positions):
    arrangement = list(records.replace("?", "."))
    for i in positions:
        arrangement[i] = "#"
    return "".join(arrangement)


def count_valid_arrangements_brute_force(records, griddlers, debug=False):
    k = sum(griddlers) - records.count("#")
    n = records.count("?")
    print(n, k)
    # print(
    #     f"Checking {factorial(n) / factorial(k) / factorial(n - k):.0f} combinations."
    # )

    count = 0
    for positions in combinations(
        [m.span()[0] for m in re.finditer(r"\?", records)], k
    ):
        arrangement = create_arrangement(records, positions)
        if check_arrangement_against_griddlers(arrangement, griddlers):
            if debug:
                print(arrangement)
            count += 1
    return count


# %%
with open(puzzle(12), "r") as f:
    data = list(map(parse_line, f.read().splitlines()))


# print("Part 1 –", sum([count_valid_arrangements_brute_force(*d) for d in data]))
print("Part 1 –", sum([count_valid_arrangements(*d) for d in data]))

part2 = 0
for i, d in enumerate(data):
    c = count_valid_arrangements(*unfold(*d))
    print(i, c)
    part2 += c
# print("Part 2 –", sum([count_valid_arrangements(*unfold(*d)) for d in data]))
print("Part 2 –", part2)

# %%
%%timeit
for i, d in enumerate(data):
    # naive = count_valid_arrangements_brute_force(*d)  # 3.49 s ± 307 ms
    smarter = count_valid_arrangements(*d)  # 89.3 ms ± 3.06 ms
    # assert naive == smarter, f"{naive} != {smarter}, line {i}: {d}"


# %%

d = []
for i, (records, griddlers) in enumerate(data):
    n = records.count("?")
    k = sum(griddlers) - records.count("#")
    print(n, k)
    d.append(factorial(n) / factorial(k) / factorial(n - k))
d = np.array(d, dtype=int)

# %%
s = []
for i, (records, griddlers) in enumerate(data):
    r = len(records) - sum(griddlers) - len(griddlers) + 1  # spaces to be placed
    n = len(griddlers) + 1  # available spaces
    s.append(factorial(n + r - 1) / factorial(r) / factorial(n - 1))
s = np.array(s, dtype=int)

# %%
records, griddlers = "##????.?.###.?", [2, 1, 3]
# %%
records, griddlers = "?.???????.???.???", [1, 2, 3, 2]
(1, 7, 3, 3)

# %%
records, griddlers = "?????#???????#???", [1, 1, 3, 6]
(5, 7, 3)

# %%
records, griddlers = "?#?????#??##??????.?", [3, 9, 1, 1]
(18, 1)

# %%
records, griddlers = "?###?#?????.????#?#?", [10, 4]
(11, 8)

# %%
n = records.count("?")
k = sum(griddlers) - records.count("#")


# %%
# %%
def extract_tiles(records):
    tiles = []
    for m in re.finditer(r"(\?|#)+", records):
        tiles.append(records[slice(*m.span())])
    return tiles


# %%


def count_tile_arrangements(tile, griddlers, debug=False):
    if not griddlers:
        return 0 if "#" in tile else 1
        # print('  ', '.' * len(tile))
        # return 1

    r = len(tile) - sum(griddlers) - len(griddlers) + 1  # spaces to be placed
    n = len(griddlers) + 1  # available spaces
    count = 0
    print(factorial(n + r - 1) / factorial(r) / factorial(n - 1))

    for c in combinations_with_replacement(range(n), r):
        # print('  c', c)
        dots = [1] * n
        dots[0] = 0
        dots[-1] = 0
        for j in c:
            dots[j] += 1
        arrangement = "".join(
            ["." * d + "#" * g for d, g in zip(dots, griddlers + [0])]
        )
        # assert check_arrangement_against_griddlers(arrangement, griddlers), f"{n}, {r}, {arrangement}, {griddlers}"
        if check_arrangement_against_records(arrangement, tile):
            if debug:
                print('  ', arrangement)
            count += 1
    # print(factorial(n + r - 1) / factorial(r) / factorial(n - 1))
    return count


# %%
def make_groups(tiles_length, numbers):
    if len(numbers) == 0:
        return [[[] for _ in range(len(tiles_length))]]

    n = numbers[0]
    new_arrangements = []
    for i, t in enumerate(tiles_length):
        if t < n:
            continue

        arrangements = make_groups(
            [0] * i + [max(0, tiles_length[i] - n - 1)] + tiles_length[i + 1 :],
            numbers[1:],
        )
        for res in arrangements:
            if not res:
                continue
            res[i].insert(0, n)

        new_arrangements.extend(arrangements)
    return new_arrangements


# for g in make_groups([18, 4, 1], [3, 9, 1, 1]):
#     print(g)


# %%
def count_valid_arrangements(records, griddlers, debug=False):
    tiles = extract_tiles(records)
    count = 0
    for group in make_groups([len(t) for t in tiles], griddlers):
        assert len(group) == len(tiles)
        if debug:
            print()
        s = 1
        for g, t in zip(group, tiles):
            if debug:
                print('\n', t, g)

            s *= count_tile_arrangements(t, g, debug)
        if debug:
            print('s', s)
        count += s
    return count


# %%


# make_groups((18, 4, 1), [3, 9, 1, 1])
#     make_groups((14, 4, 1), [9, 1, 1])
#         make_groups((4, 4, 1), [1, 1])
#             make_groups((2, 4, 1), [1])
#                 make_groups((1, 4, 1), [])
#                 (1), (), () --> (1, 1), (), ()
#                 (), (1), () --> (1), (1), ()
#                 (), (), (1) --> (1), (1), ()
#             make_groups((2, 1), [1])
#                 (1), () --> (), (1, 1), ()
#                 (), (1) --> (), (1), (1)
#     make_groups((0, 1), [9, 1, 1]))
#         None

# %%
R, G = ('?#?????#?????#?????#?????#?????#?????#?????#?????#?????#???',
 [2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1])

# 10 à placer parmi 49 emplacements

# %%
