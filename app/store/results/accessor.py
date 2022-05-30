from aiohttp.web_response import json_response
from app.base.base_accessor import BaseAccessor
from app.results.models import ClientModel, ResultsModel
from sqlalchemy import and_


class ResultsAccessor(BaseAccessor):
    async def get_responce(self, client_name, query):

        client_result = (
            await ClientModel.outerjoin(
                ResultsModel, ClientModel.id == ResultsModel.user_id
            )
            .select()
            .where(
                and_(
                    ClientModel.name == client_name,
                    # ResultsModel.distance == query["distance"]
                )
            )
            .order_by(ResultsModel.time)
            .limit(3)
            .gino.load(
                ClientModel.distinct(ClientModel.id).load(
                    add_results=ResultsModel.distinct(ResultsModel.id)
                )
            )
            .all()
        )
        print(f"Client results {client_result=}")
        print(f"Get request with {client_name=} {query=}")
        return json_response({"status": "ok", "text": "Good"})

    async def post_responce(self, data):
        print(f"Post request with {data=}")
        return json_response({"status": "ok", "text": "Good"})

    async def delete_responce(self, user_name):
        print(f"Delete request with {user_name=}")
        return json_response({"status": "ok", "text": "Good"})

    async def patch_responce(self, data):
        print(f"Patch request with {data=}")
        return json_response({"status": "ok", "text": "Good"})
