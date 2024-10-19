from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, TextAreaField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, Optional

class ExpenseForm(FlaskForm):
    purchase_from = StringField('Purchase From', validators=[DataRequired()])
    purchase_date = DateField('Purchase Date', format='%Y-%m-%d', validators=[DataRequired()])
    total_amount = FloatField('Total Amount Paid', validators=[DataRequired()])
    short_desc = TextAreaField('Short Description', validators=[Optional()])

class ExpenseDetailForm(FlaskForm):
    product_purchased = SelectField('Product Purchased', choices=[], coerce=int)
    amount = FloatField('Amount', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])

class PaymentDetailForm(FlaskForm):
    paid_via = SelectField('Paid Via', choices=[('cash', 'Cash'), ('cc', 'Credit Card'), ('dc', 'Debit Card'), ('gift_card', 'Gift Card')],  validators=[DataRequired()])
    card_number = StringField('Card Number (Last 4 Digits)', validators=[Optional()])
    amount_paid = FloatField('Amount Paid', validators=[DataRequired()])

# class PaymentDetailForm(FlaskForm):
#     paid_via = SelectField('Paid Via', choices=[], coerce=int, validators=[DataRequired()])
#     card_number = StringField('Card Number (Last 4 Digits)', validators=[Optional()])
#     amount_paid = FloatField('Amount Paid', validators=[DataRequired()])


class CompleteExpenseForm(FlaskForm):
    expense = FormField(ExpenseForm)
    expense_details = FieldList(FormField(ExpenseDetailForm), min_entries=1, max_entries=10)
    payment_details = FieldList(FormField(PaymentDetailForm), min_entries=1, max_entries=5)
