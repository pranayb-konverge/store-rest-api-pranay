import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.item import ItemModel

class Item(Resource):
    TABLE_NAME = 'items'
    # when the /item route will send the data we will capture it in the parser object
    # and validate the price
    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float,
        required=True,
        help="Price field cannot be blank!"
    )
    parser.add_argument("store_id",
        type=int,
        required=True,
        help="Every Item needs a store id."
    )

    @jwt_required() # this method requires the JWT token
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}
        
        # using the parser object we will collect the data
        data = Item.parser.parse_args()
        # here we are accesing the ItemModel class to create the item
        item = ItemModel(name, **data)

        try:
            # using the object of the ItemModel class we will insert the data
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}

        return item.json()

    # delete the item by name
    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404
    
    def put(self, name):        
        data = Item.parser.parse_args()
        # existing item we got from the db
        item = ItemModel.find_by_name(name)        
        
        if item:
            item.price = data['price']
            item.store_id = data['store_id']
        else:
            item = ItemModel(name, **data)
        
        item.save_to_db()

        return item.json()


class ItemsList(Resource):

    def get(self):
        # return {'items': list(map(lambda x : x.json(), ItemModel.query.all()))}
        return {'items':  [item.json() for item in ItemModel.query.all()]}