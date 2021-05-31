from . import db


class Stockdump(db.Document):
    stockName = db.StringField()
    lastPulledPrice = db.FloatField()
    priceChange = db.FloatField()
    percentChange = db.FloatField()
    updated_at = db.DateTimeField()
    created_at = db.DateTimeField()


class UserStock(db.EmbeddedDocument):
    ticker = db.StringField()
    notificationAmount = db.LongField()
    enabledEmailNotifications = db.BooleanField()


class User(db.Document):
    print("inside UserDb")
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
