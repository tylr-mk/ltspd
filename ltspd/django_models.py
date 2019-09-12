# """Activity is a one-off grouping of participants

# Typically an activity expresses a single type of thing happening such as
# an overnight stay, a class, or a meeting.
# """
# from ltspd.models import LtspdConstruct


# class Activity(LtspdConstruct):
#     """Activity's are singlular events happening.

#     * Organisation
#     * Series
#     * Event
#     """
#     pass
# """
# """
# from ltspd.models import LtspdBase


# class CommunicationStrategy(LtspdBase):
#     """Mostly for email

#     * Organisation
#     * Series
#     * Event
#     * Activity
#     * Template
#     * Schedule
#     * Trigger
#     """
#     pass
# """Resources required for participants
# """
# from ltspd.models import LtspdConstruct, LtspdAddressable


# class Organisation(LtspdConstruct, LtspdAddressable):
#     """
#     """
#     pass


# class Series(LtspdConstruct):
#     """A way of expressing groups of instances. This could be over time or
#     over certain selections.

#     Example: A run of a game over time. If you run a pairing game in your
#     organisation over 3 months, because you batch invite all new members at
#     3 months... your series will expire and allow you to rerun and create new
#     assets.

#     Example: You run a training day where you can successfully schedule groups
#     of 10 attendees to achieve the full day. But you can accommodate any number
#     of groups up to 5 at your facility. You can define each as a Series of
#     activities and manage them entirely separately.

#     A programme is a specialised series of Activities and Events that happen
#     over time that can be decoupled from having to rely on attendance to
#     specified instances.

#     An example would be a 1-5K programme: where individual runs, pair runs, and
#     class activities can be attended by a user and they can start at any time
#     and progress to different activities at their own pace.

#     There is also the assumed idea of progression that can be expressed as
#     DAGs.

#     Another would be developing a new habit

#     An Event is a specialised type of series.

#     * Organisation
#     """
#     pass


# class Activity(LtspdConstruct):
#     """Activity's are singlular events happening.

#     * Organisation
#     * Series
#     """
#     pass


# class Resource(LtspdConstruct):
#     """
#     * Organisation
#     * Series
#     * Activity
#     * NumParticipants
#     """
#     pass
# """Class that ties complex Activities together like a Project Dashboard

# Note that events typically occur over a single continuous timeline but that can
# be paginated into Phases for simplicification and management.
# """
# from ltspd.models import LtspdConstruct


# class Event(LtspdConstruct):
#     """
#     * Organisation
#     """
#     pass
# """
# """

# class FinancialTransaction():
#     pass


# class Coupon():
#     pass
# class Photo():
#     """
#     * Url
#     * Type
#     * Organisation
#     * Series
#     * Activity
#     """
#     pass
# """
# """
# from ltspd.models import LtspdBase


# class Membership(LtspdTimeLimited):
#     """
#     * Role
#     * Organisation
#     * Event
#     * Series
#     * Activity
#     * Group
#     * User
#     * Profile
#     * MembershipFields
#     * Ticket
#     * TicketStatus
#     """
#     pass


# class GroupMembership():
#     """
#     Group
#     User
#     """
#     pass


# class Group(LtspdBase):
#     """
#     """
#     pass
# """ I can't think how to represent this at all, maybe it is just empty.
# """


# class Selection():
#     """
#     * Name
#     * Description
#     * Organisation
#     * Series
#     * MixType
#     * Fields
#     """
#     pass
# from ltspd.model import LtspdAddressable

# class LtspdUser(LtspdAddressable):
#     """Identities are people like objects, that have common attributes such as

#     * Role
#     * PublicName
#     * FirstName
#     * LastName
#     * BirthDate
#     * Gender
#     * About
#     * Profession
#     * AuthenticationFields ...
#     * ...
#     * ...
#     * SocialIDs ...
#     * ...
#     * ...
#     * ...
#     """
#     pass
