import pytest

from ltspd.utils.groups import explode_subgroups, identify_unassigned, unnest

unnest_tests = (
    (((0, 1), (2, 3, 4)), {0, 1, 2, 3, 4}),
    (((0,), (1,), (2, 3, 4)), {0, 1, 2, 3, 4}),
    (((0, 1), (2, 3), (4,)), {0, 1, 2, 3, 4}),
    ((iter((0, 1)), iter((2, 3)), iter((4,))), {0, 1, 2, 3, 4}),
    (({0, 1}, {2, 3}, {4}), {0, 1, 2, 3, 4}),
    (([0, 1], [2, 3], [4]), {0, 1, 2, 3, 4}),
)


@pytest.mark.parametrize("feature, expected", unnest_tests)
def test_unnest(feature, expected):
    assert unnest(feature) == expected


identify_unassigned_tests = (
    ((i for i in range(5)), ((0, 1), (2, 4)), {3}),
    ((i for i in range(5)), ((1,), (2, 4)), {3, 0}),
    ((i for i in range(5)), ((3, 0, 1), (2, 4)), set()),
    ((i for i in range(5)), ((3, 0, 1), (2, 4, 8, 9)), set()),
)


@pytest.mark.parametrize("participants, groups, expected", identify_unassigned_tests)
def test_identify_unassigned(participants, groups, expected):
    assert identify_unassigned(participants, groups) == expected


explode_subgroups_tests = (
    # Basic and default behaviour
    (((0, 1),), 2, ((0, 1), (1, 0))),
    (((0, 1), (0, 2)), 2, ((0, 1), (1, 0), (0, 2), (2, 0))),
    (((0, 1),), None, ((0, 1), (1, 0))),
    (((0, 1), (0, 2)), None, ((0, 1), (1, 0), (0, 2), (2, 0))),
    # Slightly different behaviour
    (
        ((0, 1, 2), (0, 2)),
        2,
        ((0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (0, 2), (2, 0)),
    ),
    # Slightly different behaviour
    (((0, 1), (0, 2)), 3, ()),
    (
        ((0, 1, 2), (0, 2)),
        3,
        ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)),
    ),
    (
        ((0, 1, 2), (0, 2)),
        None,
        (
            (0, 1, 2),
            (0, 2, 1),
            (1, 0, 2),
            (1, 2, 0),
            (2, 0, 1),
            (2, 1, 0),
            (0, 2),
            (2, 0),
        ),
    ),
)


@pytest.mark.parametrize("feature, size, expected", explode_subgroups_tests)
def test_explode_subgroups(feature, size, expected):
    assert tuple(explode_subgroups(feature, size)) == expected
