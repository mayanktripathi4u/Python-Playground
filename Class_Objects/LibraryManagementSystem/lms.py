class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = False

    def __str__(self):
        return (f"Title : {self.title},"
                f"Author: {self.author},"
                f"ISBN: {self.isbn},"
                f"Borrowed: {'Yes' if self.is_borrowed else 'No'}"
                )

 
class Library:
    def __init__(self):
        self.book = []

    def add_book(self, book):
        self.book.append(book)
        print(f"Book '{book.title}' added to the library!")

    def list_books(self):
        if not self.books:
            print("No Books in the Library.")
        for book in self.books:
            print(book)

    def borrow_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn and not book.is_borrowed:
                book.is_borrowed = True
                print(f"You have borrowed '{book.title}'.")
                return
        print('Book is not available, or has been borrowed.')

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn and book.is_borrowed:
                book.is_borrowed = False
                print(f"You have returned '{book.title}'.")
                return
        print('Book not found or was not borrowed.')     


book1 = Book("Some Random Book 1", "Author 1", "13233333233")
book2 = Book("Some Random Book 2", "Author 2", "456373647464")
book3 = Book("Some Random Book 3", "Author 3", "987654322443")
book4 = Book("Some Random Book 4", "Author 4", "567890123456")

print(book1)


library = Library()

library.add_book(book1) 
library.add_book(book2)
library.add_book(book3)
library.add_book(book4)

library.list_books()

library.borrow_book("456373647464")
library.borrow_book("456373647464")  # Trying to borrow again
library.borrow_book("000000000000")  # Non-existing book
library.list_books()
