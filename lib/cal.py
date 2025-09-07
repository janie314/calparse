import datetime
import json
import os
import uuid

import icalendar
import requests
from tzlocal import get_localzone

from lib.display import display_str


def load_cal(urls_path, cache_path, cache_timeout, no_skip=False):
    cache_dir = os.path.join(os.path.expanduser("~"), ".cache")
    os.makedirs(cache_dir, exist_ok=True)
    # The force flag will be handled by passing cache_timeout=0
    if os.path.exists(cache_path) and float(cache_timeout) > 0:
        last_modified = os.path.getmtime(cache_path)
        age = datetime.datetime.now().timestamp() - last_modified
        if age < float(cache_timeout):
            with open(cache_path) as cache:
                return json.load(cache)
    return _curl_cals(urls_path, cache_path)


def _curl_cals(urls_path, cache_path):
    cal = {}
    with open(urls_path) as f:
        urls = json.load(f)
    start_date = datetime.datetime.now(get_localzone())
    end_date = start_date + datetime.timedelta(days=8)
    for url in urls:
        res = requests.get(url).text
        calendar = icalendar.Calendar.from_ical(res)
        for e in calendar.events:
            # cast everything to a datetime.date
            if not (
                (_cast(start_date) <= _cast(e.start) <= _cast(end_date))
                or (_cast(start_date) <= _cast(e.end) <= _cast(end_date))
            ):
                continue
            not_until_days = None
            desc_clean = str(e.get("SUMMARY"))
            for tag in ["<span>", "</span>", "<br>", "</br>"]:
                desc_clean = desc_clean.replace(tag, "")
            try:
                desc_json = json.loads(desc_clean)
                if isinstance(desc_json, dict) and "not_until_days" in desc_json:
                    not_until_days = int(desc_json["not_until_days"])
            except Exception:
                pass
            cal[e.start.isoformat() + str(uuid.uuid4())] = {
                "start": e.start.isoformat(),
                "display": display_str(e),
                "not_until_days": not_until_days,
            }
    with open(cache_path, "w") as cache:
        json.dump(cal, cache)
    return cal


def _cast(d):
    if isinstance(d, datetime.datetime):
        return d.date()
    return d
