from models import db
# from .category import Category

class SubCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    products = db.relationship('Product', backref='subcategory', lazy=True)

