import requests

from roadie.resources.estimates import EstimateResource
from roadie.resources.shipments import ShipmentResource


class APIClient:
    _shipments = None
    _estimates = None

    def __init__(self, base_url="api.roadie.com", token=None, version="v1"):
        self.base_url = f"https://{base_url}/{version}/"
        self.token = token

        # Create a session for re-use
        self.session = requests.Session()
        self.session.headers.update(self.auth_headers)

    @property
    def auth_headers(self):
        headers = {"Content-Type": "application/json"}

        if self.token:
            headers.update({"Authorization": f"Bearer {self.token}"})

        return headers

    @property
    def shipments(self):
        if self._shipments is None:
            self._shipments = ShipmentResource(self.base_url, self.session)

        return self._shipments

    @property
    def estimates(self):
        if self._estimates is None:
            self._estimates = EstimateResource(self.base_url, self.session)

        return self._estimates
