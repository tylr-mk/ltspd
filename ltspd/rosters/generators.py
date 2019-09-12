"""A roster pseudo-randomly assigns all participants into groupings

Note that the combination can either be explicitly excluded or defined every
other combination is expected to be okay.

For now the best way to ensure a groups or rosters contain more complex logic
is to manually edit them.
"""
from itertools import chain, islice

from ltspd.rosters.decorators import retry_roster
from ltspd.rosters.utils import grouper


@retry_roster(use_exclusions=True)
def generate_random_roster(participants, group_size=2, exclusions=set(), randomise=True):
    """Return one roster of pairings for an activity, it will generate roster
    that includes no pairings defined in either the exclusions or defined
    argument.

    The behaviour here is determined that if the roster must include a defined
    pairing then that should be included regardless of their exclusion rules.

    :param participants: user ids to be considered for pairing
    :type participants: list (must be mutable as is shuffled in place)
    :param exclusions: pairing of user ids that must not be present in the
        generated roster.
    """
    return grouper(participants, group_size)


@retry_roster()
def generate_mixed_size_roster(
    participants, group_schedule, exclusions=set(), randomise=True
):
    """Return one roster of groupings for the participants to be allocated to
    the schedule. While this is generalised and can be used to make mixed
    teams, this would be used for organising members into any mixed event where
    order of schedule could be order to represent time available or priority.

    Example schedules:

      * A number of taxis, or mixed size transportation coming at times
      * A number of hotel rooms, or other accommodation with piority, ie. a
        campsite that would look to fill the slots closest to the centre
        first
      * Tables available at a dining event

    Detailed example:

        Given that accommodation or rooms of certain sets have mixed capacity
        and priority and participants provided can be randomly paired, with
        some other conditions this expects to be okay.

        The simplest way to use this most effectively is to order your
        accommodation options by priority of filling, and then sub-grouping by
        bed count for each accommdation.

        An example would be if you have a lodge with 6 4-person cabins and 6
        6-person cabins, if all equal you might use
        group_schedule=((6, 4), (6, 6)), but there are times where the lodge
        might want to fill 2 of the 6-person cabins foremost because they are
        closer to the admin tent. So you might choose ((6, 2), (4, 4), (6, 4)).

    The behaviour here is determined that if the roster must include a  defined
    pairing then that should be included regardless of their exclusion rules.

    :param participants: user ids to be considered for pairing
    :type participants: list (must be mutable as is shuffled in place)
    :param group_schedule: an iterable representation of resources in order,
        containing participant count and the number available.
    :type group_schedule: iterable of sequence
    :param exclusions: pairing of user ids that must not be present in the
        generated roster.
    :param defined: pairings that must be included in the roster.
    """
    participants = iter(participants)
    return chain(
        *(
            islice(grouper(participants, num), participant_count)
            for participant_count, num in group_schedule
        )
    )
