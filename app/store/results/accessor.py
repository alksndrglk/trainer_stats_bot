from aiohttp.web_response import json_response
from app.base.base_accessor import BaseAccessor
from app.results.models import ClientModel, ResultsModel
from sqlalchemy import and_

from app.results.schemes import ClientSchema


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
                    ResultsModel.distance == query["distance"]
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
        res = "None"
        for r in client_result:
            res = r.to_dct()
        return json_response({"status": "ok", "text": ClientSchema().dump(res)})

    async def post_responce(self, data):
        #create if not exists

        #add row by user_id

        print(f"Post request with {data=}")
        return json_response({"status": "ok", "text": "Good"})

