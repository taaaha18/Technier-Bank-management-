import json
import os

def Load(filename):
    if not os.path.exists(filename):
        return []
    else:
        with open(filename, "r") as f:
            try:
                return json.load(f)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
                return []


def save(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

class Lib:
    def __init__(self):
        self.books = Load("stock.json")
        self.aprooved = Load("borrowed.json")
        self.applied = Load("applied.json")

    def addBooks(self, bookname, author):  
        for book in self.books:
            if book['bookname'].lower() == bookname.lower():
                print("Book already exists.")
                return
        self.books.append({'bookname': bookname, 'author': author})   
        save("stock.json", self.books)
        print("New stock is added") 

    def viewBooks(self):
        self.books = Load("stock.json")
        if not self.books:
            print("No books available.")
            return []
        print("\nAvailable Books:")
        for book in self.books:
            print(f"Book Name: {book['bookname']}, Author: {book['author']}")
        return self.books

    def toApprove(self):
        updated_applied = []
        for book in self.applied:
            matched_book = None
            for b in self.books:
              if b['bookname'] == book['bookname']:
                matched_book = b
                break

            if matched_book:
                print(f"\n The Client Requested for the Book -> Book Name: {book['bookname']}, Customer ID: {book['customer_id']}")
                print("If you want to approve the book press 1 else press 2")
                try:
                    a = int(input("Enter your choice: "))
                except ValueError:
                    print("Invalid input.")
                    updated_applied.append(book)
                    continue

                if a == 1:
                    self.aprooved.append({
                        'bookname': book['bookname'],
                        'customer_id': book['customer_id']
                    })
                    print(" Book approved.")
                else:
                    updated_applied.append(book)
                    print(" Book not approved.")
            else:
                print(f" Book '{book['bookname']}' is no longer in stock.")
                updated_applied.append(book)

        save("borrowed.json", self.aprooved)
        save("applied.json", updated_applied)
        self.applied = updated_applied

    def removeBook(self, bookname):
        self.books = Load("stock.json")
        if not self.books: 
            print("No books available to remove.")
            return
        for book in self.books:
            if book['bookname'].lower() == bookname.lower():
                self.books.remove(book)
                save("stock.json", self.books)
                print(" Book removed successfully.")
                return
        print(" Book not found.")

    

class Customer():
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def borrowBook(self, bookname):
        books = Load("stock.json")
        applied = Load("applied.json")
        for book in books:
            if book['bookname'].lower() == bookname.lower():
                applied.append({
                    'bookname': bookname,
                    'customer_id': self.id
                })
                save("applied.json", applied)
                books.remove(book)
                save("stock.json", books)
                print(" Book applied successfully.")
                return
        print(" Book not found in stock.")

    def viewStock(self):
        lib = Lib()
        return lib.viewBooks()

    def returnBook(self, bookname):
        borrowed = Load("borrowed.json")
        for book in borrowed:
            if book['bookname'].lower() == bookname.lower() and book['customer_id'] == self.id:
                borrowed.remove(book)
                save("borrowed.json", borrowed)

                stock = Load("stock.json")
                stock.append({
                    'bookname': bookname,
                    'author': "Unknown"
                })
                save("stock.json", stock)
                print(" Book returned successfully.")
                return
        print(" You haven’t borrowed this book.")


def librarian_menu():
    while True:
        print("\n--- Librarian Menu ---")
        print("1. Add Book")
        print("2. View All Books")
        print("3. Approve Book Requests")
        print("4. View Approved")
        print("5. Remove Book")
        print("6. Logout")

        choice = input("Enter your choice: ")

        lib = Lib()

        if choice == "1":
            bookname = input("Enter book name: ")
            author = input("Enter author name: ")
            lib.addBooks(bookname, author)

        elif choice == "2":
            lib.viewBooks()

        elif choice == "3":
            lib.toApprove()

        elif choice == "4":
            lib.viewApproved()

        elif choice == "5":
            bookname = input("Enter book name to remove: ")
            lib.removeBook(bookname)

        elif choice == "6":
            print(" Logging out")
            break

        else:
            print(" Invalid choice. Please try again.")


def customer_menu():
    name = input("Enter your name: ")
    cust_id = input("Enter your customer ID: ")
    customer = Customer(name, cust_id)

    while True:
        print("\n--- Customer Menu ---")
        print("1. View All Books")
        print("2. Borrow Book")
        print("3. Return Book")
        print("4. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            customer.viewStock()

        elif choice == "2":
            bookname = input("Enter the book name to borrow: ")
            customer.borrowBook(bookname)

        elif choice == "3":
            bookname = input("Enter the book name to return: ")
            customer.returnBook(bookname)

        elif choice == "4":
            print(" Logging out...")
            break

        else:
            print(" Invalid choice. Please try again.")


def main():
    while True:
        print("\n=== Welcome to the Library Management System ===")
        print("1. Librarian Login")
        print("2. Customer Login")
        print("3. Exit")

        role_choice = input("Enter your choice: ")

        if role_choice == "1":
            librarian_menu()
        elif role_choice == "2":
            customer_menu()
        elif role_choice == "3":
            print(" Goodbye!")
            break
        else:
            print(" Invalid choice. Please try again.")


main()
