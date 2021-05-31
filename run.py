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

from app.userviews import UserRegistration, Home, ConfirmEmail

api.add_resource(UserRegistration, '/registration')
api.add_resource(Home, '/')
api.add_resource(ConfirmEmail, '/confirm/<token>', endpoint="api.confirm")
#print(userviews.testvar)



if __name__ == '__main__':
    app.run()
