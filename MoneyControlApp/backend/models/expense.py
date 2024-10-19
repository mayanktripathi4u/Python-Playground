from models import db
from datetime import datetime
from models.product import Product

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    purchase_from = db.Column(db.String(255))
    purchase_date = db.Column(db.DateTime, default=datetime.now())
    total_amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    payment_details = db.relationship('PaymentDetail', backref='paymentdetail', lazy=True)
    expense_details = db.relationship('ExpenseDetail', backref='expensedetail', lazy=True)
    

class PaymentDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'))
    # pay_mode_id = db.Column(db.Integer, db.ForeignKey('pay_mode.id'))
    pay_mode = db.Column(db.String(50), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)


class ExpenseDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'))
    # product_name = db.Column(db.String(150), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', backref='expense_details')  # Relationship to Product
    quantity = db.Column(db.String(250), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float)
    description = db.Column(db.String(500))