from requests import request
from argparse import ArgumentParser
from html2text import html2text
from rich.markdown import Markdown
from rich.console import Console
from sys import stdout
import time
import json
from csv import writer

# you can get an example of JSON format by going to mastodon.social/api/v1/timelines/public in your browser

# 1: Get the username (account.username) and append it at the top of the output for the timeline in format "## @{username}"
# 2: We want to be able to poll our chosen mastodon server for new messages at some time interval. using time.sleep adjust the main function to poll at a interval set by the user. Use console.clear to clear the screen between users. See if you can figure out how to make it seamless!
# 3: add a --format json option to output the bare content of a JSON response from the Mastodon API. Use json.dumps with the indent option to render the response in a readable manner. We can then pipe this into a log.json file using > from the cli. 
# 4: add an option to output rows of CSV data by using --format csv and the csv.writer class. Rows are in the format [id, username, created_at, content], where content is in markdown format. You do not need to have a header (but can add an option for one if you like). Write this to stdout by attaching csv.writer to sys.stdout. Unlike --dump this should work with polling. Also, change the --format json command to use sys.stdout.write

def get_timeline(server: str):
    uri = f"https://{server}/api/v1/timelines/public"
    res = request("GET", uri)
    return res.json()

def render_message(message: dict) -> str:
    html = message.get("content")
    user = message.get("account")
    if html == None: return ""
    if user == None: return ""
    username = user.get("username")
    if username == None: return ""

    md = "\n\n".join((
        f"## @{username}",
        html2text(html)
    ))

    return md

def dump_1_to_csv(message: dict):
    csv = writer(stdout)

    id = message.get("id")
    created_at = message.get("created_at")
    html = message.get("content")
    user = message.get("account")

    for x in (id, created_at, html, user):
        if x is None: return
    
    username = user.get("username") # linter is wrong
    if username == None: return

    md = html2text(html)

    csv.writerow((id,username,created_at,md))

def dump_to_csv(timeline: list[dict]):
    for message in timeline:
        dump_1_to_csv(message)
    

def pprint_timeline(timeline: list[dict], console:Console):
    messages = []
    for message in timeline:
        as_md = render_message(message)
        messages.append(as_md)

    out = "\n\n --- \n\n".join(messages)
    console.print(Markdown(out))
        
def main():
    console = Console()
    
    parser = ArgumentParser()
    parser.add_argument("server")
    parser.add_argument("--poll")
    parser.add_argument("--format")

    parsed = parser.parse_args()

    tl = get_timeline(parsed.server)
    if parsed.format is None: pprint_timeline(tl, console)
    elif parsed.format == "json":
        stdout.write(json.dumps(tl,indent=4))
    elif parsed.format == "csv":
        dump_to_csv(tl)
    else: return

    while parsed.poll is not None:
        time.sleep(int(parsed.poll))
        tl = get_timeline(parsed.server)
        if parsed.format is None:
            console.clear()
            pprint_timeline(tl, console)
        elif parsed.format == "json":
            stdout.write(json.dumps(tl, indent=4))
        elif parsed.format == "csv":
            dump_to_csv(tl)
    
if __name__ == "__main__":
    main()
