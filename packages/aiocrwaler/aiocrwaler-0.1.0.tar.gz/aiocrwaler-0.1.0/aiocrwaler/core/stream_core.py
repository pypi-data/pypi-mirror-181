from contextlib import asynccontextmanager

import asyncio
from aiostream import pipe, operator, streamcontext


@asynccontextmanager
async def buffer(streamer, size=1):
    queue = asyncio.Queue(maxsize=size)
    sentinel = object()

    async def consume():
        try:
            async for item in streamer:
                await queue.put(item)
        finally:
            await queue.put(sentinel)

    @operator
    async def wrapper():
        while True:
            item = await queue.get()
            if item is sentinel:
                await future
                return
            yield item

    future = asyncio.ensure_future(consume())
    try:
        yield wrapper()
    finally:
        future.cancel()


@operator(pipable=True)
async def catch(source, exc_cls):
    async with streamcontext(source) as streamer:
        try:
            async for item in streamer:
                yield item
        except exc_cls:
            return


@operator(pipable=True)
async def chunks(source, n, timeout):
    async with streamcontext(source) as streamer:
        async with buffer(streamer) as buffered:
            async with streamcontext(buffered) as first_streamer:
                async for first in first_streamer:
                    tail = await (
                            buffered
                            | pipe.timeout(timeout)
                            | catch.pipe(asyncio.TimeoutError)
                            | pipe.take(n - 1)
                            | pipe.list()
                    )
                    yield [first, *tail]


class Source(object):
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        await self.activate()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.deactivate()

    async def deactivate(self):
        pass

    async def activate(self):
        pass

    async def reader(self):
        raise NotImplementedError


class Sink(object):
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        await self.activate()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.deactivate()

    async def deactivate(self):
        pass

    async def activate(self):
        pass

    async def write(self, single):
        raise NotImplementedError

    async def write_batch(self, data):
        raise NotImplementedError


pipe.timeout_buffer = chunks.pipe
