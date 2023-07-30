import json
import logging

from .bases import BaseSNSClient, BaseSQSClient

logger = logging.getLogger(__name__)


class SQSHandler(BaseSQSClient):
    queue_name = None

    def __init__(self, queue_name=None, **kwargs) -> None:
        self.queue_name = queue_name or self.queue_name
        super().__init__(**kwargs)

    def __str__(self) -> str:
        return f"<{type(self).__name__}: {self.queue_name}>"

    async def publish(self, message, encoder=json.dumps):
        if not self.queue_name:
            raise ValueError(f"{type(self).__name__}: missing queue_name attribute")

        if encoder:
            message = encoder(message)

        logger.debug("Publishing", extra={"queue": self.queue_name, "published_message": message})

        queue_url = await self.get_queue_url(self.queue_name)
        async with self.get_client() as client:
            return await client.send_message(QueueUrl=queue_url, MessageBody=message)

    async def handle(self, message, *args):  # noqa: ARG002
        return await self.publish(message)


class SNSHandler(BaseSNSClient):
    topic = None

    def __init__(self, topic=None, **kwargs) -> None:
        self.topic = topic or self.topic
        super().__init__(**kwargs)

    def __str__(self) -> str:
        return f"<{type(self).__name__}: {self.topic}>"

    async def publish(self, message, encoder=json.dumps):
        if not self.topic:
            raise ValueError(f"{type(self).__name__}: missing topic attribute")

        if encoder:
            message = encoder(message)

        topic_arn = await self.get_topic_arn(self.topic)
        logger.debug("Publishing", extra={"topic": topic_arn, "published_message": message})

        msg = json.dumps({"default": message})
        async with self.get_client() as client:
            return await client.publish(TopicArn=topic_arn, MessageStructure="json", Message=msg)

    async def handle(self, message, *args):  # noqa: ARG002
        return await self.publish(message)
