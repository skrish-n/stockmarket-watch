from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_restful import Api
from flask_mail import Mail
from flask_jwt_extended import JWTManager


db = MongoEngine()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    api = Api(app)
    mail = Mail(app)
    jwt = JWTManager(app)
    db.init_app(app)
   # app.alphavantagekey = 'TPTE05D3FRVY8IR6'
    '''
    
    api.add_resource(userviews.UserLogoutAccess, '/logout/access')
    api.add_resource(userviews.UserLogoutRefresh, '/logout/refresh')
    api.add_resource(userviews.TokenRefresh, '/token/refresh')
    api.add_resource(userviews.AllUsers, '/users')
    api.add_resource(userviews.SecretResource, '/secret')
    # api.add_resource(stock_resources.AddStock, '/addStock')
    
    
'''

    return app, api, mail, jwt
