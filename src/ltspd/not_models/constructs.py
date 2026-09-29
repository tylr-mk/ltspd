"""Resources required for participants"""

from ltspd.not_models import LtspdAddressable, LtspdConstruct


class Organisation(LtspdConstruct, LtspdAddressable):
    """ """

    pass


class Series(LtspdConstruct):
    """A way of expressing groups of instances. This could be over time or
    over certain selections. Types of series:

    * Game
    * Event
    * Programme

    Example: A run of a game over time. If you run a pairing game in your
    organisation over 3 months, because you batch invite all new members at
    3 months... your series will expire and allow you to rerun and create new
    assets.

    Example: You run a training day where you can successfully schedule groups
    of 10 attendees to achieve the full day. But you can accommodate any number
    of groups up to 5 at your facility. You can define each as a Series of
    activities and manage them entirely separately.

    A programme is a specialised series of Activities and Events that happen
    over time that can be decoupled from having to rely on attendance to
    specified instances.

    An example would be a 1-5K programme: where individual runs, pair runs, and
    class activities can be attended by a user and they can start at any time
    and progress to different activities at their own pace.

    There is also the assumed idea of progression that can be expressed as
    DAGs.

    Another would be developing a new habit

    An Event is a specialised type of series.

    * Organisation
    """

    pass


class Activity(LtspdConstruct):
    """Activity's are singlular events happening.

    * Organisation
    * Series
    """

    pass


class Resource(LtspdConstruct):
    """
    * Organisation
    * Series
    * Activity
    * NumParticipants
    """

    pass
