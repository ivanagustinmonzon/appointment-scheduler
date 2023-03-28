import re
import datetime
from datetime import datetime, timedelta

def extract_day(str):
    pattern = r"\d{2}/\d{2}/\d{4}"  # Matches DD/MM/YYYY
    match = re.search(pattern, str)
    if match:
        day = match.group(0)
    return day


def extract_hour(str):
    pattern = r"\d{2}:\d{2}"  # Matches HH:MM
    match = re.search(pattern, str)
    if match:
        day = match.group(0)
    return day


# expects "04/06/2022", "18:30"
def build_datetime(date_string, time_string):
    date = datetime.strptime(date_string, "%d/%m/%Y")
    time = datetime.strptime(time_string, "%H:%M").time()
    date_time = datetime.combine(date, time)
    return date_time

def is_in_days_range(availablilty_datetime, configured_days):
    now = datetime.now()
    future = now + timedelta(days=configured_days)
    return availablilty_datetime < future

def datetime_difference_from_now(date):
    now = datetime.now()
    diff = date - now
    date_diff = diff.days
    time_diff = diff.seconds // 3600
    return date_diff, time_diff
