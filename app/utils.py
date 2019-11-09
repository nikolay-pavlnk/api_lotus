from datetime import datetime
from functools import partial
from calendar import timegm
from time import strptime
from settings import FORMATS


def check_datetime_format(format, date: str):
    try:
        return bool(datetime.strptime(date, format))
    except ValueError:
        return False


def convert_time_range(time_range: list):
    try:
        new_time_range = []
        for time_ in time_range:
            index = list(
                map(partial(check_datetime_format, date=time_), FORMATS)
            ).index(True)
            new_time_range.append(timegm(strptime(time_, FORMATS[index])) * 1000)
        return new_time_range
    except Exception:
        return None, None
