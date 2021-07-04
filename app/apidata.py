from marshmallow import Schema, fields


class UserStockSchema(Schema):
    ticker = fields.Str(required=True)
    notification_upper_limit = fields.Float()
    notification_lower_limit = fields.Float()
    enabled_email_notifications = fields.Boolean(required=True)

class UserSchema(Schema):

    username = fields.Str(required=True)
    password = fields.Str(required=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    activated = fields.Boolean()
    updated_at = fields.DateTime(required=True)
    created_at = fields.DateTime(required=True)
    stockdetails = fields.Nested(UserStockSchema)

