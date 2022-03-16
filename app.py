from flask import Flask
from flask_restful import Api
import uuid
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister, User
from resources.item import Item, ItemsList
from resources.store import Store, StoreList

app = Flask(__name__)
# Let the SQLAlchemy know where to find the db file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# turn off Falsk SQLAlchemy modification tracker but not he SQLAlchemy one.
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.secret_key = str(uuid.uuid4()) # make a random UUID
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Item, '/item/<string:name>') 
api.add_resource(ItemsList, '/items') 
api.add_resource(UserRegister, '/register') # user registration route 
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/store/<string:name>')

if __name__ == "__main__":
    # to aviod circular imports as the models will also consume db, we need to aviod 
    # consumption of db by models and vice-versa 
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)