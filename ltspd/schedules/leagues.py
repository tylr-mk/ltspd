"""Construct leagues for a roster and timetable

Leagues are sets of games where a set number of teams take part in each.

Design choices:

 * Some functions ones where we assume the item can be infinite or any number,
   and ones where we hope to know the count up front.
 * Some methods don't find a solution, but try to allocate in a pattern from
   argds because finding effective algorithm design is currently out of scope.

"""
from itertools import chain, combinations, permutations, tee

from ltspd.schedules.decorators import randomise
from ltspd.utils import grouper
from ltspd.utils.expand import powerset


def _some_unclumping_parallel_plays():
    """We start each next group from next selection in the schedule which
    means back to back will nearly always happen, but should remove running
    through and exhausting each in order.
    """
    pass


def _clumped_parallel_plays(schedule, max_play, count=None):
    """Simply grabs the first it can which means the order really impacts
    who will be assigned.
    """
    # count = count if count else len(schedule)
    # schedule, output, grouped = iter(schedule), (), ()
    # source = tee(schedule, 1)[0]
    # max_iterations = 1000
    # for i in this_cycle:
    #     grouping, assigned, n, i = (), (), 0, tuple(i)
    #     if not any((a in i for a in assigned)):
    #         grouping += (i,)
    #         assigned += i
    #         n += 1

    #     if n == max_play:
    #         output += grouping
    #         continue
    pass


def parrallel_plays(schedule, max_play=2, clump=True):
    """When generating a league(, combinations may playable in parallel, lets
    offer that. We're going to take this as take first!

    This is problematic in many senses. We take first and that will introduce
    bias in selection that we are not accounting for, nor providing a way
    round. For example, the first members of the identified group are going
    to turn up in all of the first parallel plays, ostensibly til they are used
    up, in order. Unless you shuffle the incoming schedule. But shuffling
    inhibits choosing by design! (Like these are 5 minute intense sessions,
    there are 10 for each to do for each member, and you can do no more than
    3, of course... in my I'm now engineering for hypothetical use cases
    which I should stop!)... Maybe shuffle and refine after this step!

    It's also a while loop, which is not fun! We could also come up with cases
    where we get trapped trying to select from subsets of games that cannot be
    played together!

    Again, we rely on this not being massive! So we create tuples and evaluate.
    I wish I could think of a better approach. AAAAAAAaaaaarrrrh
    """
    # schedule, output, grouped, remainder = iter(schedule), (), (), 1
    # source = tee(schedule, 1)[0]
    # max_iterations = 100

    # while r < max_play:
    #     remainder = tuple(a, source)

    # for i in source:
    #     grouping, assigned, n, i = (), (), 0, tuple(i)
    #     if not any((a in m for a in assigned)):
    #         grouping += (i,)
    #         assigned += i
    #         n += 1

    #     if n == max_play:
    #         grouped += grouping
    #         continue

    #     if n == max_play:
    #         output += grouping
    pass


def test_continue():
    remainder = 5
    while remainder < 8:
        for i in range(8):
            if i == 2:
                print("alsdkj")
            print("es")
            print("fds")
            print(i)
        remainder += 1


@randomise
def all_play_once(participants, positions=2, must_play_positions=False):
    """Return a simple league setup of initiation where all participants
    playoff, note that this works in simplistic cases or should be used as a
    first step. Note that you can remove bias that could otherwise be
    introduced by subselecting games.

    Point for considerations
    ------------------------

    * must_play_positions=True

    So here we provide permutations meaning that each team plays all opponents
    in all combinatoric sets, for example: if the pitch has two ends (and for
    whatever reason swapping in the event is inappropriate) a plays b from both
    north and south. The problem gets even bigger when you have >3 positions.

    Either you can play many at once... in which case, how do you pick your
    order.??? TODO

    Or you likely don't have enough games to play your full league. Simply, use
    the fair selector in ltspd.utils.refine.limited_game_selector. This gives
    the fairest distribution or pairings and positions.
    """
    if must_play_positions:
        return permutations(participants, positions)
    return combinations(participants, positions)


@randomise
def all_types_played(participants, schedules, max_consistency=None):
    """Create a league where there are different game types
    """

    if max_consistency is None:
        return (grouper(participants, s.participants) for s in schedules)

    activities = (a.participants for a in (next(tee(i, 1)[0]) for i in schedules))
    ns = sorted(list(tee(activities, 1)[0]), reverse=True)
    num = ns[max_consistency]
    candidate_groups = chain(
        *(powerset(g, tuple(n for n in ns if n < num)) for g in grouper(participants, ns))
    )
    return candidate_groups


@randomise
def all_types_played_with_consistency(participants, schedules):
    pass
