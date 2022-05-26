from marshmallow import Schema, fields
from marshmallow.utils import EXCLUDE

class ResultSchema(Schema):
    id = fields.Integer(required=False)
    distance = fields.Integer(required=True)
    time = fields.TimeDelta(required=True)

class ClientShema(Schema):
    id = fields.Integer(required=False)
    name = fields.String(required=True)
    results = fields.Nested(ResultSchema, many=True)

    class Meta:
        unknown = EXCLUDE
