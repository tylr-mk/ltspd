"""Expand activities into repeating schedules

Schedulables are anything with start_date and end_date attributes. They are
never mutated, each offset schedulable is a shallow copy of the original.
"""

from copy import copy
from datetime import timedelta
from itertools import takewhile


def generate_schedule(schedulables, duration, num=None, offset=0, start=None, end=None):
    """Repeat schedulables num times (or as many as fit between start and end).
    Each repetition is shifted duration + offset minutes on from the last, the
    first repetition keeps the original timings.

    Example: ([9:00-9:30], 30, num=3) >> [9:00-9:30], [9:30-10:00], [10:00-10:30]
    """
    if start and end:
        num = (end - start) // timedelta(minutes=duration + offset)
    if num is None:
        raise ValueError("Either num or both start and end are required")

    step = timedelta(minutes=duration + offset)
    return (offset_schedule(a, step * n) for n in range(num) for a in schedulables)


def duplicate_schedule(schedule, offset=0, end=None):
    """Shift every schedulable offset minutes, stopping at the first to finish
    at or after end (if given).
    """
    shifted = (offset_schedule(a, timedelta(minutes=offset)) for a in schedule)
    if end is None:
        return shifted
    return takewhile(lambda x: x.end_date < end, shifted)


def offset_schedule(schedulable, offset):
    """Return a copy of schedulable with start_date and end_date moved by offset"""
    shifted = copy(schedulable)
    shifted.start_date = schedulable.start_date + offset
    shifted.end_date = schedulable.end_date + offset
    return shifted
