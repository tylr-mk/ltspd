from datetime import datetime, timedelta

import pytest

from ltspd.schedules.expand import duplicate_schedule, generate_schedule, offset_schedule


class Slot:
    def __init__(self, start, minutes):
        self.start_date = start
        self.end_date = start + timedelta(minutes=minutes)


NINE = datetime(2026, 1, 1, 9)


def test_offset_schedule_copies():
    slot = Slot(NINE, 30)
    shifted = offset_schedule(slot, timedelta(minutes=15))
    assert shifted.start_date == NINE + timedelta(minutes=15)
    assert slot.start_date == NINE


def test_generate_schedule_num():
    slots = list(generate_schedule([Slot(NINE, 30)], 30, num=3))
    assert [s.start_date.strftime("%H:%M") for s in slots] == ["09:00", "09:30", "10:00"]


def test_generate_schedule_start_end_with_offset():
    slots = list(
        generate_schedule(
            [Slot(NINE, 30), Slot(NINE, 30)],
            30,
            offset=10,
            start=NINE,
            end=NINE + timedelta(hours=2),
        )
    )
    assert len(slots) == 6
    assert slots[-1].start_date == NINE + timedelta(minutes=80)


def test_generate_schedule_requires_num():
    with pytest.raises(ValueError):
        generate_schedule([Slot(NINE, 30)], 30)


def test_duplicate_schedule():
    slots = [Slot(NINE + timedelta(hours=h), 30) for h in range(4)]
    assert len(list(duplicate_schedule(slots, 60))) == 4
    limited = list(duplicate_schedule(slots, 60, end=NINE + timedelta(hours=3)))
    assert [s.start_date.hour for s in limited] == [10, 11]
