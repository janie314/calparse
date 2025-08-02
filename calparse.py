import argparse
import json
import os
import random
import uuid
from datetime import datetime, timedelta
from traceback import print_exception

from icalevents.icalevents import events


def display_str(event):
    return event.start.strftime("%-m/%-d %I:%M %p") + " " + event.summary


def pull_and_display(mode, urls_path, cache_path):
    cal = {}
    with open(urls_path) as f:
        urls = json.load(f)
    start_date = datetime.now()
    end_date = start_date + timedelta(weeks=1)
    for url in urls:
        for e in events(url, sort=True, start=start_date, end=end_date):
            cal[e.start.isoformat() + str(uuid.uuid4())] = display_str(e)
    with open(cache_path, "w") as cache:
        json.dump(cal, cache)
    print_result(mode, cal)


def print_result(mode, cal):
    vals = [cal[k] for k in sorted(cal.keys())]
    if mode == "random":
        print(random.choice(vals))
    elif mode == "list":
        for e in sorted(cal.values()):
            print(e)
    elif mode == "sequence":
        minutes = datetime.now().minute
        print(vals[minutes % len(vals)])
    else:
        print_exception("bad mode....")


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        prog="calparse", description="Parses iCal URLs in different ways."
    )
    argparser.add_argument("mode", help="supports 'random', 'list'")
    argparser.add_argument(
        "-u",
        "--urls",
        help="JSON file containing a list of iCal URLs (default: ./urls.json)",
        default=os.path.join(os.path.dirname(__file__), "urls.json"),
    )
    homedir = os.environ.get("HOME")
    argparser.add_argument(
        "-c",
        "--cache",
        help="cache file of calendar state (default $HOME/.cache/calparse-cache.json)",
        default=os.path.join(homedir, ".cache/calparse-cache.json"),
    )
    args = argparser.parse_args()
    pull_and_display(args.mode.lower(), args.urls, args.cache)
