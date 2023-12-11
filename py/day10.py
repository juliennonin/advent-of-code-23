# %%
import re

from helpers.load_puzzle import puzzle

# %%
NORTH = {"L": "E", "|": "S", "J": "W"}
EAST = {"L": "N", "F": "S", "-": "W"}
SOUTH = {"7": "W", "|": "N", "F": "E"}
WEST = {"J": "N", "-": "E", "7": "S"}
NEXT_DIRECTIONS = {
    "N": (-1, 0, SOUTH),
    "E": (0, 1, WEST),
    "S": (1, 0, NORTH),
    "W": (0, -1, EAST),
}


# %%
def get_starting_direction(grid):
    [(x_start, y_start)] = [
        (i, j) for i, l in enumerate(grid) if (j := l.find("S")) != -1
    ]

    for direction, (dx, dy, next_direction) in NEXT_DIRECTIONS.items():
        x, y = x_start + dx, y_start + dy
        if (
            0 <= x < len(grid)
            and 0 <= y < len(grid[0])
            and grid[x][y] in next_direction.keys()
        ):
            return x, y, next_direction

    raise ValueError("No starting direction found")


def loop_size(grid):
    x, y, direction = get_starting_direction(grid)
    print("start", direction)

    loop = [set() for _ in range(len(grid))]
    print(x, y)
    loop[x].add(y)
    distance = 1

    new_grid = [['.'] * len(grid[0]) for _ in range(len(grid))]
    new_grid[x][y] = grid[x][y]
    print(new_grid)

    while (tile := grid[x][y]) != "S":
        distance += 1
        # if tile != "-":
        dx, dy, direction = NEXT_DIRECTIONS[direction[tile]]
        x, y = x + dx, y + dy
        if grid[x][y] != "-":
            loop[x].add(y)
            new_grid[x][y] = grid[x][y]
    print("end", direction, x, y, grid)


    return distance, new_grid


# %%
def remove_corners(line):
    line = re.sub(r'F\.*7', '', line)
    line = re.sub(r'L\.*J', '', line)
    line = re.sub(r'F\.*J', '|', line)
    line = re.sub(r'L\.*7', '|', line)
    return line


# %%
with open(puzzle(10), "r") as f:
    grid = f.read().splitlines()
    # [(x_start, y_start)] = [
    #     (i, j) for i, l in enumerate(lines) if (j := l.find("S")) != -1
    # ]
    # grid = [list(line) for line in lines]


# %%
distance, new_grid = loop_size(grid)

[(x_start, y_start)] = [
    (i, j) for i, l in enumerate(grid) if (j := l.find("S")) != -1
]
new_grid[x_start][y_start] = "7"
new_grid = [remove_corners(''.join(line)) for line in new_grid]
new_grid

count = 0
for line in new_grid:
    idx = [i for i, c in enumerate(line) if c == '|']
    c = sum([b - a - 1 for a, b in zip(idx[0::2], idx[1::2])])
    count += c


# %%
print("Part 1 —", distance // 2)
print("Part 2 —", count)

# %%
print("".join(f" {str(i).zfill(2)}" for i in range(len(grid[0]))))
for l in new_grid:
    print(
        # "".join(l)
        l.replace("-", "═══")
        .replace("|", " ║ ")
        .replace("7", "═╗ ")
        .replace("F", " ╔═")
        .replace("L", " ╚═")
        .replace("J", "═╝ ")
        .replace(".", " ⋅ ")
        .replace("S", "???")
    )

# %%


# %%
