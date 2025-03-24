from time import sleep
from logging import getLogger
import requests

logger = getLogger(__name__)


class SyncAPIClient:
    __slots__ = ("hostname", "__auth", "__headers", "__client")

    def __init__(
        self,
        hostname: str,
        username: str = None,
        password: str = None,
        timeout: int = 10,
    ):
        if not hostname:
            raise ValueError("Hostname is required")
        elif not isinstance(hostname, str):
            raise TypeError("Hostname must be a string")
        elif not hostname.startswith("http"):
            raise ValueError("Hostname must start with 'http' or 'https'")

        self.hostname = hostname
        self.__auth = (username, password) if username and password else None
        self.__headers = {"accept": "application/json"}
        self.__client = requests.Session()
        self.__client.auth = self.__auth
        self.__client.headers.update(self.__headers)
        self.__client.timeout = timeout

    def set_headers(self, headers: dict):
        self.__headers.update(headers)
        self.__client.headers.update(headers)

    def _request(
        self,
        method: str,
        tag: str,
        params: dict = None,
        data: dict = None,
        retries: int = 3,
    ):
        params = params or {}
        data = data or {}
        url = f"{self.hostname}{tag}"
        backoff = 1  # Initial backoff in seconds

        for attempt in range(retries):
            try:
                response = self.__client.request(method, url, params=params, json=data)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, requests.HTTPError) as exc:
                logger.warning(
                    f"Attempt {attempt + 1} for {method} {url} failed: {exc}"
                )
                if attempt < retries - 1:
                    sleep(backoff)
                    backoff *= 2  # Exponential backoff
                else:
                    logger.error(f"All retry attempts failed for {method} {url}")
                    raise
            except Exception as exc:
                logger.error(f"Unexpected error occurred: {exc}")
                raise

    def get(self, tag: str, params: dict = None, retries: int = 3):
        return self._request("GET", tag, params=params, retries=retries)

    def post(self, tag: str, params: dict = None, data: dict = None, retries: int = 3):
        return self._request("POST", tag, params=params, data=data, retries=retries)

    def delete(self, tag: str, params: dict = None, retries: int = 3):
        return self._request("DELETE", tag, params=params, retries=retries)

    def patch(self, tag: str, params: dict = None, data: dict = None, retries: int = 3):
        return self._request("PATCH", tag, params=params, data=data, retries=retries)

    def update(
        self, tag: str, params: dict = None, data: dict = None, retries: int = 3
    ):
        return self._request("PUT", tag, params=params, data=data, retries=retries)

    def close(self):
        self.__client.close()


class ApiClientDependency:
    def __init__(
        self,
        hostname: str,
        username: str = None,
        password: str = None,
    ):
        self.client = None
        self.hostname = hostname
        self.username = username
        self.password = password

    def init(self):
        if self.client is None:
            self.client = SyncAPIClient(self.hostname, self.username, self.password)

    def __call__(self) -> SyncAPIClient:
        if not self.client:
            self.init()
        return self.client
