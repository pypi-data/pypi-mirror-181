# pylint: disable=invalid-overridden-method,missing-class-docstring,invalid-name,too-many-arguments
# Built-In
import sys
import inspect
from typing import Sequence
from logging import Logger, Formatter, DEBUG, INFO, WARNING, ERROR, CRITICAL

# Internal
from ehandler.settings import settings
from ehandler.logging.handler import AsyncHandler, GCPHandler


class AsyncLogger(Logger):
    handlers: Sequence[AsyncHandler]  # type: ignore

    async def debug(self, msg, *args, **kwargs):
        if self.isEnabledFor(DEBUG):
            await self._log(DEBUG, msg, args, **kwargs)

    async def info(self, msg, *args, **kwargs):
        if self.isEnabledFor(INFO):
            await self._log(INFO, msg, args, **kwargs)

    async def warning(self, msg, *args, **kwargs):
        if self.isEnabledFor(WARNING):
            await self._log(WARNING, msg, args, **kwargs)

    async def error(self, msg, *args, **kwargs):
        if self.isEnabledFor(ERROR):
            await self._log(ERROR, msg, args, **kwargs)

    async def critical(self, msg, *args, **kwargs):
        if self.isEnabledFor(CRITICAL):
            await self._log(CRITICAL, msg, args, **kwargs)

    async def log(self, level: int, msg, *args, **kwargs):  # type: ignore
        if self.isEnabledFor(level):
            await self._log(level, msg, args, **kwargs)

    async def _log(
        self,
        level,
        msg,
        args,
        exc_info=None,
        extra=None,
        stack_info=False,
        stacklevel=1,
    ):
        sinfo = None
        try:
            path, lno, func, sinfo = self.findCaller(stack_info, stacklevel)
        except ValueError:
            path, lno, func = "unknown file", 0, "unknown function"

        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()

        record = self.makeRecord(
            self.name, level, path, lno, msg, args, exc_info, func, extra, sinfo  # type: ignore
        )
        await self.handle(record)

    async def handle(self, record):
        if (not self.disabled) and self.filter(record):
            await self.callHandlers(record)

    async def callHandlers(self, record):
        c = self
        found = 0
        while c:
            for hdlr in c.handlers:
                found = found + 1
                if record.levelno >= hdlr.level:
                    if inspect.iscoroutinefunction(hdlr.handle):
                        await hdlr.handle(record)
                    else:
                        hdlr.handle(record)
            if not c.propagate:
                c = None  # break out
            else:
                c = c.parent


def get_logger() -> AsyncLogger:
    """Setup logging"""
    fmt = "[%(levelname)8s] %(asctime)s (%(filename)s:%(lineno)s) --- %(message)s"
    datefmt = "%H:%M:%S"

    handler = GCPHandler()
    handler.setFormatter(Formatter(fmt, datefmt))

    logger = AsyncLogger("ehandler", settings.LOG_LEVEL)
    logger.addHandler(handler)

    return logger
