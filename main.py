from library import Library, LibraryError, LOAN_DAYS, FINE_PER_DAY

MENU = """
========== LIBRARY MENU ==========
 1. Add a book
 2. Show all books
 3. Search books
 4. Remove a book
 5. Register a member
 6. Show all members
 7. Issue a book
 8. Return a book
 9. Show overdue books
 0. Exit
==================================
"""


def ask_int(prompt, default=None):
    """Keep asking until we get a whole number."""
    while True:
        raw = input(prompt).strip()
        if raw == "" and default is not None:
            return default
        try:
            return int(raw)
        except ValueError:
            print("  Please type a number.")


def print_books(books):
    if not books:
        print("  Nothing to show.")
        return
    print(f"  {'ID':<6}{'Title':<32}{'Author':<22}{'Available'}")
    print("  " + "-" * 70)
    for bid, b in sorted(books.items()):
        print(f"  {bid:<6}{b['title'][:30]:<32}{b['author'][:20]:<22}{b['available']}/{b['copies']}")


def add_book(lib):
    title = input("Title: ")
    author = input("Author: ")
    copies = ask_int("Copies (press Enter for 1): ", default=1)
    bid = lib.add_book(title, author, copies)
    print(f"  Done. Book id is {bid}.")


def search_books(lib):
    q = input("Search by title, author or id: ")
    print_books(lib.search_books(q))


def remove_book(lib):
    bid = input("Book id to remove: ")
    lib.remove_book(bid)
    print("  Book removed.")


def add_member(lib):
    name = input("Member name: ")
    mid = lib.add_member(name)
    print(f"  Registered. Member id is {mid}.")


def show_members(lib):
    if not lib.members:
        print("  No members yet.")
        return
    for mid, m in sorted(lib.members.items()):
        print(f"  {mid}  {m['name']}  ({len(m['borrowed'])} book(s) out)")
        for r in m["borrowed"]:
            title = lib.books[r["book_id"]]["title"]
            print(f"       - {title} (due {r['due']})")


def issue(lib):
    mid = input("Member id: ")
    bid = input("Book id: ")
    due = lib.issue_book(mid, bid)
    print(f"  Issued. Please return it by {due} ({LOAN_DAYS} days).")


def give_back(lib):
    mid = input("Member id: ")
    bid = input("Book id: ")
    fine = lib.return_book(mid, bid)
    if fine:
        print(f"  Returned late. Fine to collect: Rs {fine} (Rs {FINE_PER_DAY}/day).")
    else:
        print("  Returned on time, no fine.")


def show_overdue(lib):
    rows = lib.overdue_list()
    if not rows:
        print("  No overdue books. Nice.")
        return
    for mid, name, bid, title, days in rows:
        print(f"  {name} ({mid}) - '{title}' ({bid}) is {days} day(s) late, "
              f"fine so far Rs {days * FINE_PER_DAY}")


ACTIONS = {
    "1": add_book,
    "2": lambda lib: print_books(lib.books),
    "3": search_books,
    "4": remove_book,
    "5": add_member,
    "6": show_members,
    "7": issue,
    "8": give_back,
    "9": show_overdue,
}


def main():
    lib = Library()
    print("Welcome to the Library Management System")
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Bye!")
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("  That's not an option, try again.")
            continue
        try:
            action(lib)
        except LibraryError as err:
            print(f"  Oops: {err}")
        except (KeyboardInterrupt, EOFError):
            print("\n  Cancelled.")


if __name__ == "__main__":
    main()
