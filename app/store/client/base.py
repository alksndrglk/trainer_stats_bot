import typing
from typing import Any

import aiohttp
from aiohttp import ClientResponse

from app.base.base_accessor import BaseAccessor
from .tg.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application


class ClientError(Exception):
    def __init__(self, response: ClientResponse, content: Any = None):
        self.response = response
        self.content = content


class Client(BaseAccessor):
    BASE_PATH = ""

    async def connect(self, app: "Application"):
        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False)
        )
        self.poller = Poller(app.store, app.queue)
        self.logger.info("start polling")
        await self.poller.start()

    async def disconnect(self, app: "Application"):
        if self.session:
            await self.session.close()
        if self.poller:
            await self.poller.stop()

    def get_base_path(self) -> str:
        return self.BASE_PATH.strip("/")

    def get_path(self, url: str) -> str:
        base_path = self.get_base_path().strip("/")
        url = url.lstrip("/")
        return f"{base_path}/{url}"

    async def _handle_response(self, resp: ClientResponse) -> Any:
        return resp

    async def _perform_request(self, method: str, url: str, **kwargs) -> Any:
        async with self.session.request(method, url, **kwargs) as resp:
            try:
                return await self._handle_response(resp)
            except Exception as ex:
                self.logger.info(ex)
