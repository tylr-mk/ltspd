from datetime import datetime, timedelta

from attrs import frozen


@frozen
class Role:
    pass


@frozen
class Structure:
    pass


@frozen
class StructureSet:
    structures: list[Structure]


@frozen
class Inventory:
    capacity: int
    number: int


@frozen
class Attendee:
    unique_id: str


@frozen
class InventoryThing:
    inventory: Inventory


@frozen
class InventoryAssignment:
    inventory_thing: InventoryThing
    attendees: list[Attendee]


@frozen
class ReservableThing(InventoryThing):
    """Placeholder class for type evaluation"""


@frozen
class ReservableAvailability:
    start: datetime
    end: datetime
    reservable_thing: ReservableThing


@frozen
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
            availability.start + timedelta(seconds=time * point),
            availability.start + timedelta(seconds=time * (point + 1)),
            availability.reservable_thing,
            availability.reservable_thing.inventory,
        )
