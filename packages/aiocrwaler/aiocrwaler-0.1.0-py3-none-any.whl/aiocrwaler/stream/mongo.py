from typing import List

from aiostream import stream, pipe
from motor.motor_asyncio import AsyncIOMotorClient

from aiocrwaler.core.stream_core import Source, Sink


class MongoSource(Source):
    def __init__(self, mongo_uri: str, db_name: str, coll_name: str, find: dict = None, increment: bool = True,
                 op_types: List[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.coll_name = coll_name
        self.find = find
        self.increment = increment
        self.op_types = op_types or ['insert']
        self.client = None
        self.collection = None

    async def activate(self):
        self.client = AsyncIOMotorClient(self.mongo_uri)
        self.collection = self.client[self.db_name][self.coll_name]

    async def deactivate(self):
        if self.client:
            self.client.close()
            self.client = None

    async def reader(self):
        finder = self.collection.find(self.find)
        stream_find = {}
        if self.find:
            for k, v in self.find.items():
                stream_find['fullDocument.' + k] = v
        stream_find['operationType'] = {'$in': self.op_types}
        stream_finder = self.collection.watch([{'$match': stream_find}])
        stream_finder = (stream.iterate(stream_finder)
                         | pipe.map(lambda d: d['fullDocument'])
                         # | pipe.concat()
                         )
        combine = stream.merge(finder, stream_finder)
        async with combine.stream() as streamer:
            async for item in streamer:
                yield item


class MongoSink(Sink):
    def __init__(self, mongo_uri: str, db_name: str, coll_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.coll_name = coll_name
        self.collection = None
        self.client = None

    async def activate(self):
        self.client = AsyncIOMotorClient(self.mongo_uri)
        self.collection = self.client[self.db_name][self.coll_name]

    async def deactivate(self):
        await self.client.close()

    async def write(self, single):
        await self.collection.insert_one(single)

    async def write_batch(self, data):
        try:
            await self.collection.insert_many(data, ordered=False)
        except Exception as e:
            pass
