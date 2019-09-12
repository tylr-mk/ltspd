"""Transform and refine objects which rely on ordering and selection

"""
from copy import copy
from itertools import accumulate, chain, islice, permutations, tee, zip_longest

from numpy.random import shuffle

from ltspd.utils import grouper, probability_series

EXCLUDE_FLAG = "EXCLUDE"


def nwise_mixer(num, n=2):
    """Creates the mixing groups by indices where members are grouped with
    with diferently but with recurring members.

    nwise_mixer(4) --> (0,1), (1,2), (2,3), (3,0)
    nwise_mixer(4,3) --> (0,1,2), (1,2,3), (2,3,0), (3,0,1)
    """
    b = tuple(range(num))
    b += b[: (n % num) - 1]
    args = tee(b, n)
    # exhaust the first of the iterators
    for i in (i for x, i in permutations(range(n), 2) if x < i):
        next(args[i], None)
    return zip(*args)


def cycle_step(indices, num):
    """Provide an iterator that combines ascending ranges from the start point
    of the indices provided for the total number provided, taking the modulo
    so that it cycles back from end to 0.

    This is a utility feature that is used in correctly extracting indices
    from specially created series (typically number series that are created
    for defined mix types). The reason for doing this is that specialist
    mix types rely on identifying indices over a number series because of maths,
    but consistently extracting the right members is also crucial.

    Note that we take the modulo, so as though we're pulling that indice from
    the range(num) cyclcing forever...

    Warning
    -------
        Not another application.

        Another application would be say you had a list of ranked experts and
        you wanted to use their ordinality for selection. So you want to pair
        everyone in the list, you want a better with a more junior but you
        don't want there to be a more than 10 rank gap, you could do
        ((0,9), x). Similary, you could do Top, 3 ranks, 10 ranks for a better
        spread ((0,2,9),x)

    Example: (0,1,3), 5 >> [0, 1, 3, 1, 2, 4, 2, 3, 0, 3, 4, 1, 4, 0, 2]

    :param iter(int) indices: the set of indices to take as starting points
    :param int num: the upper most index or range of set
    :rtype: generator(integers)
    """
    return ((i + n) % num for n in range(num) for i in indices)


def position_mixer(num, positions):
    """Generate the index extraction for all members, such that all members
    are in every position once and plays a new set of members in each game.

    Each index is placed in every position but groups have no or few
    repeating subgroups. If you don't want clear progression then you need to
    shuffle the returned series, or construct the new schedule from
    iterator.pop(random). Note that this is used when all teams must play and
    all games can be provided. It is not good for when number of games is
    limitied and finding a good solution then.

    Example: (1,2,3,4,5,6), 2 >> (1,2), (3,4), (5,6), (2,3), (4,5), (6,1)
    Example: (1,2,3,4,5,6,7), 3 >> (1,2,4), (2,3,5), (3,4,6), (4,5,7),
        (5,6,1), (6,7,2), (7,1,3)

    Use cases: when you want everyone to have a go at a roll, and as much as
    is possible ensure each member plays with the maximum number of other
    members.
    """
    min_num = min(num, 2 ** positions - 1 if positions < 5 else positions ** 2)
    steps = list(
        i % min_num for i in (accumulate([0] + [2 ** i for i in range(positions - 1)]))
    )
    return grouper(cycle_step(steps, num), positions)


def apply_mixer(schedule, mix):
    """Mixers simply return indices or number series
    """
    return ((schedule[i] for i in g) for g in mix)


def break_up(schedule, break_schedule=None):
    """Add a breaking schedule for regular or defined event breaks, common
    break patterns include breaking for meals. Note that the default is to
    provide a break in between every game.
    """
    if not break_schedule:
        mix_in = (None,) * len(schedule)
    else:
        mix_in = [(EXCLUDE_FLAG,) * n + (None,) for n in break_schedule]
    return chain.from_iterable(
        a for a in zip_longest(schedule, mix_in) if a != EXCLUDE_FLAG
    )


def sliding_position_mixer(schedule, pairings=2):
    """Each selection is placed in every position but groups are sliding

    Example: (1,2,3,4,5,6), 3 >> (1,2,3), (2,3,4), (3,4,5).... etc

    Use cases: when you want everyone to have a go at a roll, meet a new person
    for each each event, but retain as many relationships as possible (i.e.:
    people change groupings rarely and there's only ever one new member but
    teams always change)
    """

    return apply_mixer(schedule, nwise_mixer(len(schedule), pairings))


def limited_game_selector(games, schedule, start=()):
    """Fairly select a the games from a schedule if not enough slots are
    available from the mixer. Apply this before shuffling, randomising, or
    other schedule refinement steps.

    Note that as we pass over having more than half of the slots available
    the order of the returned list is somewhat lost. The game selection has
    the same benefits but the ordering of the output may lose some of the
    generated or built intuation around scheduling. Rather than make this
    logic complex using ranges and accumulating steps, it is advised to
    just reorder the output of this function by a retained structure.

    There is another way to think about this which is as indexes over a range
    and iterating, selecting, and zipping over the return of those number
    series.
    """
    schedule = tuple(schedule)
    if games > len(schedule):
        return schedule
    k = len(schedule) // (games)
    if k != 1:
        p = probability_series(k)
        return chain(start, islice((s for s in schedule if next(p)), games))

    new = copy(schedule)
    new = new[1::2]
    _schedule = schedule[::2]
    games -= len(_schedule)
    start = chain(start, _schedule)
    return limited_game_selector(games, new, start)


def remove_back_to_backs(schedule, iteration=0, step_backs=1):
    """Reorder the schedule by removing any instance where back to backs are
    seen, shufflinf and appending.

    The practical use case of this is to generally shuffle with a little more
    practicality than using numpy.shuffle as it will ensure the comfort of not
    having any back to back games scheduled.

    Note that step_backs = 1 will attempt to have no games scheduled where
    those selected are not playing back to back.
    """
    if iteration > 10:
        return schedule
    reserve = []
    for i in range(1, len(schedule)):
        if (
            any([p in chain(*schedule[i - step_backs : i]) for p in schedule[i]])
            and i - step_backs not in reserve
        ):
            reserve.append(i)

    if not reserve:
        return schedule

    reserved = [schedule.pop(r) for r in reversed(reserve)]
    shuffle(reserved)
    return remove_back_to_backs(schedule + reserved, iteration + 1)
