# %%
import numpy as np

from helpers.load_puzzle import puzzle

# %%
with open(puzzle(11), 'r') as f:
    data = f.read().splitlines()
    grid = np.array([[int(char == '#') for char in line] for line in data])

# %%
grid = np.insert(grid, np.where(np.sum(grid, axis=0) == 0)[0], 0, axis=1)
grid = np.insert(grid, np.where(np.sum(grid, axis=1) == 0)[0], 0, axis=0)


coords = np.argwhere(grid)
distances = np.sum(np.abs(coords[:, np.newaxis, :] - coords), axis=2)

print("Part 1 —", np.sum(distances) // 2)

# %%

