from flask_restful import Resource, reqparse
import stock_utils
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
from flask import request, jsonify
from marshmallow import ValidationError
from app.apidata import UserStockSchema
from app.models import Stockdump, UserStock, User
from mongoengine.queryset.visitor import Q


class SearchSymbols(Resource):
    def post(self):
        data = request.json


class AddStock(Resource):
    @jwt_required
    def post(self):
        print('#####Entering AddStock() Class ####')
        request_data = request.get_json()
        print(request_data)
        try:
            UserStockSchema().load(request_data)
        except ValidationError as err:
            return err.messages
        print("After Marshmallow object")
        username = get_jwt_identity()
        # Check if the ticker exists in the user stock dump
        user = User.objects(Q(username=username) & Q(user_stock_details__ticker=request_data['ticker'])).first()
        # user = Stockdump.objects(__raw__={''}
        # print(user.count())
        if user is not None:
            print('#####Exiting AddStock() Class ####')
            return {
                'returnCode': '200',
                'message': 'user stock record exists'
            }

        current_stock = Stockdump.objects(ticker=request_data['ticker']).first()
        try:
            print('current stock', current_stock)
            if current_stock is None:
                current_stock = stock_utils.add_new_stock(request_data['ticker'])
                if current_stock is False:
                    print('#####Exiting AddStock() Class Fail####')
                    return {
                        'returnCode': '600',
                        'message': 'Adding new Stock failed'
                    }

           # current_user = User.objects.get(username=username)
           # print('current user', current_user['username'])
            print('before userStock object')
            user_stock_details = UserStock(ticker=request_data['ticker'],
                                           notification_upper_limit=request_data[
                                               'notification_upper_limit'],
                                           notification_lower_limit=request_data[
                                               'notification_lower_limit'],
                                           enabled_email_notifications=request_data[
                                               'enabled_email_notifications']
                                           )
            print('after userStock object')
            print(user_stock_details.notification_lower_limit)
            user = User.objects(username=username).get()
            user.user_stock_details.append(user_stock_details)
            user.save()
        except:
            return {
                'returnCode': '600',
                'message': 'Insertion Error! Could not add stock to user collection'
            }
        print('#####Exiting AddStock() Class Completed####')
        return {
            'returnCode': '200',
            'message': 'Insertion Successful'
        }
