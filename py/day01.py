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
DIGITS_PATTERN = rf"\d|{'|'.join(DIGITS.keys())}"
DIGITS_PATTERN_INV = rf"\d|{'|'.join(digit[::-1] for digit in DIGITS.keys())}"


# %%
def find_calibration_values(data, with_spelled_digits):
    calibration_values = []
    pattern = DIGITS_PATTERN if with_spelled_digits else r"\d"
    pattern_inv = DIGITS_PATTERN_INV if with_spelled_digits else r"\d"
    for line in data:
        match1 = re.search(pattern, line).group()  # first digit
        match2 = re.search(pattern_inv, line[::-1]).group()[::-1]  # last digit

        v1 = DIGITS.get(match1, match1)
        v2 = DIGITS.get(match2, match2)
        calibration_values.append(int(v1 + v2))

    return sum(calibration_values)


# %%
if __name__ == "__main__":
    with open(puzzle(1), "r") as f:
        data = f.read().splitlines()

    print("Part 1 —", find_calibration_values(data, with_spelled_digits=False))
    print("Part 2 —", find_calibration_values(data, with_spelled_digits=True))
