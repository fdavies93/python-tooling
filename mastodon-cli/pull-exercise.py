from requests import request
from argparse import ArgumentParser
from html2text import html2text
from rich.markdown import Markdown
from rich.console import Console
from sys import stdout
import time
import json
from csv import writer

# you can get an example of the JSON format by going to mastodon.social/api/v1/timelines/public in your browser

# 1: Get the username (account.username) and append it at the top of the output for the timeline in format "## @{username}"
# 2: We want to be able to poll our chosen mastodon server for new messages at some time interval. using time.sleep adjust the main function to poll at a interval set by the user. Use console.clear to clear the screen between users. See if you can figure out how to make it seamless!
# 3: add a --format json option to output the bare content of a JSON response from the Mastodon API. Use json.dumps with the indent option to render the response in a readable manner. We can then pipe this into a log.json file using > from the cli. 
# 4: add an option to output rows of CSV data by using --format csv and the csv.writer class. Rows are in the format [id, username, created_at, content], where content is in markdown format. You do not need to have a header (but can add an option for one if you like). Write this to stdout by attaching csv.writer to sys.stdout. Also change the --format json command to use sys.stdout.write if you previously used print()

def get_timeline(server: str):
    uri = f"https://{server}/api/v1/timelines/public"
    res = request("GET", uri)
    return res.json()

def render_message(message: dict) -> str:
    html = message.get("content")
    if html == None: return ""

    # 1: Get the username (account.username) and append it at the top of the output for the timeline in format "## @{username}"
    md = "\n\n".join((
        html2text(html),
    ))

    return md    

def pprint_timeline(timeline: list[dict], console:Console):
    messages = []
    for message in timeline:
        as_md = render_message(message)
        messages.append(as_md)

    out = "\n\n --- \n\n".join(messages)
    console.print(Markdown(out))

# 4: add an option to output rows of CSV data by using --format csv and the csv.writer class. Rows are in the format [id, username, created_at, content], where content is in markdown format. You do not need to have a header (but can add an option for one if you like). Write this to stdout by attaching csv.writer to sys.stdout. Unlike --dump this should work with polling. Also, change the --format json command to use sys.stdout.write

def main():
    console = Console()
    
    parser = ArgumentParser()
    parser.add_argument("server")

    parsed = parser.parse_args()

    tl = get_timeline(parsed.server)
    pprint_timeline(tl, console)
    # 3: add a --format json option to output the bare content of a JSON response from the Mastodon API. Use json.dumps with the indent option to render the response in a readable manner. We can then pipe this into a log.json file using > from the cli. 
    # 4

    # 2: We want to be able to poll our chosen mastodon server for new messages at some time interval. using time.sleep adjust the main function to poll at a interval set by the user. Use console.clear to clear the screen between users. See if you can figure out how to make it seamless
    # 3
    # 4
if __name__ == "__main__":
    main()
