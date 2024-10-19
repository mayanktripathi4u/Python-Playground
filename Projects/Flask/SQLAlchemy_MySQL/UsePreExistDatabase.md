# Use Flask-SQLAlchemy with Existing Database with Reflect and Automap

In here we are going to use Flask + SQLAlchemy to interact with the pre-existing database.

There are 2 ways that we can interact with the pre-existing database without having to set up models. 

In MySQL, I have have existing Database Schema as `mysql_2_sqlalchemy` and it has 3 tables in it, namely `tbl_misc`, `tbl_random`, `tbl_todo`.

So, instead of writing classes for this which normally with ORM we do & create those in my app without having to do that. So there are two approaches that you can take
1. Reflection --> means that it just gets the information from the table and uses it as a table only, so you wont be able to do things line create new objects for this table, you'll basically only be able to query it.
2. Auto-Map --> Auto-map tries to create the equivalent class for the table, so like you write a class for your models in SQLAlchemy. 

## Base Configuration before applying any of the above two ways.
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/mydatabase'

db = SQLAlchemy(app)

@app.route('/')
def index():
    return ''

```
## Reflection.


# Details
Using SQLAlchemy with Flask to connect to your existing MySQL database is quite straightforward. Below are the steps to set it up:
## 1. Install Required Packages
First, ensure you have Flask, Flask-SQLAlchemy, and the MySQL client library installed. You can install them via pip:
```bash
pip install Flask Flask-SQLAlchemy mysqlclient
```
Alternatively, you can use PyMySQL if you prefer:
```bash
pip install Flask Flask-SQLAlchemy PyMySQL
```
If using PyMySQL, you need to add it to your project as the MySQL driver. You can include this in your code:
```bash
import pymysql
pymysql.install_as_MySQLdb()
```

## 2. Configure Flask to Use SQLAlchemy
In your Flask application, you need to configure the SQLAlchemy settings. Below is a sample configuration:
```bash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Replace with your actual MySQL connection details
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
```

## 3. Define ORM Models
Assuming you have existing tables, you'll need to create SQLAlchemy models that reflect these tables. Here’s an example of how you can define a model. Suppose you have a table called users:
```bash
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<User {self.username}>'
```

## 4. Reflect Existing Tables
If you want to automatically reflect existing tables into SQLAlchemy models, you can use the automap extension. Here’s how you can do it:
```bash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Reflect the existing database
Base = automap_base()
Base.prepare(db.engine, reflect=True)

# Access tables
User = Base.classes.users
```
## 5. Access and Use ORM Models
You can now use these models to interact with your database. For example:
```bash
@app.route('/users')
def get_users():
    users = User.query.all()
    return '<br>'.join([user.username for user in users])

```

## 6. Initialize the Database (Optional)
If you need to initialize the database and create the tables (if they don't already exist), you can use:
```bash
with app.app_context():
    db.create_all()
```

But since you already have existing tables, this step is typically not necessary.

## Summary
* Install Flask, Flask-SQLAlchemy, and a MySQL client library.
* Configure Flask to use SQLAlchemy with your MySQL database.
* Define ORM models or reflect existing tables.
* Use these models to interact with your database.

This setup allows you to work with your existing MySQL tables using SQLAlchemy ORM in a Flask application.


# Alternative approach using Auto-Map
If you have multiple existing tables and want to avoid manually creating ORM models for each one, SQLAlchemy’s automap feature is indeed a great alternative. It allows you to automatically generate ORM mappings based on your existing database schema. Here’s a step-by-step guide to using SQLAlchemy’s automap with Flask:

1. [Install Required Packages](#1-install-required-packages)
Ensure you have the necessary packages installed. 
2. [Set Up Flask and SQLAlchemy](#2-configure-flask-to-use-sqlalchemy)
Configure your Flask application to use SQLAlchemy, and set up the connection to your MySQL database.
3. **Reflect Existing Tables Using Automap** 
Use SQLAlchemy’s automap to reflect the existing database schema. Here’s how you can do it.
```bash
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker

# Reflect the existing database
Base = automap_base()
Base.prepare(db.engine, reflect=True)

# Access tables
Session = scoped_session(sessionmaker(bind=db.engine))
session = Session()

# Example: Access the 'users' table
User = Base.classes.users

# Example: Access the 'products' table
Product = Base.classes.products

# Access all users
users = session.query(User).all()
```

4. **Use Automapped Classes**
You can now use the automapped classes to query the database. Here’s an example of how you might use these classes in your Flask routes:
```bash
@app.route('/users')
def get_users():
    users = session.query(User).all()
    return '<br>'.join([user.username for user in users])

@app.route('/products')
def get_products():
    products = session.query(Product).all()
    return '<br>'.join([product.name for product in products])
```

5. Manage Sessions
Make sure to manage your sessions properly. You might want to use context management to handle session lifecycle:
```bash
@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()

```
## Summary
* Install Flask, Flask-SQLAlchemy, and a MySQL client library.
* Configure SQLAlchemy with Flask.
* Use SQLAlchemy’s automap to reflect existing tables and automatically generate ORM classes.
* Access and use these classes to interact with your database.

By using SQLAlchemy’s automap feature, you can quickly work with your existing database schema without needing to manually define ORM models for each table. This approach can save significant time and effort, especially when dealing with a large number of tables.