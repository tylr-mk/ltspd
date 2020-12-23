from datetime import datetime, timedelta
from typing import List

import attr
from attr import asdict


@attr.s(auto_attribs=True, frozen=True)
class Role:
    pass


@attr.s(auto_attribs=True, frozen=True)
class Structure:
    pass


@attr.s(auto_attribs=True, frozen=True)
class StructureSet:
    structures: List[Structure]


@attr.s(auto_attribs=True, frozen=True)
class Inventory:

    capacity: int
    number: int


@attr.s(auto_attribs=True, frozen=True)
class Attendee:

    unique_id: str


@attr.s(auto_attribs=True, frozen=True)
class InventoryThing:

    inventory: Inventory


@attr.s(auto_attribs=True, frozen=True)
class InventoryAssignment:

    inventory_thing: InventoryThing
    attendees: List[Attendee]


@attr.s(frozen=True, auto_attribs=True)
class ReservableThing(InventoryThing):
    """Placeholder class for type evaluation
    """
    pass


@attr.s(frozen=True, auto_attribs=True)
class ReservableAvailability:
    start: datetime
    end: datetime
    reservable_thing: ReservableThing


@attr.s(frozen=True, auto_attribs=True)
class ReservationThing:
    time_in_seconds: int
    start: datetime
    end: datetime
    reservable_thing: ReservableThing
    inventory: Inventory

    @classmethod
    def from_availability(cls, availability, time, point):
        return cls(
            time,
            availability.start + timedelta(seconds=time*point),
            availability.start + timedelta(seconds=time*(point + 1)),
            availability.reservable_thing,
            availability.reservable_thing.inventory,
        )
