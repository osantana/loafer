import logging

from .message_translators import AbstractMessageTranslator
from .providers import AbstractProvider
from .utils import ensure_coroutinefunction

logger = logging.getLogger(__name__)


class Route:
    def __init__(self, provider, handler, name="default", message_translator=None, error_handler=None) -> None:
        self.name = name

        if not isinstance(provider, AbstractProvider):
            raise TypeError(f"invalid provider instance: {provider!r}")

        self.provider = provider

        if message_translator and not isinstance(message_translator, AbstractMessageTranslator):
            raise TypeError(f"invalid message translator instance: {message_translator!r}")

        self.message_translator = message_translator

        if error_handler and not callable(error_handler):
            raise TypeError(f"error_handler must be a callable object: {error_handler!r}")

        self._error_handler = error_handler

        if callable(handler):
            self.handler = handler
            self._handler_instance = None
        else:
            self.handler = getattr(handler, "handle", None)
            self._handler_instance = handler

        if not self.handler:
            raise ValueError(f"handler must be a callable object or implement `handle` method: {self.handler!r}")

    def __str__(self) -> str:
        return f"<{type(self).__name__}(name={self.name} provider={self.provider!r} handler={self.handler!r})>"

    def apply_message_translator(self, message):
        if not self.message_translator:
            return {"content": message, "metadata": {}}

        translated = self.message_translator.translate(message)
        if not translated["content"]:
            raise ValueError(f"{self.message_translator} failed to translate message={message}")

        return translated

    async def deliver(self, raw_message):
        message = self.apply_message_translator(raw_message)
        logger.info(
            "Delivering message",
            extra={
                "route": self,
                "delivered_message": message,
            },
        )
        return await ensure_coroutinefunction(self.handler, message["content"], message["metadata"])

    async def error_handler(self, exc_info, message):
        logger.info(
            "Error handler process originated by message",
            extra={"handled_message": message},
        )

        if self._error_handler:
            return await ensure_coroutinefunction(self._error_handler, exc_info, message)

        return False

    def stop(self):
        logger.info(
            "Stopping route",
            extra={"route": self},
        )
        self.provider.stop()
        # only for class-based handlers
        if hasattr(self._handler_instance, "stop"):
            self._handler_instance.stop()
