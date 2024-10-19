from app.database import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    desc = db.Column(db.Text)

    def __init__(self, title, desc):
        self.title = title
        self.desc = desc