from db import db

# Model class to interact with the database
class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # create relationsship between the stores and items let the relationship
    # be lazy so it will not create object for each item.
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {"name": self.name, "items":[item.json() for item in self.items.all()]}

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
