from argparse import ArgumentParser
from sys import stdin
from dataclasses import dataclass
import json
import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# CONCEPTS:
# dataclasses
# reading from CLI pipes (stdin) or files; convention
# outputting visualisations with MatPlotLib.
# datetime manipulation

# 1: csv.reader and json.load share a common interface with csv.writer and json.dumps. Create a list of Status objects from the csv or JSON output of pull.py in the functions read_csv and read_json. Make sure to use the simplify_timestamp function as we'll need simpler timestamps later.
# 2: By UNIX convention, giving the - argument for a filename represents reading from stdin. Let the script take - as a filename and read from stdin when this argument is supplied. stdin should act like a file handle.
# 3: We plot the times when statuses were posted using plot_timestamps, which uses the popular MatPlotLib library. Make it so that we can plot usernames by supplying the 'users' argument on the command line.
# 4: We often get duplicates of user statuses when we read more than once from the same timeline. The Python set() type lets us store unique values which can't repeat. Fill out the dedupe_statuses function to avoid counting identical statuses more than once.

# Next time: looking at orchestrating these processes using the subprocess library. (JSON is problematic.)

@dataclass
class Status:
    id: int
    timestamp: str
    username: str

def plot_timestamps(statuses: list[Status]):
    ts = np.array([status.timestamp for status in statuses])
    plt.hist(ts)
    plt.show()

def plot_users(statuses: list[Status]):
    # 3
    pass

def simplify_timestamp(timestamp: str) -> str:
    dt = datetime.strptime(timestamp,"%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.strftime("%Y-%m-%d %H:%M")

def read_csv(input_stream) -> list[Status]:
    # 1
    return []

def read_json(input_stream) -> list[Status]:
    # 1
    return []

def dedupe_statuses(statuses: list[Status]) -> list[Status]:
    id_set = set()
    output = []
    return output

def main():
    parser = ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("format", choices=("json","csv"))
    parser.add_argument("plot", choices=("users","timestamps"))

    parsed = parser.parse_args()

    # 2
    input_stream = open(parsed.filename, "r")

    statuses = []
    if parsed.format == "json":
        statuses = read_json(input_stream)
    elif parsed.format == "csv":
        statuses = read_csv(input_stream)

    # 4

    plot_timestamps(statuses)

if __name__ == "__main__":
    main()
