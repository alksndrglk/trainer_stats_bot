import asyncio
from typing import TYPE_CHECKING, List

from app.base.base_accessor import BaseAccessor
from app.results.models import Client
from app.store.bot.const import INSTRUCTIONS
from app.store.bot.dcs import Response

if TYPE_CHECKING:
    from app.web.app import Application

from ..client.tg.dcs import UpdateObj


class BotManager(BaseAccessor):

    message = "ТОП результатов {} на дистанции {}\n{}"

    def __init__(self, app: "Application"):
        super().__init__(app)
        self.app = app
        self._tasks: List[asyncio.Task] = []
        self._queue = app.queue
        self._users = []
        self.is_running = False
        self.api_url = "http://localhost:8080/result/"

    def _pretty_answer(self, result: Client) -> str:
        return self.message.format(
            result.user_name,
            result.results[0].distance,
            "\n".join(f"{r.time} --- {r.date}" for r in result.results),
        )

    def _make_query(self, query: list):
        request = self.api_url + f"{query[0]}"
        for q in query[1:]:
            request += f"?distance={q}"
        return request

    def _parse_message(self, message: str):
        commands = message.split()
        method, query, json = None, self.api_url, {}
        commands_len = len(commands)

        if commands_len == 2:
            method = "GET"
            query = self._make_query(commands[:2])

        if commands_len == 3:
            method = "POST"
            json = {
                "name": commands[0],
                "distance": commands[1],
                "time": int(commands[2]),
            }
        return (method, query, json)

    async def handle_update(self, upd: UpdateObj):
        chat_id = upd.message.from_.id
        method, query, json = self._parse_message(upd.message.text)
        resp = INSTRUCTIONS
        if method:
            res = await self.app.store.tg_api._perform_request(
                method, query, data=json
            )
            try:
                validation = Response.Schema().load(res)
                resp = self._pretty_answer(validation.text)
            except:
                resp = "Ok"
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
