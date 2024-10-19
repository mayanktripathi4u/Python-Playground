from models import db
from datetime import datetime

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    create_date = db.Column(db.DateTime, default=datetime.now())
    last_update = db.Column(db.DateTime, nullable = True)
    subcategories = db.relationship('SubCategory', backref='category', lazy=True)

    def __init__(self, name, last_update=None):
        self.name = name 
        self.last_update = last_update

    def __repr__(self) -> str:
        return self.name
        # return f"Category : {self.name} is : {self.active}"
 