import asyncio
import contextlib
import logging
import os
from functools import cached_property

from .dispatchers import LoaferDispatcher
from .exceptions import ConfigurationError
from .routes import Route
from .runners import LoaferRunner

logger = logging.getLogger(__name__)


class LoaferManager:
    def __init__(self, routes, runner=None, _concurrency_limit=None, _max_threads=None) -> None:
        self._concurrency_limit = _concurrency_limit
        if not runner:
            self.runner = LoaferRunner(on_stop_callback=self.on_loop__stop, max_workers=_max_threads)
        else:
            self.runner = runner

        self.routes = routes

    @cached_property
    def dispatcher(self):
        if not (self.routes and all(isinstance(r, Route) for r in self.routes)):
            raise ConfigurationError(f"invalid routes to dispatch, routes={self.routes}")

        return LoaferDispatcher(self.routes, max_jobs=self._concurrency_limit)

    def run(self, forever=True, debug=False):
        loop = self.runner.loop
        self._future = asyncio.ensure_future(
            self.dispatcher.dispatch_providers(forever=forever),
            loop=loop,
        )

        self._future.add_done_callback(self.on_future__errors)
        if not forever:
            self._future.add_done_callback(self.runner.prepare_stop)

        start = "starting loafer, pid={}, forever={}"
        logger.info(start.format(os.getpid(), forever))
        self.runner.start(debug=debug)

    #
    # Callbacks
    #

    def on_future__errors(self, future):
        if future.cancelled():
            return self.runner.prepare_stop()

        exc = future.exception()
        # Unhandled errors crashes the event loop execution
        if isinstance(exc, BaseException):
            logger.critical(
                "Fatal error caught",
                extra={"exception": exc},
            )
            self.runner.prepare_stop()
            return None
        return None

    def on_loop__stop(self, *args, **kwargs):  # noqa: ARG002
        logger.info("Cancel dispatcher operations...")

        with contextlib.suppress(AttributeError):
            self._future.cancel()

        self.dispatcher.stop()
