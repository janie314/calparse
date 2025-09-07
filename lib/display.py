import datetime
import math
import random
import time
from traceback import print_exception

from tzlocal import get_localzone


def _filter(cal, no_skip):
    if no_skip:
        return cal
    # Filter events using not_until_days if present
    now = datetime.datetime.now(get_localzone())
    filtered = {}
    for k, v in cal.items():
        not_until_days = v.get("not_until_days")
        event_start = v.get("start")
        if not_until_days is not None and event_start is not None:
            event_start = datetime.datetime.fromisoformat(event_start)
            now = datetime.datetime.now(get_localzone())
            days_until = (event_start - now).days
            if days_until > not_until_days:
                continue
        filtered[k] = v
    return filtered


def display_str(event):
    return event.start.strftime("%a %-m/%-d %I:%M %p") + " " + str(event.get("SUMMARY"))


def print_result(mode, cal, interval, no_skip):
    cal = _filter(cal, no_skip)
    vals = [cal[k]["display"] for k in sorted(cal.keys())]
    if not vals:
        return
    if mode == "random":
        print(random.choice(vals))
    elif mode == "list":
        for e in vals:
            print(e)
    elif mode == "sequence":
        unix = math.floor(time.time() / interval)
        print(vals[unix % len(vals)])
    else:
        print_exception("bad mode....")
