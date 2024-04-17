from argparse import ArgumentParser
import csv

# our .csv is a record of server failures

# each record is laid out as:
# [server_id, timestamp, cause_of_failure]

# ---

# tasks to complete

# 1: Make --servers correctly log out the number of times each server failed
# 2: Make --causes correctly log out the frequency of each cause
# 3: Add two more filters: min and max. max should filter out records with timestamps smaller than it, min should filter out records with timestamps larger than it
# 4: Write another function --hour which logs out each hour of the day in order, along with the number of failures in it. It should work with min and max.

def get_causes(rows):    
    # 2: make --causes correctly log out the frequency of each cause
    pass

def get_servers(rows):
    counts = {}
    for row in rows:
        if row[0] not in counts:
            counts[row[0]] = 0
        counts[row[0]] += 1

    for server, down in counts.items():
        print(f"Server {server} was down {down} times")

def parse_logs(path, select=None, causes=False, servers=False):
    table = []
    with open(path, "r") as f:
        reader = csv.reader(f)
        next(reader) # skip the file header
        for line in reader:
            table.append(line)

    if select != None:
        to_select = select.split()
        table = filter(lambda row: row[0] in to_select, table)

    # 3: add two more filters: min and max.

    # 1: make --servers correctly log out the number of times each server failed
    # 2: make --causes correctly log out the frequency of each cause

def main():
    parser = ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--select")
    parser.add_argument("--causes", action="store_true")
    # 1: make --servers correctly log out the number of times each server failed

    args = parser.parse_args()

    parse_logs(args.path, args.select, args.causes, args.servers)

if __name__ == "__main__":
    main()
