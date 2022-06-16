from datetime import datetime
from typing import ClassVar, List, Type
from marshmallow_dataclass import dataclass
from marshmallow import Schema, EXCLUDE


@dataclass
class Result:
    distance: str
    time: int
    date: datetime

    class Meta:
        unknown = EXCLUDE


@dataclass
class ClientStats:
    user_name: str
    results: List[Result]

    class Meta:
        unknown = EXCLUDE


@dataclass
class Response:
    status: str
    text: ClientStats

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE
