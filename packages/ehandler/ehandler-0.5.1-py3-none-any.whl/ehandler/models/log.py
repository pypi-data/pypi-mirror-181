# Built-In
import traceback
from typing import Any
from urllib.parse import parse_qs

# Third-Party
import orjson
from pydantic import root_validator
from fastapi import Request, Response

# Internal
from ehandler.settings import settings
from ehandler.models.base import BaseModel
from ehandler.utils import update, get


class LogRequestModel(BaseModel):
    """
    Contains the request information
    """

    # Need to be set manually/externally
    body: dict | list | bytes | None = None

    # Default
    server_ip: str | None = settings.SERVER_IP

    # Set from `request_obj`
    headers: dict[str, list[str]] | None = None
    method: str | None = None
    protocol: str | None = None
    query_params: dict[str, list[str]] | None = None
    url: str | None = None
    remote_ip: str | None = None
    request_size: int | None = None
    user_agent: str | None = None

    request_obj: Request

    class Config:
        """
        Model Config
        """

        fields = {"request_obj": {"exclude": True}}

    @root_validator()
    @classmethod
    def parse_request(cls, values: dict[str, Any]) -> dict[str, Any]:
        """
        Set vaues from request
        """
        req: Request | None = None
        if not (req := values.get("request_obj")):
            return values

        scope = req.scope
        protocol = f'{scope.get("scheme", "")}/{scope.get("http_version", "")}'.upper()

        headers = req.headers
        headers_params = "&".join((f"{k}={v}".lower() for k, v in headers.items()))

        if not (server_ip := values.get("server_ip")):
            server_ip = ":".join((str(i) for i in scope.get("server") or []))

        remote_ip: str | None = get(headers, "x-forwarded-for")
        if not remote_ip and (client := req.client):
            remote_ip = f"{client.host}:{client.port}"

        values_temp = {
            "protocol": protocol,
            "server_ip": server_ip,
            "remote_ip": remote_ip,
            "method": req.method,
            "headers": parse_qs(headers_params),
            "url": str(req.url),
            "user_agent": get(headers, "user-agent"),
            "query_params": parse_qs(str(req.query_params)),
            "request_size": get(headers, "content-length"),
        }

        return update(values, values_temp)


class LogResponseModel(BaseModel):
    """
    Contains the response information
    """

    # Need to be set manually/externally
    latency: int | None = None  # In nanoseconds

    # Set from `response_obj`
    headers: dict[str, list[str]]
    content: dict | list | bytes
    status: int
    response_size: int | None = None

    response_obj: Response

    class Config:
        """
        Model Config
        """

        fields = {"response_obj": {"exclude": True}}

    @root_validator(pre=True)
    @classmethod
    def parse_response(cls, values: dict[str, Any]) -> dict[str, Any]:
        """
        Set vaues from response
        """
        res: Response | None = None
        if not (res := values.get("response_obj")):
            return values

        headers = res.headers
        headers_params = "&".join([f"{k}={v}".lower() for k, v in headers.items()])

        values_temp = {
            "headers": parse_qs(headers_params),
            "response_size": get(headers, "content-length"),
            "content": orjson.loads(res.body),
            "status": res.status_code,
        }
        return update(values, values_temp)


class LogSourceModel(BaseModel):
    """
    Contains the exception information to be logged
    """

    # Set from `exception_obj`
    file: str | None = None
    function: str | None = None
    line: int | None = None
    message: str | None = None
    traceback: list | None = None

    exception_obj: Exception | None = None

    class Config:
        """
        Model Config
        """

        fields = {"exception_obj": {"exclude": True}}

    @root_validator(pre=True)
    @classmethod
    def parse_exception(cls, values: dict[str, Any]) -> dict[str, Any]:
        """
        Set values from exception
        """
        exc: Exception | None = None
        if not (exc := values.get("exception_obj")):
            return values

        frame_summary = traceback.extract_tb(exc.__traceback__)[-1]
        values_temp = {
            "file": frame_summary.filename,
            "function": frame_summary.name,
            "line": frame_summary.lineno,
            "message": str(exc),
            "traceback": traceback.format_exception(exc),
        }
        return update(values, values_temp)
