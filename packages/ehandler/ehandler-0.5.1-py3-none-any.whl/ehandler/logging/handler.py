# pylint: disable=invalid-overridden-method, missing-class-docstring, invalid-name, broad-except
# Built-In
from time import time_ns
from json import JSONDecodeError
from logging import LogRecord, StreamHandler, Handler, Formatter

# Internal
from ehandler import request_ctx, response_ctx, exception_ctx, start_ns_ctx
from ehandler.settings import settings
from ehandler.models import (
    GCPLogModel,
    LogRequestModel,
    LogResponseModel,
    LogSourceModel,
)


class AsyncHandler(Handler):
    async def handle(self, record):
        if rv := self.filter(record):
            self.acquire()
            try:
                await self.emit(record)
            finally:
                self.release()
        return rv

    async def emit(self, record):
        raise NotImplementedError("emit must be implemented by Handler subclasses")

    async def format(self, record):
        fmt = self.formatter or Formatter()
        return fmt.format(record)


class AsyncStreamHandler(StreamHandler, AsyncHandler):
    async def emit(self, record):
        try:
            msg = await self.format(record)
            stream = self.stream
            stream.write(msg + self.terminator)
            self.flush()
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)


class GCPHandler(AsyncStreamHandler):
    async def format(self, record: LogRecord) -> str:  # type: ignore
        if not settings.SERVICE:
            return await super().format(record)

        req_model = res_model = source_model = None
        if res := response_ctx.get():
            res_model = LogResponseModel(response_obj=res)  # type: ignore

        if exc := exception_ctx.get():
            source_model = LogSourceModel(exception_obj=exc)  # type: ignore
        else:
            exc_info = record.exc_info
            if exc_info and isinstance(exc_info[1], Exception):
                source_model = LogSourceModel(exception_obj=exc_info[1])
            else:
                source_model = LogSourceModel(
                    message=record.getMessage(),
                    file=record.pathname,
                    function=record.funcName,
                    line=record.lineno,
                )  # type: ignore

        if req := request_ctx.get():
            try:
                body = await req.json()
            except JSONDecodeError:
                body = await req.body() or None
            req_model = LogRequestModel(body=body, request_obj=req)

        log_model = GCPLogModel(
            severity=record.levelname,
            request=req_model,
            response=res_model,
            source=source_model,
        )  # type: ignore

        if log_model.http_request and not log_model.http_request.latency:
            log_model.http_request.latency = time_ns() - start_ns_ctx.get()  # type: ignore

        return log_model.json(by_alias=True, exclude_none=True)
