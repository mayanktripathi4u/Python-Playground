from flask import Flask
from flask_restful import Api
from models import db
from resources.book import BookListResource, BookResource

app = Flask(__name__)
# Set the primary database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)

api.add_resource(BookListResource, '/api/books')
api.add_resource(BookResource, '/api/books/<int:book_id>')

if __name__ == '__main__':
    app.run(debug=True)