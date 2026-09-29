"""Generic utilities for managing common manipulations on Python natives"""

from itertools import chain, cycle, zip_longest
from random import choice, shuffle
from string import ascii_uppercase


def grouper(iterable, n):
    """Collect data into fixed-length chunks or blocks from itertools.recipes"""
    return zip_longest(*([iter(iterable)] * n))


def random_string(n=8):
    """Random uppercase string of length n, e.g. for throwaway node names."""
    return "".join(choice(ascii_uppercase) for _ in range(n))


def filter_axis(feature, exclude):
    """Clean a set of members from those that are defined in an iterable of
    groups. And example would be for iteratively creating rosters, you want
    to remove those assigned to groups in the last round from the next
    iteration.

    :param feature: something like a list of members
    """
    return (x for x in feature if x not in exclude)


def filter_second_axes(features, exclude):
    """Remove all members from exclude from all subgroups

    :param features: something like a list of teams
    """
    return (filter_axis(y, exclude) for y in features)


def shuffle_second_axis(features):
    """Performs an in place shuffle on each second axis in the participant
    groups. Which means the order is randomised.

    :param features: something like a list of teams
    """
    for feature in features:
        shuffle(feature)


def fill_series(group, size):
    """Filling a series such that the choice ends up in the series with the
    probability it reflects.

    :param group: original choices
    :type group: iterable
    :param size: target size of series
    :type size: int
    :return: a series of the choices interspersed with None values
    """
    this_size = len(group)
    if this_size >= size:
        return group

    h = size // this_size
    blanks = (None,) * h
    return chain.from_iterable((None, p) + blanks for p in group)


def probability_series(i):
    """Iterator that can be used for selecting across another iterator in order
    ie for 1 in every i.

    Example: 1 >>> iter(1,1,1 ...)
    Example: 2 >>> iter(1,0,1,0,1,0 ...)
    Example: 3 >>> iter(1,0,0,1,0,0,1,0,0 ...)
    Example: 4 >>> iter(1,0,0,0,1,0,0,0,1,0,0,0 ...)
    """
    return cycle((1,) + (0,) * (i - 1))
