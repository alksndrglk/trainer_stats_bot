import asyncio
import aiohttp
from dataclasses import dataclass
from typing import List, Dict
from contextlib import suppress
import io

from client.tg.dcs import UpdateObj
from client.tg.accessor import TgClientAccessor
from bot.utils import log_exceptions


@dataclass
class WorkerConfig:
    endpoint_url: str
    aws_secret_access_key: str
    aws_access_key_id: str
    bucket: str
    concurrent_workers: int = 1

class BotManager:
    def __init__(self, token: str, queue: asyncio.Queue, config: WorkerConfig):
        self._tasks: List[asyncio.Task] = []
        self.workers = config.concurrent_workers
        self.tg_cli = TgClientAccessor(token)
        self._queue = queue
        self._users = []
        self.is_running = False

    async def handle_update(self, upd: UpdateObj):
        pass

    async def _worker(self):
        while self.is_running:
            obj: UpdateObj = await self._queue.get()
            await self.handle_update(obj)
            self._queue.task_done()

    def start(self):
        self.is_running = True
        for _ in range(self.workers):
            self._tasks.append(asyncio.create_task(self._worker()))

    async def stop(self):
        self.is_running = False
        await self._queue.join()
        for task in self._tasks:
            if task:
                task.cancel()
        await self.tg_cli.session.close()
