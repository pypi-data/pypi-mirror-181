from roadie.resources import Resource
from roadie.types import Estimate, EstimateRequest

ESTIMATE_REQUEST_TIMEOUT = 60


class EstimateResource(Resource):
    def create_estimate(self, estimate_request: EstimateRequest) -> Estimate:
        response = self.session.post(
            self._url("/estimates"),
            data=estimate_request.json(),
            timeout=ESTIMATE_REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        return Estimate.parse_obj(response.json())
