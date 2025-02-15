import abc
import logging

logger = logging.getLogger(__name__)


class AbstractMessageTranslator(abc.ABC):
    @abc.abstractmethod
    def translate(self, message):
        """Translate a given message to an appropriate format to message processing.

        This method should return a `dict` instance with two keys: `content`
        and `metadata`.
        The `content` should contain the translated message and, `metadata` a
        dictionary with translation metadata or an empty `dict`.
        """


class StringMessageTranslator(AbstractMessageTranslator):
    def translate(self, message):
        logger.debug(
            "Message translation",
            extra={"translator": type(self).__name__, "original_message": message},
        )
        return {"content": str(message), "metadata": {}}
