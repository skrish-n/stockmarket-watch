from flask_restful import Resource, reqparse
from flask import render_template, make_response, flash, url_for, request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
from .models import User, UserStock, RevokedToken
from datetime import datetime
from .apidata import UserSchema, UserStockSchema

userSchema = UserSchema()
parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)
parser.add_argument('firstname', required=False)
parser.add_argument('lastname', required=False)


class UserRegistration(Resource):
    def post(self):
        print("#######Entering UserRegistration#######")
        import email_sends, generic_technical
        #data = parser.parse_args()
        fetch_user = User.objects(username=request.form['username'])
        if fetch_user:
            #return {'message': 'User {} already exists'.format(request.form['username'])}
            return make_response(render_template('register.html', user_exist= 'yes',user_name=request.form['username'],headers = {'Content-Type': 'text/html'}))
        try:

            new_user = User(username=request.form['username'], password=generic_technical.generate_hash(request.form['password']),
                            firstname=request.form['firstname'], lastname=request.form['lastname']
                            , activated=False, updated_at=datetime.now(), created_at=datetime.now())
            new_user.save()

            registration_token = generic_technical.generate_confirmation_token(request.form['username'])
            print('registration token:', registration_token)
            confirm_url = url_for("api.confirm", token=registration_token, _external=True)
            print(confirm_url)
            html = render_template('activate.html', confirm_url=confirm_url)
            subject = "Please confirm your email"
            email_sends.send_email(request.form['username'], subject, html)

            print("#######Exiting UserRegistration-Success#######")
            return {
                'message': 'User {} was created'.format(request.form['username']),
            }
        except:
            print("#######Exiting UserRegistration-Fail#######")
            #return {'message': 'Something went wrong'}, 500
            return

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('register.html'), 200, headers)


class UserLogin(Resource):
    def post(self):
        import generic_technical
        data = parser.parse_args()
        current_user = User.objects(username=data['username']).first()
        print(current_user)
        if current_user is None:
            #return {'message': 'User {} does not exist'.format(data['username'])}
            return make_response(render_template('login.html', user_exist='nope',headers = {'Content-Type': 'text/html'}))
        if not current_user['activated']:
            return make_response(render_template('login.html', acc_activated='nope',headers = {'Content-Type': 'text/html'}))

        if generic_technical.verify_hash(data['password'], current_user['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'Logged in as {}'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'password does not match'}


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        # token_data = TokenCollection(jti=get_raw_jwt()['jti'])
        jti = get_raw_jwt()['jti']

        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.save()
            return {'message': 'Logout token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.save()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
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
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('home.html'), 200, headers)


class ConfirmEmail(Resource):

    def get(self, token):
        print("#######Entering ConfirmEmail Class#######")
        import generic_technical

        try:
            user_name = generic_technical.confirm_token(token)
            print("decrypted username:", user_name)
        except:
            print("#######Exiting ConfirmEmail Class- Fail#######")
            return {'message': 'The confirmation link is invalid or has expired.'}

        user = User.objects.get(username=user_name)

        if user['activated']:
            return {'message': 'Account already confirmed. Please login.'}
        else:
            user.activated = True
            user.save()
            # Redirect to Login URL:
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('login.html'), 200, headers)
