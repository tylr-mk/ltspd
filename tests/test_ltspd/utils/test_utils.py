from itertools import islice

import pytest

from ltspd.utils import (
    fill_series,
    filter_axis,
    filter_second_axes,
    grouper,
    probability_series,
    random_string,
    shuffle_second_axis,
)
from ltspd.utils.generate import make_groups

grouper_tests = (
    ((0, 1, 2, 3, 4, 5, 6, 7, 8), 2),
    ((0, 1, 2, 3, 4, 5, 6, 7, 8), 3),
    ((0, 1, 2, 3, 4, 5, 6, 7, 8), 9),
)


@pytest.mark.parametrize("participants, group_size", grouper_tests)
def test_grouper(participants, group_size):
    assert tuple(grouper(participants, group_size)) == tuple(
        make_groups(participants, group_size)
    )


@pytest.mark.parametrize("n", (2, 3, 4, 5))
def test_random_string(n):
    r = random_string(n)
    assert len(r) == n
    assert type(r) == str


bad_apples = {1, 2, 3, 4, 5}


@pytest.mark.parametrize("feature, expected", ((range(0, 8), (0, 6, 7)),))
def test_filter_axis(feature, expected):
    assert tuple(filter_axis(feature, bad_apples)) == expected


@pytest.mark.parametrize(
    "feature, expected", (((range(0, 8) for _ in range(8)), (0, 6, 7)),)
)
def test_filter_second_axes(feature, expected):
    for r in filter_second_axes(feature, bad_apples):
        assert tuple(r) == expected


@pytest.mark.parametrize("n", range(1, 10))
def test_shuffle_second_axis(n):
    e = set(range(n))
    feature = list(list(range(n)) for _ in range(0, 5))
    shuffle_second_axis(feature)
    for r in feature:
        assert not e - set(r)


fill_series_tests = (((1, 2), 6, (None, 1, None, None, None, None, 2, None, None, None)),)


@pytest.mark.parametrize("group, size, expected", fill_series_tests)
def test_fill_series(group, size, expected):
    assert tuple(fill_series(group, size)) == expected


probability_series_tests = (
    (1, (1, 1, 1, 1, 1, 1, 1, 1)),
    (2, (1, 0, 1, 0, 1, 0, 1, 0)),
    (3, (1, 0, 0, 1, 0, 0, 1, 0)),
    (4, (1, 0, 0, 0, 1, 0, 0, 0)),
)


@pytest.mark.parametrize("n, expected", probability_series_tests)
def test_probability_series(n, expected):
    assert tuple(islice(probability_series(n), None, 8)) == expected
