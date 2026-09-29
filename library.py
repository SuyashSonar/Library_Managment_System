import json
import os
from datetime import date, timedelta

LOAN_DAYS = 14        # how long a member can keep a book
FINE_PER_DAY = 2      # rupees per day after the due date
MAX_BOOKS = 3         # max books one member can hold at a time


class LibraryError(Exception):
    """Raised for anything the user did wrong (bad id, no copies left, etc.)."""


class Library:
    def __init__(self, path="data/library.json"):
        self.path = path
        self.books = {}     # "B001" -> {title, author, copies, available}
        self.members = {}   # "M001" -> {name, borrowed: [{book_id, issued, due}]}
        self.load()

    # ---------- saving / loading ----------
    def load(self):
        if not os.path.exists(self.path):
            return
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            print("Warning: couldn't read the data file, starting with an empty library.")
            return
        self.books = data.get("books", {})
        self.members = data.get("members", {})

    def save(self):
        folder = os.path.dirname(self.path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({"books": self.books, "members": self.members}, f, indent=2)

    # ---------- helpers ----------
    def _next_id(self, prefix, existing):
        # take the biggest number we've used so far and add one
        nums = [int(k[1:]) for k in existing] or [0]
        return f"{prefix}{max(nums) + 1:03d}"

    def _get_book(self, book_id):
        book_id = book_id.strip().upper()
        if book_id not in self.books:
            raise LibraryError(f"No book with id {book_id}.")
        return book_id, self.books[book_id]

    def _get_member(self, member_id):
        member_id = member_id.strip().upper()
        if member_id not in self.members:
            raise LibraryError(f"No member with id {member_id}.")
        return member_id, self.members[member_id]

    # ---------- books ----------
    def add_book(self, title, author, copies=1):
        title, author = title.strip(), author.strip()
        if not title or not author:
            raise LibraryError("Title and author can't be empty.")
        if copies < 1:
            raise LibraryError("Need at least one copy.")
        # same title + author already there? just add copies to it
        for bid, b in self.books.items():
            if b["title"].lower() == title.lower() and b["author"].lower() == author.lower():
                b["copies"] += copies
                b["available"] += copies
                self.save()
                return bid
        bid = self._next_id("B", self.books)
        self.books[bid] = {"title": title, "author": author,
                           "copies": copies, "available": copies}
        self.save()
        return bid

    def remove_book(self, book_id):
        book_id, book = self._get_book(book_id)
        if book["available"] != book["copies"]:
            raise LibraryError("Some copies are still issued, can't remove this book.")
        del self.books[book_id]
        self.save()

    def search_books(self, query):
        q = query.strip().lower()
        return {bid: b for bid, b in self.books.items()
                if q in b["title"].lower() or q in b["author"].lower() or q == bid.lower()}

    # ---------- members ----------
    def add_member(self, name):
        name = name.strip()
        if not name:
            raise LibraryError("Name can't be empty.")
        mid = self._next_id("M", self.members)
        self.members[mid] = {"name": name, "borrowed": []}
        self.save()
        return mid

    # ---------- issuing / returning ----------
    def issue_book(self, member_id, book_id, today=None):
        today = today or date.today()
        member_id, member = self._get_member(member_id)
        book_id, book = self._get_book(book_id)

        if len(member["borrowed"]) >= MAX_BOOKS:
            raise LibraryError(f"{member['name']} already has {MAX_BOOKS} books.")
        if any(r["book_id"] == book_id for r in member["borrowed"]):
            raise LibraryError("This member already has a copy of that book.")
        if book["available"] < 1:
            raise LibraryError("No copies available right now.")

        due = today + timedelta(days=LOAN_DAYS)
        member["borrowed"].append({"book_id": book_id,
                                   "issued": today.isoformat(),
                                   "due": due.isoformat()})
        book["available"] -= 1
        self.save()
        return due

    def return_book(self, member_id, book_id, today=None):
        """Returns the fine (0 if the book wasn't late)."""
        today = today or date.today()
        member_id, member = self._get_member(member_id)
        book_id, book = self._get_book(book_id)

        record = next((r for r in member["borrowed"] if r["book_id"] == book_id), None)
        if record is None:
            raise LibraryError("That member hasn't borrowed this book.")

        due = date.fromisoformat(record["due"])
        days_late = (today - due).days
        fine = days_late * FINE_PER_DAY if days_late > 0 else 0

        member["borrowed"].remove(record)
        book["available"] += 1
        self.save()
        return fine

    def overdue_list(self, today=None):
        today = today or date.today()
        result = []
        for mid, m in self.members.items():
            for r in m["borrowed"]:
                due = date.fromisoformat(r["due"])
                if due < today:
                    result.append((mid, m["name"], r["book_id"],
                                   self.books[r["book_id"]]["title"],
                                   (today - due).days))
        return result
