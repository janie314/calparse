import json
import os
import uuid
from datetime import datetime, timedelta

import icalendar
import requests
from tzlocal import get_localzone

from lib.display import display_str


def load_cal(urls_path, cache_path, cache_timeout, no_skip=False):
    # The force flag will be handled by passing cache_timeout=0
    if os.path.exists(cache_path) and float(cache_timeout) > 0:
        last_modified = os.path.getmtime(cache_path)
        age = datetime.now().timestamp() - last_modified
        if age < float(cache_timeout):
            with open(cache_path) as cache:
                return json.load(cache)
    return curl_cals(urls_path, cache_path)


def curl_cals(urls_path, cache_path):
    cal = {}
    with open(urls_path) as f:
        urls = json.load(f)
    start_date = datetime.now(get_localzone())
    end_date = start_date + timedelta(days=8)
    datetime.now(get_localzone())
    for url in urls:
        res = requests.get(url).text
        calendar = icalendar.Calendar.from_ical(res)
        for e in calendar.events:
            if not (
                (start_date <= e.start <= end_date) or (start_date <= e.end <= end_date)
            ):
                continue
            not_until_days = None
            if e.description:
                try:
                    desc_clean = e.description
                    for tag in ["<span>", "</span>", "<br>", "</br>"]:
                        desc_clean = desc_clean.replace(tag, "")
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
