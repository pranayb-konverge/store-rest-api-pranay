from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token

"""
when the /register route will send the data we will capture it in the parser object
and validate the username and password
"""

_user_parser = reqparse.RequestParser()

_user_parser.add_argument('username',
        type=str,
        required=True,
        help="Username cannot be blank!"
)

_user_parser.add_argument('password',
        type=str,
        required=True,
        help="Password cannot be blank!"
)


class UserRegister(Resource):

    # registration of a user will be a post call
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class User(Resource):
    # This resource can be useful when testing our Flask app. We may not want to expose 
    # it to public users, but for the sake of demonstration in this course, 
    # it can be useful when we are manipulating data regarding the users.
    
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User Not Found'}, 404
        return user.json(), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User Not Found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200


class UserLogin(Resource):

    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()
        # find user in db
        user = UserModel.find_by_username(data['username'])

        # This is what the authenticate() method used to do
        # check password , create access token, create refresh token, return them
        if user and safe_str_cmp(user.password, data['password']):
            # identity = is what the identity() method used to do
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return{
                "access_token":access_token,
                "refresh_token":refresh_token
            }, 200
        
        return {"message": "Invalid credentials"}, 401
         
