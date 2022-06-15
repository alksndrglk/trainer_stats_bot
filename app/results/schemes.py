from marshmallow import Schema, fields
from marshmallow.utils import EXCLUDE


class ClientNameSchema(Schema):
    id = fields.Integer(required=False)
    name = fields.String(required=True)

class ResultSchema(Schema):
    id = fields.Integer(required=False)
    distance = fields.String(required=True)
    time = fields.Integer(required=True)

class AddClientSchema(Schema):
    name = fields.String(required=True)
    distance = fields.String(required=True)
    time = fields.Integer(required=True)

class ClientSchema(Schema):
    id = fields.Integer(required=False)
    user_name = fields.String(required=True)
    results = fields.Nested(ResultSchema, many=True)

class PatchingSchema(Schema):
    name = fields.String(required=False)
    results = fields.Nested(ResultSchema, many=True, required=False)
