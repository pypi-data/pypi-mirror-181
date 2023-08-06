from requests import Session


class Resource:
    def __init__(self, base_url: str, session: Session):
        self.session = session
        self.base_url = base_url.strip("/")

    def _url(self, endpoint):
        endpoint = endpoint.strip("/")
        return f"{self.base_url}/{endpoint}/"
