#from run import dbConnection, tokenDetails
from passlib.hash import pbkdf2_sha256 as sha256


def generate_hash(password):
    return sha256.hash(password)


def verify_hash(password, hashedPwd):
    return sha256.verify(password, hashedPwd)
'''
def save_one_to_db(jsonData):
    insertedId = dbConnection.insert_one(jsonData).inserted_id


def find_by_username(username):
    fetchRecord = dbConnection.find_one({'username': username})
    if fetchRecord is None:
        return False
    else:
        return fetchRecord

def update_registration(username):
    updateId = dbConnection.update_one(
        {'username':username},
        {'$set':{'activated':True}}
    )

def revokedTokenModel(jsonData):
    insertedId = tokenDetails.insert_one(jsonData).inserted_id


def is_jti_blacklisted(jti):
    fetchRecord = tokenDetails.find_one({'jti': jti})
    if fetchRecord is None:
        return False
    else:
        return fetchRecord
'''

