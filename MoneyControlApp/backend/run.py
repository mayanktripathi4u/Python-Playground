from app import app
from auth import auth
from models import db
from core import core

app.register_blueprint(auth)
app.register_blueprint(core)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug = True)