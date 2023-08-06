# Roadie API Client

### Installing

```bash
pip install python-roadie
```

### Usage

```python
from roadie import APIClient


client = APIClient(token="YOUR-AUTH-TOKEN")
```

### Resources

#### Shipments

_Create shipment_

```python
from roadie.types import (
    Contact,
    Item,
    Address,
    Location,
    TimeWindow,
    ShipmentRequest,
    ShipmentUpdateRequest,
    DeliveryOptions,
)
from datetime import datetime, timedelta


shipment_request = ShipmentRequest(
    reference_id="ABCDEFG12345",
    idempotency_key="d6f9d5bb-1ba1-48d9-9125-6a61490a5ca5",
    alternate_id_1="111",
    alternate_id_2="222",
    description="General shipment description.",
    items=[
        Item(
            description="Item description",
            length=1.0,
            width=1.0,
            height=1.0,
            weight=1.0,
            quantity=1,
            value=20,
        )
    ],
    pickup_location=Location(
        address=Address(
            street1="123 Main Street",
            city="Atlanta",
            state="GA",
            zip="30305",
        ),
        contact=Contact(
            name="Origin Contact",
            phone="4049999999",
        ),
        notes=None,
    ),
    delivery_location=Location(
        address=Address(
            street1="123 Main Street",
            city="Atlanta",
            state="GA",
            zip="30305",
        ),
        contact=Contact(
            name="Origin Contact",
            phone="4049999999",
        ),
        notes=None,
    ),
    pickup_after=datetime.now() + timedelta(hours=4),
    deliver_between=TimeWindow(
        start=datetime.now() + timedelta(hours=4),
        end=datetime.now() + timedelta(hours=8)
    ),
    options=DeliveryOptions(
        signature_required=True,
        notifications_enabled=False,
        over_21_required=False,
        extra_compensation=5.0,
        trailer_required=False,
        decline_insurance=True,
    ),
)

client.shipments.create_shipment(shipment_request)
```

Similarly you can do other operations using the shipments resource
```python

client.shipments.get_shipment(123)

client.shipments.list_shipments(ids=[123, 444], reference_ids=["someref-id"])

client.shipments.update_shipment(123, shipment_update_request)
# shipment_update_request is of type ShipmentUpdateRequest

client.shipments.cancel_shipment(123, code="item_not_ready", comment="Its not ready to be picked")

client.shipments.tip_driver(123, 10.00)

client.shipments.rate_driver(123, 10)

client.shipments.get_signature_image(123)

client.shipments.get_pickup_image(123)

client.shipments.get_delivery_image(123)
```
#### Estimates

```python
client.estimates.create_estimate(estimate_request)
# estimate_request is of type EstimateRequest
```

### Contributing

- We use poetry for building and publishing our package to pypi
- We use pytest for running tests
- To add more resources simply create a file in resource folder and start implementing
- Require tests and approval before merging to main

### Authors

- **Farhath Banu** `farhath@proxyroot.com` `Owner`

