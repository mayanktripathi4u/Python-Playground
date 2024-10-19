from datetime import datetime
from models import db
from werkzeug.security import check_password_hash, generate_password_hash

# Refer https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable = False, unique=True)
    email = db.Column(db.String(100), nullable = False, unique=True)
    password_hash = db.Column(db.String(1000), nullable = False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    create_date = db.Column(db.DateTime, default=datetime.now())
    last_login = db.Column(db.DateTime, nullable = True)

    # Constructor: define only param which we are goign to pass, rest could skip such as active; create_date; id; password 
    def __init__(self, username, email, last_login=None):
        self.username = username
        self.email = email
        # self.password = password
        # self.active = active
        # self.create_date = create_date
        self.last_login = last_login

    def __repr__(self) -> str:
        return f"Active indicator of User : {self.username} is : {self.active}"
    
    # Convert User's password into Hashed Password.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password=password)

    # Verify / Validate and compare the password (user's enetered password vs password in database)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    