from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:''@localhost/db_sql_alchemy"
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique = True)
    email = db.Column(db.String(80), unique = True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

        