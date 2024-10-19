from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

main = Flask(__name__)

main.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask-app-wit-db'

db = SQLAlchemy(main)

class ContactUs(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    fullname = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    phonenumber = db.Column(db.String)
    message = db.Column(db.Text)
    create_time = db.Column(db.DateTime, server_default = db.func.now())

# After all models and tables are defined, call SQLAlchemy.create_all() to create the table schema in the database.
# This requires an application context. 
# create_all() does not update tables if they are already in the database. If you change a model columns, use a Migration library like Alembic; Flask-Alembic; Flask-Migrate to generate migrations that update the database schema.
with main.app_context():
    db.create_all()

@main.route('/')
def home():
    return render_template("home.html")

@main.route('/about')
def aboutus():
    return render_template("about.html")

@main.route('/contact')
def contactus():
    return render_template("contact-us.html")


@main.route('/blog')
def blog():
    return render_template("blog.html")


@main.route('/services')
def services():
    return render_template("services.html")