from flask import Flask
from .database import db
from .config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
# from .routes import *
from app import routes