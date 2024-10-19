from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()

def create_app():
    # app = Flask(__name__)
    # Define the path to the frontend directory
    template_dir = os.path.abspath('../frontend')
    app = Flask(__name__, template_folder = template_dir)

    app.config['SECRET_KEY'] = "some random string"

    # Import Blueprint
    from .views import views
    from .auth import auth
    from .admin import admin

    # Register Blueprints
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(admin, url_prefix = '/auth')
    app.register_blueprint(auth, url_prefix = '/')

    return app
