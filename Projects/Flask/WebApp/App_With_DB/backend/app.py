from datetime import datetime
# from requests import request
from flask import Flask, render_template, redirect, url_for, session, flash, request, jsonify
import os
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
import bcrypt
from flask_mysqldb import MySQL
from forms import CompleteExpenseForm

# Define the path to the frontend directory
template_dir = os.path.abspath('../frontend')

app = Flask(__name__, template_folder=template_dir)

# MySQL Config
app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = ''
app.config["MYSQL_DB"] = 'money_control'
app.secret_key = "some_random_keys_type_here"

mysql = MySQL(app)

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_email(self, field):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s", (field.data,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            raise ValidationError("Email Already Taken!. Try with another email.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login_api():
    form = LoginForm()
    if form.validate_on_submit(): 
        email = form.email.data
        password = form.password.data

        # Retrieve data into Database
        cursor = mysql.connection.cursor()
        # cursor.execute(f"SELECT * FROM users WHERE email = {email}")
        cursor.execute("SELECT * FROM users WHERE email = %s", (email, ))
        user = cursor.fetchone() 
        cursor.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['user_id'] = user[0]
            return redirect(url_for('dashboard_api')) # Provide name of function
        else:
            flash("Login Failed. Please check your email and password!")
            return redirect(url_for('login_api'))

    return render_template('login.html', form = form)


@app.route('/register', methods = ['GET', 'POST'])
def register_api():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Store data into Database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('login_api')) # Provide name of function

    return render_template('register.html', form = form)

@app.route('/dashboard')
def dashboard_api():
    if 'user_id' in session:
        user_id = session['user_id']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return render_template('dashboard.html', user = user)
    return redirect(url_for('login_api'))

@app.route('/logout')
def logout_api():
    session.pop('user_id', None)
    flash("You have been logged out successfully")
    return redirect(url_for('login_api'))

def fetchall_as_dict(cursor):
    columns = [desc[0] for desc in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

@app.route('/seed_data')
def seed_data_api():
    # COnnection
    cursor = mysql.connection.cursor()
    
    # Fetch categories
    cursor.execute("SELECT id, category FROM category WHERE is_active = 'ACTV' ")
    # categories = cursor.fetchall() # Will result as Tuples
    categories = fetchall_as_dict(cursor) # convert these tuples into dictionaries 
    print(f"Categories ==> {categories}")
    print(f"Type of Categories Result ==> {type(categories)}")
    
    # Fetch subcategories
    cursor.execute("SELECT id, subcategory, category_id FROM subcategory WHERE is_active = 'ACTV' ")
    # subcategories = cursor.fetchall() # Will result as Tuples
    subcategories = fetchall_as_dict(cursor) # convert these tuples into dictionaries 
    
    # Fetch products
    cursor.execute("SELECT id, product FROM product WHERE is_active = 'ACTV' ")
    # products = cursor.fetchall() # Will result as Tuples
    products = fetchall_as_dict(cursor) # convert these tuples into dictionaries 
    
    cursor.close()
    
    return render_template('seed_data.html', categories=categories, subcategories=subcategories, products=products)

@app.route('/submit', methods=['POST'])
def submit():
    print(f"Submit Called, and request is {request}")
    data_type = request.form['data_type']
    create_by = request.form['create_by']
    create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor = mysql.connection.cursor()

    if data_type == 'category':
        category = request.form['category']
        cursor.execute(
            'INSERT INTO category (category, create_by, create_date) VALUES (%s, %s, %s)',
            (category, create_by, create_date)
        )
    elif data_type == 'subcategory':
        subcategory = request.form['subcategory']
        category_id = request.form['category_id']
        print(f"category_id : {category_id}")
        cursor.execute(
            'INSERT INTO subcategory (subcategory, category_id, create_by, create_date) VALUES (%s, %s, %s, %s)',
            (subcategory, category_id, create_by, create_date)
        )
    elif data_type == 'product':
        print("Form Submitted for Product")
        product = request.form['product']
        
        subcategory_id = request.form['subcategory_id']
        print(f"Product Received : {product} for subcategory id : {subcategory_id}")
        cursor.execute(
            'INSERT INTO product (product, subcategory_id, create_by, create_date) VALUES (%s, %s, %s, %s)',
            (product, subcategory_id, create_by, create_date)
        )
    else:
        return redirect(url_for('seed_data_api'))

    cursor.close()
    return redirect(url_for('seed_data_api'))

@app.route('/seed_data_v2')
def seed_data_api_v2():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Category')
    # categories = cur.fetchall()
    categories = fetchall_as_dict(cur) # convert these tuples into dictionaries
    cur.execute('SELECT * FROM SubCategory')
    # subcategories = cur.fetchall()
    subcategories = fetchall_as_dict(cur) # convert these tuples into dictionaries
    cur.execute('SELECT * FROM Product')
    # products = cur.fetchall()
    products = fetchall_as_dict(cur) # convert these tuples into dictionaries
    cur.close()
    
    return render_template('seed_data_v2.html', categories=categories, subcategories=subcategories, products=products)


@app.route('/seed_data_v2_add', methods=['POST'])
def add_api():
    category    = request.form.get('category')
    subcategory = request.form.get('subcategory')
    product     = request.form.get('product')
    
    cur = mysql.connection.cursor()
    create_by = 'Mayank'
    
    if category:
        # If Exists
        cur.execute("SELECT 1 FROM Category WHERE lower(category) = %s", (category.lower(),))
        if cur.fetchone()  :
            flash(f"Category : {category} already exists. Please use it.")
        else:          
            cur.execute('INSERT INTO Category (category, create_by) VALUES (%s, %s)', [category, create_by])
    if subcategory and request.form.get('category_id'):
        # If Exists
        cur.execute("SELECT 1 FROM SubCategory WHERE lower(subcategory) = %s", (subcategory.lower(),))
        if cur.fetchone()  :
            flash(f"Sub-Category : {subcategory} already exists. Please use it.")
        else:          
            cur.execute('INSERT INTO SubCategory (subcategory, category_id, create_by) VALUES (%s, %s, %s)', 
                    (subcategory, request.form.get('category_id'), create_by))
    if product and request.form.get('subcategory_id'):
        # If Exists
        cur.execute("SELECT 1 FROM Product WHERE lower(product) = %s", (product.lower(),))
        if cur.fetchone()  :
            flash(f"Product : {product} already exists. Please use it.")
        else:
            cur.execute('INSERT INTO Product (product, subcategory_id, create_by) VALUES (%s, %s, %s)', 
                    (product, request.form.get('subcategory_id'), create_by))
    
    mysql.connection.commit()
    cur.close()
    
    return redirect(url_for('seed_data_api_v2'))

@app.route('/fetch_subcategories/<int:category_id>', methods=['GET'])
def fetch_subcategories(category_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM SubCategory WHERE category_id = %s', [category_id])
    # subcategories = cur.fetchall()
    subcategories = fetchall_as_dict(cur) # convert these tuples into dictionaries
    cur.close()
    return jsonify(subcategories)

@app.route('/fetch_products/<int:subcategory_id>', methods=['GET'])
def fetch_products(subcategory_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Product WHERE subcategory_id = %s', [subcategory_id])
    # products = cur.fetchall()
    products = fetchall_as_dict(cur) # convert these tuples into dictionaries
    cur.close()
    return jsonify(products)

@app.route('/fetch_products_api', methods=['GET'])
def fetch_products_api():
    query = request.args.get('query', '')
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, product FROM Product WHERE product LIKE %s', [f'%{query}%'])
    products = cur.fetchall()
    cur.close()
    return jsonify([{'id': product[0], 'product': product[1]} for product in products])

# @app.route('/manage_expense', methods=['GET', 'POST'])
# def manage_expense():
#     form = CompleteExpenseForm()
#     if form.validate_on_submit():
#         # Insert Expense
#         expense = Expense(
#             purchase_from=form.expense.purchase_from.data,
#             purchase_date=form.expense.purchase_date.data,
#             total_amount=form.expense.total_amount.data,
#             short_desc=form.expense.short_desc.data
#         )
#         db.session.add(expense)
#         db.session.flush()  # Flush to get the ID for ExpenseDetail and PaymentDetail

#         # Insert Expense Details
#         for detail_form in form.expense_details:
#             if detail_form.product_purchased.data:
#                 detail = ExpenseDetail(
#                     expense_id=expense.id,
#                     product_purchased=detail_form.product_purchased.data,
#                     amount=detail_form.amount.data,
#                     description=detail_form.description.data
#                 )
#                 db.session.add(detail)

#         # Insert Payment Details
#         for payment_form in form.payment_details:
#             if payment_form.paid_via.data:
#                 payment = PaymentDetail(
#                     expense_id=expense.id,
#                     paid_via=payment_form.paid_via.data,
#                     card_number=payment_form.card_number.data,
#                     amount_paid=payment_form.amount_paid.data
#                 )
#                 db.session.add(payment)

#         db.session.commit()
#         return redirect(url_for('manage_expense'))

#     return render_template('manage_expense.html', form=form)


@app.route('/manage_expense', methods=['GET', 'POST'])
def manage_expense():
    form = CompleteExpenseForm()

    # Fetch payment modes from the database
    # payment_modes = PaymentMode.query.all()
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, concat(pay_mode, substr(card_nbr, -4)) as pay_mode  FROM payment_mode WHERE is_active = "ACTV"')
    payment_modes = fetchall_as_dict(cur) # convert these tuples into dictionaries
    # for mode in payment_modes:
    #     print(f"mode ==> {mode} and ID is {mode['id']}")
    payment_choices = [(mode['id'], mode['pay_mode']) for mode in payment_modes]

    # form.paid_via().choices = payment_choices

    if form.validate_on_submit():
        # Insert Expense
        purchase_from = request.form['purchase_from']
        purchase_date = request.form['purchase_date']
        total_amount = request.form['total_amount']
        short_desc = request.form['short_desc']
        
        # Insert into Expense table
        cur = mysql.cursor()
        cur.execute('''
            INSERT INTO Expense (purchase_from, purchase_date, total_amount, short_desc)
            VALUES (%s, %s, %s, %s)
        ''', (purchase_from, purchase_date, total_amount, short_desc))
        expense_id = cur.lastrowid
        mysql.commit()

        # Insert Expense Details
        for detail in request.form.getlist('expense_details'):
            product_purchased = detail['product_purchased']
            amount = detail['amount']
            description = detail['description']
            cur.execute('''
                INSERT INTO ExpenseDetails (expense_id, product_purchased, amount, description)
                VALUES (%s, %s, %s, %s)
            ''', (expense_id, product_purchased, amount, description))

        # Insert Payment Details
        paid_via = form.paid_via.data
        # card_number = form.card_number.data
        amount_paid = form.amount_paid.data
        cur.execute('''
            INSERT INTO PaymentDetails (expense_id, paid_via, amount_paid)
            VALUES (%s, %s, %s)
        ''', (expense_id, paid_via, amount_paid))

        mysql.commit()

        cur.close()
        return redirect(url_for('manage_expense'))

    return render_template('manage_expense.html', form=form)


if __name__ == "__main__":
    app.run(debug = True, port = 5001)