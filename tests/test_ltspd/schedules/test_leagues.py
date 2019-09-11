from itertools import combinations, permutations
from string import ascii_lowercase

import pytest

from ltspd.schedules.leagues import all_play_once

all_play_once_tests = tuple(
    (range(i), x, None) for i in range(5, 10) for x in range(2, 4)
)
all_play_once_tests += (
    # Add one case where results are written out
    (
        ascii_lowercase[:3],
        2,
        (
            (("a", "b"), ("a", "c"), ("b", "a"), ("b", "c"), ("c", "a"), ("c", "b")),
            (("a", "b"), ("a", "c"), ("b", "c")),
        ),
    ),
)


@pytest.mark.parametrize("participants, positions, expected", all_play_once_tests)
def test_all_play_once__can_fail_with_low_probability(participants, positions, expected):
    rp = tuple(all_play_once(participants, positions, True))
    rc = tuple(all_play_once(participants, positions))
    if expected is None:
        ep = tuple(permutations(participants, positions))
        ec = tuple(combinations(participants, positions))
    else:
        ep, ec = expected

    # Ensures the output has been shuffled
    assert rp != ep
    assert rc != ec
    # That all members are present, we may benefit from checking uniqueness
    # but that feels likely covered by functools
    assert set(rp) == set(ep)
    assert set(rc) == set(ec)


def test_all_types_played():  # participants, schedules, max_consistency=None):
    assert True
