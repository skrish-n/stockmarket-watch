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

import app


alphavantage_api_key = 'TPTE05D3FRVY8IR6'
print("run")
app, api, mail, jwt = app.create_app()



from app.userviews import UserRegistration, Home, ConfirmEmail, UserLogin, UserLogoutAccess, SecretResource,TokenRefresh, UserLogoutRefresh
from stock_resources import AddStock
import app.models as models

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedToken.is_jti_blacklisted(jti)

api.add_resource(UserRegistration, '/registration')
api.add_resource(Home, '/')
api.add_resource(ConfirmEmail, '/confirm/<token>', endpoint="api.confirm")
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogoutAccess, '/logout/access')
api.add_resource(SecretResource, '/secret')
api.add_resource(TokenRefresh, '/token/refresh')
api.add_resource(UserLogoutRefresh, '/logout/refresh')
api.add_resource(AddStock, '/addStock')

if __name__ == '__main__':
    app.run()
