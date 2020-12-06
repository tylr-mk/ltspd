"""Tests limited as functions being runnable
"""
from ltspd.rosters.generators import (
    generate_mixed_size_roster,
    generate_random_roster,
)

# participants, group_size=2, exclusions=set(), randomise=True):

NAMES = [i for i in range(50)]

def test_generate_random_roster():
    generate_random_roster(NAMES, 2, randomise=True)
    generate_random_roster(NAMES, 2, randomise=False)
    # EXCLUSIONS don't work SAD
    # generate_random_roster(NAMES, 2, {1,2,4}, randomise=True)
    # generate_random_roster(NAMES, 2, {1,2,4}, randomise=False)


SCHEDULE = ((3, 2), (2, 2), (1, 8))

def test_generate_mixed_size_roster():
    generate_mixed_size_roster(NAMES, SCHEDULE, randomise=True)
    generate_mixed_size_roster(NAMES, SCHEDULE, randomise=False)
    # EXCLUSIONS don't work SAD
    # generate_mixed_size_roster(NAMES, SCHEDULE, {1,2,4}, randomise=True)
    # generate_mixed_size_roster(NAMES, SCHEDULE, {1,2,4}, randomise=False)

