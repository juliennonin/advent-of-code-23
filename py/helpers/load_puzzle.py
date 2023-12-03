import os
import requests
from dotenv import load_dotenv

load_dotenv()

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "../../data")
AOC_SESSION_COOKIE = os.environ["AOC_SESSION_COOKIE"]


def download_puzzle(day_num, file_name):
    url = f"https://adventofcode.com/2023/day/{day_num}/input"
    cookies = {"session": AOC_SESSION_COOKIE}

    r = requests.get(url, cookies=cookies)
    if r.status_code == 200:
        with open(os.path.join(DATA_FOLDER, file_name), "w") as f:
            f.write(r.text)
    else:
        raise Exception(f"Error downloading puzzle: {r.status_code}")


def puzzle(day_num):
    file_name = f"day{str(day_num).zfill(2)}.txt"

    if file_name not in os.listdir(DATA_FOLDER):
        download_puzzle(day_num, file_name)

    assert file_name in os.listdir(DATA_FOLDER)
    return os.path.join(DATA_FOLDER, file_name)
