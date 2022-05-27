from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound, HTTPBadRequest
from aiohttp_apispec import docs, request_schema, response_schema, querystring_schema
from app.results.schemes import ClientShema, ClientNameSchema
from app.web.app import View


class UserResultsView(View):
    @docs(tags=["User"], description="Get user result by name")
    @response_schema(ClientShema)
    async def get(self):
        user_name = self.request.match_info["user_name"]
        query = self.request.query if self.request.query else None
        resp = await self.store.results.get_responce(user_name, query)
        return resp
    @docs(tags=["User"], description="Insert new results")
    @request_schema(ClientShema)
    async def post(self):
        data = self.json
        resp = await self.store.results.post_responce(data)
        return resp

    @docs(tags=["User"], description="Delete results by name")
    @request_schema(ClientShema)
    async def delete(self):
        user_name = self.request.match_info["user_name"]
        resp = await self.store.results.delete_responce(user_name)
        return resp

    @docs(tags=["User"], description="Update user result by name")
    @request_schema(ClientShema)
    async def patch(self):
        user_name = self.request.match_info["user_name"]
        data = self.json
        resp = await self.store.results.patch_responce(user_name, data)
        return resp
