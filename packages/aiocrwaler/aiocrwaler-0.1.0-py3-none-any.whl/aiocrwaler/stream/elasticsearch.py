from dataclasses import dataclass
from typing import Any, Tuple

from elasticsearch7 import AsyncElasticsearch
from elasticsearch7.helpers import async_scan

from aiocrwaler.core.stream_core import Source


@dataclass
class ElasticsearchParam:
    hosts: Any
    http_auth: Tuple[str, str]
    port: int
    use_ssl: bool


class ElasticsearchSource(Source):
    def __init__(self, elasticsearch_param: dict, index: str, query: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.elasticsearch_param = elasticsearch_param
        self.index = index
        self.query = query
        self.client = None

    async def activate(self):
        self.client = AsyncElasticsearch(**self.elasticsearch_param.__dict__)

    async def reader(self):
        async for doc in async_scan(
                client=self.client,
                query=self.query,
                index=self.index
        ):
            yield doc
