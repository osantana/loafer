import logging

from .compat import iscoroutinefunction, to_thread

logger = logging.getLogger(__name__)


async def ensure_coroutinefunction(func, *args):
    if iscoroutinefunction(func):
        logger.debug(
            "Handler is coroutine!",
            extra={"handler": func},
        )
        return await func(*args)

    logger.debug(
        "Handler will run in a separate thread",
        extra={"handler": func},
    )
    return await to_thread(func, *args)


def calculate_backoff_multiplier(number_of_tries, backoff_factor):
    return backoff_factor**number_of_tries
