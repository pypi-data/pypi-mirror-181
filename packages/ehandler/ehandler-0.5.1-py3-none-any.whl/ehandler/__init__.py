# pylint: disable=wrong-import-position

###################################################################
# Contex variables user mainly for logging and debugging purposes #
###################################################################

from contextvars import ContextVar
from time import time_ns

from fastapi import Request, Response

start_ns_ctx: ContextVar[int] = ContextVar("start_ns", default=time_ns())
request_ctx: ContextVar[Request | None] = ContextVar("request", default=None)
response_ctx: ContextVar[Response | None] = ContextVar("response", default=None)
exception_ctx: ContextVar[Exception | None] = ContextVar("exception", default=None)


##########################
# Package normal imports #
##########################

from .base import ExceptionHandlerSetter
from .utils import add_code, add_data
from .parsers import parse_exception, response_exception
from .logging import get_logger, logger
from .http import APIClient, http_client, api_client
