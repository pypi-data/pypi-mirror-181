# Built-In
from typing import Any

# Third-Party
from aiohttp import ClientSession
from orjson import dumps


class HTTPClient:
    """HTTP Client"""

    session: ClientSession | None = None

    def __init__(self, **kwargs) -> None:
        kwargs["raise_for_status"] = kwargs.get("raise_for_status", True)
        kwargs["json_serialize"] = kwargs.get("json_serialize", dumps)

        self.options = kwargs

    def start(self) -> None:
        """Start the session"""
        if not self.session:
            self.session = ClientSession(json_serialize=orjson_dumps)

    async def stop(self) -> None:
        """Close the session"""
        if self.session:
            await self.session.close()
        self.session = None

    def __call__(self) -> ClientSession:
        if not self.session:
            raise RuntimeError("HttpClient is not started")
        return self.session


def orjson_dumps(value: Any) -> str:
    """Serialize a value to JSON using orjson"""
    return dumps(value, default=str).decode()


http_client = HTTPClient()
