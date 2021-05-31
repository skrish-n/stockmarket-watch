from mongoengine import Document, StringField, DictField, ListField, DateTimeField, EmbeddedDocument, EmbeddedDocumentField, ObjectIdField


class User(Document):
    print("inside UserDb")
    _id = ObjectIdField()
    username = StringField()
    password = StringField()

from mongoengine import connect
connect(
    db='StockWatchDB',
    host='mongodb+srv://skrish:Mesutozil1234!@cluster0.rqkke.mongodb.net/StockWatchDB?retryWrites=true&w=majority',
)

user = User()
user.username = 'username test'
user.password = 'pw test'

user.save()