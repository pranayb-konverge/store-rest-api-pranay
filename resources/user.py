import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    # when the /register route will send the data we will capture it in the parser object
    # and validate the username and password
    parser = reqparse.RequestParser()

    parser.add_argument('username',
            type=str,
            required=True,
            help="Username cannot be blank!"
    )

    parser.add_argument('password',
            type=str,
            required=True,
            help="Password cannot be blank!"
    )

    # registration of a user will be a post call
    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = "INSERT INTO users VALUES (NULL, ?,?)"
        cursor.execute(insert_query, (data["username"], data["password"]))

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201
