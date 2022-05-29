import asyncio
from typing import TYPE_CHECKING, List

from app.base.base_accessor import BaseAccessor

if TYPE_CHECKING:
    from app.web.app import Application

from ..client.tg.dcs import UpdateObj


class BotManager(BaseAccessor):
    def __init__(self, app: "Application"):
        super().__init__(app)
        self.app = app
        self._tasks: List[asyncio.Task] = []
        self._queue = app.queue
        self._users = []
        self.is_running = False

    async def handle_update(self, upd: UpdateObj):
        chat_id = upd.message.from_.id
        resp = await self.app.store.tg_api._perform_request('get', 'http://localhost:8080/result/sasha')
        await self.app.store.tg_api.send_message(chat_id, resp)

    async def _worker(self):
        while self.is_running:
            obj: UpdateObj = await self._queue.get()
            await self.handle_update(obj)
            self._queue.task_done()

    async def connect(self, app: "Application"):
        self.is_running = True
        self._tasks.append(asyncio.create_task(self._worker()))

    async def disconnect(self, app: "Application"):
        self.is_running = False
        await self._queue.join()
        for task in self._tasks:
            if task:
                task.cancel()
        await self.app.store.tg_api.session.close()
