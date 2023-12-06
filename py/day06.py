# %%
import re
import math

from helpers.load_puzzle import puzzle


# %%
def number_of_new_records(time, record):
    delta_sqrt = math.sqrt(time * time - 4 * record)
    min_waiting_time = math.floor((time - delta_sqrt) / 2)
    max_waiting_time = math.ceil((time + delta_sqrt) / 2)

    return max_waiting_time - min_waiting_time - 1


# %%
if __name__ == "__main__":
    with open(puzzle(6), "r") as f:
        time_line, record_line = f.read().splitlines()

    times = list(map(int, re.findall(r"\d+", time_line)))
    records = list(map(int, re.findall(r"\d+", record_line)))

    print("Part 1 —", math.prod(map(number_of_new_records, times, records)))

# %%
