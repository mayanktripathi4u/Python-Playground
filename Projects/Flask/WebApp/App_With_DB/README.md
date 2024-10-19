# Flask App with Database


# What is `render_template` in Flask?
The `render_template` function in Flask is used to render an HTML file (a template) and return it as a response to a client's request. This is especially useful when you want to generate dynamic HTML pages, as `render_template` allows you to pass data from your Flask application to the template.

## Example of render_template Usage:
```
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title="Home Page", user="John Doe")

if __name__ == "__main__":
    app.run(debug=True)

```

## How `render_template` works:
1. Template Rendering: The function looks for the specified HTML file (e.g., index.html) in the templates directory of your Flask project.
2. Passing Data: You can pass variables (e.g., title, user) to the template, which can then be used in the HTML to display dynamic content.

## When to Use `render_template`:
1. Dynamic Web Pages: When you want to create dynamic web pages that reflect different data based on user interaction, database queries, or other backend logic.
2. Structured Web Applications: In more structured Flask applications where you separate logic (Python code) from presentation (HTML templates).

## How to Use render_template with Templates Outside the Flask App
By default, Flask expects HTML templates to be in the `templates` directory within the Flask app's root directory. However, you can use templates that are stored in a different directory by specifying the template folder's location when you create the Flask app.

### Example: Using Templates Outside of the Flask App Directory
Suppose you want to place your HTML files in a directory outside your Flask app, such as `../my_external_templates`.

Here's how you can configure your Flask app to use templates from that directory:

1. Directory Structure Example:
/my_project
├── /app
│   ├── app.py
│   ├── /static
│   └── /templates (optional)
└── /my_external_templates
    ├── index.html
    └── about.html
2. Flask App Configuration:

Modify your Flask app to specify the template_folder parameter:
```python
from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='../my_external_templates')

@app.route('/')
def home():
    return render_template('index.html', title="Home Page", user="John Doe")

if __name__ == "__main__":
    app.run(debug=True)
```

* **template_folder**: This parameter tells Flask where to look for templates. In this case, it’s set to `../my_external_templates`, which is one directory up from the current directory and then into `my_external_templates`.


# Check for Running Process on a port
To list any process listening to the port 8080:
```bash
lsof -i:8080
```
To kill any process listening to the port 8080:
```bash
kill $(lsof -t -i:8080)
```
or more violently:
```bash
kill -9 $(lsof -t -i:8080)
```
(-9 corresponds to the SIGKILL - terminate immediately/hard kill)

# Convert or Map existing MySQL DB with SQLAlchemy
To convert the results of a raw SQL query executed with flask_mysqldb to SQLAlchemy ORM objects, you need to follow these steps:

Define the SQLAlchemy Model: Ensure you have an SQLAlchemy model that matches your table structure.

Query the Database Using SQLAlchemy: Instead of using raw SQL queries, use SQLAlchemy queries to fetch the data as ORM objects.

Convert Raw Results to ORM Objects: If you have to use raw SQL and then convert the results to ORM objects, you will need to manually create ORM instances from the raw results.

## Pre-requisite
To map your existing MySQL database with SQLAlchemy in a Flask project and create models, follow these steps:

1. Set Up Flask and SQLAlchemy
First, make sure you have Flask and Flask-SQLAlchemy installed. If not, install them using pip:

```bash
pip install Flask Flask-SQLAlchemy
```
2. Configure Your Flask Application
In your Flask application, configure SQLAlchemy to connect to your existing MySQL database. You'll need to specify your database URI in the app configuration.
Say `app.py`
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/your_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import your models after setting up db
from models import *

if __name__ == '__main__':
    app.run(debug=True)

```


## Step-by-Step Guide
1. Define Your SQLAlchemy Model
First, ensure you have an SQLAlchemy model defined for your payment_mode table.

`models.py`
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PaymentMode(db.Model):
    __tablename__ = 'payment_mode'
    
    id = db.Column(db.Integer, primary_key=True)
    pay_mode = db.Column(db.String(50))
    card_nbr = db.Column(db.String(50))
    is_active = db.Column(db.String(3))

    def __repr__(self):
        return f"<PaymentMode(id={self.id}, pay_mode={self.pay_mode})>"

```
Alternate
```python
from app import db

class Category(db.Model):
    __tablename__ = 'Category'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255), nullable=False)

    # Relationships
    subcategories = db.relationship('SubCategory', backref='category', lazy=True)

class SubCategory(db.Model):
    __tablename__ = 'SubCategory'
    id = db.Column(db.Integer, primary_key=True)
    subcategory = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('Category.id'), nullable=False)

    # Relationships
    products = db.relationship('Product', backref='subcategory', lazy=True)

class Product(db.Model):
    __tablename__ = 'Product'
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(255), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('SubCategory.id'), nullable=False)

```

2. Query Using SQLAlchemy
Instead of executing raw SQL queries and converting manually, use SQLAlchemy to perform queries and automatically get ORM objects.

Example Query
```python
from flask import Flask, render_template
from models import db, PaymentMode

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/your_database'
db.init_app(app)

@app.route('/payment_modes')
def get_payment_modes():
    # Query the PaymentMode table
    payment_modes = PaymentMode.query.filter_by(is_active="ACTV").all()
    return render_template('payment_modes.html', payment_modes=payment_modes)
```
Template Example
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Payment Modes</title>
</head>
<body>
    <h1>Payment Modes</h1>
    <ul>
        {% for mode in payment_modes %}
            <li>{{ mode.pay_mode }} (Last 4 digits: {{ mode.card_nbr[-4:] }})</li>
        {% endfor %}
    </ul>
</body>
</html>

```
3. Convert Raw Results to ORM Objects
If you must use raw SQL for some reason and then convert to ORM objects, follow this approach:

Example Conversion
```python
from models import db, PaymentMode

def fetch_payment_modes_as_orm():
    cur = db.session.execute('SELECT id, concat(pay_mode, substr(card_nbr, -4)) as pay_mode FROM payment_mode WHERE is_active = "ACTV"')
    results = cur.fetchall()

    payment_modes = []
    for result in results:
        payment_mode = PaymentMode(id=result.id, pay_mode=result.pay_mode)
        payment_modes.append(payment_mode)

    return payment_modes

@app.route('/payment_modes')
def get_payment_modes():
    payment_modes = fetch_payment_modes_as_orm()
    return render_template('payment_modes.html', payment_modes=payment_modes)
```

