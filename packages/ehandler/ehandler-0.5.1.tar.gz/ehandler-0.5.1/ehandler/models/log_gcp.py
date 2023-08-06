# Built-In
import os
from typing import Any
from enum import IntEnum

# Third-Party
from pydantic import Field, validator

# Internal
from ehandler.models.base import BaseModel
from ehandler.models.log import LogSourceModel, LogRequestModel, LogResponseModel
from ehandler.settings import settings


class GCPLogSeverity(IntEnum):
    """
    Log Severity
    """

    DEFAULT = 0
    DEBUG = 100
    INFO = 200
    NOTICE = 300
    WARNING = 400
    ERROR = 500
    CRITICAL = 600
    ALERT = 700
    EMERGENCY = 800


class GCPRequestModel(BaseModel):
    """
    `gcp.logging.LogEntry.HttpRequest`
    - https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry#httprequest
    """

    latency: dict[str, int] | None = Field(None, alias="latency")
    method: str | None = Field(None, alias="requestMethod")
    protocol: str = "HTTP/1.1"
    remote_ip: str | None = Field(None, alias="remoteIp")
    request_size: str | None = Field(None, alias="requestSize")
    response_size: str | None = Field(None, alias="responseSize")
    server_ip: str | None = Field(None, alias="serverIp")
    status: int = 600
    url: str | None = Field(None, alias="requestUrl")
    user_agent: str | None = Field(None, alias="userAgent")

    @validator("latency", pre=True)
    @classmethod
    def _latency(cls, value) -> dict[str, int] | None:
        """
        Convert `latency` (ns) to `latency` as dict with `seconds` and `nanos`
        """
        if value is None or isinstance(value, dict):
            return value

        try:
            value = int(value)
            return {"nanos": int(value % 1e9), "seconds": int(value // 1e9)}
        except ValueError:
            return None


class GCPSourceLocationModel(BaseModel):
    """
    `gcp.logging.LogEntry.SourceLocation`
    - https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry#LogEntrySourceLocation
    """

    file: str | None = None
    line: int | None = None
    function: str | None = None


class GCPLogModel(BaseModel):
    """
    Log model to parse `gcp.logging.LogEntry`
    - https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry
    """

    # Need to be set manually/externally
    severity: str
    request: LogRequestModel | None = None
    response: LogResponseModel | None = None
    source: LogSourceModel | None = None

    # Set from base models
    http_request: GCPRequestModel | None = Field(None, alias="httpRequest")
    source_location: GCPSourceLocationModel | None = Field(
        None, alias="logging.googleapis.com/sourceLocation"
    )
    message: Any | None = None
    trace: str | None = Field(None, alias="logging.googleapis.com/trace")

    # Default value
    sampled: bool = Field(True, alias="logging.googleapis.com/trace_sampled")
    env: dict | None = dict(os.environ) if settings.DEBUG else None

    @validator("http_request", always=True)
    @classmethod
    def _http_request(cls, _, values: dict[str, Any]) -> GCPRequestModel | None:
        """
        Set `http_request` from `info`
        """
        data: dict = {}
        res: LogResponseModel | None = values.get("response")
        req: LogRequestModel | None = values.get("request")

        data |= res.dict() if res else {}
        data |= req.dict() if req else {}

        if data:
            return GCPRequestModel(**data)
        return None

    @validator("source_location", always=True)
    @classmethod
    def _source_location(
        cls, _, values: dict[str, Any]
    ) -> GCPSourceLocationModel | None:
        """
        Set `source_location` from `info`
        """
        source: LogSourceModel | None
        if source := values.get("source"):
            return GCPSourceLocationModel(**source.dict())
        return None

    @validator("trace", always=True)
    @classmethod
    def _trace(cls, _, values: dict[str, Any]) -> str | None:
        """
        If `trace` is not set, set `trace` from `headers.X-Cloud-Trace-Context`.
        """
        req: LogRequestModel | None
        if not (req := values.get("request")):
            return None

        headers = req.headers
        if headers and (trace_header := headers.get("x-cloud-trace-context")):
            trace = trace_header[0].split("/")[0]
            return f"projects/{settings.PROJECT_ID}/traces/{trace}"
        return None

    @validator("message", always=True)
    @classmethod
    def _message(cls, value, values: dict[str, Any]) -> str | None:
        """
        Set `message` from `source`
        """
        if value:
            return value

        source: LogSourceModel | None = values.get("source")
        if source:
            if traceback := source.traceback:
                return "".join(traceback)
            return source.message
        return None
