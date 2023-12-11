# %%
import numpy as np

from helpers.load_puzzle import puzzle


# %%
def get_galaxies_coords(universe, expansion_factor):
    coords = np.argwhere(universe)
    new_coords = np.copy(coords)

    offset_x = np.where(np.sum(universe, axis=1) == 0)[0]
    offset_y = np.where(np.sum(universe, axis=0) == 0)[0]
    for x in offset_x:
        new_coords[coords[:, 0] >= x, 0] += expansion_factor - 1
    for y in offset_y:
        new_coords[coords[:, 1] >= y, 1] += expansion_factor - 1

    return new_coords


def pairwise_distance(coords):
    return np.sum(np.abs(coords[:, np.newaxis, :] - coords), axis=2)


def cumulated_distances(universe, expansion_factor):
    coords = get_galaxies_coords(universe, expansion_factor)
    return np.sum(pairwise_distance(coords)) // 2


# %%
with open(puzzle(11), "r") as f:
    data = f.read().splitlines()
    universe = np.array([[int(char == "#") for char in line] for line in data])

print("Part 1 —", cumulated_distances(universe, 2))
print("Part 2 —", cumulated_distances(universe, 1_000_000))

# %%
