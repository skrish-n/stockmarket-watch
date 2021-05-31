from itsdangerous import URLSafeTimedSerializer
from run import app
from passlib.hash import pbkdf2_sha256 as sha256

def generate_confirmation_token(user_name):
    print("#############Entering generate_confirmation_token##############################")
    print("REGISTER_SECRET_KEY:" ,app.config['REGISTER_SECRET_KEY'])
    serializer = URLSafeTimedSerializer(app.config['REGISTER_SECRET_KEY'])
    print("#############Exiting generate_confirmation_token##############################")
    print(serializer.dumps(user_name,salt=app.config['REGISTER_SECURITY_PASSWORD_SALT']))
    return serializer.dumps(user_name,salt=app.config['REGISTER_SECURITY_PASSWORD_SALT'])

def confirm_token(token,expiration =3600):
    print("#############Entering confirm_token()##############################")
    serializer = URLSafeTimedSerializer(app.config['REGISTER_SECRET_KEY'])
    try:
        user_name = serializer.loads(
            token,
            salt=app.config['REGISTER_SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        print("#######Exiting UserRegistration- Fail#######")
        return False
    print("#######Exiting UserRegistration- Success#######")
    return user_name

def generate_hash(password):
    return sha256.hash(password)


def verify_hash(password, hashedPwd):
    return sha256.verify(password, hashedPwd)

