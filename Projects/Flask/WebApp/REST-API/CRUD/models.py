from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    publish_date = db.Column(db.String(20), nullable=False)

    def __repr__(self) -> str:
        return f'<Book (self.title)>'
    
    