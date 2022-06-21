from aiohttp.web_response import json_response
from aiohttp_apispec import docs, request_schema, response_schema, querystring_schema
from app.results.schemes import (
    AddClientSchema,
    ClientSchema,
    QuerySchema,
)
from app.web.app import View


class UserResultsView(View):
    @docs(tags=["User"], description="Get user result by name")
    @response_schema(ClientSchema)
    @querystring_schema(QuerySchema)
    async def get(self):
        user_name = self.request.match_info["user_name"]
        query = self.request.query if self.request.query else None
        resp = await self.store.results.get_responce(user_name, query)
        return json_response({"status": "ok", "text": ClientSchema().dump(resp)})


class AddResultView(View):
    @docs(tags=["User"], description="Insert new results")
    @request_schema(AddClientSchema)
    async def post(self):
        data = self.data
        await self.store.results.post_responce(data)
        return json_response({"status": "ok"})
