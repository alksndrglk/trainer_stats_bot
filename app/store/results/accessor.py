from aiohttp.web_response import json_response
from app.base.base_accessor import BaseAccessor


class ResultsAccessor(BaseAccessor):
    async def get_responce(self, user_name, query):
        print(f"Get request with {user_name=} {query=}")
        return json_response({"status":"ok", "text":"Good"})

    async def post_responce(self, data):
        print(f"Post request with {data=}")
        return json_response({"status":"ok", "text":"Good"})

    async def delete_responce(self, user_name):
        print(f"Delete request with {user_name=}")
        return json_response({"status":"ok", "text":"Good"})

    async def patch_responce(self, data):
        print(f"Patch request with {data=}")
        return json_response({"status":"ok", "text":"Good"})
