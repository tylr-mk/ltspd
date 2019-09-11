"""Activities
"""
from datetime import timedelta
from itertools import takewhile


def generate_schedule(schedulables, duration, num=None, offset=0, start=None, end=None):
    if start and end:
        num = (end - start) // duration

    schedulables = schedulables if len(schedulables) > 1 else (schedulables,)
    offset = timedelta(minutes=(duration + offset) if offset else duration)
    return (offset_schedule(a, offset) for a in schedulables * num)


def duplicate_schedule(schedule, offset=0, end=None):
    offset = timedelta(minutes=offset)
    return takewhile(
        lambda x: x.end_date < end, (offset_schedule(a, offset) for a in schedule)
    )


def offset_schedule(schedulable, offset):
    schedulable.start_date = schedulable.start_date + offset
    schedulable.end_date = schedulable.end_date + offset
    return schedulable
