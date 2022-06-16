from dataclasses import dataclass
from datetime import datetime, timedelta
from sqlalchemy.sql import func
from app.store.database.gino import db


@dataclass
class Result:
    id: int
    user_id: int
    distance: int
    time: timedelta
    date: datetime


class ResultsModel(db.Model):
    __tablename__ = "result"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("client.id", ondelete="CASCADE"))
    distance = db.Column(db.String, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(), server_default=func.now(), nullable=False)

    def to_dct(self) -> Result:
        return Result(
            id=self.id,
            user_id=self.id,
            distance=self.distance,
            time=self.time,
            date=self.created_at,
        )


@dataclass
class Client:
    id: int
    user_name: str
    results: list


class ClientModel(db.Model):
    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(), server_default=func.now(), nullable=False)

    def __init__(self, **kw):
        super().__init__(**kw)
        self._results = list()

    @property
    def results(self):
        return self._results

    @results.setter
    def add_results(self, value: "ResultsModel"):
        self._results.append(value.to_dct())

    @classmethod
    async def get_or_create(cls, user_name: str) -> "ClientModel":
        client = await cls.query.where(
            cls.name == user_name
        ).gino.first()
        if client is None:
            client = await cls.create(name=user_name)
        return client.id

    def to_dct(self) -> Client:
        return Client(id=self.id, user_name=self.name, results=self.results)
