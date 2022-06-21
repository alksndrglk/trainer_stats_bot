from marshmallow import Schema, fields

class QuerySchema(Schema):
    distance = fields.String(required=True)

class ResultSchema(Schema):
    id = fields.Integer(required=False)
    distance = fields.String(required=True)
    time = fields.Integer(required=True)
    date = fields.DateTime(required=True)

class AddClientSchema(Schema):
    name = fields.String(required=True)
    distance = fields.String(required=True)
    time = fields.Integer(required=True)

class ClientSchema(Schema):
    id = fields.Integer(required=False)
    user_name = fields.String(required=True)
    results = fields.Nested(ResultSchema, many=True)
