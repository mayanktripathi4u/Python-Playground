from models import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('sub_category.id'), nullable=False)