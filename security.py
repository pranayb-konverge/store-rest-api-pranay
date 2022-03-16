from models.user import UserModel
from hmac import compare_digest

def authenticate(username, password):
    # use the class methods to retrive the username
    user = UserModel.find_by_username(username)
    # check if the user is available and the password matches
    if user and compare_digest(user.password, password):
        return user

def identity(payload):
    # get the identity from the user payload and check if it matches with the userid_mapping
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id) # use the class methods to retrive the username