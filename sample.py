# Simple Library Management System

class Book:
    def __init__(self, title, author, available=True):
        self.title = title
        self.author = author
        self.available = available

    def __str__(self):
        status = "Available" if self.available else "Checked out"
        return f"{self.title} by {self.author} - {status}"

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print(f"Added: {book.title}")

    def list_books(self):
        print("\nLibrary Books:")
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book}")

    def borrow_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower() and book.available:
                book.available = False
                print(f"You borrowed '{book.title}'")
                return
        print("Sorry, book not available.")

    def return_book(self, title):
        for book in self.books:
            if book.title.lower() == title.lower() and not book.available:
                book.available = True
                print(f"You returned '{book.title}'")
                return
        print("Book not found or already returned.")

# Demo usage
library = Library()
library.add_book(Book("1984", "George Orwell"))
library.add_book(Book("To Kill a Mockingbird", "Harper Lee"))
library.add_book(Book("The Great Gatsby", "F. Scott Fitzgerald"))

library.list_books()

library.borrow_book("1984")
library.borrow_book("The Great Gatsby")
library.list_books()

library.return_book("1984")
library.list_books()

# Save library to file
with open("library.txt", "w") as f:
    for book in library.books:
        f.write(f"{book.title},{book.author},{book.available}\n")

print("\nLibrary saved to library.txt")
