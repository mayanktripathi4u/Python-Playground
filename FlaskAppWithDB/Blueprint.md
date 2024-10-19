# What is Blueprint in Flask?



# Organize Flask Restful API using Blueprint
When organizing a Flask RESTful API project using Blueprints, it's crucial to structure your project in a way that is both modular and scalable. Using Blueprints helps you split your application into reusable components, and having a well-defined folder structure will make it easier to manage and maintain your project.

Here’s a suggested folder structure that incorporates Blueprints, separates models, and maintains a clean organization:

## Suggested Folder Structure
my_flask_app/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── other_model.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── admin/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── models.py
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── models.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── models.py
│   │   └── common/
│   │       ├── __init__.py
│   │       └── utils.py
│   ├── extensions.py
│   └── errors/
│       ├── __init__.py
│       ├── handlers.py
│       └── errors.py
│
├── migrations/
│
├── tests/
│
├── .env
├── requirements.txt
└── run.py


## Breakdown
* `app/__init__.py`: This file initializes the Flask app and sets up extensions, Blueprints, and configuration.
```python
from flask import Flask
from .extensions import db, migrate
from .api.admin import admin_bp
from .api.auth import auth_bp
from .api.core import core_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(core_bp, url_prefix='/core')

    return app
```
* `app/config.py`: Configuration settings for your Flask app.
* `app/models/`: Contains all the model definitions. Each model file defines one or more SQLAlchemy models.
    * `user.py`: Contains the User model.
    * `post.py`: Contains the Post model.
    * `other_model.py`: Contains other models.
* `app/api/`: Contains all the Blueprints and their associated routes and models.
    * `admin/`: Blueprint for administrative functionalities.
        * `routes.py`: Contains routes related to admin functionalities.
        * `models.py`: Contains models specific to the admin Blueprint if needed.
    * `auth/`: Blueprint for authentication functionalities.
        * `routes.py`: Contains routes related to authentication.
        * `models.py`: Contains models specific to authentication if needed.
    * `core/`: Blueprint for core functionalities.
        * `routes.py`: Contains routes related to core functionalities.
        * `models.py`: Contains models specific to core functionalities if needed.
    * `common/`: Contains shared utilities and helper functions.
* `app/extensions.py`: Contains initialization code for extensions like SQLAlchemy, Migrate, etc.
```python
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
```
* `app/errors/`: Contains error handlers and custom error classes.
* `migrations/`: Directory for database migration scripts (managed by Flask-Migrate).
* `tests/`: Contains test cases and test-related utilities.
* `.env`: Environment variables for configuration (optional).
* `requirements.txt`: Lists the Python packages required for the project.
* `run.py`: Entry point for running the Flask application.

## Key Points
1. **Separation of Concerns**: Keep your models, routes, and other components separated by their functionality to make the codebase easier to manage.

2. **Blueprints**: Use Blueprints to modularize your application. Each Blueprint can have its own set of routes and models if needed.

3. **Models Directory**: Having a centralized `models` directory for common models ensures that they are easy to find and manage. If a Blueprint has models that are specific to it, you can place those models within the Blueprint’s directory.

4. **Configuration and Initialization**: Use `app/__init__.py` to set up and initialize the app, extensions, and Blueprints.

This structure should provide a clean and modular organization for your Flask RESTful API project, making it easier to maintain and extend as your application grows.