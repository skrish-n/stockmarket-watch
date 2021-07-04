from . import db


class Stockdump(db.Document):
    ticker = db.StringField()
    last_pulled_price = db.FloatField()
    last_pulled_date = db.DateTimeField()
    price_change = db.FloatField()
    percent_change = db.FloatField()
    updated_at = db.DateTimeField()
    created_at = db.DateTimeField()


class UserStock(db.EmbeddedDocument):
    ticker = db.StringField()
    notification_upper_limit = db.FloatField()
    notification_lower_limit = db.FloatField()
    enabled_email_notifications = db.BooleanField()
    last_notified = db.DateTimeField()


class User(db.Document):
    _id = db.ObjectIdField()
    username = db.StringField()
    password = db.StringField()
    firstname = db.StringField()
    lastname = db.StringField()
    activated = db.BooleanField()
    updated_at = db.DateTimeField()
    created_at = db.DateTimeField()
    user_stock_details = db.ListField(db.EmbeddedDocumentField(UserStock))

    def to_json(self):
        return {"username": self.username,
                "firstname": self.firstname}


class RevokedToken(db.Document):
    jti = db.StringField()
    _id = db.ObjectIdField()


    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.objects(jti=jti)

        return bool(query)
