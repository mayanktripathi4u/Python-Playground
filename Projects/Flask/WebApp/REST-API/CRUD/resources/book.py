from flask_restful import Resource, reqparse
from models import db, Book

class BookResource(Resource):
    def get(self, book_id):
        book = Book.query.get_or_404(book_id)
        return {"id": book.id, "title": book.title, 'author':book.author, 'publish_date': book.publish_date}
    
    def delete(self, book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return "The Book was deleted!", 204
    
    def put(self, book_id):
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('author')
        parser.add_argument('publish_date')
        args = parser.parse_args()

        book = Book.query.get_or_404(book_id)
        book.title = args['title']
        book.author = args['author']
        book.publish_date = args['publish_date']

        db.session.commit()
        return {"id": book.id, "title": book.title, 'author':book.author, 'publish_date': book.publish_date}

class BookListResource(Resource):
    def get(self):
        books = Book.query.all()
        return [
            {"id": book.id, "title": book.title, 'author':book.author, 'publish_date': book.publish_date}
                for book in books
            ]
    

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title')
        parser.add_argument('author')
        parser.add_argument('publish_date')
        args = parser.parse_args()

        book = Book(title = args['title'], author = args['author'], publish_date = args['publish_date'])
        db.session.add(book)
        db.session.commit()
        return {"id": book.id, "title": book.title, 'author':book.author, 'publish_date': book.publish_date}
 
        
