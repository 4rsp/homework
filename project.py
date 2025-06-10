#!/usr/bin/env python3
import sqlite3

DB_NAME = 'library.db'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = '12345'

class Library:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self._establish_db_connection()
        self._create_books_table()

    def _establish_db_connection(self):
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()

    def _create_books_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                publication_year INTEGER
            )
        ''')
        self.conn.commit()

    def add_book(self, title, author, isbn, publication_year):
            self.cursor.execute("INSERT INTO books (title, author, isbn, publication_year) VALUES (?, ?, ?, ?)",
                                (title, author, isbn, publication_year))
            self.conn.commit()
            print(f"Book added successfully!")

    def delete_book(self, isbn):
        self.cursor.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
        self.conn.commit()
        print(f"Book deleted succesfully!")

    def list_all_books(self):
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()
        if not books:
            print("No books currently in the library.")
            return

        for book in books:
            book_id, title, author, isbn, publication_year = book
            print(f"ID: {book_id}, Title: {title}, Author: {author}, ISBN: {isbn}, Publication Year: {publication_year}")

    def search_book(self, search_term):
        self.cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
                            (search_term, search_term))
        results = self.cursor.fetchall()

        if not results:
            print("No books found!") 
            return

        print(f"Search result:")
        for book in results:
            book_id, title, author, isbn, publication_year = book
            print(f"ID: {book_id}, Title: {title}, Author: {author}, ISBN: {isbn}, Publication Year: {publication_year}")

    def __del__(self):
        if self.conn:
            self.conn.close()

def admin_login():
    username = input("Username: ")
    password = input("Password: ")
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Admin login successful!!!")
        return True
    else:
        print("Incorrect username or password. Please try again.")
        return False

def admin_menu(library):
    while True:
        print("""
	1. Add book
	2. Delete book
	3. List all books
	4. Search book
	5. Exit""")
        choice = input("Select an option: ")

        if choice == '1':
            title = input("Book Title: ")
            author = input("Book Author: ")
	    # ISBN is unique numaric book identifier
            isbn = input("Book ISBN: ")
            publication_year = int(input("Publication Year: "))
            library.add_book(title, author, isbn, publication_year)
        elif choice == '2':
            isbn = input("Enter the ISBN of the book to delete: ")
            library.delete_book(isbn)
        elif choice == '3':
            library.list_all_books()
        elif choice == '4':
            search_term = input("Enter title or author to search: ")
            library.search_book(search_term)
        elif choice == '5':
            print("Exiting admin Menu...")
            break
        else:
            print("Invalid choice. Please try again.")

def user_menu(library):
    while True:
        print("""
	1. List all books
	2. Search book
	3. Exit
	""")
        choice = input("Select an option: ")

        if choice == '1':
            library.list_all_books()
        elif choice == '2':
            search_term = input("Enter title or author to search: ")
            library.search_book(search_term)
        elif choice == '3':
            print("Exiting user menu....")
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    library = Library(DB_NAME)

    while True:
        print("""Welcome to e-Library. Please login first.
	1. As admin
	2. As user
	3. Exit
	""")
        main_choice = input("Select an option: ")

        if main_choice == '1':
            if admin_login():
                admin_menu(library)
        elif main_choice == '2':
            user_menu(library)
        elif main_choice == '3':
            print("Goodbye!!!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
