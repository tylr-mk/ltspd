"""Expand schedules and groupings in practical ways before completion

Note that the typical output of an expand function yields indices or small
patterns of indices, this means they require to be combined with IDs or other
groupings to be useful.
"""

from itertools import chain, combinations


def powerset(iterable_len, nums=None):
    """
    From https://docs.python.org/3.6/library/itertools.html#itertools-recipes

    powerset(3) --> (0,) (1,) (2,) (0,1) (0,2) (1,2) (0,1,2)

    Yields to 0-based indices of items in groupings.

    powerset expresses ways to combine and separate subgroups, in ways that
    guarantee coverage. Say for example you want to create a tennis league
    where in groups of 4 you need to schedule games where all  subgroup members
    face each other and they also play doubles. That can be expressed with:

    powerset(4, (2,4)) --> (0,1) (0,2) (0,3) (1,2) (1,3) (2,3)
    (0,1,2,3)

    As you can see from the output every member plays each other once in the
    across the first 6 games, and then there is one game appended where all
    members play.

    Also lets say you wanted to increase the complexity here and add a single
    person event, say an interview or a one on one evaluation you can generate
    your schedule with powerset(4, (1,2,4))

    3.6: powerset(iterable_len: int, nums=None: iter[int]) -> iter[iter[int]]
    Args:
    -----
        iterable_len (int):
        nums (iter[int]): Total number of members in each set of pairings.
        Note that you can repeat any number if this is the easiest place for
        you to do so... nums = (1,1,1,2,2,4) would be valid, meaning everyone would
        play alone 4 times and play everyone else twice before the end game.
    Returns:
    --------
        iter[iter[int]]

        Combinations of all the indices 0-iterable_len expressed in nums in
        order.
    Raises:
    -------
        ValueError if any of the integers in nums are less than 1 or greater
        than iterable_len
    """
    if nums is None:
        nums = range(1, iterable_len + 1)
    if any(n > iterable_len for n in nums):
        raise ValueError(
            "No num in the numbers provided can be more than " "the iterable length"
        )
    if any(n < 1 for n in nums):
        raise ValueError("Nums must all be greater than 1")
    s = tuple(range(iterable_len))
    return chain.from_iterable(combinations(s, r) for r in nums)


def cycle_positions(positions):
    """Select a simple transposition where the groups are kept the same but
    each member plays in each roll.

    There are alternatives to this where we select specific items from an
    enumerated permutation, or cycle over the range. They both led to more
    confusing code and we don't expect positions to be massive and this
    calculation to ever be huge. Plus some day, considering the likely min
    / max of positions, it might bebetter to just cache or whatever.

    Example: 3 >> (0,1,2), (1,2,0), (2,0,1)

    This  can then be run over a selection of 3 IDs or similar to give you
    selections.

    3.6: cycle_positions(positions)
    :param int positions: the number of positions to allocate
    :return iter(iter(int)):
    """
    if positions <= 1:
        raise ValueError("There must be at least two postions")
    s = tuple(range(positions))
    for i in range(positions):
        yield s[i - positions :] + s[:i]
