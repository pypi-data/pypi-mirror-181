# Built-In
from typing import Any, Callable, Sequence, Tuple, Type
from time import time_ns

# Third-Party
from fastapi import Request, HTTPException
from fastapi.routing import APIRoute
from fastapi.responses import Response

# Internal
from ehandler import request_ctx, response_ctx, exception_ctx, start_ns_ctx
from ehandler.utils import InnerClassProperty
from ehandler.parsers import parse_exception, response_exception
from ehandler.settings import settings
from ehandler.logging import logger

TypeHanlders = Sequence[Tuple[Type[Exception], int]]
TypeContentCallback = Callable[[Request, Exception, int], Any]
TypeResponseCallback = Callable[[Request, Any, int], Response]


class ExceptionHandlerSetter:
    """
    A class to create new FastAPI exception handlers following the same "template" using callbacks

    :param handlers: List of pairs of Exceptions and the status code that want to return
        when that exception occurs
    :param content_callback: Function provide the content to `response_callback`.
    :param response_callback: Function to provide the response.
    """

    def __init__(
        self,
        handlers: TypeHanlders | None = None,
        *,
        content_callback: TypeContentCallback = parse_exception,
        response_callback: TypeResponseCallback = response_exception,
        **_,
    ):
        self.handlers = handlers or [(Exception, 500)]
        self.content_callback = content_callback
        self.response_callback = response_callback

    @InnerClassProperty
    class Route(APIRoute):
        """
        Custom API Route to add exception handlers to the route
        """

        def get_route_handler(self) -> Callable:
            """
            Get request handler with route options like `path`, `response_model`, etc.
            """
            original_route_handler = super().get_route_handler()

            async def route_handler(request: Request) -> Response:
                start_ns = time_ns()
                start_ns_ctx.set(start_ns)

                try:
                    request_ctx.set(request)
                    response = await original_route_handler(request)
                except Exception as exception:  # pylint: disable=broad-except
                    if not (status_code := self.lookup_exception(exception)):
                        raise

                    owner: ExceptionHandlerSetter = self.owner  # type: ignore
                    content = owner.content_callback(request, exception, status_code)
                    response = owner.response_callback(request, content, status_code)

                    response_ctx.set(response)
                    exception_ctx.set(exception)

                    if response.status_code >= 500:
                        await logger.critical(None, exc_info=exception)
                    else:
                        await logger.warning(None, exc_info=exception)

                if (time_ns() - start_ns) > settings.TIMEOUT:
                    msg = (
                        f"Response time has passed the threshold {settings.TIMEOUT / 1e9} sec.\n"
                        "This limit can be configured with the variable: EHANDLER_TIMEOUT (secs)"
                    )
                    await logger.error(msg)
                return response

            return route_handler

        def lookup_exception(self, exception: Exception) -> int | None:
            """
            Lookup the exception in the exception handlers

            :param exception: Exception to lookup
            :return: status code if the exception is found, None otherwise
            """
            owner: ExceptionHandlerSetter = self.owner  # type: ignore
            for exception_type, code in reversed(owner.handlers):
                if isinstance(exception, exception_type):
                    return code
            return None
