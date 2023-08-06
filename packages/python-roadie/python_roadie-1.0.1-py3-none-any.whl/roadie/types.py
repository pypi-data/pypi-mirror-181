import pydantic

from datetime import datetime
from typing import Optional, List


def iso_8601(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


class CustomBaseModel(pydantic.BaseModel):
    class Config:
        json_encoders = {datetime: iso_8601}


class Item(CustomBaseModel):
    reference_id: Optional[str]
    description: Optional[str]  # TODO says mandatory in api docs check and change
    length: float
    width: float
    height: float
    weight: float
    quantity: int
    value: float


class Address(CustomBaseModel):
    name: Optional[str]
    store_number: Optional[str]
    street1: str
    street2: Optional[str]
    city: str
    state: str
    zip: str
    latitude: Optional[float]
    longitude: Optional[float]


class Contact(CustomBaseModel):
    name: str
    phone: str


class Location(CustomBaseModel):
    address: Address
    contact: Contact
    notes: Optional[str]


class EstimateLocation(Location):
    contact: Optional[Contact]


class TimeWindow(CustomBaseModel):
    start: datetime
    end: datetime


class EstimateRequest(CustomBaseModel):
    items: List[Item]
    pickup_location: Location
    delivery_location: Location
    pickup_after: datetime
    deliver_between: TimeWindow


class Estimate(CustomBaseModel):
    price: float
    size: str
    estimated_distance: float


class DeliveryOptions(CustomBaseModel):
    signature_required: bool
    notifications_enabled: Optional[bool]
    over_21_required: Optional[bool]
    extra_compensation: Optional[float]
    trailer_required: Optional[bool]
    decline_insurance: Optional[bool]


class ShipmentRequest(CustomBaseModel):
    reference_id: str
    idempotency_key: Optional[str]
    alternate_id_1: Optional[str]
    alternate_id_2: Optional[str]
    deliver_between: TimeWindow
    description: Optional[str]
    items: List[Item]
    pickup_location: Location
    delivery_location: Location
    pickup_after: datetime
    deliver_between: TimeWindow
    options: DeliveryOptions


class ShipmentUpdateRequest(CustomBaseModel):
    reference_id: Optional[str]
    alternate_id_1: Optional[str]
    alternate_id_2: Optional[str]
    deliver_between: TimeWindow
    description: Optional[str]
    items: Optional[List[Item]]
    pickup_location: Optional[Location]
    delivery_location: Optional[Location]
    pickup_after: Optional[datetime]
    deliver_between: Optional[TimeWindow]
    options: Optional[DeliveryOptions]


class EventLocation(CustomBaseModel):
    latitude: float
    longitude: float


class Event(CustomBaseModel):
    name: str
    occurred_at: datetime
    location: EventLocation


class Shipment(ShipmentRequest):
    tracking_number: str
    signatory_name: Optional[str]
    price: float
    estimated_distance: float
    events: List[Event]
    created_at: datetime
    updated_at: datetime
