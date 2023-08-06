import csv
from typing import Union

import aiofiles
from aiocsv import AsyncWriter

from aiocrwaler.core.stream_core import Sink, Source


class CsvSink(Sink):

    def __init__(self, path: Union[AsyncWriter, str], mode: str = 'w', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mode = mode
        self.file = None
        if isinstance(path, AsyncWriter):
            self.writer = path
        else:
            self.path = path
            self.writer = None

    async def activate(self):
        if isinstance(self.path, str):
            self.file = await aiofiles.open(self.path, self.mode, encoding='utf-8', newline='').__aenter__()

            self.writer = AsyncWriter(self.file, dialect='unix')

    async def deactivate(self):
        if self.file:
            self.file.close()

    async def write(self, single):
        await self.writer.writerow(single)

    async def write_batch(self, data):
        await self.writer.writerows(data)


class CsvSource(Source):
    def __init__(self, path: str, skip: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path
        self.skip = skip

    def __filter_nul(self, f):
        line: str
        for line in f:
            yield line.replace('\000', '')

    async def reader(self):
        """
        单一读取，使用同步方法效率更高
        :return:
        """
        with open(self.path, mode='r', encoding='utf-8') as f:
            for row in csv.reader(self.__filter_nul(f)):
                yield tuple(row)


class LineSink(Sink):
    def __init__(self, path: str, mode: str = 'w', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path
        self.mode = mode
        self.file = None

    async def activate(self):
        self.file = await aiofiles.open(self.path, self.mode, encoding='utf-8', newline='').__aenter__()

    async def deactivate(self):
        if self.file:
            self.file.close()

    async def write(self, single):
        await self.file.write(single)

    async def write_batch(self, data):
        await self.file.writelines(data)


class LineSource(Source):
    def __init__(self, path: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path

    async def reader(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            for line in f:
                yield line
