# %%
import re

from helpers.load_puzzle import puzzle

DIGITS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


# %%
def replace_spelled_digits(line):
    for spelled_digit, digit in DIGITS.items():
        # Both sides are kept in case of portmeanteaus
        # For example "eightwone" → "eight8eightwo2twone1one"
        line = line.replace(spelled_digit, f"{spelled_digit}{digit}{spelled_digit}")
    return line


# %%
def find_calibration_values(data, with_spelled_digits):
    calibration_values = []
    for line in data:
        if with_spelled_digits:
            line = replace_spelled_digits(line)

        v1 = re.search(r"\d", line).group()  # first digit
        v2 = re.search(r"\d", line[::-1]).group()  # last digit
        calibration_values.append(int(v1 + v2))

    return sum(calibration_values)


# %%
if __name__ == "__main__":
    with open(puzzle(1), "r") as f:
        data = f.read().splitlines()

    print("Part 1 —", find_calibration_values(data, with_spelled_digits=False))
    print("Part 2 —", find_calibration_values(data, with_spelled_digits=True))
