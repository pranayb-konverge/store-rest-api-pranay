from db import db

# Model class to interact with the database
class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    # Applying the foreign key constrain to map the items to stores 
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name": self.name, "price":self.price}

     # this method will fetch the item by name from db table
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    # this method will insert and update item in the db table
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    # this method will delete the exisitng item record
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
