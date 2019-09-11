"""
"""
from itertools import chain, zip_longest

from ltspd.utils import grouper


def make_groups(participants, group_size=2):
    """Steps through and slices a collection of objects in order to create a
    set of groups of the defined group_size. Returned as a set for convenience
    and comparison.

    Note that the step is equal to the group size, and the start is an offset
    from 0 to the group_size, meaning that the group will be split into the
    same number of subgroups as the group size, meaning they can be zipped to
    construct the final groupings.

    :param participants: series of objects
    :type participants: list (must be mutable as is shuffled in place)
    :param group_size: size that groups should be
    :type group_size: integer
    :returns: a set of groups of size
    """
    return grouper(participants, group_size)


def zip_mix(groups, method=zip_longest):
    """Ensures that a roster contains pairings that ensure there groups are
    based on mixed participants.

    Where this becomes useful is for when group size doesn't guarantee a member
    from each group. Or when...

    For example, building a group that has at least one senior team member in.
    Or to have pairings consisting of one from team a and team b. The results
    are achieved by shuffling so that if you do specificy more groups to mingle
    than group size.

    :param participants: user ids to be considered for pairing
    :type participants: list (must be mutable as is shuffled in place)
    :param exclusions: pairing of user ids that must not be present
        in the generated roster.
    :param defined: pairings that must be included in the roster.
    """
    return chain.from_iterable((method(*groups)))


def zip_groups(groups, group_size=2):
    return make_groups([i for i in zip_mix(groups) if i is not None], group_size)
