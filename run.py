from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import Api
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/local"
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
mongo = PyMongo(app)
jwt = JWTManager(app)
dbConnection = mongo.db.dbTest
tokenDetails = mongo.db.tokenCollection
db_stock_dump = mongo.db.stockDump
alphavantage_api_key = 'TPTE05D3FRVY8IR6';

api = Api(app)

print("###### Ending dbInitialize() funtion #####w")

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
if __name__ == '__main__':
    app.run(debug=True)

