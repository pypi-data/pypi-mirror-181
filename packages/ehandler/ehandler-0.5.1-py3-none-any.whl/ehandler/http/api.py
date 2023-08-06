# Built-In
from typing import Any

# Third-Party
from aiohttp import ClientSession, ClientResponse, ClientResponseError, ContentTypeError
from orjson import loads, JSONDecodeError

# Internal
from ehandler import logger
from .client import http_client


class APIClient:
    """API Client with standard http methods and error handling"""

    global_headers: dict[str, str] = {}

    @property
    def http(self) -> ClientSession:
        """Get aiohttp global ClientSession"""
        return http_client()

    async def get(self, url: str, **kwargs) -> Any:
        """GET request"""
        return await self._request(url, method="GET", **kwargs)

    async def post(self, url: str, **kwargs) -> Any:
        """POST request"""
        return await self._request(url, method="POST", **kwargs)

    async def put(self, url: str, **kwargs) -> Any:
        """POST request"""
        return await self._request(url, method="PUT", **kwargs)

    async def delete(self, url: str, **kwargs) -> Any:
        """DELETE request"""
        return await self._request(url, method="DELETE", **kwargs)

    async def path(self, url: str, **kwargs) -> Any:
        """PATCH request"""
        return await self._request(url, method="PATCH", **kwargs)

    async def _request(self, url: str, method: str, **kwargs) -> Any:
        """
        HTTP Request. Extract the response body and return it.
        Check for status code and raise exception if upper than 400.

        :param url: URL to request
        :param method: HTTP method i.e. GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
        :param kwargs: Additional arguments to pass to the request i.e. headers, data, params, etc.

        :return: Response parsed as a JSON type [dict, list, etc].
        - https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession.request
        """
        req = getattr(self.http, method.lower())
        kwargs["headers"] = kwargs.get("headers", {}) | self.global_headers
        body = None
        try:
            response: ClientResponse
            async with req(url, **kwargs) as response:
                try:
                    body = await response.json(loads=loads)
                except (JSONDecodeError, ContentTypeError):
                    body = await response.text()

                response.raise_for_status()
                return body
        except ClientResponseError as exc:
            await logger.error(await self.__parse_error(exc, body=body, **kwargs))
            raise

    @staticmethod
    async def __parse_error(exc: ClientResponseError, **kwargs) -> dict:
        """
        Parse the error response and return a dict with the error message.

        :param exc: ClientResponseError exception raised by the request
        :return: dict with the error info
        """
        req = exc.request_info
        return kwargs | {
            "url": str(req.url),
            "method": req.method,
            "status_code": exc.status,
            "headers": dict(req.headers),
            "message": exc.message,
        }


api_client = APIClient()
