import asyncio
from dataclasses import dataclass
from typing import Any, Callable

import aio_pika
from aio_pika import IncomingMessage, Message

from aiocrwaler.core.stream_core import Source, Sink


async def apass(*args, **kwargs):
    pass


@dataclass
class RabbitElement:
    value: Any
    ack: Callable = apass
    nack: Callable = apass


class RabbitSource(Source):
    def __init__(self, rabbit_uri: str, queue: str, qos: int = None, auto_ack: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rabbit_uri = rabbit_uri
        self.queue = queue
        self.qos = qos or 1
        self.auto_ack = auto_ack
        self.connection = None
        self.channel = None

    async def activate(self):
        self.connection = await aio_pika.connect_robust(self.rabbit_uri)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(self.qos)

    async def deactivate(self):
        try:
            if self.channel:
                await self.channel.close()
        except:
            pass
        try:
            if self.connection:
                await self.connection.close()
        except:
            pass

    async def reader(self):
        queue = await self.channel.get_queue(self.queue)
        async with queue.iterator() as qi:
            message: IncomingMessage
            async for message in qi:
                async with message.process(ignore_processed=not self.auto_ack):
                    if self.auto_ack:
                        yield RabbitElement(message.body)
                    else:
                        yield RabbitElement(message.body, message.ack, message.reject)


class RabbitSink(Sink):
    def __init__(self, rabbit_uri: str, queue: str, encoder: Callable[[Any], bytes], content_type: str, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.rabbit_uri = rabbit_uri
        self.queue = queue
        self.encoder = encoder
        self.content_type = content_type
        self.connection = None
        self.channel = None

    async def activate(self):
        self.connection = await aio_pika.connect_robust(self.rabbit_uri)
        self.channel = await self.connection.channel()

    async def write_batch(self, data):
        await asyncio.gather(*[self.write(single) for single in data])

    async def write(self, single):
        await self.channel.default_exchange.publish(
            Message(body=self.encoder(single), content_type=self.content_type),
            routing_key=self.queue,
        )
