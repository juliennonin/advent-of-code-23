# %%
import numpy as np

from helpers.load_puzzle import puzzle


# %%
def predict_next_value(history):
    if np.all(history == 0):
        return 0
    else:
        return history[-1] + predict_next_value(np.diff(history))


# %%
with open(puzzle(9), "r") as f:
    report = [list(map(int, line.split(" "))) for line in f.read().splitlines()]

print("Part 1 —", sum(map(predict_next_value, report)))

# %%
