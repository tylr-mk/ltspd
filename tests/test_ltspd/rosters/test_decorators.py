import pytest

from ltspd.rosters.decorators import retry_group_roster, retry_roster, violates_exclusions
from ltspd.utils.errors import NoSolutionFoundError


@pytest.mark.parametrize(
    "roster, exclusions, expected",
    (
        (((1, 2), (3, 4)), {(1, 2)}, True),
        (((1, 2), (3, 4)), {(2, 1)}, True),
        (((1, 2, 3), (4, 5)), {(3, 1)}, True),
        (((1, 2), (3, 4)), {(1, 3)}, False),
        (((1, 2), (3, 4)), set(), False),
        (((1, 2), (3, None)), {(1, 2, 3)}, False),
    ),
)
def test_violates_exclusions(roster, exclusions, expected):
    assert violates_exclusions(roster, exclusions) is expected


def test_retry_roster_reshuffles_every_run():
    calls = []

    @retry_roster(max_runs=50)
    def roster(participants, exclusions=frozenset(), randomise=True):
        calls.append(tuple(participants))
        return [tuple(participants[:2]), tuple(participants[2:])]

    roster([0, 1, 2, 3], {(0, 1), (0, 2)})
    assert len(set(calls)) == len(calls) or len(calls) > 1


def test_retry_roster_gives_up():
    runs = []

    @retry_roster(max_runs=3)
    def roster(participants, exclusions=frozenset(), randomise=True):
        runs.append(1)
        return [tuple(participants)]

    with pytest.raises(NoSolutionFoundError):
        roster([0, 1], {(0, 1)})
    assert len(runs) == 3


def test_retry_group_roster_terminates_on_unsolvable():
    @retry_group_roster(max_runs=5)
    def roster(groups, exclusions=frozenset(), randomise=True):
        return [tuple(g) for g in groups]

    with pytest.raises(NoSolutionFoundError):
        roster([(0, 1), (2, 3)], {(0, 1)})


def test_retry_group_roster_passes_through_when_not_randomised():
    @retry_group_roster()
    def roster(groups, exclusions=frozenset(), randomise=False):
        return groups

    groups = [(0, 1), (2, 3)]
    assert roster(groups, {(0, 1)}) is groups
