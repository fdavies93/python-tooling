from argparse import ArgumentParser
import csv

def get_causes(rows):    
    counts = {}
    for row in rows:
        if row[2] not in counts:
            counts[row[2]] = 0
        counts[row[2]] += 1

    for cause, freq in counts.items():
        print(f"{cause} happened {freq} times.")

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
        next(reader) # skip header
        for line in reader:
            table.append(line)

    if select != None:
        to_select = select.split()
        table = filter(lambda row: row[0] in to_select, table)

    if causes: get_causes(table)
    if servers: get_servers(table)

def main():
    parser = ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--select")
    parser.add_argument("--causes", action="store_true")
    parser.add_argument("--servers", action="store_true")

    args = parser.parse_args()

    parse_logs(args.path, args.select, args.causes, args.servers)

if __name__ == "__main__":
    main()
