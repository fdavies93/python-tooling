import random
import csv

servers = 5
odds_of_failure = 0.0001
reasons = [
    "Splines failed to reticulate.", 
    "Cat on keyboard.", 
    "AC set too high.",
    "Mandatory windows update.",
    "Nvidia driver failure.",
    "Solar flare caused bit flip.",
    "Uses a hard drive."
]
span = 60 * 60 * 24

def tick(timestamp, writer):
    for server in range(servers):
        if random.random() >= odds_of_failure:
            continue
        writer.writerow((server, timestamp, random.choice(reasons)))
        
def main():
    with open("restarts.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(("server_id", "timestamp", "cause"))
        for ts in range(span):
            tick(ts, writer)

if __name__ == "__main__":
    main()
