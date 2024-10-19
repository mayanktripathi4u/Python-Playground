from models import db
from datetime import datetime
from sqlalchemy.types import Enum

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    income_type = db.Column(Enum('Salary', 'Refund', 'Other'), default='Salary')
    amount = db.Column(db.Float, nullable=False)
    received_date = db.Column(db.DateTime, default=datetime.now())
    salary_month = db.Column(db.DateTime, default=datetime.now())
    salary_person = db.Column(db.String(255))
    description = db.Column(db.String(255))