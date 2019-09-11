from itertools import cycle, zip_longest

import pytest

from ltspd.utils.generate import make_groups, zip_groups, zip_mix

make_groups_tests = (
    ((0, 1, 2, 3, 4, 5, 6, 7, 8), 2, ((0, 1), (2, 3))),
    ((0, 1, 2, 3, 4, 5, 6, 7, 8), 3, ((0, 1, 2), (3, 4, 5))),
    ((0, 1, 2, 3, 4, 5, 6, 7, 8), 9, ((0, 1, 2, 3, 4, 5, 6, 7, 8),)),
    ((x for x in range(50)), 2, ((0, 1), (2, 3))),
    ((x for x in range(20, 50)), 2, ((20, 21), (22, 23))),
    (cycle(x for x in range(2)), 2, ((0, 1), (0, 1))),
)


@pytest.mark.parametrize("participants, group_size, expected", make_groups_tests)
def test_make_groups(participants, group_size, expected):
    r = make_groups(participants, group_size)
    for e in expected:
        assert next(r) == e


zip_mix_tests = (
    (((0, 1, 2), ("a", "b")), zip_longest, (0, "a", 1, "b", 2, None)),
    (((x for x in range(3)), ("a", "b")), zip_longest, (0, "a", 1, "b", 2, None)),
    # Use zip which ends at shortest
    (((0, 1, 2), ("a", "b")), zip, (0, "a", 1, "b")),
    (((x for x in range(3)), ("a", "b")), zip, (0, "a", 1, "b")),
    (((x for x in range(40)), ("a", "b")), zip, (0, "a", 1, "b")),
)


@pytest.mark.parametrize("groups, method, expected", zip_mix_tests)
def test_zip_mix(groups, method, expected):
    assert tuple(zip_mix(groups, method)) == expected


zip_groups_tests = (
    (((0, 1, 2), ("a", "b")), 2, ((0, "a"), (1, "b"), (2, None))),
    (((0, 1, 2), ("a",)), 2, ((0, "a"), (1, 2))),
    (((0, 1, 2, 3, 4), ("a",)), 2, ((0, "a"), (1, 2), (3, 4))),
    # Group into 3s
    (((0, 1, 2), ("a", "b")), 3, ((0, "a", 1), ("b", 2, None))),
    (((0, 1, 2), ("a",)), 3, ((0, "a", 1), (2, None, None))),
    (((0, 1, 2, 3, 4), ("a",)), 3, ((0, "a", 1), (2, 3, 4))),
    # More than 2 Groups
    (((0,), (1,), (2,)), 2, ((0, 1), (2, None))),
    (((0,), (5,), (2,), (10, 11)), 2, ((0, 5), (2, 10), (11, None))),
    (((0,), (5,), (2,), (10, 11)), 3, ((0, 5, 2), (10, 11, None))),
    (((0, 1, 7), (5,), (2,), (10, 11)), 3, ((0, 5, 2), (10, 1, 11), (7, None, None))),
    # Groups with None in
    (((0, 1, 2), (None, "a", "b")), 2, ((0, 1), ("a", 2), ("b", None))),
    (
        ((0, 1, 2, 3, 4, 5), (None, "a", None, "b")),
        2,
        ((0, 1), ("a", 2), (3, "b"), (4, 5)),
    ),
    (((0, 1, 2), ("a", None, "b")), 2, ((0, "a"), (1, 2), ("b", None))),
    (((0, 1, 2), ("a", None)), 2, ((0, "a"), (1, 2))),
    (((None,) * 60 + (0, 1, 2), ("a", None)), 2, (("a", 0), (1, 2))),
)


@pytest.mark.parametrize("groups, group_size, expected", zip_groups_tests)
def test_zip_group(groups, group_size, expected):
    assert tuple(zip_groups(groups, group_size)) == expected
