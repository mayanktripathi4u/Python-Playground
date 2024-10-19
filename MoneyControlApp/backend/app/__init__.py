from flask import Flask
import os
from models import db
from app.config import SQLALCHEMY_DATABASE_URI, MY_SECRET 

# Define the path to the frontend directory
template_dir = os.path.abspath('../frontend/app')
print(f"Template Directory ==> {template_dir}")

app = Flask(__name__, template_folder=template_dir)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = MY_SECRET

db.init_app(app)

from app import routes