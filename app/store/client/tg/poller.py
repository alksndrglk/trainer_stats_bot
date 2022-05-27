import asyncio
from typing import Optional

from app.store import Store


class Poller:
    def __init__(self, store: Store, queue: asyncio.Queue):
        self._task: Optional[asyncio.Task] = None
        self.store = store
        self._queue = queue
        self.is_runnig = False

    async def _worker(self):
        offset = 0
        while self.is_runnig:
            upd = await self.store.tg_api.get_updates_in_objects(
                offset=offset, timeout=60
            )
            if upd:
                for obj in upd:
                    self._queue.put_nowait(obj)
                    offset = obj.update_id + 1

    async def start(self):
        self.is_runnig = True
        self._task = asyncio.create_task(self._worker())

    async def stop(self):
        self.is_runnig = False
        if self._task:
            self._task.cancel()
        await self.store.tg_api.session.close()
