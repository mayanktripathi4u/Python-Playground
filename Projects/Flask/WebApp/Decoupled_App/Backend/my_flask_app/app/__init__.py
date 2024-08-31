from flask import Flask
from app.routes import user_routes, product_routes
from app.utils.db import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Initialize the database
    init_db(app)

    # Register Blueprints
    app.register_blueprint(user_routes.bp)
    app.register_blueprint(product_routes.bp)

    return app
