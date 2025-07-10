import json

class Book:
    def __init__(self, book_id, title, author, copies):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.copies = copies

    def __str__(self):
        return f"{self.book_id}: {self.title} by {self.author} [{self.copies} copies]"

class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name

    def __str__(self):
        return f"{self.member_id}: {self.name}"

class Library:
    def __init__(self):
        self.books = {}      # book_id -> Book
        self.members = {}    # member_id -> Member
        self.issued_books = {}  # book_id -> member_id

    def add_book(self, book):
        self.books[book.book_id] = book
        print(f"✅ Book added: {book}")

    def add_member(self, member):
        self.members[member.member_id] = member
        print(f"✅ Member added: {member}")

    def show_books(self):
        if not self.books:
            print("📭 No books in library yet.")
            return
        print("\n📚 Book Catalog:")
        for book in self.books.values():
            print(book)

    def show_members(self):
        if not self.members:
            print("🧑 No members registered yet.")
            return
        print("\n🧑 Members:")
        for member in self.members.values():
            print(member)

    def issue_book(self, book_id, member_id):
        book = self.books.get(book_id)
        member = self.members.get(member_id)
        if not book:
            print("❌ Book ID not found.")
            return
        if not member:
            print("❌ Member ID not found.")
            return
        if book.copies <= 0:
            print("❌ No copies left to issue.")
            return
        book.copies -= 1
        self.issued_books[book_id] = member_id
        print(f"✅ Book '{book.title}' issued to {member.name}")

    def return_book(self, book_id, member_id):
        if self.issued_books.get(book_id) != member_id:
            print("❌ This book was not issued to this member.")
            return
        book = self.books[book_id]
        book.copies += 1
        del self.issued_books[book_id]
        print(f"✅ Book '{book.title}' returned by member {self.members[member_id].name}")

    def save_data(self):
        data = {
            "books": [
                {"book_id": b.book_id, "title": b.title, "author": b.author, "copies": b.copies}
                for b in self.books.values()
            ],
            "members": [
                {"member_id": m.member_id, "name": m.name}
                for m in self.members.values()
            ]
        }
        with open("library_data.json", "w") as f:
            json.dump(data, f, indent=4)
        print("💾 Data saved.")

    def load_data(self):
        try:
            with open("library_data.json", "r") as f:
                data = json.load(f)
            for b in data["books"]:
                self.add_book(Book(**b))
            for m in data["members"]:
                self.add_member(Member(**m))
            print("📂 Data loaded.")
        except FileNotFoundError:
            print("⚠️ No saved data found. Starting fresh.")

# ---------------- MENU ------------------

def main():
    library = Library()
    library.load_data()

    while True:
        print("""
========= 📚 LIBRARY MENU 📚 =========
1. Add Book
2. Add Member
3. Show Books
4. Show Members
5. Issue Book
6. Return Book
7. Save & Exit
""")
        choice = input("Choose an option (1-7): ")

        if choice == "1":
            book_id = input("Enter Book ID: ")
            title = input("Enter Title: ")
            author = input("Enter Author: ")
            copies = int(input("Enter Number of Copies: "))
            library.add_book(Book(book_id, title, author, copies))

        elif choice == "2":
            member_id = input("Enter Member ID: ")
            name = input("Enter Member Name: ")
            library.add_member(Member(member_id, name))

        elif choice == "3":
            library.show_books()

        elif choice == "4":
            library.show_members()

        elif choice == "5":
            book_id = input("Enter Book ID to issue: ")
            member_id = input("Enter Member ID to issue to: ")
            library.issue_book(book_id, member_id)

        elif choice == "6":
            book_id = input("Enter Book ID to return: ")
            member_id = input("Enter Member ID returning: ")
            library.return_book(book_id, member_id)

        elif choice == "7":
            library.save_data()
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
