from marshmallow import Schema, fields
from marshmallow.utils import EXCLUDE


class ClientNameSchema(Schema):
    id = fields.Integer(required=False)
    name = fields.String(required=True)


class ResultSchema(Schema):
    id = fields.Integer(required=False)
    distance = fields.Integer(required=True)
    time = fields.TimeDelta(required=True)


class ClientSchema(Schema):
    id = fields.Integer(required=False)
    name = fields.String(required=True)
    results = fields.Nested(ResultSchema, many=True)

    class Meta:
        unknown = EXCLUDE

class PatchingSchema(Schema):
    name = fields.String(required=False)
    results = fields.Nested(ResultSchema, many=True, required=False)
