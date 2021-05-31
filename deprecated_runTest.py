import os

from flask import Flask
from flask_pymongo import PyMongo

import mongoengine
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mail import Mail

import logging
handler = logging.StreamHandler()
handler.setLevel(logging.ERROR)

from stockmarketwatch import create_app


app = Flask(__name__)
mail = Mail(app)
###app.config["MONGO_URI"] = "mongodb://localhost:27017/local"
app.config["MONGO_URI"] = "mongodb+srv://skrish:Mesutozil1234!@cluster0.rqkke.mongodb.net/StockWatchDB?retryWrites=true&w=majority"
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['REGISTER_SECRET_KEY'] = 'qww'
app.config['REGISTER_SECURITY_PASSWORD_SALT'] = 'qwe'

app.logger.addHandler(handler)

# mail settings

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] =True



#gmail authentication
app.config['MAIL_USERNAME'] = 'saitest101@gmail.com'
app.config['MAIL_PASSWORD'] = 'saitest101adobe'

app.config['MAIL_DEFAULT_SENDER'] = 'saitest101@gmail.com'
mail = Mail(app)




mongo = PyMongo(app)
jwt = JWTManager(app)
dbConnection = mongo.db.userDataCollection
tokenDetails = mongo.db.tokenCollection
db_stock_dump = mongo.db.stockDump
alphavantage_api_key = 'TPTE05D3FRVY8IR6'


api = Api(app)

print("###### Ending dbInitialize() funtion #####w")

def _check_config_variables_are_set(config):
    assert config['MAIL_USERNAME'] is not None,\
           'MAIL_USERNAME is not set, set the env variable APP_MAIL_USERNAME '\
           'or MAIL_USERNAME in the production config file.'
    assert config['MAIL_PASSWORD'] is not None,\
           'MAIL_PASSWORD is not set, set the env variable APP_MAIL_PASSWORD '\
           'or MAIL_PASSWORD in the production config file.'

    print(config['MAIL_USERNAME'])

_check_config_variables_are_set(app.config)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.is_jti_blacklisted(jti)

import models, resources,stock_resources
api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')
api.add_resource(stock_resources.AddStock, '/addStock')
api.add_resource(resources.Home, '/')
api.add_resource(resources.ConfirmEmail, '/confirm/<token>', endpoint="api.confirm")



if __name__ == '__main__':
    app.run(debug=True)


