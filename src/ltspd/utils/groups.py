"""Manipulate and interact with grouped objects

Grouped objects are typically iterables of single objects such as pairs,
rosters, or excluded pairings.
"""

from itertools import chain, permutations


def unnest(feature):
    """Return all the members of an iterable of iterables, for simplicity.
    An example, would be to get all particpants from a roster which will
    be helpful for sanity / checking.

    For practicality we cast this to a set. The reason being for use in other
    features such as list comprehensions [i for i in f if i in unnest(x)].
    The case is that any i that is not in the iterator will cause a full scan
    of all of the remaining operator causing it to exhaust for the next i.
    Even locally this is a problem such that if there is a small ordering
    mismatch occurs behaviour would not be as wanted.

    :param feature: iterable with multiple groups of participants. For example
        a list of teams. Note that the iterable can be infinite or another
        iterator.
    :return: set of all members in the features.
    """
    return set(chain.from_iterable(feature))


def identify_unassigned(participants, groups):
    """Simple set comparison so that unassigned members can be identified
    and returned somewhere useful.
    """
    return set(participants) - unnest(groups)


def explode_subgroups(feature, size=None):
    """Return all the permutations of defined subgroups in an iterable of
    the given size.

    For things like exclusions and defined, ensure that permutations are
    also known for their usage.

    Example: an exclusion set says ("Terrence", "Phillip") must be excluded
    then we need to know that ("Phillip", "Terrence") is not acceptable either.
    Note that if group size is larger than the excluded group then no
    permutations will be returned. If less then all permutations will be
    included (see itertools docs.)

    :param feature: iterable of iterables containing participants typically an
        exclude or defined set.
    :param size: size of groups
    """
    if size is not None:
        return chain.from_iterable(permutations(x, size) for x in feature)
    else:
        return chain.from_iterable(permutations(x, len(x)) for x in feature)
