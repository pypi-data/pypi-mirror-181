# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roadie', 'roadie.resources']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'python-roadie',
    'version': '1.0.1',
    'description': 'Python client for roadie API',
    'long_description': '# Roadie API Client\n\n### Installing\n\n```bash\npip install python-roadie\n```\n\n### Usage\n\n```python\nfrom roadie import APIClient\n\n\nclient = APIClient(token="YOUR-AUTH-TOKEN")\n```\n\n### Resources\n\n#### Shipments\n\n_Create shipment_\n\n```python\nfrom roadie.types import (\n    Contact,\n    Item,\n    Address,\n    Location,\n    TimeWindow,\n    ShipmentRequest,\n    ShipmentUpdateRequest,\n    DeliveryOptions,\n)\nfrom datetime import datetime, timedelta\n\n\nshipment_request = ShipmentRequest(\n    reference_id="ABCDEFG12345",\n    idempotency_key="d6f9d5bb-1ba1-48d9-9125-6a61490a5ca5",\n    alternate_id_1="111",\n    alternate_id_2="222",\n    description="General shipment description.",\n    items=[\n        Item(\n            description="Item description",\n            length=1.0,\n            width=1.0,\n            height=1.0,\n            weight=1.0,\n            quantity=1,\n            value=20,\n        )\n    ],\n    pickup_location=Location(\n        address=Address(\n            street1="123 Main Street",\n            city="Atlanta",\n            state="GA",\n            zip="30305",\n        ),\n        contact=Contact(\n            name="Origin Contact",\n            phone="4049999999",\n        ),\n        notes=None,\n    ),\n    delivery_location=Location(\n        address=Address(\n            street1="123 Main Street",\n            city="Atlanta",\n            state="GA",\n            zip="30305",\n        ),\n        contact=Contact(\n            name="Origin Contact",\n            phone="4049999999",\n        ),\n        notes=None,\n    ),\n    pickup_after=datetime.now() + timedelta(hours=4),\n    deliver_between=TimeWindow(\n        start=datetime.now() + timedelta(hours=4),\n        end=datetime.now() + timedelta(hours=8)\n    ),\n    options=DeliveryOptions(\n        signature_required=True,\n        notifications_enabled=False,\n        over_21_required=False,\n        extra_compensation=5.0,\n        trailer_required=False,\n        decline_insurance=True,\n    ),\n)\n\nclient.shipments.create_shipment(shipment_request)\n```\n\nSimilarly you can do other operations using the shipments resource\n```python\n\nclient.shipments.get_shipment(123)\n\nclient.shipments.list_shipments(ids=[123, 444], reference_ids=["someref-id"])\n\nclient.shipments.update_shipment(123, shipment_update_request)\n# shipment_update_request is of type ShipmentUpdateRequest\n\nclient.shipments.cancel_shipment(123, code="item_not_ready", comment="Its not ready to be picked")\n\nclient.shipments.tip_driver(123, 10.00)\n\nclient.shipments.rate_driver(123, 10)\n\nclient.shipments.get_signature_image(123)\n\nclient.shipments.get_pickup_image(123)\n\nclient.shipments.get_delivery_image(123)\n```\n#### Estimates\n\n```python\nclient.estimates.create_estimate(estimate_request)\n# estimate_request is of type EstimateRequest\n```\n\n### Contributing\n\n- We use poetry for building and publishing our package to pypi\n- We use pytest for running tests\n- To add more resources simply create a file in resource folder and start implementing\n- Require tests and approval before merging to main\n\n### Authors\n\n- **Farhath Banu** `farhath@proxyroot.com` `Owner`\n\n',
    'author': 'Farhath Banu',
    'author_email': 'farhath@proxyroot.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fbanu95/python-roadie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
