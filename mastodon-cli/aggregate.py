import subprocess
from argparse import ArgumentParser
import time
import sys
from io import StringIO
import csv
from dataclasses import dataclass
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from typing import Union

ENCODING = "utf-8"

if sys.platform == "win32":
    ENCODING = "utf-16"

# 1: Write a method to plot the timestamps of statuses on the graph in the same way as the usernames. Add an argument to the ArgumentParser to choose username or status plotting.
# 2: Assignment / long exercise: subprocess.stdout.readline will get a single line from the output, returning None if there's no further output. Write an infinite version of the program which uses pull.py's --poll option to give a readout of the most frequent usernames and timestamps in the data that's been processed so far.

@dataclass
class Status:
    id: int
    timestamp: str
    username: str

def simplify_timestamp(timestamp: str) -> str:
    dt = datetime.strptime(timestamp,"%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.strftime("%Y-%m-%d %H:%M")

def read_csv(input_stream) -> list[Status]:
    reader = csv.reader(input_stream)
    statuses = []
    for ln in reader:
        # deal with ridiculous Windows console behaviours
        if len(ln) == 0: continue
        statuses.append(Status(
        int(ln[0]),
        simplify_timestamp(ln[2]),
        ln[1]    
    ))
    return statuses

def dedupe_statuses(statuses: list[Status]):
    id_set = set()
    output = []
    for status in statuses:
        if status.id in id_set:
            continue
        id_set.add(status.id)
        output.append(status)
    return output

def plot_users(statuses: list[Status], image_path: Union[str,None]):
    users = np.array([status.username for status in statuses])
    plt.hist(users)
    if image_path is None:
        plt.show()
    else:
        plt.savefig(image_path)

def main():
    parser = ArgumentParser()

    parser.add_argument("--output")
    parser.add_argument("--rate")
    parser.add_argument("--times")

    parsed = parser.parse_args()

    times = 3
    rate = 20

    if parsed.times is not None:
        times = int(parsed.times)

    if parsed.rate is not None:
        rate = int(parsed.rate)

    statuses = []

    for i in range(times):
        print(f"Pulling request {i+1}/{times}",end="\r")
        result = subprocess.run(["python","pull.py","mastodon.social","--format", "csv"], stdout=subprocess.PIPE)
        rows = read_csv(StringIO(result.stdout.decode(ENCODING)))
        statuses.extend(rows)
        if not i == (times - 1):
            time.sleep(rate)

    statuses = dedupe_statuses(statuses)

    print()
    print(f"Got {len(statuses)} statuses.")

    plot_users(statuses, parsed.output)

if __name__ == "__main__":
    main()
