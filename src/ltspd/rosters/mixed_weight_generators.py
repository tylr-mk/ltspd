"""Rosters for occasions where participants are not consistently weighted

These may be more practical and applied directly, such as trying to combine
to the requirements of a mix process with each participant taking up multiple
weights. One example would be to apply this to a single event seating plan
where we want to seat attendees with their plus ones.

The other way to use this would be as an outer principal. For example, at a
corporate training course that has 20 seats per day. And there are 10 companies
with varying number of employees between 3 and 8, these functions could be used
to create a schedule where you only schedule whole companies.

Two notes:

    *   Many of these functions will consider something called non-breaking,
        which toggles the behaviour of whether groups can be broken at the
        point of dividing into teams.

    *   Not all of these functions treat these problems as opimisation tasks,
        those that do use Google OR Tools and cast them accordingly.
"""
