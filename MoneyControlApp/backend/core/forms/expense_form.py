from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import DateField, FieldList, FloatField, FormField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Optional
from models.expense import Expense
from models.paymode import PayMode
from models.product import Product
from wtforms_sqlalchemy.fields import QuerySelectField

class PaymentDetailForm(FlaskForm):
    # Form for each payment detail
    # pay_mode = StringField('Payment Mode', validators=[DataRequired()])

    # Dropdown populated from PayMode model
    pay_mode = QuerySelectField(
        'Payment Mode', 
        # query_factory=lambda: PayMode.query.all(), 
        query_factory=lambda: PayMode.query.order_by(PayMode.pay_mode).all(), 
        get_label='pay_mode', 
        allow_blank=False,
        validators=[DataRequired()]
    )

    amount_paid = FloatField('Amount Paid', validators=[DataRequired(), NumberRange(min=0)])

    # Disable CSRF for this sub-form
    class Meta:
        csrf = False  # Disable CSRF for dynamically added subforms


# Form for Expense
class ExpenseForm(FlaskForm):
    # Purchase from (where the expense was made)
    purchase_from = StringField('Purchase From', validators=[DataRequired()])

    # Purchase date (default to the current date, but allow the user to enter a date)
    purchase_date = DateField('Purchase Date', format='%Y-%m-%d', default=datetime.now, validators=[Optional()])

    # Total amount spent (must be a positive number)
    total_amount = FloatField('Total Amount', validators=[DataRequired(), NumberRange(min=0)])

    # Description of the expense (optional field)
    description = TextAreaField('Description', validators=[Optional()])

    # FieldList to handle dynamic rows for multiple payment details
    payment_details = FieldList(FormField(PaymentDetailForm), min_entries=1)


    # Submit button
    submit_expense = SubmitField('Add Expense')

    # Search form field
    search_query = StringField('Search Purchase From', validators=[Optional()])
    
    # Start and End Dates for searching past expenses
    # start_date = DateField('Start Date', format='%Y-%m-%d', validators=[Optional()])
    # end_date = DateField('End Date', format='%Y-%m-%d', validators=[Optional()])

    start_date  = DateField('Start Date', format='%Y-%m-%d', default=datetime(datetime.now().year, datetime.now().month, 1))  # Start of current month
    end_date    = DateField('End Date'  , format='%Y-%m-%d', default=datetime.now())  # Current date

    # Submit button for search
    submit_search = SubmitField('Search Expenses')



class ExpenseDetailForm(FlaskForm):
    product_id = SelectField('Product', coerce=int, validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    amount_paid = FloatField('Amount Paid', validators=[DataRequired()])
    discount = FloatField('Discount', validators=[Optional()])
    description = StringField('Description', validators=[Optional()])
    submit = SubmitField('Add Expense Detail')

    # To populate product choices dynamically
    def __init__(self, *args, **kwargs):
        super(ExpenseDetailForm, self).__init__(*args, **kwargs)
        self.product_id.choices = [(p.id, p.name) for p in Product.query.all()]