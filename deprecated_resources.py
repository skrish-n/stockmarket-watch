from flask_restful import Resource, reqparse
from flask import render_template, make_response, flash, url_for
import modelss,email_sends,generic_technical
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)

parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)
parser.add_argument('firstname',required = False)
parser.add_argument('lastname',required =False)


class UserRegistration(Resource):
    def post(self):
        print("##########Starting Registration Process###############")
        data = parser.parse_args()
        fetchResult = models.find_by_username(data['username'])
        if fetchResult:
            return {'message': 'User {} already exists'.format(data['username'])}

        try:

            new_user = {
                'username': data['username'],
                'password': models.generate_hash(data['password']),
                'firstname':data['firstname'],
                'lastname':data['lastname'],
                'activated':False,
            }
            models.save_one_to_db(new_user)
            print("")
            registration_token = generic_technical.generate_confirmation_token(data['username'])
            print('registration token:',registration_token)
            confirm_url = url_for("api.confirm",token=registration_token, _external=True)
            print(confirm_url)
            html = render_template('activate.html', confirm_url = confirm_url)
            subject = "Please confirm your email"
            email_sends.send_email(data['username'],subject,html)


            return {
                'message': 'User {} was created'.format(data['username']),
            }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        currentUser = models.find_by_username(data['username'])
        if not currentUser:
            return {'message': 'User {} does not exist'.format(data['username'])}

        if models.verify_hash(data['password'], currentUser['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'Logged in as {}'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message':'password does not match'}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        insertJtiData = {
            'jti': jti
        }
        try:
            revoked_token = models.revokedTokenModel(insertJtiData)
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        insertJtiData = {
            'jti': jti
        }
        try:
            revoked_token = models.revokedTokenModel(insertJtiData)
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        return {'message': 'List of users'}

    def delete(self):
        return {'message': 'Delete all users'}


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'jwtIdentity': get_jwt_identity(),
            'answer': 42
        }


class Home(Resource):

    def get(self):
        headers = {'COntent-Type': 'text/html'}
        return make_response(render_template('home.html'),200,headers)


class ConfirmEmail(Resource):

    def get(self,token):
        try:
           user_name = generic_technical.confirm_token(token)
        except:
            return {'message':'The confirmation link is invalid or has expired.'}
        user = models.find_by_username(user_name)
        print(user)
        if user['activated']:
            return {'message':'Account already confirmed. Please login.'}
        else:
            models.update_registration(user_name)

            #Redirect to Login URL:
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('login.html'), 200, headers)





