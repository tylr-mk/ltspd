from itertools import combinations

import pytest

from ltspd.models import Inventory, InventoryThing
from ltspd.rosters.decorators import violates_exclusions
from ltspd.rosters.generators import (
    assign_inventory_things,
    generate_mixed_size_roster,
    generate_random_roster,
)
from ltspd.utils.errors import NoSolutionFoundError
from ltspd.utils.groups import unnest

NAMES = list(range(50))
SCHEDULE = ((3, 2), (2, 2), (1, 8))
EXCLUSIONS = {(1, 2), (3, 4), (5, 6, 7)}


def test_generate_random_roster():
    roster = tuple(generate_random_roster(list(NAMES), 2, randomise=True))
    assert unnest(roster) == set(NAMES)
    assert tuple(generate_random_roster(list(NAMES), 2, randomise=False))[0] == (0, 1)


def test_generate_random_roster_respects_exclusions():
    for _ in range(20):
        roster = tuple(generate_random_roster(list(NAMES), 3, EXCLUSIONS))
        assert unnest(roster) - {None} == set(NAMES)
        assert not violates_exclusions(roster, EXCLUSIONS)


def test_generate_random_roster_does_not_mutate_default_exclusions():
    generate_random_roster(list(NAMES), 2)
    assert generate_random_roster.__wrapped__.__defaults__[1] == frozenset()


def test_generate_random_roster_no_solution():
    everyone = set(combinations(range(4), 2))
    with pytest.raises(NoSolutionFoundError):
        generate_random_roster(list(range(4)), 2, everyone)


def test_generate_mixed_size_roster():
    roster = tuple(generate_mixed_size_roster(list(NAMES), SCHEDULE, randomise=True))
    assert [len(g) for g in roster] == [2, 2, 2, 2, 2, 8]
    ordered = tuple(generate_mixed_size_roster(list(NAMES), SCHEDULE, randomise=False))
    assert ordered[:3] == ((0, 1), (2, 3), (4, 5))


def test_generate_mixed_size_roster_respects_exclusions():
    for _ in range(20):
        roster = generate_mixed_size_roster(list(NAMES), SCHEDULE, EXCLUSIONS)
        assert not violates_exclusions(roster, EXCLUSIONS)


def test_assign_inventory_things():
    rooms = [
        InventoryThing(Inventory(capacity=2, number=2)),
        InventoryThing(Inventory(3, 1)),
    ]
    assignments = list(assign_inventory_things(list(range(7)), rooms))
    assert [a.attendees for a in assignments] == [[0, 1], [2, 3], [4, 5, 6]]
    assert assignments[2].inventory_thing is rooms[1]
