import pytest
from pytest import raises

from ltspd.utils.expand import cycle_positions, powerset

powerset_tests = (
    (1, None, ((0,),)),
    (1, (1,), ((0,),)),
    # Twos
    (2, (1,), ((0,), (1,))),
    (2, (1, 2), ((0,), (1,), (0, 1))),
    (2, None, ((0,), (1,), (0, 1))),
    # Threes
    (3, (1,), ((0,), (1,), (2,))),
    (3, (1, 2), ((0,), (1,), (2,), (0, 1), (0, 2), (1, 2))),
    (3, (1, 2, 3), ((0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2))),
    (3, None, ((0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2))),
    (3, (1, 3), ((0,), (1,), (2,), (0, 1, 2))),
    # Combinations become massive and unuseful where iterable_len > 5 and n > 3
    # n < iterable_len - 3
    (
        11,
        (10,),
        (
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 10),
            (0, 1, 2, 3, 4, 5, 6, 7, 9, 10),
            (0, 1, 2, 3, 4, 5, 6, 8, 9, 10),
            (0, 1, 2, 3, 4, 5, 7, 8, 9, 10),
            (0, 1, 2, 3, 4, 6, 7, 8, 9, 10),
            (0, 1, 2, 3, 5, 6, 7, 8, 9, 10),
            (0, 1, 2, 4, 5, 6, 7, 8, 9, 10),
            (0, 1, 3, 4, 5, 6, 7, 8, 9, 10),
            (0, 2, 3, 4, 5, 6, 7, 8, 9, 10),
            (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        ),
    ),
)


@pytest.mark.parametrize("iterable_len, nums, expected", powerset_tests)
def test_powertest(iterable_len, nums, expected):
    assert tuple(powerset(iterable_len, nums)) == expected


powerset_errors = ((1, (0,)), (1, (-1,)), (1, (2,)))


@pytest.mark.parametrize("iterable_len, nums", powerset_errors)
def test_powertest_errors(iterable_len, nums):
    with raises(ValueError):
        powerset(iterable_len, nums)


cycle_positions_tests = (
    (2, ((0, 1), (1, 0))),
    (3, ((0, 1, 2), (1, 2, 0), (2, 0, 1))),
    (4, ((0, 1, 2, 3), (1, 2, 3, 0), (2, 3, 0, 1), (3, 0, 1, 2))),
    (
        5,
        (
            (0, 1, 2, 3, 4),
            (1, 2, 3, 4, 0),
            (2, 3, 4, 0, 1),
            (3, 4, 0, 1, 2),
            (4, 0, 1, 2, 3),
        ),
    ),
)


@pytest.mark.parametrize("positions, expected", cycle_positions_tests)
def test_cycle_positions(positions, expected):
    assert tuple(cycle_positions(positions)) == expected


@pytest.mark.parametrize("positions", (i for i in range(-5, 1)))
def test_cycle_positions_errors(positions):
    """Errors are raised from first out of the generator if the positions arg
    is 0 or less"""
    r = cycle_positions(positions)
    with raises(ValueError):
        next(r)
