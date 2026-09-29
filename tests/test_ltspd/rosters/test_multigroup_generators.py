"""Tests limited as functions being runnable"""

from string import ascii_lowercase, ascii_uppercase

from ltspd.rosters.multi_group_generators import (
    _proportional_indices,
    _representational_indices,
    _select_from_groups,
    _select_from_lengths,
    defined_mix,
    even_spread_mix,
    generate_mixed_size_zip_roster,
    group_representation,
)

# _select_from_lengths(lengths, indices, exclude_tail=False, complete_current=False):
# defined_mix(groups, indices):
# even_spread_mix(groups):
# group_representation(groups, num_groups, exclusions=set(), randomise=True):
# generate_mixed_size_zip_roster(groups, indices, group_schedule):


def test__proportional_indices():
    # _proportional_indices(lengths):
    # _proportional_indices()
    assert _proportional_indices([50, 50]) == (0, 1)
    assert _proportional_indices([600, 500]) == (0, 1)
    assert _proportional_indices([6000, 5000, 2000]) == (0, 1, 0, 1, 0, 1, 2)


def test__representational_indices():
    # _representational_indices(lengths, num_groups):
    # _representational_indices()
    _representational_indices((5, 2), 2)
    _representational_indices((3,), 1)
    _representational_indices((5, 7, 8, 8, 2, 2), 2)


def test__select_from_groups():
    # _select_from_groups()
    # _select_from_groups(groups, indices, exclude_tail=False, complete_current=False):
    assert list(
        _select_from_groups([ascii_lowercase[:5], ascii_uppercase[:5]], (0, 0, 1))
    ) == ["a", "b", "A", "c", "d", "B", "e", "C", "D", "E"]
    assert list(
        _select_from_groups([ascii_lowercase[:5], ascii_uppercase[:5]], (1, 0, 1))
    ) == ["A", "a", "B", "C", "b", "D", "E", "c", "d", "e"]
    assert list(
        _select_from_groups(
            [ascii_lowercase[:5], ascii_uppercase[:5], range(2)], (2, 1, 0)
        )
    ) == [0, "A", "a", 1, "B", "b", "C", "c", "D", "d", "E", "e"]
    assert list(
        _select_from_groups([ascii_lowercase[:5], ascii_uppercase[:5]], (0, 0, 1), True)
    ) == ["a", "b", "A", "c", "d", "B", "e"]
    assert list(
        _select_from_groups(
            [ascii_lowercase[:5], ascii_uppercase[:5]], (0, 0, 1), False, True
        )
    ) == ["a", "b", "A", "c", "d", "B", "e", "C"]


def test__select_from_lengths():
    # _select_from_lengths()
    assert list(_select_from_lengths((5, 5, 5), (0, 1, 2))) == [
        0,
        1,
        2,
        0,
        1,
        2,
        0,
        1,
        2,
        0,
        1,
        2,
        0,
        1,
        2,
    ]
    # Haven't handled??? Dunno just yet.
    # assert list(_select_from_lengths((10,5,5), (0,1,2))) == [0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,0,0,0,0]
    # assert list(_select_from_lengths((10,5,5), (0,1,2))) == [0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,0,0,0,0]
    # assert list(_select_from_lengths((10,5,5), (0,1,2), True)) == [0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0]
    # assert list(_select_from_lengths((10,5,5), (0,1,2), False, True)) == [0,1,2,0,1,2,0,1,2,0,1,2,0, 1,2,0]


def test_defined_mix():
    # defined_mix()
    assert list(defined_mix(((1, 2, 3, 4), ("a", "b")), (0, 0, 1))) == [
        1,
        2,
        "a",
        3,
        4,
        "b",
    ]
    assert list(defined_mix(((1, 2, 3, 4), ("a", "b"), ("x", "y")), (0, 0, 1, 2))) == [
        1,
        2,
        "a",
        "x",
        3,
        4,
        "b",
        "y",
    ]


def test_even_spread_mix():
    # even_spread_mix()
    assert list(even_spread_mix([(1, 2), ("a", "b")])) == [1, "a", 2, "b"]
    assert list(even_spread_mix([(1, 2, 3, 4), ("a", "b")])) == [1, 2, "a", 3, 4, "b"]


def test_group_representation():
    # group_representation()
    assert list(group_representation([ascii_lowercase[:9], ascii_uppercase[:3]], 3)) == [
        "a",
        "b",
        "c",
        "A",
        "d",
        "e",
        "f",
        "B",
        "g",
        "h",
        "i",
        "C",
    ]


def test_generate_mixed_size_zip_roster():
    # generate_mixed_size_zip_roster(groups, indices, group_schedule):
    assert list(
        generate_mixed_size_zip_roster(
            [ascii_lowercase[:3], ascii_uppercase[:9]], (1, 0, 1), ((1, 2), (2, 6))
        )
    ) == [("A",), ("a",), ("B", "C"), ("b", "D"), ("E", "c"), ("F", "G"), ("H", "I")]


def test_even_spread_mix_does_not_mutate():
    groups = [["a", "b"], [1, 2, 3, 4]]
    assert list(even_spread_mix(groups)) == [1, 2, "a", 3, 4, "b"]
    assert groups == [["a", "b"], [1, 2, 3, 4]]


def test_even_spread_mix_gathers_all():
    assert list(even_spread_mix([(1, 2, 3, 4, 5), ("a",)])) == [1, 2, 3, 4, 5, "a"]
