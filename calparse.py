import argparse
import json
import os
import random
from datetime import datetime, timedelta
from traceback import print_exception

from icalevents.icalevents import events


def parse(mode, urls_path):
    cal = []
    with open(urls_path) as f:
        urls = json.load(f)
    start_date = datetime.now()
    end_date = start_date + timedelta(weeks=1)
    for url in urls:
        cal += events(url, sort=True, start=start_date, end=end_date)
    if mode == "random":
        e = random.choice(cal)
        print(e.start.strftime("%-m/%-d %I:%M %p") + " " + e.summary)
    elif mode == "list":
        cal = sorted(cal, key=lambda e: e.start)
        for e in cal:
            print(e.start.strftime("%-m/%-d %I:%M %p") + " " + e.summary)
    elif mode == "sequence":
        cal = sorted(cal, key=lambda e: e.start)
        minutes = datetime.now().minute
        e = cal[minutes % len(cal)]
        print(e.start.strftime("%-m/%-d %I:%M %p") + " " + e.summary)
    else:
        print_exception("bad mode....")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="calparse", description="Parses iCal URLs in different ways."
    )
    parser.add_argument("mode", help="supports 'random', 'list'")
    parser.add_argument(
        "-u",
        "--urls",
        help="JSON file containing a list of iCal URLs",
        default=os.path.join(os.path.dirname(__file__), "urls.json"),
    )
    args = parser.parse_args()
    parse(args.mode.lower(), args.urls)
