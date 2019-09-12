from itertools import tee
from string import ascii_lowercase, ascii_uppercase

import pytest

from ltspd.utils.refine import (
    apply_mixer,
    break_up,
    cycle_step,
    limited_game_selector,
    nwise_mixer,
    position_mixer,
    remove_back_to_backs,
    sliding_position_mixer,
)

nwise_mixer_tests = (
    (4, 2, ((0, 1), (1, 2), (2, 3), (3, 0))),
    (4, 3, ((0, 1, 2), (1, 2, 3), (2, 3, 0), (3, 0, 1))),
    (
        8,
        4,
        (
            (0, 1, 2, 3),
            (1, 2, 3, 4),
            (2, 3, 4, 5),
            (3, 4, 5, 6),
            (4, 5, 6, 7),
            (5, 6, 7, 0),
            (6, 7, 0, 1),
            (7, 0, 1, 2),
        ),
    ),
)


@pytest.mark.parametrize("num, n, expected", nwise_mixer_tests)
def test_nwise_mixer(num, n, expected):
    assert tuple(nwise_mixer(num, n)) == expected


cycle_step_tests = (
    ((0, 1, 3), 5, (0, 1, 3, 1, 2, 4, 2, 3, 0, 3, 4, 1, 4, 0, 2)),
    ((0, 9), 5, (0, 4, 1, 0, 2, 1, 3, 2, 4, 3)),
)


@pytest.mark.parametrize("indices, num, expected", cycle_step_tests)
def test_cycle_step(indices, num, expected):
    assert tuple(cycle_step(indices, num)) == expected


position_mixer_tests = (
    (6, 2, ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0))),
    (6, 3, ((0, 1, 3), (1, 2, 4), (2, 3, 5), (3, 4, 0), (4, 5, 1), (5, 0, 2))),
    (
        9,
        3,
        (
            (0, 1, 3),
            (1, 2, 4),
            (2, 3, 5),
            (3, 4, 6),
            (4, 5, 7),
            (5, 6, 8),
            (6, 7, 0),
            (7, 8, 1),
            (8, 0, 2),
        ),
    ),
    (5, 4, ((0, 1, 3, 2), (1, 2, 4, 3), (2, 3, 0, 4), (3, 4, 1, 0), (4, 0, 2, 1))),
)


@pytest.mark.parametrize("num, positions, expected", position_mixer_tests)
def test_position_mixer(num, positions, expected):
    assert tuple(position_mixer(num, positions)) == expected


position_mixer_tests_lrg = (
    (25, 5, ((0, 1, 3, 7, 15), (2, 3, 5, 9, 17), (4, 5, 7, 11, 19))),
)


@pytest.mark.parametrize("num, positions, expected", position_mixer_tests_lrg)
def test_position_mixer_lrg(num, positions, expected):
    r = position_mixer(num, positions)
    for e in expected:
        _test_r = tee(r, 1)[0]
        assert any(mix == e for mix in _test_r)


apply_mixer_tests = (
    (ascii_lowercase, position_mixer(3, 2), (("a", "b"), ("b", "c"), ("c", "a"))),
    (ascii_uppercase, position_mixer(3, 2), (("A", "B"), ("B", "C"), ("C", "A"))),
    (
        ascii_uppercase,
        position_mixer(5, 3),
        (("A", "B", "D"), ("B", "C", "E"), ("C", "D", "A")),
    ),
    (
        ascii_lowercase,
        nwise_mixer(3, 3),
        (("a", "b", "c"), ("b", "c", "a"), ("c", "a", "b")),
    ),
    (
        ascii_uppercase,
        nwise_mixer(3, 3),
        (("A", "B", "C"), ("B", "C", "A"), ("C", "A", "B")),
    ),
)


@pytest.mark.parametrize("schedule, mix, expected", apply_mixer_tests)
def test_apply_mixer(schedule, mix, expected):
    r = apply_mixer(schedule, mix)
    for e in expected:
        assert tuple(next(r)) == e


def test_break_up():
    assert tuple(break_up(ascii_lowercase[:3])) == ("a", None, "b", None, "c", None)
    assert tuple(break_up(ascii_lowercase[3:6])) == ("d", None, "e", None, "f", None)


sliding_position_mixer_tests = (
    (ascii_lowercase[:8], 2, (("a", "b"), ("b", "c"), ("c", "d"))),
    (ascii_lowercase[:3], 2, (("a", "b"), ("b", "c"), ("c", "a"))),
    (ascii_lowercase[3:6], 3, (("d", "e", "f"), ("e", "f", "d"), ("f", "d", "e"))),
)


@pytest.mark.parametrize("schedule, pairings, expected", sliding_position_mixer_tests)
def test_sliding_position_mixer(schedule, pairings, expected):
    r = sliding_position_mixer(schedule, pairings)
    for e in expected:
        assert tuple(next(r)) == e


limited_game_selector_tests = (
    (5, ("a", "f", "k", "p", "u")),
    (6, ("a", "e", "i", "m", "q", "u")),
    (8, ("a", "d", "g", "j", "m", "p", "s", "v")),
    (11, ("a", "c", "e", "g", "i", "k", "m", "o", "q", "s", "u")),
    (
        21,
        (
            "a",
            "c",
            "e",
            "g",
            "i",
            "k",
            "m",
            "o",
            "q",
            "s",
            "u",
            "w",
            "y",
            "b",
            "f",
            "j",
            "n",
            "r",
            "v",
            "z",
            "d",
        ),
    ),
)


@pytest.mark.parametrize("games, expected", limited_game_selector_tests)
def test_limited_game_selector(games, expected):
    assert tuple(limited_game_selector(games, ascii_lowercase)) == expected


remove_back_to_backs_tests = (
    ([(1, 0), (1, 0), (2, 3), (4, 5)], ((1, 0), (2, 3), (4, 5), (1, 0))),
    ([(1, 0), (2, 3), (2, 3), (4, 5)], ((1, 0), (2, 3), (4, 5), (2, 3))),
)


@pytest.mark.parametrize("schedule, expected", remove_back_to_backs_tests)
def test_remove_back_to_backs(schedule, expected):
    assert tuple(remove_back_to_backs(schedule)) == expected


remove_back_to_backs_extra_tests = (
    ([(1, 0), (1, 0), (2, 3), (2, 3), (4, 5)], 2, ((1, 0), (2, 3))),
)


@pytest.mark.parametrize("schedule, tail, expected", remove_back_to_backs_extra_tests)
def test_remove_back_to_backs_extra(schedule, tail, expected):
    r = tuple(remove_back_to_backs(schedule))[-tail:]
    for e in expected:
        assert e in r
