from marshmallow import Schema, fields


class UserStockSchema(Schema):
    ticker = fields.Str(required=True)
    notificationAmount = fields.Float(required=True)
    enabledEmailNotifications = fields.Boolean()

class UserSchema(Schema):

    username = fields.Str(required=True)
    password = fields.Str(required=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    activated = fields.Boolean()
    updated_at = fields.DateTime(required=True)
    created_at = fields.DateTime(required=True)
    stockdetails = fields.Nested(UserStockSchema)

