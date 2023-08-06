from typing import List

from pydantic import parse_obj_as

from roadie.resources import Resource
from roadie.types import ShipmentRequest, Shipment


SHIPMENT_REQUEST_TIMEOUT = 60


class ShipmentResource(Resource):
    def create_shipment(self, shipment_request: ShipmentRequest) -> Shipment:
        response = self.session.post(
            self._url("/shipments"),
            data=shipment_request.json(),
            timeout=SHIPMENT_REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        return Shipment.parse_obj(response.json())

    def get_shipment(self, shipment_id: int) -> Shipment:
        response = self.session.get(
            self._url(f"/shipments/{shipment_id}"),
            timeout=SHIPMENT_REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        return Shipment.parse_obj(response.json())

    def list_shipments(
        self,
        ids: List[int] = [],
        reference_ids: List[str] = [],
    ) -> List[Shipment]:
        params = {}

        if ids:
            params["ids"] = ",".join(map(str, ids))

        if reference_ids:
            params["reference_ids"] = ",".join(reference_ids)

        response = self.session.get(
            self._url(f"/shipments"),
            params=params,
            timeout=SHIPMENT_REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        return parse_obj_as(List[Shipment], response.json())

    def update_shipment(
        self,
        shipment_id: int,
        shipment_request: ShipmentRequest,
    ) -> Shipment:
        response = self.session.patch(
            self._url(f"/shipments/{shipment_id}"),
            data=shipment_request.json(),
            timeout=SHIPMENT_REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        return Shipment.parse_obj(response.json())

    def cancel_shipment(self, shipment_id: int, code: str = "", comment: str = ""):
        response = self.session.delete(
            self._url(f"/shipments/{shipment_id}"),
            json={
                "cancellation_code": code,
                "cancellation_comment": comment,
            },
            timeout=SHIPMENT_REQUEST_TIMEOUT,
        )
        response.raise_for_status()

    def tip_driver(self, shipment_id: int, amount: float):
        response = self.session.post(
            self._url(f"/shipments/{shipment_id}/tips"),
            json={"amount": amount},
            timeout=SHIPMENT_REQUEST_TIMEOUT,
        )
        response.raise_for_status()

    def rate_driver(self, shipment_id: int, rating: int):
        response = self.session.post(
            self._url(f"/shipments/{shipment_id}/ratings"),
            json={"value": rating},
            timeout=SHIPMENT_REQUEST_TIMEOUT,
        )
        response.raise_for_status()

    def get_signature_image(self, shipment_id: int) -> bytes:
        response = self.session.post(
            self._url(f"/shipments/{shipment_id}/images/signature"),
            timeout=SHIPMENT_REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        return response.content

    def get_pickup_image(self, shipment_id: int) -> bytes:
        response = self.session.post(
            self._url(f"/shipments/{shipment_id}/images/pickup"),
            timeout=SHIPMENT_REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        return response.content

    def get_delivery_image(self, shipment_id: int) -> bytes:
        response = self.session.post(
            self._url(f"/shipments/{shipment_id}/images/delivery"),
            timeout=SHIPMENT_REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        return response.content
