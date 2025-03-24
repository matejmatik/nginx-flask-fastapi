from asyncio import sleep as asyncio_sleep
from logging import getLogger
from httpx import AsyncClient, RequestError, HTTPStatusError

logger = getLogger(__name__)


class AsyncAPIClient:
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
        self.__client = AsyncClient(
            auth=self.__auth, headers=self.__headers, timeout=timeout
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    def set_headers(self, headers: dict):
        self.__headers.update(headers)
        self.__client.headers.update(headers)

    async def _request(
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
                response = await self.__client.request(
                    method, url, params=params, json=data
                )
                response.raise_for_status()
                return response.json()
            except (RequestError, HTTPStatusError) as exc:
                logger.warning(
                    f"Attempt {attempt + 1} for {method} {url} failed: {exc}"
                )
                if attempt < retries - 1:  # Retry if more attempts are available
                    await asyncio_sleep(backoff)
                    backoff *= 2  # Exponential backoff
                else:
                    logger.error(f"All retry attempts failed for {method} {url}")
                    raise
            except Exception as exc:
                logger.error(f"Unexpected error occurred: {exc}")
                raise

    async def get(self, tag: str, params: dict = None, retries: int = 3):
        return await self._request("GET", tag, params=params, retries=retries)

    async def post(
        self, tag: str, params: dict = None, data: dict = None, retries: int = 3
    ):
        return await self._request(
            "POST", tag, params=params, data=data, retries=retries
        )

    async def delete(self, tag: str, params: dict = None, retries: int = 3):
        return await self._request("DELETE", tag, params=params, retries=retries)

    async def patch(
        self, tag: str, params: dict = None, data: dict = None, retries: int = 3
    ):
        return await self._request(
            "PATCH", tag, params=params, data=data, retries=retries
        )

    async def update(
        self, tag: str, params: dict = None, data: dict = None, retries: int = 3
    ):
        return await self._request(
            "PUT", tag, params=params, data=data, retries=retries
        )

    async def close(self):
        await self.__client.aclose()


class APIClientDependency:
    def __init__(self, hostname: str, username: str = None, password: str = None):
        self.client = None
        self.hostname = hostname
        self.username = username
        self.password = password

    async def init(self):
        if self.client is None:
            self.client = AsyncAPIClient(self.hostname, self.username, self.password)

    async def __call__(self) -> AsyncAPIClient:
        if not self.client:
            await self.init()
        return self.client


# Example usage:
# async def main():
#     api_dependency = APIClientDependency("https://api.example.com", username="user", password="pass")
#     api_client = await api_dependency()
#     response = await api_client.get("/endpoint")
#     print(response)
#     await api_client.close()
