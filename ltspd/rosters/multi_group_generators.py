"""Generate rosters based on mixes and strategies on multiple groups

Functions that build groups dependent on strategies of mixing particular
subgroups of participants. Important and obvious cases would be things like
creating a roster where groups are mixed age, gender, or other demographic
feature, or are mixed affiliation, skill level, seniority, or professional
training.

Explicit examples would be to evenly spread a senior team. Ensuring each team
has the same probability of containing the same number of senior team members.
In the case of a road biking trip, each sub group contains 2 less-able riders.
"""
from itertools import chain, cycle, islice, repeat, tee
from math import floor

from ltspd.rosters.decorators import retry_group_roster
from ltspd.utils import grouper


def _proportional_indices(lengths):
    """Generates as small a sequence of indices that will assist selection in
    comparing groups. Note that lengths need to be in reverse sorted order.

    Example: (50, 50) >> (0,1)
    Example: (600, 500) >> (0,1)
    Example: (6000, 5000, 2000) >> (0, 1, 0, 1, 0, 1, 2)
    Example: (16, 3) >> (0, 0, 0, 0, 0, 1)
    Example: (32, 16, 16, 5) >> (0, 0, 1, 2, 0, 0, 1, 2, 0, 0, 1, 2, 3)
    """
    check, s = tee(lengths, 2)
    length = next(check)
    for i in check:
        if length < i:
            raise ValueError(
                "The calculation relies on the lengths being sorted from "
                "highest to lowest"
            )
        length = i

    i, curr_size, output = 1, next(s), None
    for l in s:
        curr_size += l
        m = round(max(floor(curr_size / l), 1))
        if output is None:
            output = (0,) * (m - 1)
        elif m != i + 1:
            output = output * round(m / len(output))
        output += (i,)
        i += 1
    return output


def _representational_indices(lengths, num_groups):
    """Generates a sequence of indices such that each the same number are in
    each group.
    """
    for i, l in enumerate(lengths):
        for _ in range(round(max(floor(l / num_groups), 1))):
            yield i


def _select_from_groups_gather_all(groups, indices, exhaust=None, output=None, total_size=None):
    """Annoyingly UGLY... but it works for now SO...
    """
    total_size = sum([len(groups[g]) for g in set(indices)]) if total_size is None else total_size
    exhaust = exhaust if exhaust else set()
    output = output if output else []
    if not indices or len(exhaust) == len(groups):
        return []
    spread_size = len(indices)
    positional = cycle(range(spread_size))
    c = filter(lambda x: x not in exhaust, cycle(indices))
    for i in range(total_size):
        p = next(positional)
        i = next(c)
        if groups[i]:
            output.append(groups[i].pop())
        else:
            exhaust.add(i)
            indices = [i for i in indices[p:] + indices[:p] if i not in exhaust]
            output += _select_from_groups_gather_all(groups, indices, exhaust, output)
            # Handle some repeated appending from the recursion
            # there's definitely a smart way of doing this.
            return output[:total_size]
    return output


def _select_from_groups(groups, indices, exclude_tail=False, complete_current=False):
    """Return an iterator collecting the members of the subgroups, note
    that the return is simply the index of the group to select from so that
    it can be run over iterators.exhaust

    Example ((5,5,5), (0,1,2)) >> gen(0,1,2,0,1,2,0,1,2,0,1,2,0,1,2)
    Example ((10,5,5), (0,1,2)) >> gen(0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,0,0,0,0)
    Example ((10,5,5), (0,1,2)) >> gen(0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,0,0,0,0)
    Example ((10,5,5), (0,1,2), True) >> gen(0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0)
    Example ((10,5,5), (0,1,2), False, True) >> gen(0,1,2,0,1,2,0,1,2,0,1,2,0,
        1,2,0)

    The usefuleness of this is to never have to deal with any of the series
    in memory, should lengths be calculated another way, estimated or another
    calculation / representation would be approrpiate.
    """
    exhaust = []
    group_size = len(indices)
    positional = cycle(range(group_size))
    s = tuple(iter(g) for g in groups)
    c = filter(lambda x: x not in exhaust, cycle(indices))
    for _ in chain(*groups):
        p = next(positional)
        try:
            i = next(c)
            yield next(s[i])
        except StopIteration:
            exhaust.append(i)
            if exclude_tail:
                return
            elif complete_current:
                if p == 0:
                    return
                for k in filter(lambda x: x != i, indices[p:]):
                    try:
                        yield (next(s[k]))
                    except StopIteration:
                        pass
                return
            else:
                yield next(s[next(c)])


def _select_from_lengths(lengths, indices, exclude_tail=False, complete_current=False):
    """Return an iterator collecting the indices to pull out of groups, note
    that the return is simply the index of the group to select from so that
    it can be run over iterators.

    Example ((5,5,5), (0,1,2)) >> gen(0,1,2,0,1,2,0,1,2,0,1,2,0,1,2)
    Example ((10,5,5), (0,1,2)) >> gen(0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,0,0,0,0)
    Example ((10,5,5), (0,1,2)) >> gen(0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,0,0,0,0)
    Example ((10,5,5), (0,1,2), True) >> gen(0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0)
    Example ((10,5,5), (0,1,2), False, True) >> gen(0,1,2,0,1,2,0,1,2,0,1,2,0,
        1,2,0)

    The usefuleness of this is to never have to deal with any of the series
    in memory, should lengths be calculated another way, estimated or another
    calculation / representation would be approrpiate.
    """
    exhaust = ()
    # Utility that cycles along the count within the current group meaning
    # we can use it to define behaviour for dealing with the tail after the
    # first group is exhausted.
    positional = cycle(range(len(indices)))
    s = tuple(iter(range(l)) for l in lengths)
    c = filter(lambda x: x not in exhaust, cycle(indices))
    for _ in range(sum(lengths)):
        p = next(positional)
        try:
            i = next(c)
            next(s[i])
            yield i
        except StopIteration:
            exhaust += (i,)
            if exclude_tail:
                return

            elif complete_current:
                if p == 0:
                    return
                for k in filter(lambda x: x != i, indices[p:]):
                    try:
                        next(s[k])
                        yield k
                    except StopIteration:
                        pass
                return

            else:
                next(s[next(c)])
                yield i


def defined_mix(groups, indices):
    """Select the participants such that we include them mixed in the defined
    proportions. For example, having at least 2 guides for every 10 customers.
    This could be achieved with: ((guide_names, customer_names),
    (0,0,1,1,1,1,1,1,1,1,1)). Note that if either the guides or the customer
    names are exhausted the selection will stop.

    Example: (((1,2,3,4),(a,b)), (0,0,1)) >> (1,2,a,3,4,b)
    Example: (((1,2,3,4),(a,b), (x,y)), (0,0,1,2)) >> (1,2,a,x,3,4,b,y)
    """
    return _select_from_groups(groups, indices, False, True)


def even_spread_mix(groups):
    """Combine the participants such that the selection or inclusion of a
    member of each sub group has the same probability over the whole set.

    Note that

    Example: ((1,2),(a,b)) >> (1,2,a,3,4,b)
    Example: ((1,2,3,4),(a,b)) >> (1,2,a,3,4,b)
    """
    groups.sort(key=len, reverse=True)
    return _select_from_groups_gather_all(groups, _proportional_indices((len(g) for g in groups)))


def group_representation(groups, num_groups, exclusions=set(), randomise=True):
    """Ensures that for each group the same number of members are present
    """
    return _select_from_groups(
        groups, tuple(_representational_indices((len(g) for g in groups), num_groups))
    )


@retry_group_roster()
def generate_mixed_size_zip_roster(groups, indices, group_schedule):
    feed = _select_from_groups(groups, indices)
    return chain(
        *(
            islice(grouper(feed, participant_count), num)
            for participant_count, num in group_schedule
        )
    )
