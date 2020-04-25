from flask_restful import Resource, reqparse
import models, stock_technicals
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)

parser = reqparse.RequestParser()
parser.add_argument('bestMatches')


class SearchSymbols(Resource):
    def post(self):
        data = parser.parse_args()


class AddStock(Resource):
    @jwt_required
    def post(self):
        parser.add_argument('ticker', help='The ticker symbol is not present', required=True)
        parser.add_argument('notificationAmount', type=int, help='Type of notificationAmount should be int')
        parser.add_argument('enabledEmailNotifications',type=bool, help='Type of notificationAmount should be bool')
        data = parser.parse_args()
        stock_dump_return = stock_technicals.add_to_stock_dump(data)
        if stock_dump_return is False:
            return {
                'returnCode': '601',
                'message': 'Insertion Error! Could not fetch/add stock details'
            }
        username = get_jwt_identity()
        return_value = stock_technicals.add_user_stock_details(data, username)
        if return_value == 1:
            return {
                'returnCode': '200',
                'message': 'Insertion Successful'
            }
        elif return_value == 0:
            return {
                'returnCode' : 201,
                'message': 'No db updates'
            }
        else:
            return {
                'returnCode': '600',
                'message': 'Insertion Error! Could not add stock to user collection'
            }
