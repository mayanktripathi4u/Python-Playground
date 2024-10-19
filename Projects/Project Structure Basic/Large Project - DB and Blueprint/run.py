from app import app
from blog import blog
from app.database import db 

app.register_blueprint(blog)

with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
    app.run(debug = True)