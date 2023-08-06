# Built-In
from http import HTTPStatus
from typing import Any

# Third-Party
from fastapi.responses import ORJSONResponse

# Internal
from ehandler.utils import get_exc_name
from ehandler.settings import settings


def parse_exception(_, exception: Exception, status_code: int) -> dict[str, Any]:
    """
    :param request: Request passed from fastapi exception handler
    :param exception: Exception that invoked the exception handler
    :param status_code: HTTP status code passed through the callback

    :return: dict with exception and status code parsed
        i.e. {
            "error": "ValueError",
            "detail": "Not Found",
            "message": "ID not found",
            "data": {"user": "Alan", "id": 2}
        }
    """
    content = {}

    try:
        detail = getattr(exception, "detail", None) or HTTPStatus(status_code).phrase
        content["detail"] = detail
    except ValueError:
        content["detail"] = "Unknown Error"

    if settings.VERBOSITY >= 4:
        content["traceback"] = exception.__traceback__

    if settings.VERBOSITY >= 3:
        content["error"] = get_exc_name(exception)

    if settings.VERBOSITY >= 2:
        content["message"] = str(exception) or "unknown_error"

    if settings.VERBOSITY >= 1:
        if data := getattr(exception, "data", None):
            content["data"] = data

    return content


def response_exception(_, content: Any, status_code: int) -> ORJSONResponse:
    """
    It responds a JSON with a status code and a defined content

    :param request: Request passed from fastapi exception handler
    :param content: Content to response to the client
    :param status_code: HTTP status code passed through the callback

    :return: JSONResponse
    """
    return ORJSONResponse(content=content, status_code=status_code)
