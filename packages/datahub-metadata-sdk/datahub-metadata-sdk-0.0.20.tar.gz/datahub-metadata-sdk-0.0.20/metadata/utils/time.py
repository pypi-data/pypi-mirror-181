# -*- encoding: utf-8 -*-

from time import time
from datetime import datetime


def get_current_timestamp(precision='ms', _round=True):
    t = time()
    if precision == 'ms':
        t = t * 1000
    elif precision == 'us':
        t = t * 1000 * 1000
    return int(t) if _round else t

def get_current_datetime():
    return datetime.now()

def timestamp_to_datetime(ts):
    t = int(ts)
    while t > 0:
        try:
            return datetime.fromtimestamp(t)
        except ValueError as e:
            if 'is out of range' not in str(e):
                raise
            t = t / 1000.
    return datetime.fromtimestamp(ts)

def datetime_to_timestamp(dt, precision='ms', _round=True):
    t = dt.timestamp()
    if precision == 'ms':
        t = t * 1000
    elif precision == 'us':
        t = t * 1000 * 1000
    return int(t) if _round else t