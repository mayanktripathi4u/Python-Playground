from models import db
from datetime import datetime

class PayMode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pay_mode = db.Column(db.String(50), nullable=False)
    # values will be like CC-Discover-1234; GC-Walmart-3456
    card_bank_name = db.Column(db.String(50), nullable=True)
    card_nbr = db.Column(db.String(50), nullable=True)
    active = db.Column(db.Boolean, nullable=False, default=True)
    create_date = db.Column(db.DateTime, default=datetime.now())
    last_update = db.Column(db.DateTime, nullable = True)

    def __init__(self, pay_mode, card_bank_name, card_nbr, last_update=None):
        self.pay_mode = pay_mode 
        self.card_bank_name = card_bank_name 
        self.card_nbr = card_nbr 
        self.last_update = last_update

    def __repr__(self) -> str:
        return self.pay_mode